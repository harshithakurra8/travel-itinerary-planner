import json
import os

def load_prompts():
    # Support running from any working directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_path = os.path.join(base_dir, "prompts", "prompts.json")
    
    with open(prompts_path, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    
    return prompts
