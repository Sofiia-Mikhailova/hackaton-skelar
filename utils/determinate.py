import json
import os

def compare_results(file1_name="analysis_results1.json", file2_name="analysis_results2.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.join(base_dir, file1_name)
    path2 = os.path.join(base_dir, file2_name)

    if not os.path.exists(path1) or not os.path.exists(path2):
        return

    with open(path1, "r", encoding="utf-8") as f1, open(path2, "r", encoding="utf-8") as f2:
        data1 = {item["id"]: item["analysis"] for item in json.load(f1)}
        data2 = {item["id"]: item["analysis"] for item in json.load(f2)}

    all_ids = sorted(set(data1.keys()) | set(data2.keys()))
    
    diffs = []
    for chat_id in all_ids:
        res1 = data1.get(chat_id)
        res2 = data2.get(chat_id)

        if not res1 or not res2:
            continue

        item_diff = {"id": chat_id, "changes": {}}
        for key in ["intent", "scenario", "satisfaction", "quality_score", "agent_mistakes"]:
            val1 = res1.get(key)
            val2 = res2.get(key)
            
            if val1 != val2:
                item_diff["changes"][key] = {"file1": val1, "file2": val2}
        
        if item_diff["changes"]:
            diffs.append(item_diff)

    output_path = os.path.join(base_dir, "comparison_diff.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(diffs, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    compare_results()