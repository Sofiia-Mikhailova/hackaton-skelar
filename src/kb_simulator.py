import json

def simulate_growth():
    try:
        with open('potential_kb_articles.json', 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    total_cases = len(kb_data)
    initial_ai_cases = len([item for item in kb_data if item["source"] == "AI Autonomous (Tier-1)"])
    learned_cases = len([item for item in kb_data if item["source"] == "Learned from Human (Tier-2)"])
    
    # Calculation
    initial_rate = (initial_ai_cases / total_cases) * 100
    new_rate = ((initial_ai_cases + learned_cases) / total_cases) * 100
    improvement = new_rate - initial_rate

    print("="*60)
    print("SKELAR AI: LEARNING PROGRESS SIMULATION")
    print("="*60)
    print(f"Total Scenarios in KB: {total_cases}")
    print(f"Initial AI Automation Rate: {initial_rate:.1f}%")
    print(f"Cases Learned from Human Demo: +{learned_cases}")
    print("-" * 30)
    print(f"NEW POTENTIAL AUTOMATION RATE: {new_rate:.1f}%")
    print(f"IMPROVEMENT: +{improvement:.1f}% Efficiency Boost")
    print("="*60)

    # Save metrics for Dashboard
    metrics = {
        "initial_rate": initial_rate,
        "new_rate": new_rate,
        "improvement": improvement,
        "total_learned": learned_cases
    }
    with open('learning_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    simulate_growth()