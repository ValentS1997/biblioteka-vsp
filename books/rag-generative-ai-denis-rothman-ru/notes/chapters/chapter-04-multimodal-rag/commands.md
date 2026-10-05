# Commands and tools — глава 4

Only source-confirmed operations from `p0115:c01–p0133:c01` are included.

No real secrets are stored. Account-specific paths are replaced when appropriate.

## Classification

| Command / tool | Class | Effect |
|---|---|---|
| `deeplake.load(...)` | read-only | loads text or VisDrone dataset |
| `VectorStoreIndex.from_documents(...)` | workload/runtime state | builds in-memory index |
| `.as_query_engine(...)` | runtime configuration | creates query engine |
| `.query(...)` | workload-generating | retrieval + LLM synthesis |
| `ds.summary()` | read-only | displays dataset structure |
| `ds.visualize()` | read-only | opens visualization |
| DataFrame creation | local workload | materializes dataset metadata/content in runtime |
| OpenCV/PIL display | local workload | renders image |
| save `boxed_image.jpg` | state-changing | writes local file |
| `!rm /content/boxed_image.jpg` | destructive/state-changing | deletes local file |
| GPTVectorStoreIndex over label documents | runtime workload | builds in-memory index |
| base64 encoding | local transformation | converts image bytes to text representation |
| GPT-4o image request | workload-generating | external multimodal API call |
| SentenceTransformer similarity | workload-generating | local embedding/evaluation |

## 1. Load text dataset

Source: `p0115:c01`.

```python
import deeplake

dataset_path_llm = "hub://<ORG>/<TEXT_DATASET>"
ds_llm = deeplake.load(dataset_path_llm)
```

Class: read-only.

Verification:
- dataset loads;
- inspect tensors.

## 2. Build text query engine

Source: `p0116:c01`.

```python
from llama_index.core import VectorStoreIndex

vector_store_index_llm = VectorStoreIndex.from_documents(documents_llm)

vector_query_engine_llm = vector_store_index_llm.as_query_engine(
    similarity_top_k=2,
    temperature=0.1,
    num_output=1024,
)
```

Class: runtime workload/configuration.

Verification:
- query engine object created.

## 3. Query text module

Sources: `p0116:c01–p0117:c01`.

```python
user_input = "How do drones identify a truck?"
```

```python
import time
import textwrap

start_time = time.time()
llm_response = vector_query_engine_llm.query(user_input)
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Query execution time: {elapsed_time:.4f} seconds")
print(textwrap.fill(str(llm_response), 100))
```

Class: workload-generating.

## 4. Load VisDrone

Source: `p0117:c01`.

```python
import deeplake

dataset_path = "hub://activeloop/visdrone-det-train"
ds = deeplake.load(dataset_path)
```

Source output explicitly states read-only mode.

Verification:

```python
ds.summary()
ds.visualize()
```

## 5. Materialize VisDrone into a DataFrame

Sources: `p0118:c01–p0119:c01`.

```python
import pandas as pd

df = pd.DataFrame(columns=["image", "boxes", "labels"])

for i, sample in enumerate(ds):
    df.loc[i, "image"] = sample.images.tobytes()

    boxes_list = sample.boxes.numpy(aslist=True)
    df.loc[i, "boxes"] = [box.tolist() for box in boxes_list]

    label_data = sample.labels.data()
    df.loc[i, "labels"] = label_data["text"]
```

Class: local workload/runtime memory use.

## 6. Inspect labels / image

Sources: `p0119:c01–p0121:c01`.

Class names:

```python
labels_list = ds.labels.info["class_names"]
```

Select image:

```python
ind = 0
image = ds.images[ind].numpy()
```

Display:

```python
from IPython.display import display
from PIL import Image
import cv2

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img = Image.fromarray(image_rgb)
display(img)
```

Read labels:

```python
labels = ds.labels[ind].data()
```

Class: read-only/local workload.

## 7. Draw and save bounding boxes

Source: `p0123:c01`.

Core behavior:

```python
import io
from PIL import ImageDraw

def display_image_with_bboxes(image_data, bboxes, labels, label_name, ind=0):
    image_bytes = io.BytesIO(image_data)
    img = Image.open(image_bytes)

    class_names = ds.labels[ind].info["class_names"]
    label_index = class_names.index(label_name)
    relevant_indices = np.where(labels == label_index)[0]

    draw = ImageDraw.Draw(img)

    for idx, box in enumerate(bboxes):
        if idx in relevant_indices:
            x1, y1, w, h = box
            x2, y2 = x1 + w, y1 + h
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1), label_name, fill="red")

    save_path = "boxed_image.jpg"
    img.save(save_path)
    display(img)
```

