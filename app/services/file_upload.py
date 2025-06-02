from fastapi import UploadFile, HTTPException, status
from tempfile import NamedTemporaryFile
import shutil
import os
from app.core.config import settings

def validate_file(file: UploadFile) -> None:
    if file.filename is None or file.filename == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл не выбран"
        )
    
    if file.content_type not in settings.ALLOWED_MIME:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Разрешен только тип .txt",
        )

def extract_text(file: UploadFile) -> str:
    with NamedTemporaryFile(delete=True, mode="wb+", suffix=".txt") as tmp:
        shutil.copyfileobj(file.file, tmp)
        
        tmp.seek(0, os.SEEK_END)
        size = tmp.tell()
        if size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Файл превышает размер {settings.MAX_FILE_SIZE / 1024 / 1024} МБ",
            )
        if size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл пуст"
            )
        
        tmp.seek(0)
        raw = tmp.read()
        
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return raw.decode("cp1251")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Файл не является корректным текстом или имеет неподдерживаемую кодировку",
                )
