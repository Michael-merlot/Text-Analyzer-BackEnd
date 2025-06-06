﻿from fastapi import APIRouter, HTTPException, status, Request
from app.services import text_analyzer
from typing import Dict, Any, List
from app.database.schemas import TextRequest, AnalysisResponse
import bleach
import html
from app.core.logging_config import check_xss_attempt

router = APIRouter()

def sanitize_input(text: str) -> str:
    """Sanitize input text to prevent XSS attacks"""
    if not text:
        return text
    
    # Clean with bleach (allow no HTML tags at all)
    cleaned = bleach.clean(
        text,
        tags=[],  # No allowed tags
        attributes={},  # No allowed attributes
        strip=True  # Remove disallowed tags instead of escaping
    )
    
    # Additional HTML escaping
    return html.escape(cleaned)

@router.post("/", summary="Анализировать текст", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest, fastapi_request: Request):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        
        # XSS protection
        if check_xss_attempt(request.text, fastapi_request):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Обнаружена потенциальная XSS атака"
            )
        
        # Sanitize input before processing
        sanitized_text = sanitize_input(request.text)
        analysis_result = text_analyzer.analyze_text(sanitized_text)
        return analysis_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при анализе текста: {str(e)}"
        )

@router.post("/check-keywords", summary="Проверить текст на ключевые слова")
async def check_keywords(request: TextRequest, fastapi_request: Request):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        
        # XSS protection
        if check_xss_attempt(request.text, fastapi_request):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Обнаружена потенциальная XSS атака"
            )
        
        from app.services.keyword_extractor import extract_keywords
        sanitized_text = sanitize_input(request.text)
        keywords = extract_keywords(sanitized_text)
        return {"keywords": keywords}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при извлечении ключевых слов: {str(e)}"
        )

@router.get("/test", summary="Тестовый эндпоинт")
def test_endpoint():
    return {"status": "ok", "message": "API анализа работает"}

@router.get("/", summary="Получить информацию об API анализа")
async def get_analysis_info():
    return {
        "message": "API анализа текста. Используйте POST запрос с текстом для выполнения анализа.",
        "example": {
            "text": "Ваш текст для анализа здесь"
        }
    }