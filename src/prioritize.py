import json
from llm_client import LLMClient

def prioritize_tickets(input_file=r"C:\Users\HP\source\repos\skelar\Sofiia-Mikhailova\hackaton-skelar\data\dataset_clean.json", output_file="prioritized_queue.json"):
    client = LLMClient()
    
    with open(input_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    prioritized_results = []

    for item in dataset:
        customer_text = " ".join([m['text'] for m in item['messages'] if m['role'] == 'customer'][:2])
        
        prompt = f"""
        Analyze the following customer request and assign a priority level.
        
        CRITERIA:
        - CRITICAL: Financial risks (refunds), churn threats, extreme anger, VIP status.
        - HIGH: Technical errors (Tier-2/3), billing issues.
        - MEDIUM: Pricing plans, account access questions.
        - LOW: General FAQ, Tier-1 basic questions.

        CUSTOMER TEXT: "{customer_text}"

        RETURN ONLY JSON:
        {{
            "id": {item['id']},
            "priority": "CRITICAL/HIGH/MEDIUM/LOW",
            "score": 1-100,
            "reason": "short explanation"
        }}
        """
        
        response = client.get_json_response(prompt, model="llama-3.3-70b-versatile")
        prioritized_results.append({
            "id": item['id'],
            "customer_name": item['customer_name'],
            "priority_data": response
        })

    prioritized_results.sort(key=lambda x: x['priority_data']['score'], reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(prioritized_results, f, ensure_ascii=False, indent=4)

    print(f"Чергу сформовано та збережено у {output_file}")

if __name__ == "__main__":
    prioritize_tickets()