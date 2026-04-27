from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.attachment_processor import process_file

router = APIRouter()


@router.post("/attachmentProcessingService")
async def process_attachment(file: UploadFile = File(...)):
    try:
        content = await process_file(file)
        return {"filename": file.filename, "extracted_content": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
