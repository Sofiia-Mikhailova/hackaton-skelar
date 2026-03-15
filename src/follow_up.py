import json
from datetime import datetime, timedelta

def run_post_resolution_follow_up():
    try:
        with open('system_execution_log.json', 'r', encoding='utf-8') as f:
            execution_data = json.load(f)
        with open('detailed_operational_audit.json', 'r', encoding='utf-8') as f:
            audit_data = {item['chat_id']: item for item in json.load(f)}
    except Exception as e:
        print(f"Error: {e}")
        return

    follow_up_log = []
    successful_actions = [e for e in execution_data if 'Executed' in e['status']]

    print("="*60)
    print("SKELAR AI: GENERATING POST-RESOLUTION FOLLOW-UPS")
    print("="*60)

    for action in successful_actions:
        chat_id = action['chat_id']
        customer_name = audit_data.get(chat_id, {}).get('customer_name', 'Customer')
        action_type = action.get('action_taken', 'Resolution')
        
        scheduled_time = (datetime.now() + timedelta(seconds=3)).strftime("%Y-%m-%d %H:%M:%S")
        #scheduled_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        message = f"Hi {customer_name}! This is Skelar Support. We noticed your {action_type} was processed recently. Was your issue fully resolved?"

        print(f"\n[FOLLOW-UP SCHEDULED]")
        print(f"  ID: {chat_id}")
        print(f"  Recipient: {customer_name}")
        print(f"  Time: {scheduled_time}")
        print(f"  Message: {message}")

        follow_up_log.append({
            "chat_id": chat_id,
            "customer_name": customer_name,
            "status": "Scheduled",
            "scheduled_at": scheduled_time,
            "content": message
        })

    with open('follow_up_log.json', 'w', encoding='utf-8') as f:
        json.dump(follow_up_log, f, indent=4, ensure_ascii=False)

    print("\n" + "="*60)
    print(f"SUCCESS: {len(follow_up_log)} FOLLOW-UPS CREATED")
    print("="*60)

if __name__ == "__main__":
    run_post_resolution_follow_up()