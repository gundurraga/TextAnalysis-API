from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.text_analysis_service import TextAnalysisService

app = FastAPI()
text_analysis_service = TextAnalysisService()


class TextRequest(BaseModel):
    text: str


@app.post("/analyze")
async def analyze_text(request: TextRequest):
    try:
        return text_analysis_service.analyze_text(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
