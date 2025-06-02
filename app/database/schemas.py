from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TextRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    word_count: int
    sentence_count: int
    readability_score: float
    keywords: List[str]
    main_topic: Optional[str] = None

class ReadabilityResponse(BaseModel):
    readability_score: float
    interpretation: str
    stats: dict

class DocumentBase(BaseModel):
    title: str
    content: str
    word_count: int
    sentence_count: int
    readability_score: float
    keywords: List[str]

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }
