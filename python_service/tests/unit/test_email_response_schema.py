"""Unit tests for EmailResult and AttachmentSummary Pydantic response schemas.

Tests written before implementation (TDD RED phase).
Nomenclature: test_<model>_<scenario>_<expected_result>
"""

import pytest
from pydantic import ValidationError

from app.domain.schemas.email_response import AttachmentSummary, EmailResult

# ---------------------------------------------------------------------------
# AttachmentSummary tests
# ---------------------------------------------------------------------------


def test_attachment_summary_with_preview_valid_returns_model() -> None:
    """AttachmentSummary validates when preview (first 5k chars) is present."""
    summary = AttachmentSummary(preview="A" * 5000, fileName="doc.pdf", fileType="pdf")
    assert summary.preview is not None
    assert len(summary.preview) == 5000
    assert summary.fileType == "pdf"


def test_attachment_summary_without_preview_valid_returns_none() -> None:
    """AttachmentSummary allows preview=None for non-PDF or un-parseable files."""
    summary = AttachmentSummary(preview=None, fileName="doc.odt", fileType="odt")
    assert summary.preview is None
    assert summary.fileName == "doc.odt"


# ---------------------------------------------------------------------------
# EmailResult tests
# ---------------------------------------------------------------------------


def test_email_result_with_attachment_summary_valid_returns_model() -> None:
    """EmailResult validates correctly when attachmentSummary list is present."""
    result = EmailResult(
        email="email_1",
        requisitioner="user@example.com",
        subject="test title",
        text="body text",
        attachmentSummary=[
            AttachmentSummary(preview="pdf content", fileName="doc.pdf", fileType="pdf")
        ],
    )
    assert result.email == "email_1"
    assert result.attachmentSummary is not None
    assert len(result.attachmentSummary) == 1
    assert result.attachmentSummary[0].fileType == "pdf"


def test_email_result_without_attachment_summary_defaults_to_none() -> None:
    """EmailResult allows omitting attachmentSummary; it defaults to None."""
    result = EmailResult(
        email="email_0",
        requisitioner="user@example.com",
        subject="no attachment",
        text="body",
    )
    assert result.attachmentSummary is None


def test_email_result_missing_required_field_raises_validation_error() -> None:
    """EmailResult raises ValidationError when a required field (email) is missing."""
    with pytest.raises(ValidationError):
        EmailResult(  # type: ignore[call-arg]
            requisitioner="user@example.com",
            subject="test",
            text="body",
        )
