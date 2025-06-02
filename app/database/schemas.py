from pydantic import BaseModel
from typing import List
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    content: str
    word_count: int
    sentence_count: int
    readability_score: float
    keywords: str

class Document(DocumentCreate):
    id: int
    created_at: datetime
