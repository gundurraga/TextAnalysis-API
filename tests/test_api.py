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
    response = client.post("v1/analyze", json={"text": input_text})
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
    response = client.post("v1/analyze", json={"text": ""})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_whitespace_text():
    response = client.post("v1/analyze", json={"text": "   "})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_long_text():
    long_text = "a" * 10001
    response = client.post("v1/analyze", json={"text": long_text})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_offensive_language():
    response = client.post(
        "v1/analyze", json={"text": "You are a terrible person!"})
    assert response.status_code == 200
    result = response.json()
    assert result["is_offensive"] == True

    response = client.post("v1/analyze", json={"text": "This is a great day!"})
    assert response.status_code == 200
    result = response.json()
    assert result["is_offensive"] == False


def test_named_entity_recognition():
    response = client.post(
        "v1/analyze", json={"text": "Apple Inc. is headquartered in Cupertino, California."})
    assert response.status_code == 200
    result = response.json()
    assert len(result["entities"]) > 0
    assert any(entity["name"] == "Apple Inc." for entity in result["entities"])
    assert any(entity["name"] == "Cupertino" for entity in result["entities"])
    assert any(entity["name"] == "California" for entity in result["entities"])


def test_language_detection():
    response = client.post("v1/analyze", json={"text": "こんにちは、世界！"})
    assert response.status_code == 200
    result = response.json()
    assert result["language"] == "ja"


def test_sentiment_analysis():
    response = client.post(
        "v1/analyze", json={"text": "I love this product! It's amazing."})
    assert response.status_code == 200
    result = response.json()
    assert "positive" in result["sentiment"]
    assert result["sentiment"]["positive"] > 0.5

    response = client.post(
        "v1/analyze", json={"text": "I hate this product. It's terrible."})
    assert response.status_code == 200
    result = response.json()
    assert "negative" in result["sentiment"]
    assert result["sentiment"]["negative"] > 0.5


def test_text_summarization():
    long_text = "This is a long text. " * 20 + \
        "This is an important sentence that should be in the summary."
    response = client.post("v1/analyze", json={"text": long_text})
    assert response.status_code == 200
    result = response.json()
    assert len(result["summary"]) < len(long_text)
    assert "important sentence" in result["summary"]


def test_invalid_json():
    response = client.post(
        "v1/analyze", json={"invalid_key": "This should not work"})
    assert response.status_code == 422  # Bad Request
    assert "detail" in response.json()


def test_method_not_allowed():
    response = client.get("v1/analyze")
    assert response.status_code == 405


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_very_short_text():
    response = client.post("v1/analyze", json={"text": "Hi"})
    assert response.status_code == 200
    result = response.json()
    assert result["text_length"] == 2
    assert "language" in result
    assert "sentiment" in result
    assert "is_offensive" in result
    assert "entities" in result
    assert "summary" in result


def test_max_length_text():
    max_length_text = "a" * 10000
    response = client.post("v1/analyze", json={"text": max_length_text})
    assert response.status_code == 200
    result = response.json()
    assert result["text_length"] == 10000


def test_mixed_language_text():
    response = client.post(
        "v1/analyze", json={"text": "Hello world. Bonjour monde. Hola mundo."})
    assert response.status_code == 200
    result = response.json()
    assert "language" in result  # We don't assert a specific language as it might vary


def test_text_with_special_characters():
    response = client.post(
        "v1/analyze", json={"text": "Hello! @#$%^&*() World 123"})
    assert response.status_code == 200
    result = response.json()
    assert result["text_length"] == 26
    assert "entities" in result
