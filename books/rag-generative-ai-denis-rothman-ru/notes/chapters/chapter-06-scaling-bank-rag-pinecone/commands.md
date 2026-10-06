# Commands and tools — глава 6

Only source-confirmed operations from `p0166:c01–p0197:c01` are included.

Secrets and account-specific names are replaced with placeholders.

## Classification

| Operation | Class | Effect |
|---|---|---|
| `drive.mount(...)` | state-changing | mounts external storage |
| set Kaggle env vars | state-changing | changes process environment |
| `!pip install kaggle` | state-changing | changes Python environment |
| Kaggle dataset download | state-changing/external | downloads archive |
| unzip | state-changing | writes extracted files |
| DataFrame `drop(..., inplace=True)` | state-changing in memory | removes columns |
| `to_csv` / `cp` | state-changing | writes/copies files |
| k-means / metrics | local workload | analysis |
| OpenAI embeddings | workload-generating | external API |
| Pinecone index creation | remote state-changing | creates vector index |
| Pinecone `upsert` | remote state-changing | writes vectors/metadata |
| Pinecone query | workload-generating | vector retrieval |
| GPT-4o completion | workload-generating | external generation |

## 1. Kaggle credentials

Sources: `p0166:c01–p0167:c01`.

```python
from google.colab import drive
drive.mount("/content/drive")
```

```python
import os
import json

with open("<KAGGLE_JSON_FILE>", "r") as f:
    kaggle_credentials = json.load(f)

os.environ["KAGGLE_USERNAME"] = kaggle_credentials["username"]
os.environ["KAGGLE_KEY"] = kaggle_credentials["key"]
```

Verification:
- environment variables exist;
- do not print values.

## 2. Install/authenticate Kaggle

Source: `p0167:c01`.

```python
try:
    import kaggle
except:
    !pip install kaggle

import kaggle
kaggle.api.authenticate()
```

Rollback: `[Needs confirmation]`.

## 3. Download and unpack dataset

Source: `p0167:c01`.

```bash
!kaggle datasets download -d radheshyamkollipara/bank-customer-churn
```

```python
import zipfile

with zipfile.ZipFile("/content/bank-customer-churn.zip", "r") as zip_ref:
    zip_ref.extractall("/content/")
```

Effect:
- creates local archive/extracted files.

## 4. Remove columns and save cleaned dataset

Source: `p0168:c01`.

```python
data1.drop(
    columns=["RowNumber", "Surname", "Gender", "Geography"],
    inplace=True,
)
```

```python
data1.to_csv("data1.csv", index=False)
```

Source also copies the file to Google Drive.

Verification:
- inspect resulting columns;
- row count remains 10,000.

## 5. EDA

Sources: `p0169:c01–p0172:c01`.

The source evaluates:
- `Exited`;
- `Complain`;
- age threshold;
- salary threshold;
- numeric correlation heatmap.

Example code computes:

```python
percentage_complain_over_exited = (
    sum_complain / sum_exited
) * 100
```

Source wording calls the 100.29% result a strong correlation.

Status: `[Source wording/code mismatch]`.

## 6. K-means evaluation

Sources: `p0173:c01–p0175:c01`.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

features = data2[
    [
        "CreditScore",
        "Age",
        "EstimatedSalary",
        "Exited",
        "Complain",
        "Point Earned",
    ]
]

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
```

Compare k:

```python
for n_clusters in range(2, 5):
    kmeans = KMeans(
        n_clusters=n_clusters,
        n_init=20,
        random_state=0,
    )
    cluster_labels = kmeans.fit_predict(features_scaled)
    silhouette_avg = silhouette_score(
        features_scaled,
        cluster_labels,
    )
    db_index = davies_bouldin_score(
        features_scaled,
        cluster_labels,
    )
```

Chosen source run:

```python
kmeans = KMeans(
    n_clusters=2,
    n_init=10,
    random_state=0,
)
data2["class"] = kmeans.fit_predict(features_scaled)
```

## 7. Install OpenAI and Pinecone

Source: `p0179:c01`.

```python
!pip install openai==1.40.3
!pip install pinecone-client==5.0.1
```

Credentials are read from files; artifacts use placeholders.

## 8. Convert rows to chunks

Sources: `p0180:c01–p0181:c01`.

```python
output_lines = []

