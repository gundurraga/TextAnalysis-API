from typing import Dict, Any
from ..models.nlp_model import NLPModel
import logging

logger = logging.getLogger(__name__)


class TextAnalysisService:
    def __init__(self):
        self.nlp_model = NLPModel()

    def validate_text(self, text: str) -> None:
        if not text.strip():
            raise ValueError("Empty text is not allowed")
        if len(text) > 10000:
            raise ValueError("Text exceeds maximum length of 10000 characters")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            self.validate_text(text)

            analysis = {
                "text_length": len(text),
                "language": self.nlp_model.detect_language(text),
                "sentiment": self.nlp_model.analyze_sentiment(text),
                "is_offensive": self.nlp_model.detect_offensive_language(text),
                "entities": self.nlp_model.extract_entities(text),
                "summary": self.nlp_model.summarize_text(text)
            }

            return analysis
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise
