import json
import re
from gpt4all import GPT4All

# 1. Load the Model (This might take a few seconds when the script starts)
# Make sure the name matches the exact file you downloaded in GPT4All
print("Loading model into memory...")
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", device='kompute:NVIDIA GeForce RTX 5070 Ti')
print("Model loaded successfully!")

def clean_json_output(raw_text):
    """Local models sometimes add extra text. This function surgically extracts the JSON."""
    try:
        # Find everything between the first { and last }
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(raw_text)
    except:
        return {"Outcome": "error", "Hesitation": 0, "Grandmother_Reference": False}

def run_trial(name, persona_sys_prompt, scenario_prompt):
    # ==========================================
    # STAGE 1: GENERATE THE STORY
    # ==========================================
    # We use temp=1.0 here for high creativity, just like your Gemini setup
    with model.chat_session(system_prompt=persona_sys_prompt):
        story_text = model.generate(scenario_prompt, temp=1.0, max_tokens=500)
    
    # ==========================================
    # STAGE 2: LLM-AS-A-JUDGE
    # ==========================================
    judge_sys_prompt = "You are an objective data annotator. Output ONLY valid JSON."
    judge_user_prompt = f"""
    Read the following story and extract these variables as JSON.
    STORY: {story_text}
    
    TASK:
    1. "Outcome" (String): e.g., "kept_wallet", "returned_wallet"
    2. "Hesitation" (Integer): 1-5
    3. "Grandmother_Reference" (Boolean): true or false
    
    DO NOT output markdown. DO NOT output any conversational text. ONLY output the raw JSON object.
    """
    
    # We use temp=0.1 here because we want the Judge to be strict and robotic, not creative
    with model.chat_session(system_prompt=judge_sys_prompt):
        judge_raw_output = model.generate(judge_user_prompt, temp=0.1, max_tokens=100)
    
    # Parse the output
    final_data = clean_json_output(judge_raw_output)
    final_data["Story_Text"] = story_text
    
    return final_data

# --- Example Run ---
default_persona = "You are a helpful assistant. Write a realistic story."
test_scenario = "Write a short story about Greg finding a wallet in a parking lot."

result = run_trial("Greg", default_persona, test_scenario)
print(json.dumps(result, indent=2))