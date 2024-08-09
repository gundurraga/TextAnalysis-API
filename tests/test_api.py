import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.parametrize("input_text, expected_keys", [
    ("This is a simple English sentence.", [
     "text_length", "language", "sentiment", "is_offensive", "entities", "summary"]),
    ("Je suis très heureux aujourd'hui!", [
     "text_length", "language", "sentiment", "is_offensive", "entities", "summary"]),
    ("This is a longer text that might need summarization. " * 10,
     ["text_length", "language", "sentiment", "is_offensive", "entities", "summary"]),
])
def test_analyze_endpoint(input_text, expected_keys):
    response = client.post("/analyze", json={"text": input_text})
    assert response.status_code == 200
    result = response.json()
    assert all(key in result for key in expected_keys)


def test_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_long_text():
    long_text = "This is a test sentence. " * 1000
    response = client.post("/analyze", json={"text": long_text})
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result


def test_offensive_language():
    response = client.post(
        "/analyze", json={"text": "This is a fucking disaster!"})
    assert response.status_code == 200
    result = response.json()
    assert result["is_offensive"] == True


def test_named_entity_recognition():
    response = client.post(
        "/analyze", json={"text": "Apple Inc. is headquartered in Cupertino, California."})
    assert response.status_code == 200
    result = response.json()
    assert len(result["entities"]) > 0
    assert any(entity["name"] == "Apple Inc." for entity in result["entities"])
    assert any(entity["name"] == "Cupertino" for entity in result["entities"])
    assert any(entity["name"] == "California" for entity in result["entities"])
