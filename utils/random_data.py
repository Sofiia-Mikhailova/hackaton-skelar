import json
import random
import os

def select_random_samples(input_filename="dataset_clean.json", output_filename="dataset_determinate.json", count=20):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(os.path.dirname(base_dir), "data", input_filename)
    
    if not os.path.exists(input_path):
        input_path = os.path.join(base_dir, input_filename)

    if not os.path.exists(input_path):
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    samples = random.sample(data, min(len(data), count))

    output_path = os.path.join(base_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    select_random_samples()