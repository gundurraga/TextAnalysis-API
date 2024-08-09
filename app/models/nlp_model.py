import logging
from typing import List, Dict
from transformers import pipeline
from langdetect import detect, DetectorFactory
import spacy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DetectorFactory.seed = 0  # For consistent results in language detection


class NLPModel:
    def __init__(self):
        try:
            # Sentiment Analysis
            self.sentiment_model = pipeline(
                "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

            # Named Entity Recognition
            self.nlp = spacy.load("en_core_web_sm")

            logger.info("NLP models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading NLP models: {str(e)}")
            raise

        self.offensive_words = {
            "shit", "motherfucker", "fuck", "bitch", "asshole"
        }

    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return "unknown"

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        result = self.sentiment_model(text)[0]
        return {result['label'].lower(): result['score']}

    def detect_offensive_language(self, text: str) -> bool:
        return any(word in text.lower() for word in self.offensive_words)

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        doc = self.nlp(text)
        entities = [{"name": ent.text, "type": ent.label_} for ent in doc.ents]
        return entities

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        sentences = text.split('.')
        if len(sentences) <= max_sentences:
            return text

        # Simple extractive summarization
        word_counts = [len(sentence.split()) for sentence in sentences]
        avg_word_count = sum(word_counts) / len(word_counts)

        important_sentences = [sentence for sentence, count in zip(
            sentences, word_counts) if count >= avg_word_count * 0.8]

        summary = '. '.join(important_sentences[:max_sentences]) + '.'
        return summary
