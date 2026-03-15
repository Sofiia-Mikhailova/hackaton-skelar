import os
from src.llm_client import LLMClient

class CustomerSimulator:
    def __init__(self):
        self.client = LLMClient()

    def get_customer_response(self, history, scenario_type="success"):
        """
        Simulates a customer reaction using the STRICT HUMAN RULES 
        from the generator logic.
        """
        prompt = f"""
        ACT AS: A customer in a support chat. 
        SCENARIO CONTEXT: {scenario_type}

        HUMAN BEHAVIOR RULES (from generator.py):
        1. BE HUMAN: Use slang, casual language, and emotional punctuation (!!!, ?, ...). 
        2. NO REPETITION: Do NOT use "I appreciate it" or formal robot talk. 
           Use: "cool", "fine", "noted", "thx", "ok then", "finally", "ugh", "dude".
        3. MESSENGER STYLE: Use typos, no caps (mostly), and short, fragmented sentences.
        4. EMOTIONAL REACTION: 
           - If the agent repeats the same info: Get aggressive, use CAPS, or say "u already said that."
           - If the agent answers your specific question: Say "thx" or "finally."
           - If the agent is vague: Demand a supervisor or threaten social media reviews.

        RULES:
        1. CLOSING LOGIC: If the agent says they are escalating or fixing it, and you've already expressed your frustration, just say "thx, i'll wait" or nothing at all.
        2. TERMINATION: If the conversation is clearly over, return the string "END_OF_CHAT".

        HISTORY:
        {history}

        Return ONLY a JSON object with a single key "reply":
        {{
            "reply": "your messenger-style message here"
        }}
        """
        
        try:
            response = self.client.get_json_response(prompt)
            if isinstance(response, dict):
                return response.get("reply", "...")
            return str(response)
        except Exception as e:
            return "system error... one sec"