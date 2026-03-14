import json
import time
from datetime import datetime

class ActionExecutor:
    def __init__(self, copilot_file="copilot_results.json", log_file="system_execution_log.json"):
        self.copilot_file = copilot_file
        self.log_file = log_file

    def execute_workflow(self, action_name, chat_id):
        steps = {
            "Initiate Refund": ["Verifying transaction", "Processing reversal", "Success"],
            "Reset Password": ["Generating secure link", "Email sent", "Done"],
            "Check Transaction Status": ["Connecting to gateway", "Fetching status", "Completed"],
            "Escalate to Tier-3 Engineering": ["Collecting logs", "Jira ticket created", "Escalated"]
        }

        if action_name in steps:
            for step in steps[action_name]:
                time.sleep(0.3) 
            return True
        return False

    def run_and_save(self):
        try:
            with open(self.copilot_file, "r", encoding="utf-8") as f:
                suggestions = json.load(f)

            system_history = []

            for item in suggestions:
                chat_id = item.get("chat_id")
                action = item.get("suggested_action")
                confidence = int(item.get("confidence", "0%").replace("%", ""))
                
                status = "Skipped (Low Confidence)"
                if confidence >= 90 and action != "None":
                    success = self.execute_workflow(action, chat_id)
                    status = "Executed Automatically" if success else "Execution Failed"

                log_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "chat_id": chat_id,
                    "intent": item.get("intent"),
                    "action_taken": action,
                    "confidence": f"{confidence}%",
                    "status": status,
                    "risk_level": item.get("risk_level")
                }
                system_history.append(log_entry)

            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(system_history, f, indent=4, ensure_ascii=False)

            print(f"--- All actions recorded to {self.log_file} ---")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    executor = ActionExecutor()
    executor.run_and_save()