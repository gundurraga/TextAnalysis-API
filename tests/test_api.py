import requests
import json


def test_api(text):
    url = "http://localhost:8000/analyze"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Input text: {text}")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)


def run_tests():
    test_cases = [
        "This is a simple English sentence.",
        "Je suis très heureux aujourd'hui!",
        "This is a longer text that might need summarization. " * 10,
        "Apple Inc. is headquartered in Cupertino, California.",
        "I love this product! It's amazing!",
        "This movie is terrible. I hated every minute of it.",
        "This is a f***ing disaster!"
    ]

    for case in test_cases:
        test_api(case)


if __name__ == "__main__":
    run_tests()
