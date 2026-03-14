import json

def audit_to_file():
    try:
        with open('prioritized_queue.json', 'r', encoding='utf-8') as f:
            priority_data = {t['id']: t['priority_data'] for t in json.load(f)}
        with open('copilot_results.json', 'r', encoding='utf-8') as f:
            copilot_data = {c['chat_id']: c for c in json.load(f)}
        with open('system_execution_log.json', 'r', encoding='utf-8') as f:
            execution_data = {e['chat_id']: e for e in json.load(f)}
        
        data_path = r"C:\Users\HP\source\repos\skelar\Sofiia-Mikhailova\hackaton-skelar\data\dataset_clean.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            raw_chats = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    detailed_audit = []

    for chat in raw_chats:
        chat_id = chat['id']
        p_info = priority_data.get(chat_id, {})
        c_info = copilot_data.get(chat_id, {})
        e_info = execution_data.get(chat_id, {})

        customer_msgs = [m['text'] for m in chat['messages'] if m['role'] == 'customer']
        last_input = customer_msgs[-1] if customer_msgs else "No input"

        audit_entry = {
            "chat_id": chat_id,
            "customer_name": chat.get('customer_name', 'Unknown'),
            "last_customer_input": last_input,
            "prioritization": {
                "level": p_info.get('priority', 'N/A'),
                "score": p_info.get('score', 0)
            },
            "copilot_analysis": {
                "intent": c_info.get('intent', 'Undefined'),
                "confidence": c_info.get('confidence', '0%'),
                "risk_level": c_info.get('risk_level', 'low'),
                "recommendation": c_info.get('suggested_action', 'None')
            },
            "system_execution": {
                "status": e_info.get('status', 'Pending/Manual'),
                "action_taken": e_info.get('action_taken', 'None'),
                "timestamp": e_info.get('timestamp', 'N/A')
            }
        }
        detailed_audit.append(audit_entry)

    with open('detailed_operational_audit.json', 'w', encoding='utf-8') as f:
        json.dump(detailed_audit, f, indent=4, ensure_ascii=False)

    print("Success: Detailed audit saved to detailed_operational_audit.json")

if __name__ == "__main__":
    audit_to_file()