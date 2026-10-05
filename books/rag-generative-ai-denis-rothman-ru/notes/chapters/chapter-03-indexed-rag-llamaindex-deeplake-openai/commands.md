# Commands and tools — глава 3

Only source-confirmed commands/tools from `p0085:c01–p0107:c01` are included.

Secrets/account-specific paths are replaced with placeholders. Source contradictions are preserved.

## Classification

| Command / tool | Class | Effect |
|---|---|---|
| `!pip install llama-index-vector-stores-deeplake==0.1.6` | state-changing | changes Python environment |
| `!pip install deeplake==3.9.8` | state-changing | changes Python environment |
| `!pip install llama-index==0.10.64` | state-changing | changes Python environment |
| `!mkdir data` | state-changing | creates local directory |
| `requests.get(...)` | workload-generating | performs external HTTP request |
| writing `./data/*.txt` | state-changing | creates/overwrites local source files |
| `SimpleDirectoryReader(...).load_data()` | read/workload | loads files and metadata |
| `DeepLakeVectorStore(..., overwrite=True)` | state-changing | creates/replaces remote dataset |
| `VectorStoreIndex.from_documents(...)` | workload/stateful in runtime | creates index from documents |
| `deeplake.load(...)` | read-only | loads dataset |
| `VectorStoreIndex.from_documents(...)` | workload | builds vector index |
| `TreeIndex.from_documents(...)` | workload | builds tree index |
| `ListIndex.from_documents(...)` | workload | builds list/summary index |
| `KeywordTableIndex.from_documents(...)` | workload | builds keyword table index |
| `.query(...)` | workload-generating | retrieval + LLM synthesis |
| SentenceTransformer encode | workload-generating | creates semantic embeddings for evaluation |

## 1. Install integration packages

Source: `p0085:c01`.

```python
!pip install llama-index-vector-stores-deeplake==0.1.6
!pip install deeplake==3.9.8
!pip install llama-index==0.10.64
```

Verification:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
```

Rollback: `[Needs confirmation]`.

### Source contradiction

`p0097:c01` separately states `llama-index-vector-stores-deeplake==0.1.2`.

Do not treat `0.1.2` and `0.1.6` as equivalent. The chapter source is inconsistent.

## 2. Create local data directory

Source: `p0086:c01`.

```python
!mkdir data
```

Class: state-changing.

Effect:
- creates local `data` directory.

Verification:
- directory exists before writing files.

Rollback:
- exact source procedure `[Needs confirmation]`.

## 3. Collect and clean source documents

Sources: `p0086:c01–p0087:c01`.

```python
import requests
from bs4 import BeautifulSoup
import re
import os
```

Cleaning:

```python
def clean_text(content):
    content = re.sub(r"\[\d+\]", "", content)
    content = re.sub(r"[^\w\s\.]", "", content)
    return content
