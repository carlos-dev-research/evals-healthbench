# 1. Initialize Environment
from dotenv import load_dotenv
load_dotenv()


# 2. Import libraries and dependencies
from openai import OpenAI
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import os
from pygrader import grade, calculate_score

# 3. Define parameters
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DATASET = "healthbench/2025-05-07-06-14-12_oss_eval_N200.jsonl"
FOLDER_NAME = f"test-{timestamp}"
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_TEST=os.getenv("MODEL_TEST")
MODEL_GRADER= os.getenv("MODEL_GRADER")
RESONING_TEST=os.getenv("RESONING_TEST")  # low | medium | high | None
RESONING_GRADER=os.getenv("RESONING_GRADER") # low | medium | high | None

folder = Path(FOLDER_NAME)
folder.mkdir(parents=True, exist_ok=True)

# 4. Create OpenAI lib client to test model
client = OpenAI(
    base_url= BASE_URL,
    api_key=API_KEY
)

# 5. Load Template for the Grader
with open('GRADER.md','r') as f:
    template = f.read()

# 6. Load and evaluate dataset
with open(DATASET, "r") as f:
    acc = 0
    for line in tqdm(f, desc="Evaluation Model"):
        report_line = grade(client, MODEL_TEST,RESONING_TEST, MODEL_GRADER, RESONING_GRADER, template, line)
        with open(folder / "results.jsonl", "a") as fa:
            if acc >0:
                fa.write("\n")
            fa.write(report_line)
        acc += 1

# 6. Scoring Model and writing report
score = calculate_score(folder / "results.jsonl")

description = f"""# TEST RUN DESCRIPTION

Dataset: {DATASET}

Model Evaluated: {MODEL_TEST}

Model Evaluated Reasoning Effort: {RESONING_TEST}

Model Grader: {MODEL_GRADER}

Model Grader Reasoning Effort: {RESONING_GRADER}

Timestamp: {timestamp}

Score: {score}
"""

with open(folder / "description.md", "w") as f:
     f.write(description)

print("Report Finish")
