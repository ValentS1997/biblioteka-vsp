# Commands and tools — глава 8

Only source-confirmed operations from `p0231:c01–p0250:c01` are included.

Secrets are replaced by placeholders.

## Classification

| Operation | Class | Effect |
|---|---|---|
| `drive.mount(...)` | state-changing | mounts external storage |
| set `HF_TOKEN` | state-changing | changes process environment |
| pip installs | state-changing | changes Python environment |
| model/dataset download | external + local state | downloads/cache files |
| `chromadb.Client()` | runtime state | creates local temporary client |
| `create_collection` | state-changing | creates local collection |
| `collection.add` | state-changing | writes documents/embeddings |
| `collection.query` | workload | semantic retrieval |
| spaCy similarity | local workload | evaluates retrieval |
| Llama pipeline generation | workload | local/GPU text generation |
| `delete_collection` | destructive state-changing | deletes collection |

## 1. Token handling

Sources: `p0231:c01–p0232:c01`.

Artifact-safe form:

```python
from google.colab import drive
drive.mount("/content/drive")

with open("<HF_TOKEN_FILE>", "r") as f:
    access_token = f.readline().strip()

import os
os.environ["HF_TOKEN"] = access_token
```

Risk:
- token enters process memory/environment;
- do not print or commit it.

## 2. Install Hugging Face stack

Source: `p0232:c01`.

```python
!pip install datasets==2.20.0
!pip install transformers==4.41.2
!pip install accelerate==0.31.0
```

The chapter notes possible dependency conflicts, specifically mentioning pyarrow/Colab compatibility at the time of writing.

Rollback: `[Needs confirmation]`.

## 3. Initialize Llama pipeline

Sources: `p0232:c01–p0233:c01`.

Source intent:

```python
from transformers import AutoTokenizer
import transformers
import torch

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)
```

### Source code issue

The source text itself shows `import tranformers`; this artifact uses the intended module name only to present the surrounding call coherently and records the typo rather than attributing it to the source as correct code.

## 4. Install Chroma

Source: `p0233:c01`.

```python
!pip install chromadb==0.5.3
```

The source notes ONNX Runtime as part of the installed dependency stack.

## 5. Install spaCy model

Source: `p0234:c01`.

```bash
!python -m spacy download en_core_web_md
```

Source note:
- runtime/session restart is required after installation.

## 6. Start session timer

Source: `p0235:c01`.

```python
session_start_time = time.time()
```

Class: read-only metric state.

## 7. Load and prepare SciQ

Source: `p0236:c01`.

```python
from datasets import load_dataset
import pandas as pd

dataset = load_dataset("sciq", split="train")

filtered_dataset = dataset.filter(
    lambda x:
        x["support"] != ""
        and x["correct_answer"] != ""
)

df = pd.DataFrame(filtered_dataset)

df.drop(
    columns=[
        "distractor3",
        "distractor1",
        "distractor2",
    ],
    inplace=True,
)

df["completion"] = (
    df["correct_answer"]
    + " because "
    + df["support"]
)

df.dropna(
    subset=["completion"],
    inplace=True,
)
```

Verification:
- source output reports `10481` rows;
- source output reports four columns:
  `question`, `correct_answer`, `support`, `completion`.

## 8. Create/check Chroma collection

Sources: `p0237:c01–p0238:c01`.

```python
import chromadb

client = chromadb.Client()
collection_name = "sciq_supports6"

collections = client.list_collections()

collection_exists = any(
    collection.name == collection_name
    for collection in collections
)

if collection_exists != True:
    collection = client.create_collection(
        collection_name
    )
```

Class: state-changing local runtime.

## 9. Populate collection

Sources: `p0239:c01–p0240:c01`.

```python
ldf = len(df)
nb = ldf

completion_list = (
    df["completion"][:nb]
    .astype(str)
    .tolist()
)

if collection_exists != True:
    collection.add(
        ids=[
            str(i)
            for i in range(0, nb)
        ],
        documents=completion_list,
        metadatas=[
            {"type": "completion"}
            for _ in range(0, nb)
        ],
    )
```

Class: state-changing.

Source example:
- >10k documents;
- response time `234.25 s`.

## 10. Inspect embeddings

Source: `p0240:c01–p0241:c01`.

```python
result = collection.get(
    include=["embeddings"]
)

first_embedding = result["embeddings"][0]
embedding_length = len(first_embedding)
```

Source-observed length:
- `384`.

## 11. Bulk query

Sources: `p0241:c01–p0242:c01`.

```python
results = collection.query(
    query_texts=df["question"][:nb],
    n_results=1,
)
```

Source example:
- >10k queries;
- response time `199.34 s`.

## 12. spaCy similarity

Sources: `p0242:c01–p0244:c01`.

```python
import spacy
import numpy as np

nlp = spacy.load(
    "en_core_web_md"
)

def simple_text_similarity(
    text1,
    text2,
):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    vector1 = doc1.vector
    vector2 = doc2.vector

    if (
        np.linalg.norm(vector1) == 0
        or np.linalg.norm(vector2) == 0
    ):
        return 0.0

    return (
        np.dot(vector1, vector2)
        /
        (
            np.linalg.norm(vector1)
            * np.linalg.norm(vector2)
        )
    )
```

Source acceptance-example:

```python
if similarity_score > 0.7:
    acc_counter += 1
```

This threshold is not universal.

## 13. Single meeting-time retrieval

Source: `p0246:c01`.

```python
results = collection.query(
    query_texts=[prompt],
    n_results=1,
)
```

Verification:
- at least one retrieved document;
- inspect returned text.

Source example response time:
- `0.03 s`.

## 14. Llama generation

Sources: `p0247:c01–p0248:c01`.

```python
def LLaMA2(prompt):
    sequences = pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=100,
        temperature=0.5,
        repetition_penalty=2.0,
        truncation=True,
    )

    return sequences
```

Augmentation:

```python
iprompt = (
    "Read the following input "
    "and write a summary for beginners."
)

lprompt = (
    iprompt
    + " "
    + results["documents"][0][0]
)
```

Source example response time:
- `5.91 s`.

## 15. Delete collection

Source: `p0250:c01`.

Displayed source:

```python
#client.delete_collection(collection_name)
```

Class if uncommented:
- destructive state-changing.

Verification:

```python
collections = client.list_collections()

collection_exists = any(
    collection.name == collection_name
    for collection in collections
)
```

Rollback after actual deletion:
- `[Needs confirmation]`.

## 16. Session duration

Source: `p0250:c01`.

Source computes:

```python
end_time = (
    time.time()
    - session_start_time
)
```

but prints `response_time` instead of `end_time`.

Status: `[Source code mismatch]`.

Source narrative reports:
- `780.35 s`;
- “less than 15 minutes”.

Treat as an example run, not an SLO.
