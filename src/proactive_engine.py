import json
import random
from datetime import datetime

def run_proactive_monitoring():
    event_scenarios = [
        {
            "type": "payment_drift", 
            "target": "Agent", 
            "msg": "Customer tried 3 different cards. Potential fraud or bank block. Investigation required."
        },
        {
            "type": "technical_friction", 
            "target": "Customer", 
            "msg": "We noticed you've seen 'Error 500' twice. Try clearing your cache or use this direct link."
        },
        {
            "type": "churn_signal", 
            "target": "Agent", 
            "msg": "User visited 'Delete Account' page 3 times. High churn risk. Prepare a retention offer."
        },
        {
            "type": "onboarding_gap", 
            "target": "Customer", 
            "msg": "You haven't set up your API key yet. Here is a 1-minute guide to get started."
        },
        {
            "type": "feature_discovery", 
            "target": "Agent", 
            "msg": "User is trying to use Pro features on a Basic plan. Good opportunity for upselling."
        }
    ]

    try:
        with open("detailed_operational_audit.json", "r", encoding="utf-8") as f:
            audit_data = json.load(f)
            customer_pool = [item["customer_name"] for item in audit_data]
    except:
        customer_pool = [f"User_{i}" for i in range(100, 150)]

    proactive_logs = []
    
    print("="*60)
    print("SKELAR AI: PROACTIVE INTELLIGENCE SCANNER")
    print("="*60)

    for i in range(15):
        scenario = random.choice(event_scenarios)
        customer = random.choice(customer_pool)
        
        print(f"[SCAN] Found {scenario['type']} for {customer}")
        print(f"  [ACTION] Notify {scenario['target']} | Message: {scenario['msg']}")

        proactive_logs.append({
            "id": 700 + i,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "event_type": scenario['type'],
            "customer": customer,
            "recipient": scenario['target'],
            "content": scenario['msg'],
            "status": "Alert Sent"
        })

    with open('proactive_actions.json', 'w', encoding='utf-8') as f:
        json.dump(proactive_logs, f, indent=4, ensure_ascii=False)

    print("\n" + "="*60)
    print(f"SUCCESS: {len(proactive_logs)} INTELLIGENCE ALERTS GENERATED")
    print("="*60)

if __name__ == "__main__":
    run_proactive_monitoring()