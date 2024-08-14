import json
import requests

# Define the API endpoints
ANALYZE_ENDPOINT = "http://localhost:8000/v1/analyze"

# Define test texts
test_texts = [
    # Short English text with mild offensive language
    "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet. Damn, that's cool!",

    # Long English text about AI with some technical terms
    """Artificial Intelligence (AI) is revolutionizing various sectors of society. Machine learning algorithms, neural networks, and deep learning models are at the forefront of this technological advancement. Natural Language Processing (NLP) enables machines to understand and generate human language, while computer vision allows AI systems to interpret and analyze visual information from the world. The ethical implications of AI, including bias in algorithms and the potential for job displacement, are subjects of ongoing debate. As AI continues to evolve, it presents both unprecedented opportunities and challenges for humanity.""",

    # Medium-length Spanish text about climate change with strong language
    """El cambio climático es una crisis mundial que afecta a todos los países. Los científicos advierten que si no reducimos drásticamente las emisiones de gases de efecto invernadero, las consecuencias serán catastróficas. Aumento del nivel del mar, eventos climáticos extremos, pérdida de biodiversidad... ¡La situación es una mierda! Necesitamos acción inmediata de los gobiernos y las empresas para evitar el desastre.""",

    # Short French text with offensive language
    "Merde alors ! Le français est une langue magnifique mais difficile à apprendre. Les conjugaisons sont un vrai bordel !",

    # Long mixed-language text (Portuguese and Italian) about food and culture
    """A culinária é uma parte fundamental da cultura de qualquer país. No Brasil, a feijoada é um prato icônico que reflete a mistura de influências africanas, indígenas e portuguesas. Já na Itália, a pasta é il cuore della cucina italiana. La pasta al dente, condita con sugo di pomodoro fresco e basilico, è un piatto semplice ma delizioso. Porca miseria, ora ho fame! A diversidade gastronômica do mundo é uma das coisas mais incríveis que temos. Mangiare è una gioia, non è vero?"""
]


def test_api_responses():
    responses = {}

    for i, text in enumerate(test_texts, 1):
        print(f"Testing text {i}...")

        # Test /analyze endpoint
        analyze_response = requests.post(ANALYZE_ENDPOINT, json={"text": text})
        responses[f"text_{i}_analyze"] = analyze_response.json()

    # Save responses to a JSON file
    with open("api_test_responses.json", "w") as f:
        json.dump(responses, f, indent=2)

    print("Testing completed. Responses saved to api_test_responses.json")


if __name__ == "__main__":
    test_api_responses()
