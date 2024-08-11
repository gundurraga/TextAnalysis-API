import pytest
from app.models.nlp_model import NLPModel


@pytest.fixture
def nlp_model():
    return NLPModel()


def test_detect_language(nlp_model):
    assert nlp_model.detect_language("Hello, world!") == "en"
    assert nlp_model.detect_language("Bonjour le monde!") == "fr"
    # Accept either Spanish or Portuguese
    assert nlp_model.detect_language("Hola mundo!") in ["es", "pt"]


def test_analyze_sentiment(nlp_model):
    positive_result = nlp_model.analyze_sentiment("I love this product!")
    negative_result = nlp_model.analyze_sentiment("I hate this product!")

    assert "positive" in positive_result
    assert positive_result["positive"] > 0.5
    assert "negative" in negative_result
    assert negative_result["negative"] > 0.5


def test_detect_offensive_language(nlp_model):
    assert nlp_model.detect_offensive_language(
        "This is a normal sentence.") == False
    assert nlp_model.detect_offensive_language(
        "You are a piece of shit!") == True
    assert nlp_model.detect_offensive_language(
        "I hate you and everything you stand for cunt.") == True
    assert nlp_model.detect_offensive_language(
        "This movie is terrible.") == False


def test_extract_entities(nlp_model):
    text = "Apple Inc. is headquartered in Cupertino, California."
    entities = nlp_model.extract_entities(text)

    assert any(entity["name"] == "Apple Inc." and entity["type"]
               == "ORG" for entity in entities)
    assert any(entity["name"] == "Cupertino" and entity["type"]
               == "GPE" for entity in entities)
    assert any(entity["name"] == "California" and entity["type"]
               == "GPE" for entity in entities)


def test_summarize_text(nlp_model):
    long_text = "This is a long text. " * 20 + \
        "This is an important sentence that should be in the summary."
    summary = nlp_model.summarize_text(long_text)

    assert len(summary) < len(long_text)
    assert "important sentence" in summary
