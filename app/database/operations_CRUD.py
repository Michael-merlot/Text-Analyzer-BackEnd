import json
from sqlalchemy.orm import Session
from app.database import models
from app.database.schemas import DocumentCreate

def create_document(db: Session, document: DocumentCreate):
    try:
        db_document = models.Document(
            title=document.title,
            content=document.content,
            word_count=document.word_count,
            sentence_count=document.sentence_count,
            readability_score=document.readability_score,
            keywords=json.dumps(document.keywords)
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    except Exception as e:
        db.rollback()
        raise Exception(f"Ошибка при сохранении документа: {str(e)}")

def get_document(db: Session, document_id: int):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if document:
        document_dict = {c.name: getattr(document, c.name) for c in document.__table__.columns}
        if document_dict["keywords"]:
            document_dict["keywords"] = json.loads(document_dict["keywords"])
        return document_dict
    return None

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    documents = db.query(models.Document).offset(skip).limit(limit).all()
    result = []
    for doc in documents:
        doc_dict = {c.name: getattr(doc, c.name) for c in doc.__table__.columns}
        if doc_dict["keywords"]:
            doc_dict["keywords"] = json.loads(doc_dict["keywords"])
        result.append(doc_dict)
    return result
