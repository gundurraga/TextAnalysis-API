# TextAnalysis API

TextAnalysis API is a robust, Python-based API for natural language processing tasks. It provides endpoints for text analysis including language detection, sentiment analysis, offensive language detection, named entity recognition, and text summarization.

## Features

- Language Detection
- Sentiment Analysis
- Offensive Language Detection
- Named Entity Recognition
- Text Summarization
- Input validation and error handling
- Performance optimization with caching
- Health check endpoint

## Requirements

- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn
- Other dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/TextAnalysis-API.git
   cd TextAnalysis-API
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the API:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## Usage

### Health Check

Send a GET request to the `/health` endpoint to check the API status:

```
GET http://localhost:8000/health
```

### Text Analysis

Send a POST request to the `/analyze` endpoint with your text:

```python
import requests

response = requests.post('http://localhost:8000/analyze',
                         json={'text': 'Your text here'})
print(response.json())
```

#### Example Response

```json
{
  "text_length": 13,
  "language": "en",
  "sentiment": { "positive": 0.9998 },
  "is_offensive": false,
  "entities": [{ "name": "Your", "type": "PRON" }],
  "summary": "Your text here"
}
```

### Input Constraints

- The input text must be between 1 and 10,000 characters long.
- Empty strings or strings containing only whitespace are not allowed.

## Error Handling

The API returns appropriate HTTP status codes for different scenarios:

- 200: Successful analysis
- 400: Bad request (e.g., empty input, input too long)
- 500: Unexpected server error

Error responses include a JSON body with a `detail` field explaining the error.

## API Documentation

For full API documentation, visit `http://localhost:8000/docs` after starting the server.

## Running Tests

To run the test suite:

```
pytest
```

## Performance Optimization

The API uses LRU (Least Recently Used) caching for frequently accessed results, improving response times for repeated queries.

## Limitations and Areas for Improvement

While the TextAnalysis API provides useful functionality, it's important to be aware of its current limitations:

1. Language Support: The API currently has limited support for languages other than English.
2. Model Size and Performance: The current models used are relatively small for the sake of speed and resource efficiency.
3. Context Understanding: The API processes each request independently and doesn't maintain context between requests.
4. Scalability: The current implementation may face challenges with high concurrent loads.
5. Privacy and Data Handling: The API doesn't currently implement any data retention policies or privacy features.
6. Customization: There's currently no way for users to fine-tune models or customize the analysis for specific domains.
7. Bias in Models: Like many NLP models, our current implementation may exhibit biases present in its training data.

These limitations present opportunities for future improvements. Contributions addressing any of these areas are particularly welcome!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the excellent API framework
- Hugging Face for transformer models
- spaCy for NLP tools
