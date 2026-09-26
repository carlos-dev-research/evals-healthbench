# Initialize Environment
from dotenv import load_dotenv
load_dotenv()


# Import libraries and dependencies
from openai import OpenAI
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import os
from pygrader import grade

# Define parameters
SAMPLES=10
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DATASET = "healthbench/2025-05-07-06-14-12_oss_eval_N100.jsonl"
FOLDER_NAME = f"test-{timestamp}"
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_TEST=os.getenv("MODEL_TEST")
MODEL_GRADER= os.getenv("MODEL_GRADER")
RESONING_TEST=os.getenv("RESONING_TEST")  # low | medium | high | None
RESONING_GRADER=os.getenv("RESONING_GRADER") # low | medium | high | None

# 1. Create Description File for metadata
description = f"""# TEST RUN DESCRIPTION

Dataset: {DATASET}

Model Evaluated: {MODEL_TEST}

Model Evaluated Reasoning Effort: {RESONING_TEST}

Model Grader: {MODEL_GRADER}

Model Grader Reasoning Effort: {RESONING_GRADER}

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
    for line in tqdm(f, desc="Evaluation Model"):
        report_line = grade(client, MODEL_TEST,RESONING_TEST, MODEL_GRADER, RESONING_GRADER, template, line)
        with open(folder / "results.jsonl", "a") as fa:
            if acc >0:
                fa.write("\n")
            fa.write(report_line)
        acc += 1


print("Report Finish")
