import os
import json
import time
from dotenv import load_dotenv
from src.llm_client import LLMClient

load_dotenv()

class AICopilot:
    def __init__(self):
        self.client = LLMClient()
        self.workflows = {
            "refund_request": "Initiate Refund",
            "account_access": "Reset Password",
            "payment_issue": "Check Transaction Status",
            "pricing_plan": "Send Pricing Comparison",
            "tech_error": "Escalate to Tier-3 Engineering"
        }

    def get_ai_advice(self, history_str, customer_name="Customer"):
        workflow_list = list(self.workflows.values())
        prompt = f"""
        STRICT GOALS:
        1. Identify the 'intent'.
        2. Detect 'hidden_dissatisfaction': true if user is polite but the problem is not solved.
        3. Detect 'churn_risk': low/medium/high. 
           IMPORTANT: Re-evaluate based on the NEWEST message. If the customer is satisfied, the risk must decrease.
        4. Suggest an action from the workflows.
           IMPORTANT: Do NOT suggest 'Escalate' if the agent has already escalated in the history. 
           If the customer says thanks/cool, suggest 'Close Ticket' or 'Final Follow-up' instead.
        5. CONVERSATION STATE: 
           - If the customer's LAST message contains 'thx', 'thanks', 'thank you', or 'fine', 
             the intent is now 'Successful Resolution'.
           - In this case, 'suggested_action' MUST be 'Close Ticket'.
           - The 'suggested_reply' should be a polite closing like: "You're very welcome, {customer_name}! I'm glad I could help. Feel free to reach out if you need anything else."


        CRITICAL REPETITION RULES:
        - Analyze the history carefully. If the agent has already said "it's with Tier-3" or "processed soon," DO NOT suggest that again.
        - If the customer uses words like "seriously," "dude," or "again," the churn_risk is HIGH.
        - If the customer asks for a "timeline" or "estimate," the suggested_reply MUST address that directly (e.g., giving a 24-hour estimate or checking the actual queue status).
        - DO NOT REPEAT phrases the agent has already said (e.g., "check the actual queue status").
        - If the solution/timeline has already been provided and the customer acknowledges it, STOP explaining the solution and MOVE TO CLOSING.
        
        HISTORY:
        {history_str}

        Available workflows: {workflow_list}

        Return ONLY JSON in this format:
        {{
            "intent": "string",
            "confidence": 0-100,
            "suggested_action": "string",
            "is_hidden_dissatisfaction": boolean,
            "churn_risk": "string",
            "suggested_reply": "A fresh, non-repetitive response addressing the specific latest concern."
        }}
        """
        return self.client.get_json_response(prompt)

    def display_ui(self, res):
        print("\n" + "="*30)
        print("AI ASSISTANT")
        print(f"Intent: {res.get('intent')} ({res.get('confidence')}%)")
        print(f"Churn Risk: {res.get('churn_risk', '').upper()}")
        print(f"Action: {res.get('suggested_action')}")
        if res.get('is_hidden_dissatisfaction'):
            print("⚠️ WARNING: Hidden Dissatisfaction Detected")
        print(f"Draft: {res.get('suggested_reply')}")
        print("="*30 + "\n")

    def simulate_live_chat(self, chat_id, data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chat = next((c for c in data if c["id"] == chat_id), None)
        if not chat:
            print("Chat ID not found.")
            return

        print("SYSTEM INITIALIZED")
        print(f"LIVE DEMO: {chat['customer_name'].upper()}")

        cumulative_history = []
        for msg in chat['messages']:
            cumulative_history.append(f"{msg['role'].upper()}: {msg['text']}")

            if msg['role'] == "customer":
                print(f"Customer: {msg['text']}")
                print("AI IS ANALYZING CONTEXT...")
                history_str = "\n".join(cumulative_history)

                try:
                    res = self.get_ai_advice(history_str)
                    if res:
                        self.display_ui(res)
                except Exception as e:
                    print(f"API Call Failed: {e}")
                time.sleep(1)
            else:
                print(f"Agent: {msg['text']}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(base_dir, "..", "data", "dataset_clean.json")

    copilot = AICopilot()
    copilot.simulate_live_chat(chat_id=1, data_path=DATA_PATH)