from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import operations_CRUD
from app.services import file_upload, text_analyzer
from typing import List, Dict, Any
from app.database.schemas import DocumentCreate
import os

router = APIRouter()

@router.post("/", summary="Загрузить и проанализировать текстовый файл")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if file is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не был предоставлен"
            )
        print(f"Получен файл: {file.filename}, content_type: {file.content_type}")
        
        result_with_id = analysis_result.copy()
        result_with_id["id"] = document["id"] if isinstance(document, dict) else document.id
        
        return result_with_id
    except Exception as e:
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

