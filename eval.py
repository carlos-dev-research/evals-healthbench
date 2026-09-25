from openai import OpenAI
from typing import Callable

DATASET = "healthbench/2025-05-07-06-14-12_oss_eval.jsonl"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)






#print(rsp.choices[0].message.content)
import json
class Rubric:
    def __init__(self, rubric):
        '''Properties
        - Criterion: What the model should have done
        - Points: How many points fulfilling the criterion is worth
        - Tags
        '''
        x = None
        if isinstance(rubric, str):
            x = json.loads(rubric)
        elif isinstance(rubric, dict):
            x = rubric
        else:
            raise Exception("No valid data type for criterion")

        self.criterion = x.get('criterion')
        self.points = x.get('points')
        self.tags = x.get('tags')


    def __str__(self):
        return (
            f"Points: {self.points} Tags: {" ".join(self.tags)}\n"
            f"{self.criterion}"
        )

    def __repr__(self):
        return f"Points: {self.points} Tags: {" ".join(self.tags)}\n"

class HeathBenchRecord:
    def __init__(self, record):    
        '''Properties
        - prompt_id: unique id
        - prompt: Actual conversation the model responds to
        - rubrics: Grading criteria usesd to score a model's response to that prompt
            - criterion
            - points
            - tags metadata about the criterion
        - example_tags: tags categorizing the record
        - ideal_completions_data: optional reference/ideal answer data
        - canary : contamination marker
        '''
        x = json.loads(record)
        self.prompt_id = x.get('prompt_id')
        self.prompt = x.get('prompt')
        self.rubrics = [Rubric(r) for r in x.get('rubrics')]
        self.example_tags = x.get('example_tags')
        self.ideal_completions_data = x.get('ideal_completions_data')
        self.canary = x.get('canary')

    def __str__(self):
        return (
            f"Health Bench Record\n"
            f"Prompt Id: {self.prompt_id}\n"
            f"Canary: {self.canary}\n"
            f"Example Tags: {" ".join(self.example_tags)}\n"
            f"Ideal Completions Data: {self.ideal_completions_data}\n\n"
            f"Prompt:\n{self.prompt}\n\n"
            f"Rubrics:\n\n{"\n\n".join([str(r) for r in self.rubrics])}\n"
        )

    def __repr__(self):
        return f"HealthBenchRecord(prompt_id={self.prompt_id!r})"

    




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




def grade(model:str, temperature:int, completion:str, record:HeathBenchRecord):
    with open('./prompts/GRADER.md','r') as f:
        template = f.read()
    grades = []
    rubrics = record.rubrics


    prompt = "\n\n".join([f"{x.get('role')}\n{x.get('content')}" for x in record.prompt])

    for rubric in rubrics:
        grader_prompt = template.format(prompt=prompt, completion=completion, criterion=rubric.criterion)
        ans = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": grader_prompt}],
            temperature=temperature,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "grading_result",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "explanation": {"type": "string"},
                            "criteria_met": {"type": "boolean"}
                        },
                        "required": ["explanation", "criteria_met"],
                        "additionalProperties": False
                    }
                }
            }
        ).choices[0].message.content
        grade = get_result(ans)
        grade['prompt_id'] = record.prompt_id
        grade['points'] = rubric.points
        grades.append(grade)

    report = {
        "prompt": record.prompt,
        "completion": completion,
        "rubrics": grades
        }

    return report
        





with open(DATASET, "r") as f:
    for line in f:
        try:
            x = HeathBenchRecord(line)
            print(x.prompt)
            completion = client.chat.completions.create(
                model="ministral-3:8b",
                messages=x.prompt,
                temperature=0.3
            ).choices[0].message.content
            report = grade("ministral-3:8b", 0.3, completion, x)
            with open('./tmp.json','w') as f:
                json.dump(report, f, indent=4 )
            #print(grades)
        except Exception as e:
            print(e)
        
        break


    #rsp = client.chat.completions.create(
#    model="ministral-3:8b",
#    messages=[{"role": "user", "content": "Write a short poem"}],
#    temperature=0.3
#)