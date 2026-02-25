import json
import time
import random
from datetime import datetime, timedelta
from faker import Faker
from llm_client import LLMClient

fake = Faker()

def get_random_timestamp():
    start_date = datetime(2024, 1, 1)
    random_days = random.randint(0, 60)
    return start_date + timedelta(days=random_days, hours=random.randint(8, 20), minutes=random.randint(0, 59))

def generate_skelar_dataset(count=50):
    client = LLMClient()
    dataset_clean = []
    dataset_reference = []
    
    topics = ["billing", "tech_error", "account_access", "pricing", "shipping", "promo_code"]
    
    scenarios = [
        {"type": "success", "label": "satisfied", "mistake": "none"},
        {"type": "refund_success", "label": "satisfied", "mistake": "none"},
        {"type": "hidden_dissatisfaction", "label": "unsatisfied", "mistake": "no_resolution"},
        {"type": "agent_error", "label": "unsatisfied", "mistake": "incorrect_info"},
        {"type": "rude_agent", "label": "unsatisfied", "mistake": "rude_tone"},
        {"type": "ignored_issue", "label": "neutral", "mistake": "ignored_question"},
        {"type": "bad_escalation", "label": "unsatisfied", "mistake": "unnecessary_escalation"}
    ]

    for i in range(1, count + 1):
        topic = random.choice(topics)
        if i % 2 == 0:
            scenario = random.choice([s for s in scenarios if s["type"].startswith("success") or s["type"] == "refund_success"])
        else:
            scenario = random.choice([s for s in scenarios if s["label"] != "satisfied"])
            
        customer_name = fake.name()
        start_time = get_random_timestamp()

        prompt = f"""
        Generate a realistic customer support chat.
        Topic: {topic}. Scenario: {scenario['type']}. 
        Customer satisfaction: {scenario['label']}. Agent mistake: {scenario['mistake']}.

        STRICT STYLE RULES FOR CUSTOMER:
        1. BE HUMAN: Use typos and casual language. 
        2. SPLIT MESSAGES: Send 2-3 short messages instead of one frequently.
        3. INFORMAL: Use short phrases, slang, or emotional punctuation.
        4. ROLE: "customer".

        STRICT RULES FOR AGENT:
        1. Professional tone, but include mistake if specified: {scenario['mistake']}.
        2. ROLE: "agent".

        Return ONLY JSON structure with "id", "customer_name", and "messages" (role, text, timestamp).
        """
        chat_data = client.get_json_response(prompt)
        
        if chat_data:
            messages = chat_data.get("messages", [])
            
            # 1. ЧИСТИЙ ДАТАСЕТ (без топіка і сценаріїв)
            clean_item = {
                "id": i,
                "customer_name": chat_data.get("customer_name", customer_name),
                "messages": messages
            }
            
            # 2. РЕФЕРЕНСНИЙ ДАТАСЕТ (з усіма мітками)
            agent_msgs = [m["text"] for m in messages if m["role"] == "agent"]
            avg_agent_len = sum(len(m.split()) for m in agent_msgs) / len(agent_msgs) if agent_msgs else 0
            
            ref_item = clean_item.copy()
            ref_item["topic"] = topic
            ref_item["reference_data"] = {
                "true_scenario": scenario["type"],
                "true_satisfaction": scenario["label"],
                "true_mistake": scenario["mistake"],
                "metrics": {
                    "message_count": len(messages),
                    "total_word_count": sum(len(m["text"].split()) for m in messages),
                    "avg_agent_response_length": round(avg_agent_len, 2)
                }
            }
            
            dataset_clean.append(clean_item)
            dataset_reference.append(ref_item)
        
        time.sleep(1)

    with open("dataset_clean.json", "w", encoding="utf-8") as f:
        json.dump(dataset_clean, f, ensure_ascii=False, indent=4)
    
    with open("dataset_reference.json", "w", encoding="utf-8") as f:
        json.dump(dataset_reference, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_skelar_dataset(150)