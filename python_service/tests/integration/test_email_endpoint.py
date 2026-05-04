"""Integration tests for the POST /emailProcessingService endpoint.

Tests written before implementation (TDD RED phase).
Tests the full HTTP contract: status codes, response schema, data transformations.
Nomenclature: test_<endpoint>_<scenario>_<expected_result>
"""

import base64

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_email_payload(
    email_id: str = "email_1",
    requisitioner: str = 'From: "testing" <user@example.com>',
    subject: str = "Subject: test subject",
    text: str = "email body text",
    attachment: dict | None = None,
) -> dict:
    """Build a single email item dict for use in the JSON array payload."""
    item: dict = {
        "email": email_id,
        "requisitioner": requisitioner,
        "subject": subject,
        "text": text,
    }
    if attachment is not None:
        item["attachment"] = attachment
    return item


def _make_attachment(file_name: str = "doc.pdf", ext: str = "pdf") -> dict:
    """Build a minimal attachment dict with base64-encoded content."""
    return {
        "attachment_0": {
            "mimeType": "application/pdf",
            "fileExtension": ext,
            "data": base64.b64encode(b"%PDF-1.4 minimal content").decode(),
            "fileName": file_name,
            "fileSize": "1 kB",
        }
    }


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_post_email_valid_with_attachment_returns_200(client) -> None:
    """Valid JSON payload with a base64 attachment returns HTTP 200."""
    payload = [_make_email_payload(attachment=_make_attachment())]
    response = await client.post("/emailProcessingService", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_email_valid_without_attachment_returns_200(client) -> None:
    """Valid JSON payload without attachment returns HTTP 200."""
    payload = [_make_email_payload()]
    response = await client.post("/emailProcessingService", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_email_batch_multiple_returns_200_with_two_results(client) -> None:
    """Batch of 2 emails returns HTTP 200 and a JSON array with 2 items."""
    payload = [
        _make_email_payload(email_id="email_0"),
        _make_email_payload(email_id="email_1", attachment=_make_attachment()),
    ]
    response = await client.post("/emailProcessingService", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_post_email_empty_payload_returns_200_with_empty_array(client) -> None:
    """Empty JSON array returns HTTP 200 and an empty response array."""
    response = await client.post("/emailProcessingService", json=[])
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_post_email_invalid_json_returns_422(client) -> None:
    """Malformed JSON body (not a list) returns HTTP 422 Unprocessable Entity."""
    response = await client.post(
        "/emailProcessingService",
        content=b"not json at all",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_email_missing_required_fields_returns_422(client) -> None:
    """Payload missing the required 'email' field returns HTTP 422."""
    bad_payload = [
        {
            "requisitioner": 'From: "name" <a@b.com>',
            "subject": "Subject: test",
            "text": "body",
        }
    ]
    response = await client.post("/emailProcessingService", json=bad_payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Data transformation assertions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_post_email_subject_cleaned_removes_prefix(client) -> None:
    """Response 'subject' field has the 'Subject:' prefix stripped."""
    payload = [_make_email_payload(subject="Subject: clean this title")]
    response = await client.post("/emailProcessingService", json=payload)
    data = response.json()
    assert data[0]["subject"] == "clean this title"


@pytest.mark.asyncio
async def test_post_email_requisitioner_cleaned_returns_email_only(client) -> None:
    """Response 'requisitioner' contains only the email address (no 'From:' wrapper)."""
    payload = [_make_email_payload(requisitioner='From: "Full Name" <clean@example.com>')]
    response = await client.post("/emailProcessingService", json=payload)
    data = response.json()
    assert data[0]["requisitioner"] == "clean@example.com"


@pytest.mark.asyncio
async def test_post_email_footer_removed_from_text(client) -> None:
    """Provider footer is stripped from the 'text' field in the response."""
    body_with_footer = "real content\n\nEnviado com um e-mail seguro do Proton Mail"
    payload = [_make_email_payload(text=body_with_footer)]
    response = await client.post("/emailProcessingService", json=payload)
    data = response.json()
    assert "Enviado" not in data[0]["text"]
    assert "real content" in data[0]["text"]


@pytest.mark.asyncio
async def test_post_email_without_attachment_has_no_attachment_summary(client) -> None:
    """Email without attachment key returns result with attachmentSummary absent/null."""
    payload = [_make_email_payload()]
    response = await client.post("/emailProcessingService", json=payload)
    data = response.json()
    # attachmentSummary should be None (null in JSON) or absent
    assert data[0].get("attachmentSummary") is None
