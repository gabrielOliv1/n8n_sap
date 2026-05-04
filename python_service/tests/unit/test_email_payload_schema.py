"""Unit tests for EmailPayload and AttachmentData Pydantic schemas.

Tests written before implementation (TDD RED phase).
Nomenclature: test_<model>_<scenario>_<expected_result>
"""

import pytest
from pydantic import ValidationError

from app.domain.schemas.email_payload import AttachmentData, EmailPayload


# ---------------------------------------------------------------------------
# AttachmentData tests
# ---------------------------------------------------------------------------


def test_attachment_data_valid_returns_model() -> None:
    """AttachmentData validates when all required fields are present."""
    data = {
        "mimeType": "application/pdf",
        "fileExtension": "pdf",
        "data": "dGVzdA==",
        "fileName": "invoice.pdf",
        "fileSize": "30.4 kB",
    }
    attachment = AttachmentData(**data)
    assert attachment.fileName == "invoice.pdf"
    assert attachment.fileExtension == "pdf"


def test_attachment_data_missing_data_field_raises_validation_error() -> None:
    """AttachmentData raises ValidationError when 'data' (base64) field is absent."""
    data = {
        "mimeType": "application/pdf",
        "fileExtension": "pdf",
        "fileName": "invoice.pdf",
        "fileSize": "30.4 kB",
    }
    with pytest.raises(ValidationError):
        AttachmentData(**data)


# ---------------------------------------------------------------------------
# EmailPayload tests
# ---------------------------------------------------------------------------


def test_email_payload_with_attachment_valid_returns_model() -> None:
    """EmailPayload validates correctly when payload contains one attachment."""
    payload = {
        "email": "email_1",
        "requisitioner": 'From: "testing" <testing@email.com>',
        "subject": "Subject: teste 23/04 com docs",
        "text": "email body text",
        "attachment": {
            "attachment_0": {
                "mimeType": "application/pdf",
                "fileExtension": "pdf",
                "data": "dGVzdA==",
                "fileName": "invoice.pdf",
                "fileSize": "30.4 kB",
            }
        },
    }
    model = EmailPayload(**payload)
    assert model.email == "email_1"
    assert model.attachment is not None
    assert "attachment_0" in model.attachment


def test_email_payload_without_attachment_valid_returns_none() -> None:
    """EmailPayload validates when no 'attachment' key is present; field defaults to None."""
    payload = {
        "email": "email_0",
        "requisitioner": 'From: "gabriel.ov" <testing@email.com>',
        "subject": "Subject: teste 23/04 sem docs",
        "text": "sem docs",
    }
    model = EmailPayload(**payload)
    assert model.attachment is None


def test_email_payload_missing_required_field_raises_validation_error() -> None:
    """EmailPayload raises ValidationError when 'subject' (required) is missing."""
    payload = {
        "email": "email_0",
        "requisitioner": 'From: "gabriel.ov" <testing@email.com>',
        "text": "sem docs",
    }
    with pytest.raises(ValidationError):
        EmailPayload(**payload)


def test_email_payload_multiple_attachments_valid_returns_model() -> None:
    """EmailPayload validates correctly when 'attachment' dict has 2 entries."""
    payload = {
        "email": "email_2",
        "requisitioner": 'From: "name" <user@example.com>',
        "subject": "Subject: multiple attachments",
        "text": "body",
        "attachment": {
            "attachment_0": {
                "mimeType": "application/pdf",
                "fileExtension": "pdf",
                "data": "dGVzdA==",
                "fileName": "file1.pdf",
                "fileSize": "10 kB",
            },
            "attachment_1": {
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "fileExtension": "docx",
                "data": "dGVzdA==",
                "fileName": "file2.docx",
                "fileSize": "20 kB",
            },
        },
    }
    model = EmailPayload(**payload)
    assert len(model.attachment) == 2  # type: ignore[arg-type]
    assert "attachment_1" in model.attachment  # type: ignore[operator]
