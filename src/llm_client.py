import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("ERROR: API Key not found in .env!")
            self.client = None
            return
        
        try:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama-3.1-8b-instant"
        except Exception as e:
            print(f"Error: {e}")
            self.client = None

    def get_json_response(self, prompt, temperature=0.7):
        if not self.client:
            return None
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional assistant. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            print(f"API Error: {e}")
            return None

if __name__ == "__main__":
    client = LLMClient()
    result = client.get_json_response("Say 'Ready' in JSON format")
    if result:
        print("Success:", result)
    else:
        print("Failed to connect.")