```

Fetch pattern:

```python
def fetch_and_clean(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        content = (
            soup.find("div", {"class": "mw-parser-output"})
            or soup.find("div", {"id": "content"})
        )
        if content is None:
            return None

        text = content.get_text(separator=" ", strip=True)
        return clean_text(text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None
```

The full source also removes sections such as References, Bibliography, External links, See also and Notes.

Write per-source files:

```python
output_dir = "./data/"
os.makedirs(output_dir, exist_ok=True)

for url in urls:
    article_name = url.split("/")[-1].replace(".html", "")
    filename = os.path.join(output_dir, article_name + ".txt")
    clean_article_text = fetch_and_clean(url)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(clean_article_text)
```

Effect:
- performs external HTTP requests;
- creates/overwrites files.

Risk:
- source can be noisy, malformed or non-decodable;
- the chapter intentionally includes imperfect documents.

Verification:
- inspect output directory;
- handle decoding warnings according to project requirements.

Rollback: `[Needs confirmation]`.

## 4. Load documents and metadata

Source: `p0088:c01`.

```python
documents = SimpleDirectoryReader("./data/").load_data()
documents[0]
```

Class: read/workload.

Verification:
- inspect returned text and metadata;
- confirm file path/name/source details are available.

## 5. Create/populate Deep Lake vector store

Sources: `p0089:c01–p0090:c01`.

Artifact-safe path:

```python
from llama_index.core import StorageContext

vector_store_path = "hub://<ORG>/<DATASET>"
dataset_path = "hub://<ORG>/<DATASET>"
```

Creation:

```python
vector_store = DeepLakeVectorStore(
    dataset_path=dataset_path,
    overwrite=True,
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store,
)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

Class: state-changing.

Effect:
- `overwrite=True` replaces existing dataset content in source explanation;
- documents are indexed and uploaded.

Risk:
- destructive replacement of prior dataset state;
- external/remote side effects;
- chapter provides no restore procedure.

Verification:
- successful dataset creation/upload;
- inspect tensors and dataset structure.

Rollback: `[Needs confirmation]`.

### Source extraction issue

`p0090:c01` contains a standalone closing `)` after the index call. The intended call is clear; this artifact omits only that isolated extraction artifact.

## 6. Load dataset

Source: `p0090:c01`.

```python
import deeplake
ds = deeplake.load(dataset_path)
```

Class: read-only.

Verification:
- successful load;
- inspect dataset/tensors.

### Source contradiction

The code path uses a `drone_v2` dataset, while one visualization URL shown on `p0091:c01` points to `drone_v1`.

## 7. Inspect dataset records

Source: `p0091:c01`.

```python
import json
import pandas as pd
import numpy as np
```

Source converts tensors to a Pandas DataFrame and displays a selected record containing:
- ID;
- Metadata;
- Text;
- Embedding.

Class: read-only / local workload.

Verification:
- metadata includes source file information;
- text and embedding are associated with the same record.

## 8. Baseline query parameters

Source: `p0095:c01`.

```python
user_input = "How do drones identify vehicles?"

k = 3
temp = 0.1
mt = 1024
```

Source meaning:
- `k`: top retrieval count / ranking input;
- `temp`: LLM temperature;
- `mt`: output token limit.

These values are chapter example parameters, not universal defaults.

## 9. Semantic similarity metric

Sources: `p0095:c01–p0096:c01`.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

```python
def calculate_cosine_similarity_with_embeddings(text1, text2):
    embeddings1 = model.encode(text1)
    embeddings2 = model.encode(text2)
    similarity = cosine_similarity([embeddings1], [embeddings2])
    return similarity[0][0]
```

Class: workload-generating.

## 10. VectorStoreIndex

Sources: `p0096:c01–p0100:c01`.

Create:

```python
from llama_index.core import VectorStoreIndex

vector_store_index = VectorStoreIndex.from_documents(documents)
```

Query engine:

```python
vector_query_engine = vector_store_index.as_query_engine(
    similarity_top_k=k,
    temperature=temp,
    num_output=mt,
)
```

Query:

```python
response = vector_query_engine.query(user_input)
```

Source inspection:
- `response.source_nodes`;
- node ID;
- score;
- text;
- source metadata.

The source also measures elapsed query time and a derived performance indicator.

## 11. TreeIndex

Source: `p0102:c01`.

```python
from llama_index.core import TreeIndex

tree_index = TreeIndex.from_documents(documents)

tree_query_engine = tree_index.as_query_engine(
    similarity_top_k=k,
    temperature=temp,
    num_output=mt,
)

response = tree_query_engine.query(user_input)
```

Class: workload-generating.

Verification:
- generated answer;
- execution time;
- cosine similarity;
- performance indicator.

## 12. ListIndex / SummaryIndex

Source: `p0104:c01`.

```python
from llama_index.core import ListIndex

list_index = ListIndex.from_documents(documents)

list_query_engine = list_index.as_query_engine(
    similarity_top_k=k,
    temperature=temp,
    num_output=mt,
)

response = list_query_engine.query(user_input)
```

Source output identifies the class as `SummaryIndex`.

The chapter’s one run was slower than the tree/vector examples, but explicitly warns against generalizing this result.

## 13. KeywordTableIndex

Sources: `p0105:c01–p0107:c01`.

```python
from llama_index.core import KeywordTableIndex

keyword_index = KeywordTableIndex.from_documents(documents)
```

Inspect keyword table:

```python
data = []

for keyword, doc_ids in keyword_index.index_struct.table.items():
    for doc_id in doc_ids:
        data.append({
            "Keyword": keyword,
            "Document ID": doc_id,
        })

df = pd.DataFrame(data)
```

Query engine:

```python
keyword_query_engine = keyword_index.as_query_engine(
    similarity_top_k=k,
    temperature=temp,
    num_output=mt,
)

response = keyword_query_engine.query(user_input)
```

Class: workload-generating.

Verification:
- keyword→document-ID structure;
- response;
- query time;
- similarity;
- performance indicator.

## 14. Performance metric

Sources: `p0099:c01–p0100:c01`, repeated for later indexes.

Source concept:

```python
scores = [
    node.score
    for node in response.source_nodes
    if node.score is not None
]
```

Then the source computes a weighted average of scores and divides by elapsed time.

Interpretation:
- indicator for comparing mechanisms in the chapter’s experiment;
- not an absolute quality score;
- stochastic timing makes runs variable.
