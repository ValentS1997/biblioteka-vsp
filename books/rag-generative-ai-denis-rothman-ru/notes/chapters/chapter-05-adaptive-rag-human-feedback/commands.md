# Commands and tools — глава 5

Only source-confirmed operations from `p0140:c01–p0158:c01` are included.

Secrets are replaced with placeholders. Unsupported setup steps remain `[Needs confirmation]`.

## Classification

| Command / tool | Class | Effect |
|---|---|---|
| `!pip install requests==2.32.3` | state-changing | changes Python environment |
| `!pip install beautifulsoup4==4.12.3` | state-changing | changes Python environment |
| `requests.get(...)` | workload-generating | external HTTP request |
| `process_query(...)` | local workload | keyword retrieval + truncation |
| helper `download(...)` | state-changing/external | downloads expert/helper assets |
| `!pip install openai==1.40.3` | state-changing | changes Python environment |
| `drive.mount('/content/drive')` | state-changing | mounts external storage |
| set `OPENAI_API_KEY` | state-changing | changes process environment |
| GPT-4o completion | workload-generating | external generation |
| TF-IDF cosine similarity | local workload | automatic evaluation |
| `input(...)` user rating | interactive | collects human feedback |
| HTML/callback expert UI | interactive/runtime | collects expert feedback |
| write `expert_feedback.txt` | state-changing | overwrites local feedback file |

## 1. Retriever packages

Source: `p0141:c01`.

```python
!pip install requests==2.32.3
!pip install beautifulsoup4==4.12.3
```

Verification:

```python
import requests
from bs4 import BeautifulSoup
```

Rollback: `[Needs confirmation]`.

## 2. Source map

Source: `p0141:c01`.

```python
urls = {
    "prompt engineering": "https://en.wikipedia.org/wiki/Prompt_engineering",
    "artificial intelligence": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "llm": "https://en.wikipedia.org/wiki/Large_language_model",
    "llms": "https://en.wikipedia.org/wiki/Large_language_model",
}
```

Class: configuration/read-only.

## 3. Fetch and clean

Sources: `p0141:c01–p0142:c01`.

```python
def fetch_and_clean(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    content = soup.find("div", {"class": "mw-parser-output"})

    for section_title in [
        "References",
        "Bibliography",
        "External links",
        "See also",
    ]:
        section = content.find("span", {"id": section_title})
        if section:
            for sib in section.parent.find_next_siblings():
                sib.decompose()
            section.parent.decompose()

    paragraphs = content.find_all("p")
    cleaned_text = " ".join(
        paragraph.get_text(separator=" ", strip=True)
        for paragraph in paragraphs
    )

    cleaned_text = re.sub(r"\[\d+\]", "", cleaned_text)
    return cleaned_text
```

Class: external workload.

Risk:
- depends on external page structure/content;
- no source-provided integrity verification.

## 4. Keyword retrieval

Sources: `p0142:c01–p0143:c01`.

```python
def process_query(user_input, num_words):
    user_input = user_input.lower()

    matched_keyword = next(
        (keyword for keyword in urls if keyword in user_input),
        None,
    )

    if matched_keyword:
        cleaned_text = fetch_and_clean(urls[matched_keyword])
        words = cleaned_text.split()
        first_n_words = " ".join(words[:num_words])
        return first_n_words

    return None
```

Class: workload-generating.

Verification:
- matched keyword;
- returned text;
- requested word count.

## 5. Adaptive branch — no RAG

Source: `p0147:c01`.

```python
if ranking >= 1 and ranking < 3:
    text_input = user_input
```

Class: local control logic.

## 6. Adaptive branch — expert feedback

Source: `p0148:c01`.

```python
hf = False

if ranking > 3 and ranking < 5:
    hf = True
```

Source contradiction:
- narrative says ratings 3–4;
- this code activates only rating 4.

Download:

```python
if hf:
    from grequests import download
    directory = "Chapter05"
    filename = "human_feedback.txt"
    download(directory, filename, private_token)
```

`private_token` initialization: `[Needs confirmation]`.

Read expert document:

```python
if hf:
    efile = os.path.exists("human_feedback.txt")

    if efile:
        with open("human_feedback.txt", "r") as file:
            content = file.read().replace("\n", " ").replace("#", "")
        text_input = content
    else:
        hf = False
```

## 7. Adaptive branch — ordinary retrieval

Source: `p0150:c01`.

```python
if ranking >= 5:
    max_words = 100
    rdata = process_query(user_input, max_words)

    if rdata:
        rdata_clean = rdata.replace("\n", " ").replace("#", "")
        rdata_sentences = rdata_clean.split(". ")

    text_input = rdata
```

Class: external/local workload.

The `100` word cap is an example cost-control setting, not a universal limit.

## 8. OpenAI package and credential handling

Sources: `p0151:c01–p0152:c01`.

```python
!pip install openai==1.40.3
```

Mount:

```python
from google.colab import drive
drive.mount("/content/drive")
```

Artifact-safe credential form:

```python
with open("<OPENAI_KEY_FILE>", "r") as f:
    API_KEY = f.readline().strip()

import os
import openai

os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
```

Risk:
- credential enters process memory/environment;
- do not print or commit the secret.

## 9. GPT-4o generation

Source: `p0152:c01`.

```python
from openai import OpenAI
import time

client = OpenAI()
gptmodel = "gpt-4o"
start_time = time.time()
```

Source function calls `client.chat.completions.create(...)` with:
- model `gpt-4o`;
- system/assistant/user messages;
- `temperature=0.1`.

Class: external workload-generating.

Verification:
- returned response;
- formatted output.

## 10. Response time

Sources: `p0153:c01–p0154:c01`.

```python
response_time = time.time() - start_time
print(f"Response Time: {response_time:.2f} seconds")
```

Class: read-only metric.

## 11. TF-IDF cosine similarity

Source: `p0154:c01`.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return similarity[0][0]
```

Source example compares `text_input` with `gpt4_response`.

Interpretation:
- similarity, not factual correctness.

## 12. User rating

Sources: `p0155:c01–p0156:c01`.

Initial example state:

```python
counter = 20
score_history = 30
threshold = 4
```

Rating function accepts integer scores 1–5 and recursively retries invalid input.

Update:

```python
counter += 1
score_history += score
mean_score = round(np.mean(score_history / counter), 2)
```

Class: interactive/local state.

## 13. Expert trigger

Source: `p0157:c01`.

```python
if counter > counter_threshold and score_history <= score_threshold:
    print("Human expert evaluation is required for the feedback loop.")
```

Source contradiction:
- `mean_score` is computed earlier;
- trigger compares accumulated `score_history` with threshold.

Do not silently replace `score_history` with `mean_score`.

## 14. Expert assets and feedback

Sources: `p0157:c01–p0158:c01`.

Downloads:

```python
from grequests import download

download("commons", "thumbs_up.png", private_token)
download("commons", "thumbs_down.png", private_token)
```

`private_token`: `[Needs confirmation]`.

Feedback write:

```python
def save_feedback(feedback):
    with open("/content/expert_feedback.txt", "w") as f:
        f.write(feedback)
    print("Feedback saved successfully.")
```

Class: state-changing.

Effect:
- overwrites `/content/expert_feedback.txt`.

Rollback:
- `[Needs confirmation]`.
