from fastapi import UploadFile, HTTPException
import io

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv", ".txt"}
MAX_FILE_SIZE_MB = 10

async def process_file(file: UploadFile) -> str:
    # Apenas um mock simples por enquanto para MVP
    file_bytes = await file.read()
    
    # Validar tamanho do arquivo
    if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File too large. Max size is {MAX_FILE_SIZE_MB}MB")
        
    # Aqui pode-se adicionar lógica real de extração (ex: pdfplumber, python-docx)
    return f"File {file.filename} processed successfully. Size: {len(file_bytes)} bytes."
