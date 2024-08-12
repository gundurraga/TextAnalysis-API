import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.parametrize("input_text, expected_keys", [
    ("This is a simple English sentence.", [
     "text_length", "language", "sentiment", "is_offensive", "entities", "summary"]),
    ("Je suis très heureux aujourd'hui!", [
     "text_length", "language", "sentiment", "is_offensive", "entities", "summary"]),
])
def test_analyze_endpoint(input_text, expected_keys):
    response = client.post("/analyze", json={"text": input_text})
    assert response.status_code == 200
    result = response.json()
    assert all(key in result for key in expected_keys)
    assert isinstance(result["text_length"], int)
    assert isinstance(result["language"], str)
    assert isinstance(result["sentiment"], dict)
    assert isinstance(result["is_offensive"], bool)
    assert isinstance(result["entities"], list)
    assert isinstance(result["summary"], str)


def test_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_whitespace_text():
    response = client.post("/analyze", json={"text": "   "})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_long_text():
    long_text = "a" * 10001
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_offensive_language():
    response = client.post(
        "/analyze", json={"text": "You are a terrible person!"})
    assert response.status_code == 200
    result = response.json()
    assert result["is_offensive"] == True

    response = client.post("/analyze", json={"text": "This is a great day!"})
    assert response.status_code == 200
    result = response.json()
    assert result["is_offensive"] == False


def test_named_entity_recognition():
    response = client.post(
        "/analyze", json={"text": "Apple Inc. is headquartered in Cupertino, California."})
    assert response.status_code == 200
    result = response.json()
    assert len(result["entities"]) > 0
    assert any(entity["name"] == "Apple Inc." for entity in result["entities"])
    assert any(entity["name"] == "Cupertino" for entity in result["entities"])
    assert any(entity["name"] == "California" for entity in result["entities"])


def test_language_detection():
    response = client.post("/analyze", json={"text": "こんにちは、世界！"})
    assert response.status_code == 200
    result = response.json()
    assert result["language"] == "ja"


def test_sentiment_analysis():
    response = client.post(
        "/analyze", json={"text": "I love this product! It's amazing."})
    assert response.status_code == 200
    result = response.json()
    assert "positive" in result["sentiment"]
    assert result["sentiment"]["positive"] > 0.5

    response = client.post(
        "/analyze", json={"text": "I hate this product. It's terrible."})
    assert response.status_code == 200
    result = response.json()
    assert "negative" in result["sentiment"]
    assert result["sentiment"]["negative"] > 0.5


def test_text_summarization():
    long_text = "This is a long text. " * 20 + \
        "This is an important sentence that should be in the summary."
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 200
    result = response.json()
    assert len(result["summary"]) < len(long_text)
    assert "important sentence" in result["summary"]


def test_invalid_json():
    response = client.post(
        "/analyze", json={"invalid_key": "This should not work"})
    assert response.status_code == 400  # Bad Request
    assert "detail" in response.json()


def test_method_not_allowed():
    response = client.get("/analyze")
    assert response.status_code == 405


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
