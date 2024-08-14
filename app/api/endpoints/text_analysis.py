from fastapi import APIRouter
from pydantic import BaseModel
from app.services.text_analysis_service import TextAnalysisService

router = APIRouter()
text_analysis_service = TextAnalysisService()


class TextRequest(BaseModel):
    text: str


@router.post("/analyze")
async def analyze_text(request: TextRequest):
    return text_analysis_service.analyze_text(request.text)
