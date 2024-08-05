# TextAnalysis API Documentation

## Overview

The TextAnalysis API provides text analysis capabilities including language detection and sentiment analysis.

## Endpoints

### POST /analyze

Analyzes the provided text, returning language detection and sentiment analysis results.

#### Request Body

```json
{
  "text": "String to be analyzed"
}
```

#### Response

```json
{
  "text_length": int,
  "language": string,
  "language_confidence": float,
  "sentiment": string,
  "sentiment_confidence": float
}
```

#### Fields

- `text_length`: The number of characters in the input text.
- `language`: The detected language of the text (ISO 639-1 code).
- `language_confidence`: Confidence score for language detection (0-1).
- `sentiment`: The detected sentiment ("POSITIVE", "NEGATIVE", or "NEUTRAL").
- `sentiment_confidence`: Confidence score for sentiment analysis (0-1).

#### Example

Request:

```
POST /analyze
{
  "text": "I love this new sentiment analysis feature!"
}
```

Response:

```json
{
  "text_length": 44,
  "language": "en",
  "language_confidence": 0.9998,
  "sentiment": "POSITIVE",
  "sentiment_confidence": 0.9998
}
```

## Error Handling

The API will return appropriate HTTP status codes for different types of errors:

- 400 Bad Request: Invalid input (e.g., empty text)
- 500 Internal Server Error: Unexpected server-side errors

Each error response will include a message explaining the error.
