import logging
from typing import List, Dict, Any
from transformers import pipeline
from langdetect import detect, DetectorFactory
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DetectorFactory.seed = 0  # For consistent results in language detection


class NLPModel:
    def __init__(self):
        try:
            # Sentiment Analysis
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                max_length=512,
                truncation=True
            )

            # Toxicity Detection
            self.toxicity_model = pipeline(
                "text-classification",
                model="martin-ha/toxic-comment-model",
                max_length=512,
                truncation=True
            )

            # Named Entity Recognition
            self.nlp = spacy.load("en_core_web_sm")

            # TF-IDF Vectorizer for text summarization
            self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')

            logger.info("NLP models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading NLP models: {str(e)}")
            raise

    @lru_cache(maxsize=100)
    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return "unknown"

    @lru_cache(maxsize=100)
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        result = self.sentiment_model(text)[0]
        return {result['label'].lower(): result['score']}

    @lru_cache(maxsize=100)
    def detect_offensive_language(self, text: str) -> bool:
        result = self.toxicity_model(text)[0]
        return result['label'] == 'toxic' and result['score'] > 0.5

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        # Truncate text to 1,000,000 characters to avoid potential issues with very long texts
        truncated_text = text[:1000000]
        doc = self.nlp(truncated_text)
        entities = [{"name": ent.text, "type": ent.label_} for ent in doc.ents]
        return entities

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        sentences = text.split('.')
        if len(sentences) <= max_sentences:
            return text

        # Calculate TF-IDF scores
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)
        sentence_scores = tfidf_matrix.sum(axis=1).A1

        # Get indices of top sentences
        top_sentence_indices = sentence_scores.argsort()[-max_sentences:][::-1]

        # Sort the indices to maintain original order
        top_sentence_indices = sorted(top_sentence_indices)

        # Join the top sentences
        summary = '. '.join([sentences[i].strip()
                            for i in top_sentence_indices]) + '.'
        return summary
