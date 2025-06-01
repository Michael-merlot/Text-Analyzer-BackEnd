from fastapi import APIRouter, HTTPException, status
from app.services import readability_calculator
from typing import Dict, Any
from app.database.schemas import TextRequest, ReadabilityResponse # ����� ����� ���, ���� ��� �������� �� ������, ������� ���� �� ����

router = APIRouter()

@router.post("/", summary="������� ���������� ������", response_model=ReadabilityResponse)
async def check_readability(request: TextRequest):
    """
    # ������� ������ � ������� ������
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="����� �� ����� ���� ������"
        )
    
    readability_score = readability_calculator.calculate_readability(request.text)
    interpretation = readability_calculator.interpret_readability(readability_score)
    stats = readability_calculator.get_text_stats(request.text)
    
    return {
        "readability_score": readability_score,
        "interpretation": interpretation,
        "stats": stats
    }

@router.post("/detailed", summary="�������� ��������� ������ ����������")
async def detailed_readability(request: TextRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="����� �� ����� ���� ������"
        )
    
    detailed_metrics = readability_calculator.get_detailed_metrics(request.text)
    return detailed_metrics
