from transformers import pipeline


class NLPModel:
    def __init__(self):
        self.language_detector = pipeline(
            "text-classification", model="papluca/xlm-roberta-base-language-detection")

    def detect_language(self, text):
        result = self.language_detector(text)[0]
        return {
            "detected_language": result["label"],
            "confidence": result["score"]
        }
