# Commands and tools — глава 2

Only source-confirmed commands/tools from `p0058:c01–p0077:c01` are included.

Secrets, account-specific dataset names and credential paths are replaced with placeholders where practical. Source behavior is not silently corrected.

## Classification

| Command / tool | Class | Effect |
|---|---|---|
| `!pip install beautifulsoup4==4.12.3` | state-changing | changes notebook Python environment |
| `!pip install requests==2.31.0` | state-changing | changes notebook Python environment |
| `drive.mount('/content/drive')` | state-changing | mounts Google Drive into Colab runtime |
| `subprocess.run(curl...)` | state-changing | downloads a file to local runtime |
| `!pip install deeplake==3.9.18` | state-changing | installs Deep Lake |
| `!pip install openai==1.40.3` | state-changing | installs OpenAI package |
| write `/etc/resolv.conf` | state-changing | changes runtime DNS configuration |
| set `OPENAI_API_KEY` / `ACTIVELOOP_TOKEN` | state-changing | changes process environment |
| `requests.get(...)` | workload-generating | performs HTTP requests |
| write `llm.txt` | state-changing | creates/overwrites local prepared dataset file |
| `VectorStore(path=...)` | read / may create | source uses it to load or create vector store |
| OpenAI embeddings API | workload-generating | creates embeddings; may be billable |
| `vector_store.add(...)` | state-changing | writes text/metadata/embeddings to vector dataset |
| `deeplake.load(...)` | read-only | loads dataset handle |
| `vector_store.search(...)` | workload-generating | performs vector retrieval |
| OpenAI chat completion | workload-generating | generates response; may be billable |
| `!pip install sentence-transformers` | state-changing | changes Python environment |
| SentenceTransformer encode | workload-generating | creates local semantic embeddings |

## 1. Data-collection dependencies

Source: `p0058:c01`.

```python
!pip install beautifulsoup4==4.12.3
!pip install requests==2.31.0
```

Effect:
- installs pinned versions in the notebook environment.

Risk:
- dependency/version conflicts;
- chapter explicitly discusses the tradeoff between pinning and upgrading.

Verification:
```python
import requests
from bs4 import BeautifulSoup
```

Rollback: `[Needs confirmation]`.

## 2. Mount Google Drive

Source: `p0059:c01`.

```python
from google.colab import drive
drive.mount('/content/drive')
```

Effect:
- mounts external storage into Colab runtime.

Risk:
- notebook code can access files allowed by the mount.

Verification:
- confirm the mount succeeds before reading credential files.

Rollback: `[Needs confirmation]`.

## 3. Download helper file

Source: `p0059:c01`.

```python
import subprocess

url = "<SOURCE_URL>/commons/grequests.py"
output_file = "grequests.py"

curl_command = [
    "curl",
    "-o", output_file,
    url,
]

subprocess.run(curl_command, check=True)
```

Effect:
- creates/overwrites `grequests.py` in the runtime.

Risk:
- remote content is executed later if imported;
- chapter source does not specify integrity verification.

Verification:
- subprocess exits successfully;
- inspect the downloaded file before import.

Rollback: remove/restore the downloaded file — exact source procedure `[Needs confirmation]`.

### Source extraction warning

`p0060:c01` also shows a shell-string form similar to:

```python
curl_command = f'curl -H -o {filename} {file_url}'
```

The shown `-H` form is incomplete/ambiguous in the extracted source. It is preserved as a source issue and is **not normalized into a runnable command**.

## 4. Deep Lake and OpenAI packages

Source: `p0060:c01`.

```python
!pip install deeplake==3.9.18
!pip install openai==1.40.3
```

The source explicitly places Deep Lake first because of the described Colab/Pillow compatibility situation at the time of writing.

Verification:
```python
import deeplake
import openai
```

Rollback: `[Needs confirmation]`.

## 5. Change runtime DNS configuration

Source: `p0060:c01`.

```python
with open("/etc/resolv.conf", "w") as file:
    file.write("nameserver 8.8.8.8")
```

Class: state-changing.

Effect:
- replaces the runtime resolver configuration with the shown nameserver line.

Risk:
- changes DNS behavior for the runtime;
- can break name resolution or violate environment/network policy;
- source presents it specifically for the Google Colab + Activeloop scenario.

Read-only verification:
```python
with open("/etc/resolv.conf", "r") as file:
    print(file.read())
```

Rollback: `[Needs confirmation]` — the chapter does not preserve or restore the previous resolver configuration.

## 6. Credentials

Source: `p0061:c01`.

Artifact-safe form:

```python
import os
import openai

with open("<OPENAI_KEY_FILE>", "r") as f:
    API_KEY = f.readline().strip()

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("<ACTIVELOOP_TOKEN_FILE>", "r") as f:
    ACTIVELOOP_TOKEN = f.readline().strip()

os.environ["ACTIVELOOP_TOKEN"] = ACTIVELOOP_TOKEN
```

Risk:
- secrets enter process memory/environment;
- do not print, commit or embed them in notebooks/artifacts.

Verification:
```python
assert os.getenv("OPENAI_API_KEY")
assert os.getenv("ACTIVELOOP_TOKEN")
```

Rollback: `[Needs confirmation]`.

## 7. Collect and clean documents

Sources: `p0063:c01–p0064:c01`.

Imports:

```python
import requests
from bs4 import BeautifulSoup
import re
```

