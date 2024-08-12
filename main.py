from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.services.text_analysis_service import TextAnalysisService, InputValidationError, AnalysisError
from app.models.api_models import TextRequest

app = FastAPI(
    title="TextAnalysis API",
    description="An API for various text analysis tasks including language detection, sentiment analysis, and more.",
    version="1.0.0",
)

# Create a router for v1 of the API
v1_router = APIRouter(prefix="/v1")

text_analysis_service = TextAnalysisService()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )


@app.exception_handler(InputValidationError)
async def input_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(AnalysisError)
async def analysis_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


@app.get("/health")
async def health_check():
    """
    Perform a health check on the API.
    """
    return {"status": "healthy"}


@v1_router.post("/analyze")
async def analyze_text(request: TextRequest):
    """
    Analyze the given text and return various linguistic insights.
    """
    try:
        return text_analysis_service.analyze_text(request.text)
    except InputValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AnalysisError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the v1 router in the main app
app.include_router(v1_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
