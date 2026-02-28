import json
import os

def run_test(reference_file="dataset_reference.json", results_file="analysis_results.json"):
    try:
        if not os.path.exists(reference_file) or not os.path.exists(results_file):
            print("Error: One of the files is missing.")
            return

        with open(reference_file, "r", encoding="utf-8") as f:
            ref_data = {item["id"]: item["reference_data"] for item in json.load(f)}
        
        with open(results_file, "r", encoding="utf-8") as f:
            res_data = {item["id"]: item["analysis"] for item in json.load(f)}
            
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    total = len(res_data)
    correct_satisfaction = 0
    correct_scenarios = 0
    mismatches = []

    for idx, analysis in res_data.items():
        if idx not in ref_data:
            continue
        
        true_label = ref_data[idx].get("label") 
        pred_label = analysis.get("satisfaction")

        true_scenario = str(ref_data[idx].get("scenario")).lower()
        pred_scenario = str(analysis.get("scenario")).lower()

        if true_label == pred_label:
            correct_satisfaction += 1
        
        if true_scenario == pred_scenario:
            correct_scenarios += 1
        else:
            if true_label != pred_label or true_scenario != pred_scenario:
                mismatches.append({
                    "id": idx,
                    "true_label": true_label,
                    "pred_label": pred_label,
                    "true_scenario": true_scenario,
                    "pred_scenario": pred_scenario
                })

    accuracy_label = (correct_satisfaction / total) * 100 if total > 0 else 0
    accuracy_scenario = (correct_scenarios / total) * 100 if total > 0 else 0

    print("-" * 50)
    print(f"SATISFACTION ACCURACY: {accuracy_label:.2f}% ({correct_satisfaction}/{total})")
    print(f"SCENARIO DETECTION ACCURACY: {accuracy_scenario:.2f}% ({correct_scenarios}/{total})")
    print("-" * 50)

    if mismatches:
        print("\nMISMATACHES:")
        for m in mismatches[:15]:
            print(f"ID {m['id']} | Scenario: [Ref: {m['true_scenario']} | Pred: {m['pred_scenario']}]")
            print(f"      | Satisfaction: [Ref: {m['true_label']} | Pred: {m['pred_label']}]")
            print("-" * 20)

if __name__ == "__main__":
    run_test()