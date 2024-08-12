# TextAnalysis API Documentation

## Overview

The TextAnalysis API provides advanced natural language processing capabilities, including language detection, sentiment analysis, offensive language detection, named entity recognition, text summarization, and topic extraction.

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

### Topic Extraction

```http
POST /v1/extract_topics
```

Extracts topics from the provided text.

#### Request Body

```json
{
  "text": "String to extract topics from (1-10000 characters)"
}
```

#### Response

```json
{
  "topics": [
    {
      "topic": string,
      "score": float
    }
  ]
}
```

#### Fields

- `topics`: Array of extracted topics.
  - `topic`: The extracted topic.
  - `score`: Confidence score for the topic (0-1).

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests.

- 200 OK: Successful request
- 400 Bad Request: Invalid input (e.g., empty text, text too long, invalid JSON)
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

## Additional Notes

- The API is optimized for English text. Results for non-English text may vary in accuracy.
- The maximum allowed length for input text is 10,000 characters.
- The summarization feature works best with longer texts (>100 words).
- Entity recognition may not catch all entities and can occasionally misclassify entities.
- Topic extraction works best with longer, more diverse texts.

## Support

For support or to report issues, please open an issue on the project's GitHub repository.
