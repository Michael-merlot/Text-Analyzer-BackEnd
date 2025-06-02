from fastapi import APIRouter, HTTPException, status
from app.services import text_analyzer
from typing import Dict, Any, List
from app.database.schemas import TextRequest, AnalysisResponse

router = APIRouter()

@router.post("/", summary="Анализировать текст", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        
        analysis_result = text_analyzer.analyze_text(request.text)
        return analysis_result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при анализе текста: {str(e)}"
        )

@router.post("/check-keywords", summary="Проверить текст на ключевые слова")
async def check_keywords(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        
        from app.services.keyword_extractor import extract_keywords
        keywords = extract_keywords(request.text)
        return {"keywords": keywords}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
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

