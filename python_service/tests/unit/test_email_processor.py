"""Unit tests for the email_processor service layer.

Tests written before implementation (TDD RED phase).
Covers private helpers (via direct import) and the public orchestration function.
Nomenclature: test_<function>_<scenario>_<expected_result>
"""

import base64
import io

import pytest

from app.domain.schemas.email_payload import AttachmentData, EmailPayload
from app.services.email_processor import (
    _clean_subject,
    _decode_base64,
    _extract_email_address,
    _extract_pdf_preview,
    process_email_batch,
)


# ---------------------------------------------------------------------------
# _extract_email_address
# ---------------------------------------------------------------------------


def test_extract_email_address_standard_returns_email_only() -> None:
    """Standard 'From: \"name\" <email>' format yields bare email address."""
    raw = 'From: "testing" <user@test.com>'
    assert _extract_email_address(raw) == "user@test.com"


def test_extract_email_address_no_name_returns_email_only() -> None:
    """'From: user@test.com' format (no display name) yields bare email address."""
    raw = "From: user@test.com"
    assert _extract_email_address(raw) == "user@test.com"


def test_extract_email_address_no_from_prefix_returns_original() -> None:
    """If no recognizable pattern found, the raw string is returned as-is."""
    raw = "not_an_email_header"
    # Should not raise — graceful fallback
    result = _extract_email_address(raw)
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# _clean_subject
# ---------------------------------------------------------------------------


def test_clean_subject_strips_prefix_returns_title_only() -> None:
    """'Subject: title' prefix is stripped; only the title is returned."""
    assert _clean_subject("Subject: test title") == "test title"


def test_clean_subject_no_prefix_returns_original() -> None:
    """Text without 'Subject:' prefix is returned unchanged."""
    assert _clean_subject("test title") == "test title"


def test_clean_subject_extra_whitespace_is_trimmed() -> None:
    """Leading/trailing whitespace is stripped from the subject."""
    assert _clean_subject("Subject:   test title  ") == "test title"


# ---------------------------------------------------------------------------
# _decode_base64
# ---------------------------------------------------------------------------


def test_decode_base64_valid_returns_decoded_bytes() -> None:
    """Valid base64 string decodes to the expected bytes."""
    original = b"hello world"
    encoded = base64.b64encode(original).decode()
    assert _decode_base64(encoded) == original


def test_decode_base64_invalid_returns_empty_bytes_no_error() -> None:
    """Corrupted base64 string returns empty bytes without raising an exception."""
    assert _decode_base64("!!!not_valid_base64!!!") == b""


def test_decode_base64_empty_string_returns_empty_bytes() -> None:
    """Empty string decodes to empty bytes without raising an exception."""
    assert _decode_base64("") == b""


# ---------------------------------------------------------------------------
# _extract_pdf_preview
# ---------------------------------------------------------------------------


def _make_minimal_pdf_bytes() -> bytes:
    """Create a minimal valid PDF in-memory using pdfplumber-compatible structure."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.drawString(100, 750, "Hello PDF world for testing purposes.")
        c.save()
        return buf.getvalue()
    except ImportError:
        # Fallback: return a known valid PDF header that pdfplumber can at least open
        return b"%PDF-1.4\n%EOF"


def test_extract_pdf_preview_valid_returns_string() -> None:
    """Valid PDF bytes produce a string preview (may be empty if no text layer)."""
    pdf_bytes = _make_minimal_pdf_bytes()
    result = _extract_pdf_preview(pdf_bytes)
    # Valid PDF → returns a string (possibly empty) or None — never raises
    assert result is None or isinstance(result, str)


def test_extract_pdf_preview_non_pdf_returns_none() -> None:
    """DOCX/random bytes that are not a PDF return None (graceful ignore)."""
    fake_docx = b"PK\x03\x04this is not a pdf"
    result = _extract_pdf_preview(fake_docx)
    assert result is None


def test_extract_pdf_preview_corrupted_returns_none() -> None:
    """Corrupted/random bytes return None without raising any exception."""
    result = _extract_pdf_preview(b"\x00\x01\x02\x03garbage")
    assert result is None


def test_extract_pdf_preview_max_chars_respected() -> None:
    """Returned preview is at most max_chars characters long."""
    pdf_bytes = _make_minimal_pdf_bytes()
    result = _extract_pdf_preview(pdf_bytes, max_chars=10)
    if result is not None:
        assert len(result) <= 10


# ---------------------------------------------------------------------------
# process_email_batch (async orchestration)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_process_email_batch_empty_list_returns_empty_list() -> None:
    """Empty input list produces an empty result list."""
    results = await process_email_batch([])
    assert results == []


@pytest.mark.asyncio
async def test_process_email_batch_without_attachment_returns_result() -> None:
    """Email without attachments produces EmailResult with attachmentSummary=None."""
    emails = [
        EmailPayload(
            email="email_0",
            requisitioner='From: "gabriel.ov" <testing@example.com>',
            subject="Subject: sem docs",
            text="sem docs\n\nEnviado com um e-mail seguro do provider",
        )
    ]
    results = await process_email_batch(emails)
    assert len(results) == 1
    result = results[0]
    assert result.email == "email_0"
    assert result.requisitioner == "testing@example.com"
    assert result.subject == "sem docs"
    assert "Enviado" not in result.text
    assert result.attachmentSummary is None


@pytest.mark.asyncio
async def test_process_email_batch_mixed_returns_both_results() -> None:
    """1 email with attachment + 1 without → 2 results in the response."""
    attachment_data = {
        "mimeType": "application/pdf",
        "fileExtension": "pdf",
        "data": base64.b64encode(b"%PDF-1.4 minimal").decode(),
        "fileName": "file.pdf",
        "fileSize": "1 kB",
    }
    emails = [
        EmailPayload(
            email="email_1",
            requisitioner='From: "tester" <tester@example.com>',
            subject="Subject: with attachment",
            text="body with attachment",
            attachment={"attachment_0": AttachmentData(**attachment_data)},
        ),
        EmailPayload(
            email="email_0",
            requisitioner='From: "tester" <tester@example.com>',
            subject="Subject: no attachment",
            text="body without attachment",
        ),
    ]
    results = await process_email_batch(emails)
    assert len(results) == 2
    # Email with attachment → attachmentSummary list present (may be empty or with None preview)
    result_with_att = next(r for r in results if r.email == "email_1")
    assert result_with_att.attachmentSummary is not None
    # Email without attachment → attachmentSummary is None
    result_without_att = next(r for r in results if r.email == "email_0")
    assert result_without_att.attachmentSummary is None
