# Commands and tools — глава 7

Only source-confirmed operations from `p0203:c01–p0224:c01` are included.

## Classification

| Operation | Class | Effect |
|---|---|---|
| `!pip install Wikipedia-API==0.6.0` | state-changing | changes Python environment |
| Wikipedia API calls | external workload | retrieves page data/metadata |
| citation/URL file writes | state-changing | creates/overwrites local files |
| Deep Lake population | remote state-changing | writes vector data |
| `ow=True` | destructive remote state-changing | overwrites existing dataset |
| `KnowledgeGraphIndex.from_documents` | workload | builds graph index |
| PyVis `write_html` | state-changing | writes graph HTML |
| query engine `.query(...)` | workload-generating | retrieval + LLM response |
| `!pip install sentence-transformers==3.0.1` | state-changing | changes runtime environment |
| SentenceTransformer encode | local workload | computes semantic embeddings |
| NumPy metrics | local workload | computes descriptive statistics |

## 1. Install Wikipedia API client

Source: `p0207:c01`.

```python
try:
    import wikipediaapi
except:
    !pip install Wikipedia-API==0.6.0
    import wikipediaapi
```

Rollback: `[Needs confirmation]`.

## 2. Create Wikipedia API client

Source: `p0207:c01`.

Artifact-safe form:

```python
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="Knowledge/1.0 (<USER_AGENT_CONTACT>)",
)
```

The artifact substitutes the contact placeholder; no actual address is stored.

## 3. Root topic and limits

Source: `p0207:c01`.

```python
topic = "Marketing"
filename = "Marketing"
maxl = 100
```

These are scenario values, not universal limits.

## 4. Page check

Source: `p0208:c01`.

```python
page = wiki.page(topic)

if page.exists() == True:
    summary = page.summary
    print(page.fullurl)
else:
    print("Page does not exist")
```

Class: external/read workload.

## 5. Extract linked pages

Sources: `p0208:c01–p0209:c01`.

```python
links = page.links
urls = []
counter = 0

for link in links:
    counter += 1
    summary = wiki.page(link).summary
    urls.append(wiki.page(link).fullurl)
    if counter >= maxl:
        break
```

### Source code issue

The source later shows:

```python
except page.exists()==False:
    pass
```

This is not valid Python exception syntax and is not reproduced as runnable guidance.

## 6. Write citations

Source: `p0209:c01`.

```python
from datetime import datetime

fname = filename + "_citations.txt"

with open(fname, "w") as file:
    file.write(
        "Citation. In Wikipedia, The Free Encyclopedia. "
        f"Pages retrieved on {datetime.now()}\n"
    )
    file.write("Root page: " + page.fullurl + "\n")
```

Class: state-changing.

## 7. Write URL list

Source: `p0210:c01`.

```python
ufname = filename + "_urls.txt"

with open(ufname, "w") as file:
    for url in urls:
        file.write(url + "\n")
```

Class: state-changing.

## 8. Deep Lake scenario switches

Source: `p0211:c01`.

```python
graph_name = "Marketing"

db = "hub://<ORG>/<DATASET>"
vector_store_path = db
dataset_path = db

pop_vs = True
ow = True
```

Meaning from source:
- `pop_vs=True`: insert/populate data;
- `ow=True`: overwrite existing dataset;
- `ow=False`: append instead.

Risk:
- `ow=True` is destructive remote state-changing.

Rollback:
- `[Needs confirmation]`.

The exact reused Deep Lake ingestion code is not repeated in this chapter’s extracted section; this artifact does not reconstruct it from memory.

## 9. Build knowledge graph index

Sources: `p0214:c01–p0215:c01`.

```python
from llama_index.core import KnowledgeGraphIndex
import time

start_time = time.time()

graph_index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    include_embeddings=True,
)

elapsed_time = time.time() - start_time
print(type(graph_index))
```

Source example:
- index creation time: `371.9844 s`.

## 10. Configure query engine

Sources: `p0215:c01–p0216:c01`.

```python
k = 3
temp = 0.1
mt = 1024

graph_query_engine = graph_index.as_query_engine(
    similarity_top_k=k,
    temperature=temp,
    num_output=mt,
)
```

## 11. Export graph as HTML

Source: `p0216:c01`.

```python
from pyvis.network import Network

g = graph_index.get_networkx_graph()

net = Network(
    notebook=True,
    cdn_resources="in_line",
    directed=True,
)

net.from_nx(g)

fgraph = "Knowledge_graph_" + graph_name + ".html"
net.write_html(fgraph)
```

Class: state-changing local file write.

## 12. Query graph

Source: `p0217:c01`.

Core call:

```python
response = graph_query_engine.query(user_input)
```

Source example query:
`What is the primary goal of marketing for the consumer market?`

Verification:
- response text;
- query execution time;
- source nodes.

## 13. SentenceTransformer

Source: `p0218:c01`.

```python
!pip install sentence-transformers==3.0.1
```

```python
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

The Hugging Face token import in the extracted source is malformed and left as `[Source extraction issue]`.

## 14. Semantic similarity

Source: `p0218:c01`.

```python
def calculate_cosine_similarity_with_embeddings(text1, text2):
    embeddings1 = model.encode(text1)
    embeddings2 = model.encode(text2)

    similarity = cosine_similarity(
        [embeddings1],
        [embeddings2],
    )

    return similarity[0][0]
```

## 15. Rerank source nodes

Source: `p0219:c01`.

The source:
- iterates `response.source_nodes`;
- compares each node text to the user query;
- tracks the best semantic score;
- prints the best-ranked text.

Interpretation:
- automated reranking can disagree with the LLM summary/user preference.

## 16. Evaluation arrays

Sources: `p0220:c01–p0222:c01`.

```python
rscores = []
scores = []
```

Per example:
- execute query;
- compute cosine similarity;
- append automated score;
- append human-feedback score.

## 17. Aggregate metrics

Source: `p0222:c01–p0224:c01`.

```python
mean_score = np.mean(scores)
median_score = np.median(scores)
std_deviation = np.std(scores)
variance = np.var(scores)
min_score = np.min(scores)
max_score = np.max(scores)
range_score = max_score - min_score
percentile_25 = np.percentile(scores, 25)
percentile_75 = np.percentile(scores, 75)
iqr = percentile_75 - percentile_25
```

Source example output:
- Mean: 0.68
- Median: 0.71
- Std dev: 0.15
- Variance: 0.02
- Min: 0.45
- Max: 0.90
- Range: 0.46
- Q1: 0.56
- Q3: 0.80
- IQR: 0.24

These are experiment outputs, not thresholds.
