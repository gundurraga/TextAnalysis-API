# TextAnalysis API Documentation

## Overview

The TextAnalysis API provides advanced natural language processing capabilities, including language detection, sentiment analysis, offensive language detection, named entity recognition, and text summarization.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

```http
GET /health
```

Checks the health status of the API.

#### Response

```json
{
  "status": "healthy"
}
```

### Text Analysis

```http
POST /v1/analyze
```

Performs comprehensive analysis on the provided text.

#### Request Body

```json
{
  "text": "String to be analyzed (1-10000 characters)"
}
```

#### Response

```json
{
  "text_length": int,
  "language": string,
  "sentiment": {
    "label": string,
    "score": float
  },
  "is_offensive": boolean,
  "entities": [
    {
      "name": string,
      "type": string
    }
  ],
  "summary": string
}
```

#### Fields

- `text_length`: The number of characters in the input text.
- `language`: The detected language of the text (ISO 639-1 code).
- `sentiment`: Object containing sentiment analysis results.
  - `label`: Either "positive" or "negative".
  - `score`: Confidence score for the sentiment (0-1).
- `is_offensive`: Boolean indicating whether the text is considered offensive.
- `entities`: Array of named entities found in the text.
  - `name`: The text of the entity.
  - `type`: The type of the entity (e.g., PERSON, ORG, GPE).
- `summary`: A brief summary of the input text.

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests.

- 200 OK: Successful request
- 400 Bad Request: Invalid input (e.g., empty text, text too long)
- 422 Unprocessable Entity: Request validation error
- 500 Internal Server Error: Unexpected server-side errors

Error responses include a JSON body with a `detail` field explaining the error.

Example error response:

```json
{
  "detail": "Text cannot be empty or just whitespace"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider implementing appropriate rate limiting.

## Authentication

The API currently does not require authentication. For production deployments, implement suitable authentication mechanisms.

## Versioning

The current version of the API is v1, which is included in the URL path.

## Limitations

1. Language support: The API primarily supports English and may have reduced accuracy for other languages.
2. Text length: The API has a maximum input length of 10,000 characters, which may not be suitable for very long documents.
3. Sentiment analysis: The sentiment analysis is binary (positive/negative) and doesn't capture nuanced emotions or neutral sentiments.
4. Named Entity Recognition: The NER model may not recognize domain-specific entities or newer named entities not in its training data.
5. Summarization: The summarization feature uses extractive methods and may not produce coherent summaries for all types of texts.
6. Processing time: For longer texts, the API may take several seconds to respond, which might not be suitable for real-time applications.
7. Offensive language detection: This feature may have biases and might not catch all instances of offensive language, especially in context-dependent cases.
8. No continuous learning: The models used in the API are static and do not learn from new data or user feedback.

## Additional Notes

- The API is optimized for English text. Results for non-English text may vary in accuracy.
- The maximum allowed length for input text is 10,000 characters.
- The summarization feature works best with longer texts (>100 words).
- Entity recognition may not catch all entities and can occasionally misclassify entities.
