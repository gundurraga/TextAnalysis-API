import pytest
from app.models.nlp_model import NLPModel
import numpy as np


@pytest.fixture
def nlp_model():
    return NLPModel()


def test_detect_language(nlp_model):
    assert nlp_model.detect_language("Hello, world!") == "en"
    assert nlp_model.detect_language("Bonjour le monde!") == "fr"
    assert nlp_model.detect_language("Hola mundo!") in ["es", "pt"]
    assert nlp_model.detect_language("こんにちは世界！") == "ja"
    assert nlp_model.detect_language("") == "unknown"


def test_analyze_sentiment(nlp_model):
    positive_result = nlp_model.analyze_sentiment("I love this product!")
    negative_result = nlp_model.analyze_sentiment("I hate this product!")
    neutral_result = nlp_model.analyze_sentiment("The sky is blue.")

    assert "positive" in positive_result
    assert positive_result["positive"] > 0.5
    assert "negative" in negative_result
    assert negative_result["negative"] > 0.5
    assert "positive" in neutral_result or "negative" in neutral_result


def test_detect_offensive_language(nlp_model):
    assert nlp_model.detect_offensive_language(
        "This is a normal sentence.") == False
    assert nlp_model.detect_offensive_language(
        "You are a piece of shit!") == True
    assert nlp_model.detect_offensive_language(
        "I hate you and everything you stand for cunt.") == True
    assert nlp_model.detect_offensive_language(
        "This movie is terrible.") == False
    assert nlp_model.detect_offensive_language("") == False


def test_extract_entities(nlp_model):
    text = "Apple Inc. is headquartered in Cupertino, California. Tim Cook is the CEO."
    entities = nlp_model.extract_entities(text)

    assert any(entity["name"] == "Apple Inc." and entity["type"]
               == "ORG" for entity in entities)
    assert any(entity["name"] == "Cupertino" and entity["type"]
               == "GPE" for entity in entities)
    assert any(entity["name"] == "California" and entity["type"]
               == "GPE" for entity in entities)
    assert any(entity["name"] == "Tim Cook" and entity["type"]
               == "PERSON" for entity in entities)

    assert nlp_model.extract_entities("") == []


def test_summarize_text(nlp_model):
    long_text = "This is a long text. " * 20 + \
        "This is an important sentence that should be in the summary."
    summary = nlp_model.summarize_text(long_text)

    assert len(summary) < len(long_text)
    assert "important sentence" in summary

    # Test with short text
    short_text = "This is a short text."
    assert nlp_model.summarize_text(short_text) == short_text

    # Test with empty text
    assert nlp_model.summarize_text("") == ""


def test_model_initialization(nlp_model):
    assert nlp_model.sentiment_model is not None
    assert nlp_model.toxicity_model is not None
    assert nlp_model.nlp is not None
    assert nlp_model.tfidf_vectorizer is not None


def test_long_text_handling(nlp_model):
    very_long_text = "a" * 1100000  # Exceed the 1,000,000 character limit for NER
    entities = nlp_model.extract_entities(very_long_text)
    assert isinstance(entities, list)
    assert len(entities) == 0  # No entities should be extracted from this text
