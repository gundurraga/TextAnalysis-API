from transformers import pipeline


class NLPModel:
    def __init__(self):
        self.language_detector = pipeline(
            "text-classification", model="papluca/xlm-roberta-base-language-detection")
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def detect_language(self, text):
        result = self.language_detector(text)[0]
        return {
            "detected_language": result["label"],
            "confidence": result["score"]
        }

    def analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)[0]
        return {
            "sentiment": result["label"],
            "confidence": result["score"]
        }
