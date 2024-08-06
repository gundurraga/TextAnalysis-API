from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class NLPModel:
    def __init__(self):
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            low_cpu_mem_usage=True
        ).to(self.device)

        self.pipe = pipeline("text-generation", model=self.model,
                             tokenizer=self.tokenizer, device=self.device)

        self.offensive_words = {
            "shit", "motherfucker", "fuck", "bitch", "asshole"}

    def generate_response(self, instruction, input_text="", max_length=100):
        prompt = f"Human: {instruction}\n\nInput: {input_text}\n\nAssistant: Here's the answer:"
        response = self.pipe(prompt, max_length=max_length, do_sample=True,
                             top_p=0.95, top_k=50, truncation=True)[0]['generated_text']
        return response.split("Assistant: Here's the answer:")[-1].strip()

    def detect_language(self, text):
        instruction = "Detect the primary language of the following text. Respond with the language name only. If it's a mix of languages, state the primary language and mention it's mixed."
        response = self.generate_response(instruction, text)
        return response.split(".")[0]  # Take only the first sentence

    def analyze_sentiment(self, text):
        instruction = "Analyze the sentiment of the following text. Respond with ONLY 'positive', 'negative', or 'neutral'."
        response = self.generate_response(instruction, text).lower()
        if 'positive' in response:
            return 'positive'
        elif 'negative' in response:
            return 'negative'
        else:
            return 'neutral'

    def detect_offensive_language(self, text):
        # First, use our simple word list
        if any(word in text.lower() for word in self.offensive_words):
            return True

        # If no offensive words found, use the model for a more nuanced check
        instruction = "Is the following text offensive or inappropriate? Respond with ONLY 'yes' or 'no'."
        response = self.generate_response(instruction, text).lower()
        return 'yes' in response

    def extract_entities(self, text):
        instruction = "Extract named entities (persons, organizations, locations) from the following text. List them in a comma-separated format. If no entities are found, respond with 'No entities found'."
        response = self.generate_response(instruction, text)
        entities = [entity.strip() for entity in response.split(
            ',') if entity.strip() and entity.strip().lower() != 'no entities found']
        return entities if entities else []

    def summarize_text(self, text):
        instruction = "Summarize the following text in one or two sentences."
        return self.generate_response(instruction, text, max_length=150)
