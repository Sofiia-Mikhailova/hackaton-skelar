import json
import time
from llm_client import LLMClient

def analyze_dialogues(input_file="dataset_clean.json", output_file="analysis_results.json"):
    client = LLMClient()
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    analysis_report = []

    for chat in data:
        prompt = f"""
        Analyze this customer support chat and provide a strict JSON response.
        
        CONTEXT:
        Customer: {chat['customer_name']}
        Messages: {json.dumps(chat['messages'], ensure_ascii=False)}

        CATEGORIES FOR INTENT:
        - billing
        - tech_error
        - account_access
        - pricing
        - shipping
        - promo_code
        - other

        POSSIBLE AGENT MISTAKES:
        - ignored_question
        - incorrect_info
        - rude_tone
        - no_resolution
        - unnecessary_escalation

        EVALUATION STEPS:
        1. Intent: Identify the main goal even if there are typos.
        2. Satisfaction: Detect "Hidden Dissatisfaction" (e.g., customer says "thanks" but problem remains).
        3. Quality Score (1-5): 
           - 5: Perfect, solved fast.
           - 3: Solved but slow or impersonal.
           - 1: Wrong info, rude, or ignored questions.
        4. Mistakes: Check if the agent missed split messages from the customer.

        RETURN ONLY VALID JSON:
        {{
            "id": {chat['id']},
            "intent": "string",
            "satisfaction": "satisfied/neutral/unsatisfied",
            "quality_score": int,
            "agent_mistakes": ["mistake1", "mistake2"],
            "hidden_dissatisfaction_detected": bool,
            "brief_reason": "string"
        }}
        """
        
        result = client.get_json_response(prompt)
        if result:
            analysis_report.append(result)
        
        time.sleep(0.5)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis_report, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    analyze_dialogues()