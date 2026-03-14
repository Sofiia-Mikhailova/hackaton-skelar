import json
import os
from llm_client import LLMClient

def ask_ai_to_extract_knowledge(chat_item):
    client = LLMClient()
    
    history = ""
    for m in chat_item.get("messages", []):
        history += f"{m.get('role', '').upper()}: {m.get('text', '')}\n"
        
    prompt = f"""
    Analyze this support chat and create a technical KB article.
    Identify how the issue was resolved and formulate it as a reusable algorithm.

    CHAT HISTORY:
    {history}

    RETURN ONLY JSON:
    {{
        "intent": "Short topic name",
        "resolution_steps": ["Step 1", "Step 2", "..."],
        "confidence_score": 0.0-1.0
    }}
    """
    
    try:
        response = client.get_json_response(prompt, model="llama-3.3-70b-versatile")
        return response
    except:
        return None

def build_ai_kb():
    try:
        with open(r'C:\Users\HP\source\repos\skelar\Sofiia-Mikhailova\hackaton-skelar\data\dataset_clean.json', 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except:
        return

    knowledge_base = []

    for chat in dataset:
        extracted = ask_ai_to_extract_knowledge(chat)
        
        if extracted:
            kb_entry = {
                "chat_id": chat.get("id"),
                "query": chat.get("messages", [{}])[0].get("text", "N/A"),
                "intent": extracted.get("intent"),
                "status": "Ready for Automation" if extracted.get("confidence_score", 0) > 0.8 else "Needs Review",
                "source": "AI Extraction",
                "resolution_steps": extracted.get("resolution_steps")
            }
            knowledge_base.append(kb_entry)
            print(f"Processed Chat #{chat.get('id')}")

    with open('potential_kb_articles.json', 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    build_ai_kb()