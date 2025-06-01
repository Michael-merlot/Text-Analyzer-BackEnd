from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil
import os

app = FastAPI()

ALLOWED_MIME = "text/plain"
MAX_SIZE = 1 * 1024 * 1024 # 1 MB(примерно 500 страниц)


def validate_file(file: UploadFile) -> None:
    if file.content_type != ALLOWED_MIME:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Разрешён только тип .txt",
        )


def extract_text(file: UploadFile) -> str:
    with NamedTemporaryFile(delete=True, mode="wb+", suffix=".txt") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp.seek(0, os.SEEK_END)
        if tmp.tell() > MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Файл превышает размер 1 MB",
            )
        tmp.seek(0)
        raw = tmp.read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не является корректным UTF-8 текстом",
            )


"""Добавить код для анализа текста
def analyze_text(text: str) -> dict:
"""


@app.post("/upload/", summary="Загрузить и проанализировать текст")
async def upload_text(file: UploadFile = File(...)):
    validate_file(file)
    text = extract_text(file)
    analysis_result = analyze_text(text)


    """ Добавить схранение в бд
    fake_db.append()
    """


    return JSONResponse(content=analysis_result)
