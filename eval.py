from openai import OpenAI
from datetime import datetime
from pathlib import Path
from pygrader import grade

DATASET = "healthbench/2025-05-07-06-14-12_oss_eval.jsonl"
BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"
MODEL_TEST="ministral-3:8b"
MODEL_GRADER="ministral-3:8b"
FOLDER_NAME = "first_test"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



# 1. Create Description File for metadata
description = f"""TEST RUN DESCRIPTION
Dataset: {DATASET}
Model Evaluated: {MODEL_TEST}
Model Grader: {MODEL_GRADER}
Timestamp: {timestamp}
"""

folder = Path(FOLDER_NAME)
folder.mkdir(parents=True, exist_ok=True)

with open(folder / "description.md", "w") as f:
     f.write(description)


# 2. Create OpenAI lib client to test model, right now usign Ollama
client = OpenAI(
    base_url= BASE_URL,
    api_key=API_KEY
)

# 3. Load Template for the Grader
with open('GRADER.md','r') as f:
    template = f.read()

# 4. Load and evaluate dataset
with open(DATASET, "r") as f:
    acc = 0
    for line in f:
        acc += 1
        report_line = grade(client, MODEL_TEST, MODEL_GRADER, template, line)
        with open(folder / "results.jsonl", "a") as fa:
            fa.write(f"\n{report_line}")
        if acc == 3:
            break

print("Report Finish")
    






