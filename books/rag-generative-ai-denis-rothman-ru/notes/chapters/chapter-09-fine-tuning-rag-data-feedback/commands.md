# Commands and tools — глава 9

Only source-confirmed operations from `p0256:c01–p0269:c01` are included.

Secrets and account-specific IDs are replaced with placeholders.

## Classification

| Operation | Class | Effect |
|---|---|---|
| Drive mount | state-changing | mounts external storage |
| set `OPENAI_API_KEY` | state-changing | changes process environment |
| pip installs | state-changing | changes Python environment |
| Hugging Face dataset load | external/local workload | downloads/caches dataset |
| JSONL-style write | state-changing | creates/overwrites training file |
| OpenAI file upload | remote state-changing | creates training-file object |
| fine-tuning job creation | remote state-changing | starts billable training |
| fine-tuning job list | read-only remote | monitors job status |
| chat completion on tuned model | workload-generating | external/billable generation |

## 1. OpenAI credential handling

Sources: `p0256:c01–p0257:c01`.

Artifact-safe form:

```python
from google.colab import drive
drive.mount("/content/drive")

with open("<OPENAI_API_KEY_FILE>", "r") as f:
    API_KEY = f.readline().strip()

import os
import openai

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
```

Source extraction issue:
- the displayed Colab import on p256 is malformed.

## 2. Install packages

Sources: `p0256:c01–p0257:c01`.

```python
!pip install openai==1.42.0
!pip install jsonlines==4.0.0
!pip install datasets==2.20.0
```

Rollback: `[Needs confirmation]`.

## 3. Load/filter SciQ

Sources: `p0257:c01–p0258:c01`.

```python
from datasets import load_dataset
import pandas as pd

dataset_view = load_dataset(
    "sciq",
    split="train",
)

filtered_dataset = dataset_view.filter(
    lambda x:
        x["support"] != ""
        and x["correct_answer"] != ""
)
```

Source-observed count:
- `10481`.

## 4. Remove distractors

Source: `p0258:c01`.

Intended source structure:

```python
df_view = pd.DataFrame(
    filtered_dataset
)

columns_to_drop = [
    "distractor3",
    "distractor1",
    "distractor2",
]
```

Source then shows:

```python
df_view = df.drop(
    columns=columns_to_drop
)
```

Status: `[Source code mismatch]` because `df_view` was created but `df` is referenced.

## 5. Build chat-format training examples

Source: `p0259:c01`.

```python
items = []

for idx, row in df.iterrows():
    detailed_answer = (
        row["correct_answer"]
        + " Explanation: "
        + row["support"]
    )

    items.append({
        "messages": [
            {
                "role": "system",
                "content":
                    "Given a science question, "
                    "provide the correct answer "
                    "with a detailed explanation."
            },
            {
                "role": "user",
                "content": row["question"],
            },
            {
                "role": "assistant",
                "content": detailed_answer,
            },
        ]
    })
```

## 6. Write JSONL-style training file

Source: `p0259:c01`.

```python
with jsonlines.open(
    "/content/QA_prompts_and_completions.json",
    "w",
) as writer:
    writer.write_all(items)
```

Class: state-changing local file write.

Source mismatch:
- format is described as JSONL;
- filename uses `.json`.

Verification:

```python
df = pd.read_json(
    "/content/QA_prompts_and_completions.json",
    lines=True,
)
```

## 7. Initialize OpenAI client

Source: `p0260:c01`.

```python
from openai import OpenAI

client = OpenAI()
```

## 8. Upload training file

Source: `p0260:c01`.

```python
result_file = client.files.create(
    file=open(
        "QA_prompts_and_completions.json",
        "rb",
    ),
    purpose="fine-tune",
)

param_training_file_name = result_file.id
```

Class: remote state-changing.

Verification:
- inspect returned file object;
- confirm file status is processed before training.

## 9. Create fine-tuning job

Sources: `p0260:c01–p0261:c01`.

```python
ft_job = client.fine_tuning.jobs.create(
    training_file=param_training_file_name,
    model="gpt-4o-mini-2024-07-18",
)
```

Class: remote state-changing / billable.

Source-observed hyperparameters:
- `n_epochs='auto'`;
- `batch_size='auto'`;
- `learning_rate_multiplier='auto'`.

## 10. Monitor fine-tuning jobs

Sources: `p0262:c01–p0263:c01`.

```python
response = client.fine_tuning.jobs.list(
    limit=3
)
```

The source collects:
- job ID;
- created at;
- status;
- model;
- training file;
- error message;
- fine-tuned model ID.

Class: read-only remote monitoring.

## 11. Select latest usable fine-tuned model

Sources: `p0263:c01–p0264:c01`.

```python
generation = False

non_empty_models = df[
    df["Fine-Tuned Model"].notna()
    & (
        df["Fine-Tuned Model"] != ""
    )
]

if not non_empty_models.empty:
    first_non_empty_model = (
        non_empty_models[
            "Fine-Tuned Model"
        ].iloc[0]
    )
    generation = True
```

Verification:
- do not generate unless a model ID exists.

## 12. Query fine-tuned model

Sources: `p0264:c01–p0265:c01`.

```python
if generation == True:
    response = client.chat.completions.create(
        model=first_non_empty_model,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content":
                    "Given a question, reply "
                    "with a complete explanation "
                    "for students."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
```

Class: external/billable workload.

Source chooses `temperature=0.0` because scientific Q/A does not require creative variation.

## 13. Inspect generated text

Source: `p0265:c01`.

```python
if generation == True:
    response_text = (
        response
        .choices[0]
        .message
        .content
    )
```

Verification:
- compare with expected science answer/explanation.

## 14. Metrics / monitoring

Sources: `p0266:c01–p0269:c01`.

Source UI exposes:
- status;
- job ID;
- base model;
- output model;
- created at;
- trained tokens;
- epochs;
- batch size;
- LR multiplier;
- seed;
- training loss;
- time/step information;
- usage/cost information.

Source example:
- training loss: `1.1570`.

Interpretation:
- lower training loss is described as better fit to training data;
- do not treat this one value as a universal acceptance threshold.
