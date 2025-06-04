from fastapi import UploadFile, HTTPException, status
import io
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
            detail=f"Разрешен только тип .txt. Текущий тип: {file.content_type}",
        )

def extract_text(file: UploadFile) -> str:
    try:
        contents = file.file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Файл превышает размер {settings.MAX_FILE_SIZE / 1024 / 1024} МБ",
            )

        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл пуст"
            )
        
        try:
            text = contents.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = contents.decode("cp1251")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Файл не является корректным текстом или имеет неподдерживаемую кодировку",
                )
        file.file.seek(0)
        
        return text
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        
        print(f"Ошибка при извлечении текста: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )
