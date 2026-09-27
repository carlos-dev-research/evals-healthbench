import json
import pandas as pd
import numpy as np

class JsonNotFoundError(Exception):
    """Raised when no valid JSON object could be found in the model's answer."""
    def __init__(self, message="No valid JSON object found in model answer", raw_text=None):
        self.message = message
        self.raw_text = raw_text
        super().__init__(self.message)

def get_result(ans: str) -> dict:
    '''Scan for JSON object in model answer; returns the first valid balanced-brace JSON found.'''
    found = False
    acc = 0
    start = -1

    for i in range(len(ans)):
        if ans[i] == "{":
            if not found:
                start = i
            found = True
            acc += 1
        elif ans[i] == "}":
            acc -= 1

        if found and acc == 0:
            candidate = ans[start:i + 1]
            try:
                return json.loads(candidate, strict=False)
            except json.JSONDecodeError:
                found = False  # reset and keep scanning for another candidate
                continue

    raise JsonNotFoundError("No valid JSON object found in model answer")

def get_score(row):
    X = row['rubrics']
    A = [int(xj.get("criteria_met")) * xj.get("points") for xj in X]
    B = [max(0,xj.get("points")) for xj in X]
    return sum(A)/sum(B)

def calculate_score(results_file):
    dx = pd.read_json(results_file, lines=True)
    dx['score'] = dx.apply(get_score, axis=1)
    return float(np.clip(dx.score.mean(),0,1))