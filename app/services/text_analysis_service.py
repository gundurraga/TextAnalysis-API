from ..models.nlp_model import NLPModel


class TextAnalysisService:
    def __init__(self):
        self.nlp_model = NLPModel()

    def analyze_text(self, text):
        if not text.strip():
            raise ValueError("Empty text is not allowed")

        analysis = {
            "text_length": len(text),
            "language": self.nlp_model.detect_language(text),
            "sentiment": self.nlp_model.analyze_sentiment(text),
            "is_offensive": self.nlp_model.detect_offensive_language(text),
            "entities": self.nlp_model.extract_entities(text),
            # Always include summary
            "summary": self.nlp_model.summarize_text(text)
        }

        return analysis
