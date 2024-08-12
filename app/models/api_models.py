from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    """
    Represents a request to analyze text.
    """
    text: str = Field(..., min_length=1, max_length=10000,
                      description="Text to analyze")

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        """
        Validate that the text is not empty or just whitespace.
        """
        if not v.strip():
            raise ValueError('Text cannot be empty or just whitespace')
        return v


class AnalysisResponse(BaseModel):
    """
    Represents the response from text analysis.
    """
    text_length: int
    language: str
    sentiment: dict
    is_offensive: bool
    entities: list
    summary: str
