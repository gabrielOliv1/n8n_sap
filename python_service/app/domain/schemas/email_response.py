"""Pydantic schemas for the outbound email processing response.

Models the cleaned, transformed data ready for LLM consumption.
"""

from pydantic import BaseModel


class AttachmentSummary(BaseModel):
    """Preview of a single parsed attachment.

    Attributes:
        preview: First 5 000 characters of extracted text content.
            None when the file is not a PDF or cannot be parsed.
        fileName: Original file name including extension.
        fileType: Lowercase file extension without leading dot (e.g. 'pdf').
    """

    preview: str | None = None
    fileName: str
    fileType: str


class EmailResult(BaseModel):
    """Processed email with cleaned fields and optional attachment previews.

    All string fields have been normalised:
    - requisitioner: bare email address (From header stripped).
    - subject: title only (Subject: prefix stripped).
    - text: body without known provider/device footers.

    Attributes:
        email: Internal n8n email identifier (e.g. 'email_1').
        requisitioner: Cleaned sender email address.
        subject: Cleaned subject line.
        text: Cleaned email body.
        attachmentSummary: List of attachment previews, or None if no attachments.
    """

    email: str
    requisitioner: str
    subject: str
    text: str
    attachmentSummary: list[AttachmentSummary] | None = None
