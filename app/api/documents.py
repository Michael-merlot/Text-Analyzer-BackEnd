from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import operations_CRUD
from app.services import file_upload, text_analyzer
from typing import List, Dict, Any
from app.database.schemas import DocumentCreate, Document
import os

router = APIRouter()

@router.post("/", summary="Загрузить и проанализировать текстовый файл", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db) # по поводу бд
):
    # загружает текстовый файл, анализирует его содержимое 
    # и сохраняет результат в базе данных.
    
    file_upload.validate_file(file)
    text = file_upload.extract_text(file)
    analysis_result = text_analyzer.analyze_text(text)

    title = os.path.splitext(file.filename)[0]
    document = operations_CRUD.create_document(
        db=db, # тут посмотрите по поводу бд
        document=DocumentCreate(
            title=title,
            content=text[:1000],  # сохранение первых 1000 символов, можете поиграться со значениями
            word_count=analysis_result["word_count"],
            sentence_count=analysis_result["sentence_count"],
            readability_score=analysis_result["readability_score"],
            keywords=analysis_result["keywords"]
        )
    )
    
    result_with_id = analysis_result.copy()
    result_with_id["id"] = document.id # добавление ID документа в результат анализа
    
    return result_with_id

@router.get("/{document_id}", summary="Получить информацию о документе", response_model=Document)
def get_document(document_id: int, db: Session = Depends(get_db)):

    document = operations_CRUD.get_document(db, document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден"
        )
    
    return document

@router.get("/", summary="Получить список документов", response_model=List[Document])
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    documents = operations_CRUD.get_documents(db, skip=skip, limit=limit)
    return documents
