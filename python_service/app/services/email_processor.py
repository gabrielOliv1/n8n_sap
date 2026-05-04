"""Email processing service — core orchestration layer.

Processes a batch of raw EmailPayload objects received from n8n:
1. Cleans the requisitioner field (extracts bare email address).
2. Cleans the subject field (strips 'Subject:' prefix).
3. Cleans the email body (removes provider footers via text_cleaner).
4. Decodes base64 attachments and extracts PDF text previews.

PDF parsing is scoped to the first 5 000 characters (M2). Non-PDF files
and parse errors are silently ignored (returns None preview).
"""

import base64
import io
import logging
import re

import pdfplumber

from app.domain.schemas.email_payload import AttachmentData, EmailPayload
from app.domain.schemas.email_response import AttachmentSummary, EmailResult
from app.services.text_cleaner import remove_email_footer

logger = logging.getLogger(__name__)

# Maximum characters extracted from a PDF for the LLM preview.
# Value chosen to provide a meaningful document preview without exceeding
# typical LLM context budgets (approx. 1 250 tokens at 4 chars/token).
_PDF_PREVIEW_MAX_CHARS = 5_000

# Regex to extract a bare email address from common "From:" header formats:
#   'From: "Display Name" <user@host.com>'  → user@host.com
#   'From: user@host.com'                   → user@host.com
_EMAIL_ADDR_RE = re.compile(r"<([^>]+)>|[\w.+-]+@[\w.-]+\.\w+")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def process_email_batch(emails: list[EmailPayload]) -> list[EmailResult]:
    """Process a batch of raw email payloads from n8n into cleaned results.

    For each email in the batch:
        1. Extracts the bare email address from the 'requisitioner' header.
        2. Strips the 'Subject:' prefix from the 'subject' field.
        3. Removes provider footers from the 'text' field (with logging).
        4. Decodes and parses attachments (PDF preview, first 5k chars).

    Args:
        emails: List of raw EmailPayload objects deserialized from the n8n
            JSON array. May be empty.

    Returns:
        List of EmailResult objects in the same order as the input. Empty
        list when input is empty.
    """
    return [_process_single_email(email) for email in emails]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _process_single_email(email: EmailPayload) -> EmailResult:
    """Transform a single raw EmailPayload into a cleaned EmailResult.

    Args:
        email: Raw email payload item from n8n.

    Returns:
        Cleaned EmailResult ready for LLM consumption.
    """
    attachment_summary = (
        _process_attachments(email.attachment) if email.attachment else None
    )
    return EmailResult(
        email=email.email,
        requisitioner=_extract_email_address(email.requisitioner),
        subject=_clean_subject(email.subject),
        text=remove_email_footer(email.email, email.text),
        attachmentSummary=attachment_summary if attachment_summary else None,
    )


def _extract_email_address(raw_requisitioner: str) -> str:
    """Extract a bare email address from a raw 'From:' header string.

    Handles two common formats:
        - 'From: "Display Name" <user@host.com>' → 'user@host.com'
        - 'From: user@host.com'                  → 'user@host.com'

    Args:
        raw_requisitioner: Raw value of the 'requisitioner' field from n8n.

    Returns:
        Bare email address string. Returns raw_requisitioner unchanged when
        no recognizable pattern is found.
    """
    match = _EMAIL_ADDR_RE.search(raw_requisitioner)
    if match:
        # Group 1 is set when angle-bracket format matches, else use full match.
        return match.group(1) if match.group(1) else match.group(0)
    return raw_requisitioner


def _clean_subject(raw_subject: str) -> str:
    """Strip the 'Subject:' prefix from a raw subject header string.

    Args:
        raw_subject: Raw subject value from n8n (e.g. 'Subject: meeting notes').

    Returns:
        Subject title with any leading 'Subject:' prefix and surrounding
        whitespace removed.
    """
    return re.sub(r"^Subject:\s*", "", raw_subject, flags=re.IGNORECASE).strip()


def _process_attachments(
    attachments: dict[str, AttachmentData],
) -> list[AttachmentSummary]:
    """Decode and summarise all attachments in a single email.

    Iterates over the n8n attachment dict (keys: 'attachment_0', etc.) and
    builds an AttachmentSummary for each entry. Non-PDF files receive a None
    preview; parse errors are silently swallowed.

    Args:
        attachments: Dict mapping n8n attachment keys to AttachmentData objects.

    Returns:
        List of AttachmentSummary objects (one per attachment entry).
    """
    summaries: list[AttachmentSummary] = []
    for att in attachments.values():
        preview = _build_attachment_preview(att)
        summaries.append(
            AttachmentSummary(
                preview=preview,
                fileName=att.fileName,
                fileType=att.fileExtension.lower(),
            )
        )
    return summaries


def _build_attachment_preview(att: AttachmentData) -> str | None:
    """Decode a single attachment and extract a PDF text preview if applicable.

    Args:
        att: Single AttachmentData entry from the n8n payload.

    Returns:
        First _PDF_PREVIEW_MAX_CHARS characters of extracted text for PDF files,
        or None for non-PDF files and any parsing error.
    """
    if att.fileExtension.lower() != "pdf":
        return None
    raw_bytes = _decode_base64(att.data)
    if not raw_bytes:
        return None
    return _extract_pdf_preview(raw_bytes, _PDF_PREVIEW_MAX_CHARS)


def _decode_base64(data: str) -> bytes:
    """Decode a base64-encoded string to raw bytes.

    Returns empty bytes on any decoding error so that a single corrupt
    attachment does not abort processing of the entire email batch.

    Args:
        data: Base64-encoded string as provided by n8n.

    Returns:
        Decoded bytes, or b'' when data is empty or invalid base64.
    """
    if not data:
        return b""
    try:
        return base64.b64decode(data)
    except Exception:
        logger.warning("Failed to decode base64 attachment data (len=%d)", len(data))
        return b""


def _extract_pdf_preview(
    pdf_bytes: bytes, max_chars: int = _PDF_PREVIEW_MAX_CHARS
) -> str | None:
    """Extract a text preview from PDF bytes using pdfplumber.

    Concatenates text from all pages until max_chars is reached. Returns None
    on any exception (corrupt PDF, password-protected, image-only, etc.) so
    that attachment errors do not propagate to the caller.

    Args:
        pdf_bytes: Raw bytes of a PDF file.
        max_chars: Maximum number of characters to extract. Defaults to 5 000.

    Returns:
        Extracted text string (possibly shorter than max_chars if the PDF has
        little text), or None when extraction fails for any reason.
    """
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text_parts: list[str] = []
            total = 0
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                remaining = max_chars - total
                text_parts.append(page_text[:remaining])
                total += len(page_text[:remaining])
                if total >= max_chars:
                    break
            result = "".join(text_parts).strip()
            return result if result else None
    except Exception:
        return None
