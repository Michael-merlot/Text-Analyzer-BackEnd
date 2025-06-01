from fastapi import APIRouter, HTTPException, status
from app.services import text_analyzer
from typing import Dict, Any, List
from app.database.schemas import TextRequest, AnalysisResponse # пусть будет так, если что измените на нужное, , другого пока не знаю

router = APIRouter()

@router.post("/", summary="Анализировать текст", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текст не может быть пустым"
        )
    
    analysis_result = text_analyzer.analyze_text(request.text)
    return analysis_result

@router.post("/check-keywords", summary="Проверить текст на ключевые слова")
async def check_keywords(request: TextRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текст не может быть пустым"
        )
    
    keywords = text_analyzer.extract_keywords(request.text)
    return {"keywords": keywords}
