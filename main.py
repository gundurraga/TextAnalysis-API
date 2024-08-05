from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Welcome to TextAnalysis API"}


@app.post("/analyze")
async def analyze_text(request: TextRequest):
    # Por ahora, simplemente devolveremos la longitud del texto
    return {"text_length": len(request.text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