Class: state-changing.

Effect:
- writes `boxed_image.jpg`.

Verification:
- inspect displayed/saved image.

Rollback:
- source later deletes the file, but does not restore a previous version.

## 8. Build label-document index

Sources: `p0125:c01–p0126:c01`.

```python
df["doc_id"] = df.index.astype(str)

documents = []

for _, row in df.iterrows():
    text_labels = row["labels"]
    text = " ".join(text_labels)
    document = Document(
        text=text,
        doc_id=row["doc_id"],
    )
    documents.append(document)
```

Source then uses:

```python
from llama_index.core import GPTVectorStoreIndex

vector_store_index = GPTVectorStoreIndex.from_documents(documents)
```

Class: runtime workload.

Note:
- source uses `GPTVectorStoreIndex` here, while earlier pages use `VectorStoreIndex`;
- this artifact preserves source terminology without normalizing aliases/version behavior.

## 9. Query multimodal label index

Source: `p0126:c01`.

```python
vector_query_engine = vector_store_index.as_query_engine(
    similarity_top_k=1,
    temperature=0.1,
    num_output=1024,
)

response = vector_query_engine.query(user_input)
```

Class: workload-generating.

Verification:
- response text;
- query execution time;
- `response.source_nodes`.

## 10. Extract unique words from source node

Sources: `p0126:c01–p0127:c01`.

```python
from itertools import groupby

def get_unique_words(text):
    text = text.lower().strip()
    words = text.split()
    unique_words = [
        word
        for word, _ in groupby(sorted(words))
    ]
    return unique_words
```

Then:
- iterate `response.source_nodes`;
- get node text;
- derive `unique_words`.

Class: local transformation.

## 11. Delete previous image

Source: `p0127:c01`.

```bash
!rm /content/boxed_image.jpg
```

Class: destructive/state-changing.

Effect:
- removes prior output image.

Risk:
- irreversible unless another copy exists.

Verification:
- source proceeds to regenerate/display a new image.

Rollback:
- `[Needs confirmation]`.

## 12. Resolve source image and display boxes

Sources: `p0127:c01–p0128:c01`.

The source function:
- iterates source nodes;
- maps node/document ID back to DataFrame row;
- reads corresponding image/labels/boxes from VisDrone;
- uses first unique word as target class;
- calls `display_image_with_bboxes(...)`.

Class: read/workload + local file write through display function.

## 13. Final multimodal output

Source: `p0129:c01`.

```python
print(user_input)
print(textwrap.fill(str(llm_response), 100))

image_path = "/content/boxed_image.jpg"
display_source_image(image_path)
```

Output combines:
- user request;
- LLM response;
- image.

## 14. Text evaluation

Source: `p0130:c01`.

```python
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_cosine_similarity_with_embeddings(text1, text2):
    embeddings1 = model.encode(text1)
    embeddings2 = model.encode(text2)
    similarity = cosine_similarity([embeddings1], [embeddings2])
    return similarity[0][0]
```

Then compare:
- `user_input`;
- `llm_response`.

Class: local workload.

## 15. Encode image for GPT-4o

Source: `p0131:c01`.

```python
import base64

IMAGE_PATH = "/content/boxed_image.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)
```

Class: read-only/local transformation.

## 16. GPT-4o image analysis

Source: `p0132:c01`.

```python
from openai import OpenAI

client = OpenAI(api_key=openai.api_key)
MODEL = "gpt-4o"
```

The source sends:
- system instruction containing target word;
- text prompt;
- image URL with embedded base64 image;
- `temperature=0.0`.

Class: external workload-generating.

### Source MIME mismatch

Source file is named `boxed_image.jpg`, but request embeds:

`data:image/png;base64,...`

Status: `[Source contradiction]`.

## 17. Multimodal similarity / combined score

Source: `p0133:c01`.

```python
resp = u_word + "s"

multimodal_similarity_score = (
    calculate_cosine_similarity_with_embeddings(
        resp,
        str(response_image),
    )
)
```

Combined score:

```python
score = (
    llm_similarity_score
    + multimodal_similarity_score
) / 2
```

Interpretation:
- comparative experiment only;
- source itself says image relevance remains difficult to assess.
