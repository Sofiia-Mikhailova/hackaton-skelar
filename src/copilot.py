import json
import os
from llm_client import LLMClient

DATA_PATH = r"C:\Users\HP\source\repos\skelar\Sofiia-Mikhailova\hackaton-skelar\data\dataset_clean.json"

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

    def run_all(self):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            all_suggestions = []
            
            for chat in data:
                chat_id = chat["id"]
                history = "\n".join([f"{m['role']}: {m['text']}" for m in chat['messages']])
                
                prompt = f"""
                Analyze chat history and suggest next steps for the agent.
                History:
                {history}

                Available workflows: {list(self.workflows.values())}

                Return ONLY JSON:
                {{
                    "chat_id": {chat_id},
                    "intent": "identified intent",
                    "confidence": "0-100%",
                    "suggested_action": "workflow from list",
                    "risk_level": "low/medium/high",
                    "suggested_reply": "draft for agent"
                }}
                """
                suggestion = self.client.get_json_response(prompt, model="llama-3.3-70b-versatile")
                all_suggestions.append(suggestion)
                print(f"Processed Chat ID: {chat_id}") 
            
            return all_suggestions
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    assistant = AICopilot()
    results = assistant.run_all()
    
    with open("copilot_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("Done! All suggestions saved to copilot_results.json")