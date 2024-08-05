from app.services.text_analysis_service import TextAnalysisService
from pydantic import BaseModel
from fastapi import FastAPI
import sys
from pathlib import Path

# Añade el directorio raíz del proyecto al path de Python
sys.path.append(str(Path(__file__).parent))


app = FastAPI()
text_analysis_service = TextAnalysisService()


class TextRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Welcome to TextAnalysis API"}


@app.post("/analyze")
async def analyze_text(request: TextRequest):
    return text_analysis_service.analyze_text(request.text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
