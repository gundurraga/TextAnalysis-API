# TextAnalysis API [DEPRECATED]

**IMPORTANT: This project is no longer maintained and has been deprecated. It is provided as-is for historical reference only.**

TextAnalysis API was a Python-based API for natural language processing tasks. It provided endpoints for text analysis including language detection, sentiment analysis, offensive language detection, named entity recognition, and text summarization.

## Deprecation Notice

This project has been deprecated as it is no longer considered very useful in its current form. Future approaches will explore using a single large language model (LLM) to achieve similar functionalities, specifically using LLaMA 3.1 8B. For up-to-date NLP solutions, please check Hugging Face's model hub and libraries.

## Features

- Language Detection
- Sentiment Analysis
- Offensive Language Detection
- Named Entity Recognition
- Text Summarization
- Input validation and error handling
- Health check endpoint

## Requirements

- Python 3.8+
- FastAPI
- Transformers
- spaCy

For a complete list of dependencies, please refer to `requirements.txt`. Note that some listed libraries may no longer be in use due to the project's deprecated status.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/gundurraga/TextAnalysis-API.git
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

Send a POST request to the `/v1/analyze` endpoint with your text:

```python
import requests

response = requests.post('http://localhost:8000/v1/analyze',
                         json={'text': 'Your text here'})
print(response.json())
```

## API Documentation

API documentation is available in the `docs/en/api_reference.md` file.

## Running Tests

To run the test suite:

```
pytest
```

## Limitations

1. Language Support: The API primarily supports English and may have reduced accuracy for other languages.
2. Text Length: The API has a maximum input length of 10,000 characters.
3. Sentiment Analysis: The sentiment analysis is binary (positive/negative) and doesn't capture nuanced emotions or neutral sentiments.
4. Named Entity Recognition: The NER model may not recognize domain-specific entities or newer named entities not in its training data.
5. Summarization: The summarization feature uses extractive methods and may not produce coherent summaries for all types of texts.
6. Processing Time: For longer texts, the API may take several seconds to respond.
7. Offensive Language Detection: This feature may have biases and might not catch all instances of offensive language, especially in context-dependent cases.
8. No Continuous Learning: The models used in the API are static and do not learn from new data or user feedback.

## Alternative Approaches

For those looking to implement similar functionalities, consider exploring:

1. Hugging Face's Transformers library and model hub for state-of-the-art NLP models.
2. Large Language Models (LLMs) like LLaMA 3.1 8B for comprehensive text analysis tasks.
3. OpenAI's GPT models for advanced language understanding and generation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the API framework
- Hugging Face for transformer models
- spaCy for NLP tools