Cleaning function:

```python
def clean_text(content):
    content = re.sub(r"\[\d+\]", "", content)
    return content
```

Fetch pattern:

```python
def fetch_and_clean(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find("div", {"class": "mw-parser-output"})
    text = content.get_text(separator=" ", strip=True)
    return clean_text(text)
```

The full source version also removes sections such as References/Bibliography/External links/See also before extracting text.

Write prepared data:

```python
with open("llm.txt", "w", encoding="utf-8") as file:
    for url in urls:
        clean_article_text = fetch_and_clean(url)
        file.write(clean_article_text + "\n")
```

Effect:
- external HTTP workload;
- overwrites/creates `llm.txt`.

Verification:
- read the first 20 lines, as shown later in the chapter.

Rollback: `[Needs confirmation]`.

## 8. Verify and chunk prepared data

Source: `p0066:c01`.

Read-only check:

```python
with open("llm.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines[:20]:
        print(line.strip())
```

Chunking:

```python
with open(source_text, "r") as f:
    text = f.read()

CHUNK_SIZE = 1000
chunked_text = [
    text[i:i + CHUNK_SIZE]
    for i in range(0, len(text), CHUNK_SIZE)
]
```

The source presents `1000` characters as the example chunk size, not as a universal optimum.

## 9. Load/create Deep Lake vector store

Sources: `p0066:c01–p0067:c01`.

```python
from deeplake.core.vectorstore.deeplake_vectorstore import VectorStore
import deeplake.util

vector_store_path = "hub://<ORG>/<DATASET>"

try:
    vector_store = VectorStore(path=vector_store_path)
    print("Vector store exists")
except FileNotFoundError:
    print("Vector store does not exist. You can create it.")
    create_vector_store = True
```

Effect:
- depending on library behavior/source state, loads or creates the vector dataset.

Risk:
- remote dataset/account state can change;
- source does not provide a transaction/rollback boundary.

Verification:
- source checks output and later calls `vector_store.summary()`.

Rollback: `[Needs confirmation]`.

## 10. Embedding function

Source: `p0067:c01`.

```python
def embedding_function(texts, model="text-embedding-3-small"):
    if isinstance(texts, str):
        texts = [texts]
    texts = [t.replace("\n", " ") for t in texts]
    return [
        data.embedding
        for data in openai.embeddings.create(
            input=texts,
            model=model,
        ).data
    ]
```

Class: workload-generating; external API.

Risk:
- API cost/rate limits;
- model-specific behavior.

Verification:
- returned embeddings are consumed by vector-store add/search.

### Source contradiction

The displayed code uses `text-embedding-3-small`. A prose sentence in `p0071:c01` instead names `text-embedding-ada-002` when discussing compatibility. This artifact does not silently reconcile the discrepancy.

## 11. Add chunks to vector store

Source: `p0068:c01`.

```python
vector_store.add(
    text=chunked_text,
    embedding_function=embedding_function,
    embedding_data=chunked_text,
    metadata=[{"source": source_text}] * len(chunked_text),
)
```

Class: state-changing + workload-generating.

Effect:
- generates embeddings;
- writes text, metadata, embeddings and IDs to the dataset.

Verification:
```python
print(vector_store.summary())
```

Rollback: `[Needs confirmation]`.

## 12. Load and inspect dataset

Sources: `p0069:c01–p0070:c01`.

```python
ds = deeplake.load(vector_store_path)
ds_size = ds.size_approx()
```

Conversions shown by source:

```python
ds_size_mb = ds_size / 1048576
ds_size_gb = ds_size / 1073741824
```

Class: read-only.

## 13. Query vector store

Sources: `p0071:c01–p0072:c01`.

```python
search_results = vector_store.search(
    embedding_data=user_prompt,
    embedding_function=embedding_function,
)
```

Read top result:

```python
top_score = search_results["score"][0]
top_text = search_results["text"][0].strip()
top_metadata = search_results["metadata"][0]["source"]
```

Class: workload-generating.

Verification:
- inspect score, text and source metadata.

## 14. Build augmented input

Source: `p0073:c01`.

```python
augmented_input = user_prompt + " " + top_text
```

Class: in-memory transformation.

Verification:
- print/inspect the value before generation.

## 15. GPT-4o generation

Sources: `p0073:c01–p0074:c01`.

```python
from openai import OpenAI
import time

client = OpenAI()
gpt_model = "gpt-4o"
start_time = time.time()
```

The source calls:

```python
response = client.chat.completions.create(
    model=gpt_model,
    messages=[
        {"role": "system", "content": "<SYSTEM_INSTRUCTION>"},
        {"role": "assistant", "content": "<ASSISTANT_INSTRUCTION>"},
        {"role": "user", "content": "<AUGMENTED_PROMPT>"},
    ],
    temperature=0.1,
)
```

Class: workload-generating.

Verification:
- response content;
- measured response time.

Rollback:
- not applicable to a completed external API request.

## 16. Cosine similarity evaluation

Sources: `p0075:c01–p0076:c01`.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return similarity[0][0]
```

Class: workload-generating, local calculation.

## 17. Sentence Transformers evaluation

Source: `p0076:c01–p0077:c01`.

```python
!pip install sentence-transformers
```

```python
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

Risk:
- source warns the package can conflict with previously installed pipeline components;
- model/token behavior can depend on environment.

Rollback: `[Needs confirmation]`.
