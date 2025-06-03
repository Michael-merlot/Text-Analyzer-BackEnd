from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import bleach
import html

class TextRequest(BaseModel):
    text: str

    @field_validator('text')
    def sanitize_text(cls, v):
        """Очистка текста от XSS-угроз"""
        if not v:
            return v
            
        # Удаляем все HTML/JS-теги
        cleaned = bleach.clean(
            v,
            tags=[],  # Не разрешаем никакие теги
            attributes={},  # Запрещаем все атрибуты
            strip=True  # Удаляем запрещённое вместо экранирования
        )
        
        # Дополнительное экранирование спецсимволов
        return html.escape(cleaned)

class AnalysisResponse(BaseModel):
    word_count: int
    sentence_count: int
    readability_score: float
    keywords: List[str]
    main_topic: Optional[str] = None

    @field_validator('keywords', 'main_topic')
    def sanitize_output_fields(cls, v):
        """Санитизация полей вывода"""
        if isinstance(v, str):
            return html.escape(v)
        elif isinstance(v, list):
            return [html.escape(item) for item in v]
        return v

class ReadabilityResponse(BaseModel):
    readability_score: float
    interpretation: str
    stats: dict

    @field_validator('interpretation')
    def sanitize_interpretation(cls, v):
        """Очистка текста интерпретации"""
        return html.escape(v) if v else v

class DocumentBase(BaseModel):
    title: str
    content: str
    word_count: int
    sentence_count: int
    readability_score: float
    keywords: List[str]

    @field_validator('title', 'content')
    def sanitize_document_fields(cls, v):
        """Защита основных полей документа"""
        return html.escape(v) if v else v

    @field_validator('keywords')
    def sanitize_keywords(cls, v):
        """Очистка ключевых слов"""
        return [html.escape(item) for item in v]

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }