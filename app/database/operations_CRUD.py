import sqlite3
from app.database.schemas import DocumentCreate, Document

def create_document(db: sqlite3.Connection, document: DocumentCreate):
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO documents
        (title, content, word_count, sentence_count, readability_score, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (document.title,
         document.content,
         document.word_count,
         document.sentence_count,
         document.readability_score,
         document.keywords)

    )
    db.commit()

def get_document(db: sqlite3.Connection, document_id: int):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * from documents WHERE id = ?
        """, (document_id,)
    )
    result = cursor.fetchone()

    document_data = {
        "id": result[0],
        "title": result[1],
        "content": result[2],
        "word_count": result[3],
        "sentence_count": result[4],
        "readability_score": result[5],
        "keywords": result[6]
    }
    return Document(**document_data)

def get_documents(skip: int, limit: int, db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id, title, content, word_count, 
               sentence_count, readability_score, keywords
        FROM documents
        ORDER BY id ASC
        LIMIT ? OFFSET ?
        """,
        (limit, skip)
    )
    results = cursor.fetchall()
    documents = []
    for row in results:
        document = Document(
            id=row[0],
            title=row[1],
            content=row[2],
            word_count=row[3],
            sentence_count=row[4],
            readability_score=row[5],
            keywords=row[6]
        )
        documents.append(document)
    return documents
