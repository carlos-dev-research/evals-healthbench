from openai import OpenAI
import json
from .models import *
from .tools import *


def grade_prompt(client:OpenAI, model:str, template:str, temperature:int, completion:str, record:HeathBenchRecord):
    
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
        

def grade(client:OpenAI, test_model:str, grader_model:str, template:str, line_record:str) ->str:
    record = HeathBenchRecord(line_record)
    completion = client.chat.completions.create(
        model=test_model,
        messages=record.prompt,
        temperature=0.3
    ).choices[0].message.content
    report = grade_prompt(client, grader_model, template, 0.3, completion, record)
    return json.dumps(report)