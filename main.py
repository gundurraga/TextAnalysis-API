from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from app.services.text_analysis_service import TextAnalysisService
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()
text_analysis_service = TextAnalysisService()


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000,
                      description="Text to analyze")

    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or just whitespace')
        return v


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.post("/analyze")
async def analyze_text(request: TextRequest):
    """
    Analyze the given text and return various linguistic insights.

    Args:
        request (TextRequest): The request body containing the text to analyze.

    Returns:
        dict: A dictionary containing analysis results.

    Raises:
        HTTPException: 400 for invalid input, 500 for unexpected errors.
    """
    try:
        return text_analysis_service.analyze_text(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
