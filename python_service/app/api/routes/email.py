"""API route for the email processing endpoint.

Receives a JSON array of raw email payloads from n8n, delegates processing to
the email_processor service, and returns a cleaned, transformed response array
ready for LLM consumption.
"""

from fastapi import APIRouter

from app.domain.schemas.email_payload import EmailPayload
from app.domain.schemas.email_response import EmailResult
from app.services.email_processor import process_email_batch

router = APIRouter()


@router.post("/emailProcessingService", response_model=list[EmailResult])
async def process_emails(payload: list[EmailPayload]) -> list[EmailResult]:
    """Process a batch of emails from the n8n workflow.

    Receives the raw JSON array produced by the n8n merge node. Each item
    contains email metadata and optional base64-encoded attachments.

    Args:
        payload: List of raw EmailPayload objects. May be empty.

    Returns:
        List of EmailResult objects with cleaned fields and attachment previews.
        Returns an empty list when payload is empty.
    """
    return await process_email_batch(payload)
