import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_upload_valid_file(client: AsyncClient):
    file_content = b"PDF content mock"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    response = await client.post("/attachmentProcessingService", files=files)

    assert response.status_code == 200
    assert response.json()["filename"] == "test.pdf"
    assert "processed successfully" in response.json()["extracted_content"]


@pytest.mark.asyncio
async def test_upload_no_file(client: AsyncClient):
    response = await client.post("/attachmentProcessingService")
    assert response.status_code == 422  # FastAPI validation error
