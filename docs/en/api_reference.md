# TextAnalysis API Documentation

## Overview

The TextAnalysis API provides advanced natural language processing capabilities, including language detection, sentiment analysis, offensive language detection, named entity recognition, and text summarization.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. (Note: Consider implementing authentication for production use.)

## Endpoints

### Health Check

```
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

```
POST /analyze
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
    "positive": float,
    "negative": float
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
- `sentiment`: Object containing sentiment scores.
  - `positive`: Confidence score for positive sentiment (0-1).
  - `negative`: Confidence score for negative sentiment (0-1).
- `is_offensive`: Boolean indicating whether the text is considered offensive.
- `entities`: Array of named entities found in the text.
  - `name`: The text of the entity.
  - `type`: The type of the entity (e.g., PERSON, ORG, GPE).
- `summary`: A brief summary of the input text.

#### Example

Request:

```http
POST /analyze
Content-Type: application/json

{
  "text": "Apple Inc. is headquartered in Cupertino, California. The company was founded by Steve Jobs and has revolutionized the tech industry with products like the iPhone and MacBook."
}
```

Response:

```json
{
  "text_length": 172,
  "language": "en",
  "sentiment": {
    "positive": 0.9998
  },
  "is_offensive": false,
  "entities": [
    {
      "name": "Apple Inc.",
      "type": "ORG"
    },
    {
      "name": "Cupertino",
      "type": "GPE"
    },
    {
      "name": "California",
      "type": "GPE"
    },
    {
      "name": "Steve Jobs",
      "type": "PERSON"
    },
    {
      "name": "iPhone",
      "type": "PRODUCT"
    },
    {
      "name": "MacBook",
      "type": "PRODUCT"
    }
  ],
  "summary": "Apple Inc. is headquartered in Cupertino, California. The company was founded by Steve Jobs and has revolutionized the tech industry with products like the iPhone and MacBook."
}
```

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests.

- 200 OK: Successful request
- 400 Bad Request: Invalid input (e.g., empty text, text too long, invalid JSON)
- 500 Internal Server Error: Unexpected server-side errors

Error responses include a JSON body with a `detail` field explaining the error.

Example error response:

```json
{
  "detail": "Text cannot be empty or just whitespace"
}
```

Note: Invalid JSON payloads or requests with missing required fields will result in a 400 Bad Request response.

## Rate Limiting

Currently, there are no rate limits implemented. (Note: Consider implementing rate limiting for production use.)

## Versioning

The current version of the API is v1. The version is not included in the URL path but may be in future releases.

## Additional Notes

- The API is designed for use with English text. Results for non-English text may vary in accuracy.
- The maximum allowed length for input text is 10,000 characters.
- The summarization feature works best with longer texts (>100 words).
- Entity recognition may not catch all entities and can occasionally misclassify entities.

## Support

For support, please open an issue on the project's GitHub repository.
