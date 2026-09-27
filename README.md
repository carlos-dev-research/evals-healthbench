# evals-healthbench

These repository has the purpose of testing different models on the healthbench dataset, which was published and collected by openAI in order to test model performance as physician assistant. The repo comes with some helper tools to aid in the evaluation and with a jupyter notebook that was used to explore the data and the scoring. The repo using the openAI python library so it can be use to test any model that is compatible with the openAI API. For each test run the script creates a test folder with text description with the score and the model use. The API keys and URL paramters are set in the .env file. The temperature both for the model and the grader are set to 0.3. The GRADER.md is a template use by the script in order to provide structure for the grader so evaluate it can be modified as long as it keep consistent with the parameters used by the script. In the .env file the model top test and the model to grade can be chosen , API URL and Reasonign efforts. The repo was serve from hugging face and it was based on the openAI paper on healthbench. The score and results were test on subset of healthbench in order to save on API credits.

# Dependencies and Setup
- Using python 3.12.14 on MacOS M1, virtual enviroment with miniconda

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

# Resoucres
- [Hugging Face Healthbench Repo](https://huggingface.co/datasets/openai/healthbench)
- [OpenAI Research Paper](https://arxiv.org/abs/2505.08775)
- [OpenAI Main Page description](https://openai.com/index/healthbench/)