for _, row in data1.iterrows():
    row_data = [
        f"{col}: {row[col]}"
        for col in data1.columns
    ]
    output_lines.append(" ".join(row_data))

chunks = []
for line in output_lines:
    chunks.append(line)
```

Verification:
- 10,000 rows;
- 10,000 chunks.

## 9. OpenAI embeddings

Sources: `p0182:c01–p0184:c01`.

```python
embedding_model = "text-embedding-3-small"
client = openai.OpenAI()

def get_embedding(text, model=embedding_model):
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[text],
        model=model,
    )
    return response.data[0].embedding
```

Source batch example:
- chunk window: 1000;
- pause: 3 seconds;
- 10 batches for 10,000 chunks.

Verification:
- `len(chunks) == len(embeddings)`.

## 10. Duplicate data for scale simulation

Sources: `p0184:c01–p0185:c01`.

```python
dsize = 5

duplicated_chunks = []
duplicated_embeddings = []

for i in range(len(chunks)):
    for _ in range(dsize):
        duplicated_chunks.append(chunks[i])
        duplicated_embeddings.append(embeddings[i])
```

Example result:
- 50,000 chunks;
- 50,000 embeddings.

## 11. Create Pinecone client/index

Sources: `p0185:c01–p0186:c01`.

Artifact-safe form:

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="<PINECONE_API_KEY>")

index_name = "<INDEX_NAME>"
spec = ServerlessSpec(
    cloud="aws",
    region="us-east-1",
)

if index_name not in pc.list_indexes().names():
    pc.create_index(
        index_name,
        dimension=1536,
        metric="cosine",
        spec=spec,
    )

index = pc.Index(index_name)
```

Source note:
- an intermediate variable `api_key` is assigned, while the shown constructor uses `PINECONE_API_KEY`.
- artifact uses a placeholder instead of silently depending on ambiguous variable state.

## 12. Batch upsert

Sources: `p0187:c01–p0188:c01`.

```python
def upsert_to_pinecone(data, batch_size):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        index.upsert(vectors=batch)
```

Source batch-size helper targets slightly below 4 MB.

Upload shape:

```python
data_for_upsert = [
    {
        "id": str(id),
        "values": emb,
        "metadata": {"text": chunk},
    }
    for id, (chunk, emb)
    in zip(
        ids,
        zip(
            duplicated_chunks,
            duplicated_embeddings,
        ),
    )
]
```

Class: remote state-changing.

Verification:
- progress output;
- `index.describe_index_stats(...)`;
- expected vector count.

Rollback: `[Needs confirmation]`.

## 13. Upsert timing source inconsistency

- `p0188:c01`: 50,000 items → 560.66 seconds.
- `p0189:c01`: prose says 10,000 points → about 56 seconds.

Do not normalize these into one benchmark.

## 14. Query Pinecone

Sources: `p0189:c01–p0190:c01`.

```python
query_embedding = get_embedding(
    query_text,
    model=embedding_model,
)

query_results = index.query(
    vector=query_embedding,
    top_k=1,
    include_metadata=True,
)
```

Verification:
- ID;
- score;
- text metadata;
- query time.

The artifact uses `query_text`; source p193 later shows a mismatch using `text`.

## 15. Target-vector RAG

Sources: `p0192:c01–p0194:c01`.

Source selects a customer-profile target vector and retrieves top-k similar records:

```python
query_results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
)

relevant_texts = [
    match["metadata"]["text"]
    for match in query_results["matches"]
    if "metadata" in match
    and "text" in match["metadata"]
]

combined_context = "\n".join(relevant_texts)
```

Source code mismatch:
- p192 defines `query_text`;
- p193 shows `get_embedding(text,...)`.

Status: `[Source code mismatch]`.

## 16. GPT-4o recommendation

Sources: `p0194:c01–p0197:c01`.

The prompt combines:
- instruction;
- target customer profile;
- retrieved similar profiles.

Model:
- GPT-4o;
- `temperature=0`;
- `max_tokens=300`;
- `top_p=1`;
- penalties = 0.

Source extraction issue:
- `gpt_model = "gpt-4o` appears without a closing quote on p195.

Verification:
- inspect generated retention email;
- record response time.
