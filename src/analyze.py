import json
import time
import re
from llm_client import LLMClient

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(match.group(0)) if match else None
    except:
        return None

def analyze_support_performance(input_file="dataset_clean.json", output_file="analysis_results.json"):
    client = LLMClient() 
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except:
        print("Error: Input file not found.")
        return

    results = []
    total = len(dataset)

    for index, item in enumerate(dataset, 1):
        chat_id = item.get("id")
        customer_name = item.get("customer_name", "Unknown")
        
        print(f"Progress: {index}/{total} | {customer_name}", end="\r")

        history = ""
        for m in item.get("messages", []):
            history += f"[{m.get('timestamp', '')}] {m.get('role', '').upper()}: {m.get('text', '')}\n"

        prompt = f"""
        Rules:
        - Determine the topic (intent) from: payment_issue, tech_error, account_access, pricing_plan, refund_request, other.
        - Determine scenario: Identify the specific scenario type (e.g., success, hidden_dissatisfaction, aggressive_customer, rude_agent, customer_silent, etc.). 
          CRITICAL: Look closely for 'hidden_dissatisfaction' where the user says "ok/thanks" but the problem remains unresolved.
        - Determine satisfaction:
            - satisfied / neutral / unsatisfied
            - hidden_dissatisfaction: if customer says "thanks" or "ok" but issue not solved → unsatisfied.
            - aggressive_customer: aggressive tone alone does NOT mean unsatisfied; if issue resolved → satisfied.
            - customer_silent: if the customer stopped responding after 1-2 messages and agent followed protocol → neutral.
            - ESCALATION LOGIC: If agent transfers to supervisor without trying to solve the issue → satisfaction = neutral.
        - Determine quality_score (1-5):
            1 - Rude agent, zero help, or SECURITY VIOLATION (asked for password).
            2 - Major mistakes: ignored questions, incorrect info, unnecessary escalation, or WRONG NAME ({customer_name}).
            3 - Issue didn`t solved but agent was helpful. or the tone was robotic, slow, or ignored a side question.
            4 - Good service, main issue solved quickly.
            5 - Perfect, polite, fast, all questions answered, addressed customer as {customer_name} correctly.
        - Determine agent_mistakes: list any of ignored_question, incorrect_info, rude_tone, no_resolution, unnecessary_escalation, security_violation, wrong_customer_name.
        - SECURITY: Any request for password/credentials = SCORE 1 + 'security_violation'.
        
        CHAT HISTORY:
        {history}

        RETURN ONLY JSON:
        {{
            "id": {chat_id},
            "intent": "...",
            "scenario": "...",
            "satisfaction": "...",
            "quality_score": ...,
            "agent_mistakes": [...]
        }}
        """

        while True:
            try:
                response = client.get_json_response(prompt, model="llama-3.3-70b-versatile", temperature=0.0)
                
                data = response if isinstance(response, dict) else extract_json(str(response))
                
                if data:
                    results.append({
                        "id": chat_id,
                        "customer_name": customer_name,
                        "analysis": data
                    })
                    break
            except Exception as e:
                if "429" in str(e):
                    time.sleep(70)
                else:
                    print(f"\nError on ID {chat_id}: {e}")
                    break

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"\nDone. Analysis with scenarios saved to {output_file}")

if __name__ == "__main__":
    analyze_support_performance()