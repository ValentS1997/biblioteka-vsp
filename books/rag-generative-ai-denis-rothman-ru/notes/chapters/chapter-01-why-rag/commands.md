# Commands and tools — глава 1

Only source-confirmed commands/tools from RAG chunks `p0030:c01–p0049:c01` are included.

Environment-specific paths, credentials and secrets are replaced with placeholders.

## Classification

| Command / tool | Class | Source role |
|---|---|---|
| `!pip install openai==1.40.3` | state-changing | Installs pinned OpenAI package in notebook environment |
| `drive.mount('/content/drive')` | state-changing | Mounts Google Drive in Colab runtime |
| `os.environ['OPENAI_API_KEY'] = <OPENAI_API_KEY>` | state-changing | Sets process environment credential |
| OpenAI `client.chat.completions.create(...)` | workload-generating | Sends generation request to GPT-4o |
| `TfidfVectorizer` | workload-generating | Builds TF-IDF representation |
| `cosine_similarity` | workload-generating | Computes similarity |
| `nltk.download('wordnet')` | state-changing | Downloads WordNet data |
| `spacy.load("en_core_web_sm")` | read-only / workload | Loads local spaCy model |
| keyword/vector/indexed retrieval functions | workload-generating | Search and select best record |

## 1. Install OpenAI package

Source: `p0030:c01`.

```python
!pip install openai==1.40.3
```

Effect:
- changes notebook Python environment;
- pins the package version used in the chapter.

Risk:
- package/dependency changes can affect the runtime;
- the chapter explicitly recommends version pinning to reduce conflicts.

Verification:
```python
import openai
```

Rollback:
`[Needs confirmation]` — the chapter does not provide an uninstall/recovery procedure.

## 2. Mount credential storage

Source: `p0031:c01`.

```python
from google.colab import drive
drive.mount('/content/drive')
```

Effect:
- mounts Google Drive into the Colab runtime.

Risk:
- exposes mounted files to notebook code according to the runtime permissions.

Verification:
- successful mount and ability to open the configured key file.

Rollback:
`[Needs confirmation]`.

## 3. Read API key and set process environment

Source: `p0031:c01`.

The source reads the key from a file. Repository artifact uses placeholders instead of a real path/key:

```python
import os
import openai

with open("<API_KEY_FILE>", "r") as f:
    API_KEY = f.readline().strip()

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
```

Effect:
- loads a credential into process memory/environment.

Risk:
- secret disclosure if printed, committed or exposed by notebook output.

Verification:
```python
assert os.getenv("OPENAI_API_KEY")
```

Rollback:
`[Needs confirmation]`.

## 4. Create GPT-4o client and generation call

Sources: `p0031:c01–p0032:c01`.

```python
from openai import OpenAI

client = OpenAI()
gptmodel = "gpt-4o"
```

Generation method used in the source:

```python
response = client.chat.completions.create(
    model=gptmodel,
    messages=[
        {"role": "system", "content": "<SYSTEM_INSTRUCTION>"},
        {"role": "assistant", "content": "<ASSISTANT_INSTRUCTION>"},
        {"role": "user", "content": "<AUGMENTED_PROMPT>"}
    ],
    temperature=0.1
)
```

Class: workload-generating.

Risk:
- external API request;
- potentially billable according to the provider plan;
- probabilistic outputs can differ between calls.

Verification:
- inspect `response.choices[0].message.content`.

Rollback:
- not applicable to an already completed API call.

## 5. TF-IDF and cosine similarity

Source: `p0036:c01`.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

Core calculation:

```python
def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        use_idf=True,
        norm="l2",
        ngram_range=(1, 2),
        sublinear_tf=True,
        analyzer="word",
    )
    tfidf = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return similarity[0][0]
```

Class: workload-generating.

Verification:
- returned similarity value;
- interpret with caution because the chapter explicitly describes metric limitations.

## 6. Enhanced similarity dependencies

Sources: `p0037:c01–p0038:c01`.

```python
import spacy
import nltk
nltk.download("wordnet")

from nltk.corpus import wordnet
from collections import Counter
import numpy as np

nlp = spacy.load("en_core_web_sm")
```

Notes:
- WordNet is downloaded by the shown command.
- The chapter loads `en_core_web_sm`, but does not provide a source-confirmed installation command for that model.

spaCy model installation: `[Needs confirmation]`.

## 7. Keyword retrieval

Source: `p0039:c01`.

```python
def find_best_match_keyword_search(query, db_records):
    best_score = 0
    best_record = None

    query_keywords = set(query.lower().split())

    for record in db_records:
        record_keywords = set(record.lower().split())
        common_keywords = query_keywords.intersection(record_keywords)
        current_score = len(common_keywords)

        if current_score > best_score:
            best_score = current_score
            best_record = record

    return best_score, best_record
```

Class: workload-generating.

Verification:
- `best_score`;
- selected `best_record`.

## 8. Augment the input

Sources: `p0040:c01–p0041:c01`.

```python
augmented_input = query + ": " + best_matching_record
```

Class: read-only transformation of in-memory values.

Verification:
- inspect `augmented_input` before sending it to the generator.

## 9. Indexed/vector retrieval

Sources: `p0045:c01`, `p0048:c01–p0049:c01`.

```python
def find_best_match(query, vectorizer, tfidf_matrix):
    query_tfidf = vectorizer.transform([query])
    similarities = cosine_similarity(query_tfidf, tfidf_matrix)
    best_index = similarities.argmax()
    best_score = similarities[0, best_index]
    return best_score, best_index
```

Modular strategy selection:

```python
retrieval = RetrievalComponent(method="vector")
retrieval.fit(db_records)
best_matching_record = retrieval.retrieve(query)
```

Allowed source strategies:
- `keyword`
- `vector`
- `indexed`

Verification:
- selected record;
- similarity result where applicable;
- final generated answer after augmentation.
