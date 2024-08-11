from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000,
                      description="Text to analyze")

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Text cannot be empty or just whitespace')
        return v
