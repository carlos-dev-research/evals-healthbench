# evals-healthbench
Evals for Health Bench

# Dependencies and Setup
- Using python 3.12.14 on MacOS M1

```bash
pip install huggingface_hub
pip install jupyterlab
pip install pandas
pip install python-dotenv
```

## Download dataset
```bash

hf download openai/healthbench --repo-type dataset --local-dir ./healthbench
```

# Sample .env
```text
BASE_URL=http://localhost:11434/v1
API_KEY=xxxxxx
MODEL_TEST=openai/gpt-oss-20b
MODEL_GRADER=openai/gpt-oss-20b
RESONING_TEST=low
RESONING_GRADER=low
```