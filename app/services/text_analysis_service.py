from ..models.nlp_model import NLPModel


class TextAnalysisService:
    def __init__(self):
        self.nlp_model = NLPModel()

    def analyze_text(self, text):
        language_info = self.nlp_model.detect_language(text)
        return {
            "text_length": len(text),
            "language": language_info["detected_language"],
            "language_confidence": language_info["confidence"]
        }
