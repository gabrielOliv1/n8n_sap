import pytest
from fastapi import UploadFile
import io
from app.services.attachment_processor import process_file

@pytest.mark.asyncio
async def test_process_file_valid():
    content = b"Mock document content"
    mock_file = UploadFile(filename="doc.pdf", file=io.BytesIO(content))
    
    result = await process_file(mock_file)
    assert "doc.pdf" in result
    assert "21 bytes" in result

@pytest.mark.asyncio
async def test_process_file_too_large():
    # Simulate a file larger than 10MB
    large_content = b"0" * (11 * 1024 * 1024)
    mock_file = UploadFile(filename="large.pdf", file=io.BytesIO(large_content))
    
    with pytest.raises(ValueError, match="File too large"):
        await process_file(mock_file)
