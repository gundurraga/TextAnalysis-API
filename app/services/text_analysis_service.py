from ..models.nlp_model import NLPModel


class TextAnalysisService:
    def __init__(self):
        self.nlp_model = NLPModel()

    def analyze_text(self, text):
        analysis = {
            "text_length": len(text),
            "language": self.nlp_model.detect_language(text),
            "sentiment": self.nlp_model.analyze_sentiment(text),
            "is_offensive": self.nlp_model.detect_offensive_language(text),
            "entities": self.nlp_model.extract_entities(text)
        }

        # Add summarization for texts longer than 100 words
        if len(text.split()) > 100:
            analysis["summary"] = self.nlp_model.summarize_text(text)

        return analysis
