from fastapi import HTTPException, status, UploadFile
from typing import List

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

async def validate_files(files: List[UploadFile]):
    for file in files:
        ext = file.filename.lower().rsplit(".", 1)[-1]
        if f".{ext}" not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo {file.filename} não suportado"
            )
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo {file.filename} excede o tamanho máximo permitido"
            )
        await file.seek(0)
