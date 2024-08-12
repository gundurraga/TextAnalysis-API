# File: app/services/text_analysis_service.py

from typing import Dict, Any
from ..models.nlp_model import NLPModel
import logging

logger = logging.getLogger(__name__)


class TextAnalysisError(Exception):
    """Base class for TextAnalysis exceptions"""
    pass


class InputValidationError(TextAnalysisError):
    """Raised when input validation fails"""
    pass


class AnalysisError(TextAnalysisError):
    """Raised when text analysis fails"""
    pass


class TextAnalysisService:
    def __init__(self):
        self.nlp_model = NLPModel()

    def validate_text(self, text: str) -> None:
        if not text.strip():
            raise InputValidationError("Empty text is not allowed")
        if len(text) > 10000:
            raise InputValidationError(
                "Text exceeds maximum length of 10000 characters")

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
        except InputValidationError as e:
            logger.warning(f"Input validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error analyzing text: {str(e)}")
            raise AnalysisError(
                "An unexpected error occurred during text analysis")

    def extract_topics(self, text: str) -> Dict[str, Any]:
        try:
            self.validate_text(text)
            topics = self.nlp_model.extract_topics(text)
            return {"topics": topics}
        except InputValidationError as e:
            logger.warning(f"Input validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error extracting topics: {str(e)}")
            raise AnalysisError(
                "An unexpected error occurred during topic extraction")
