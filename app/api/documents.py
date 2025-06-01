from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import operations_CRUD
from app.services import file_upload, text_analyzer
from typing import List, Dict, Any
from app.database.schemas import DocumentCreate, Document
import os

router = APIRouter()

@router.post("/", summary="��������� � ���������������� ��������� ����", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db) # �� ������ ��
):
    # ��������� ��������� ����, ����������� ��� ���������� 
    # � ��������� ��������� � ���� ������.
    
    file_upload.validate_file(file)
    text = file_upload.extract_text(file)
    analysis_result = text_analyzer.analyze_text(text)

    title = os.path.splitext(file.filename)[0]
    document = operations_CRUD.create_document(
        db=db, # ��� ���������� �� ������ ��
        document=DocumentCreate(
            title=title,
            content=text[:1000],  # ���������� ������ 1000 ��������, ������ ���������� �� ����������
            word_count=analysis_result["word_count"],
            sentence_count=analysis_result["sentence_count"],
            readability_score=analysis_result["readability_score"],
            keywords=analysis_result["keywords"]
        )
    )
    
    result_with_id = analysis_result.copy()
    result_with_id["id"] = document.id # ���������� ID ��������� � ��������� �������
    
    return result_with_id

@router.get("/{document_id}", summary="�������� ���������� � ���������", response_model=Document)
def get_document(document_id: int, db: Session = Depends(get_db)):

    document = operations_CRUD.get_document(db, document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="�������� �� ������"
        )
    
    return document

@router.get("/", summary="�������� ������ ����������", response_model=List[Document])
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    documents = operations_CRUD.get_documents(db, skip=skip, limit=limit)
    return documents
