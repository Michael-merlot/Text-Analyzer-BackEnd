from fastapi import APIRouter, HTTPException, status
from app.services import readability_calculator
from typing import Dict, Any
from app.database.schemas import TextRequest, ReadabilityResponse

router = APIRouter()

@router.post("/", summary="Оценить читаемость текста", response_model=ReadabilityResponse)
async def check_readability(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        readability_score = readability_calculator.calculate_readability(request.text)
        interpretation = readability_calculator.interpret_readability(readability_score)
        stats = readability_calculator.get_text_stats(request.text)
        
        return {
            "readability_score": readability_score,
            "interpretation": interpretation,
            "stats": stats
        }
    except Exception as e:
        import traceback
        print(f"Ошибка при оценке читаемости: {str(e)}")
        print(traceback.format_exc())
        
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при оценке читаемости: {str(e)}"
        )

@router.post("/detailed", summary="Получить детальный анализ читаемости")
async def detailed_readability(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст не может быть пустым"
            )
        
        detailed_metrics = readability_calculator.get_detailed_metrics(request.text)
        return detailed_metrics
    except Exception as e:
        import traceback
        print(f"Ошибка при получении детального анализа: {str(e)}")
        print(traceback.format_exc())
        
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении детального анализа читаемости: {str(e)}"
        )

@router.get("/test", summary="Тестовый эндпоинт")
def test_endpoint():
    return {"status": "ok", "message": "API читаемости работает"}
