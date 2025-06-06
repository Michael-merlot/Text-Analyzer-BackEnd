from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import operations_CRUD
from app.services import file_upload, text_analyzer
from typing import List, Dict, Any
from app.database.schemas import DocumentCreate
import os
import mimetypes

router = APIRouter()

ALLOWED_EXTENSIONS = {".txt", ".docx", ".md", ".rtf", ".pdf"}
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 МБ

@router.post("/", summary="Загрузить и проанализировать текстовый файл")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Новые проверки безопасности
        if file is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не был предоставлен"
            )

        ext = os.path.splitext(file.filename)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Недопустимый тип файла: {ext}. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Проверка MIME-типа
        guessed_type, _ = mimetypes.guess_type(file.filename)
        if not guessed_type or not guessed_type.startswith("text") and "pdf" not in guessed_type:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Недопустимый MIME-тип: {guessed_type}"
            )

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Файл превышает допустимый размер 1 МБ"
            )
            
        # Возвращаем указатель файла в начало, так как мы уже прочитали его содержимое
        await file.seek(0)

        # Существующая логика обработки
        file_upload.validate_file(file)  # Возможно, эту функцию нужно будет обновить
        print(f"Файл получен: {file.filename}, размер: {len(contents)} байт")
        
        text = file_upload.extract_text(file)

        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Извлеченный текст пуст"
            )
            
        print(f"Текст извлечен, длина: {len(text)} символов")

        analysis_result = text_analyzer.analyze_text(text)
        print(f"Анализ выполнен: {analysis_result}")
        title = os.path.splitext(file.filename)[0] if file.filename else "Без названия"
        document = operations_CRUD.create_document(
            db=db,
            document=DocumentCreate(
                title=title,
                content=text[:1000], 
                word_count=analysis_result["word_count"],
                sentence_count=analysis_result["sentence_count"],
                readability_score=analysis_result["readability_score"],
                keywords=analysis_result["keywords"]
            )
        )
        result_with_id = analysis_result.copy()
        if hasattr(document, "id"):
            result_with_id["id"] = document.id
        elif isinstance(document, dict) and "id" in document:
            result_with_id["id"] = document["id"]
        else:
            print(f"Тип документа: {type(document)}")
            result_with_id["id"] = 0 
            
        print(f"Документ сохранен, ID: {result_with_id['id']}")
        
        return result_with_id
    except Exception as e:
        print(f"ОШИБКА при загрузке документа: {str(e)}")
        print(traceback.format_exc())
        
        if isinstance(e, HTTPException):
            raise e
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при обработке файла: {str(e)}"
        )

@router.get("/test", summary="Тестовый эндпоинт")
def test_endpoint():
    return {"status": "ok", "message": "API документов работает"}

@router.get("/{document_id}", summary="Получить информацию о документе")
def get_document(document_id: int, db: Session = Depends(get_db)):

    try:
        document = operations_CRUD.get_document(db, document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Документ с ID {document_id} не найден"
            )
        return document
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении документа: {str(e)}"
        )

@router.get("/", summary="Получить список документов")
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        documents = operations_CRUD.get_documents(db, skip=skip, limit=limit)
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка документов: {str(e)}"
        )

