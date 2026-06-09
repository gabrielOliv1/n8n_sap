"""Pydantic schemas for the inbound n8n email JSON payload.

Models the raw array produced by the n8n merge node before any transformation.
"""

from pydantic import BaseModel


class AttachmentData(BaseModel):
    """Single attachment entry from the n8n email payload.

    Attributes:
        mimeType: MIME type of the file (e.g. 'application/pdf').
        fileExtension: File extension without leading dot (e.g. 'pdf').
        data: Base64-encoded file content as produced by n8n.
        fileName: Original file name including extension.
        fileSize: Human-readable file size string (e.g. '30.4 kB').
    """

    mimeType: str
    fileExtension: str
    data: str  # base64-encoded content
    fileName: str
    fileSize: str


class EmailPayload(BaseModel):
    """Single email item from the n8n JSON array.

    Attributes:
        email: Internal email identifier assigned by n8n (e.g. 'email_1').
        requisitioner: Raw sender header (e.g. 'From: "name" <email@host.com>').
        subject: Raw subject header (e.g. 'Subject: title').
        text: Raw email body text including any provider footers.
        attachment: Optional dict mapping attachment keys to AttachmentData objects.
            Key format used by n8n: 'attachment_0', 'attachment_1', etc.
            None when the email has no attachments.
    """

    email: str
    requisitioner: str
    subject: str
    text: str
    attachment: dict[str, AttachmentData] | None = None
