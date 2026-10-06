# Commands and tools — глава 10

Only source-confirmed operations from `p0275:c01–p0304:c01` are included.

Secrets are replaced with placeholders. Reused chapter-6 Pinecone implementation is not reconstructed where chapter 10 does not reprint it.

## Classification

| Operation | Class | Effect |
|---|---|---|
| Drive mount | state-changing | mounts external storage |
| GitHub `curl` download | state-changing/external | downloads files |
| set OpenAI/Pinecone credentials | state-changing | changes runtime secret state |
| `pip install pinecone-client==4.1.1` | state-changing | changes Python environment |
| video display/base64 | local workload | reads/encodes media |
| OpenCV frame extraction | state-changing | writes JPG files |
| OpenAI vision request | workload-generating | external/billable model call |
| CSV append | state-changing | writes comment metadata |
| Drive copy | state-changing | copies files to external storage |
| `rm -f *.mp4/*.jpg/*.csv` | destructive state-changing | deletes session files |
| Pinecone upsert | remote state-changing | writes vectors/metadata |
| Pinecone query | workload-generating/read | vector retrieval |
| GPT-4o Video Expert | workload-generating | rewrites/labels retrieved comment |
| SentenceTransformer similarity | local workload | evaluation |

## 1. Shared imports

Sources: `p0275:c01–p0276:c01`.

```python
from IPython.display import HTML
import base64
from base64 import b64encode
import os
import subprocess
import time
import csv
import uuid
import cv2
from PIL import Image
import pandas as pd
import numpy as np
from io import BytesIO
```

## 2. Download helper

Sources: `p0276:c01–p0277:c01`.

```python
def download(directory, filename):
    base_url = "<SOURCE_REPOSITORY_RAW_BASE>/"
    file_url = f"{base_url}{directory}/{filename}"

    curl_command = (
        f"curl -o {filename} {file_url}"
    )

    subprocess.run(
        curl_command,
        check=True,
        shell=True,
    )
```

Class: external + local state-changing.

Risk:
- shell execution;
- file overwrite;
- no source integrity/hash verification.

## 3. OpenAI credential handling

Source: `p0277:c01`.

Artifact-safe form:

```python
from google.colab import drive

drive.mount("/content/drive")

with open(
    "<OPENAI_API_KEY_FILE>",
    "r",
) as f:
    API_KEY = f.readline().strip()

os.environ["OPENAI_API_KEY"] = API_KEY
```

Source extraction issue:
- p277 contains damaged lines `API_KEY=f.readline()o` and `Nf.close()`.

## 4. Pinecone package / credential

Source: `p0278:c01`.

```python
!pip install pinecone-client==4.1.1
import pinecone
```

Artifact-safe credential read:

```python
with open(
    "<PINECONE_API_KEY_FILE>",
    "r",
) as f:
    PINECONE_API_KEY = f.readline().strip()
```

The chapter states that production should use a method that does not expose the key.

## 5. Display video

Source: `p0282:c01`.

```python
def display_video(file_name):
    with open(file_name, "rb") as file:
        video_data = file.read()

    video_url = b64encode(
        video_data
    ).decode()

    html = f"""
    <video width="640" height="480" controls>
      <source
        src="data:video/mp4;base64,{video_url}"
        type="video/mp4">
    </video>
    """

    return HTML(html)
```

Class: read/local workload.

## 6. Display selected frame

Sources: `p0282:c01–p0284:c01`.

Core sequence:
- `cv2.VideoCapture(file_name)`;
- seek to `frame_number`;
- `cap.read()`;
- BGR→RGB;
- convert to PIL;
- resize;
- encode as JPEG/base64;
- display HTML.

Read-only checks shown by source:

```python
frame_count = int(
    video_capture.get(
        cv2.CAP_PROP_FRAME_COUNT
    )
)

frame_rate = video_capture.get(
    cv2.CAP_PROP_FPS
)

video_duration = (
    frame_count
    / frame_rate
)
```

## 7. download_video source mismatch

Source: `p0282:c01`.

Displayed code:

```python
def download_video(filename):
    directory = "Chapter10/videos"
    filename = file_name
    download(directory, filename)
```

Status: `[Source code mismatch]` because it replaces the function argument with global `file_name`.

## 8. Split video into JPG frames

Source: `p0289:c01`.

```python
def split_file(file_name):
    cap = cv2.VideoCapture(
        file_name
    )

    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imwrite(
            f"frame_{frame_number}.jpg",
            frame,
        )

        frame_number += 1

    cap.release()
```

Class: state-changing local writes.

## 9. Extract model comment

Source: `p0290:c01`.

```python
def generate_comment(response_data):
    try:
        return (
            response_data
            .choices[0]
            .message
            .content
        )
    except (KeyError, AttributeError):
        return "No caption available."
```

## 10. Save comment metadata

Source: `p0290:c01`.

Displayed structure:

```python
def save_comment(
    comment,
    frame_number,
    file_name,
):
    path = f"{file_name}.csv"
    write_header = not os.path.exists(path)

    with open(
        path,
        "a",
        newline="",
    ) as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "ID",
                "FrameNumber",
                "Comment",
                "FileName",
            ])

            unique_id = str(
                uuid.uuid4()
            )

            writer.writerow([
                unique_id,
                frame_number,
                comment,
                file_name,
            ])
```

Source code issue:
- displayed row write is inside `if write_header`, so subsequent comments would not be written as shown.

This artifact does not silently move the row write.

## 11. Comment sampled frames

Source: `p0291:c01`.

Source sampling:

```python
nb = 3
counter = 0
```

For selected frames, source reads the JPG and sends:
- text: `What is happening in this image?`
- image as base64 JPEG
- `max_tokens=150`

Source model string:
- `gpt-4-vision-preview`.

Class: external/billable workload.

## 12. Read comment CSV

Source: `p0292:c01`.

```python
def display_comments(file_name):
    path = f"{file_name}.csv"
    return pd.read_csv(path)
```

Class: read-only.

## 13. Persist comments/frames

Sources: `p0293:c01–p0294:c01`.

Source guards:

```python
save = True
save_frames = True
```

Comment copy:

```python
if save == True:
    cpath = f"{file_name}.csv"

    if os.path.exists(cpath):
        # source then copies to Drive
        pass
```

Frames:
- create target directory;
- iterate JPG files;
- copy them with `shutil.copy(...)`.

Class: state-changing.

## 14. Destructive session cleanup

Source: `p0294:c01`.

```python
delf = False

if delf == True:
    !rm -f *.mp4
    !rm -f *.jpg
    !rm -f *.csv
```

Class: destructive state-changing.

Verification before enabling:
- confirm required artifacts have been persisted elsewhere.

Rollback:
- `[Needs confirmation]`.

## 15. Pinecone ingestion

Sources: `p0295:c01–p0296:c01`.

The chapter states that component 2 reuses chapter-6 logic for:
- processing comment CSV;
- chunking;
- embedding generation;
- Pinecone index creation;
- upload.

The full code is not repeated in these chapter-10 chunks.

Therefore:
- exact commands are not reconstructed here;
- remote index creation/upsert remain classified as state-changing.

## 16. Pinecone query

Sources: `p0296:c01–p0297:c01`.

```python
k = 1

query_text = (
    "Find a basketball player "
    "that is scoring with a dunk."
)

query_embedding = get_embedding(
    query_text,
    model=embedding_model,
)

query_results = index.query(
    vector=query_embedding,
    top_k=k,
    include_metadata=True,
)
```

Expected metadata:
- `text`;
- `frame_number`;
- `file_name`.

Source example:
- score ≈ `0.8667`;
- frame 191;
- `basketball3.mp4`;
- query time `0.57 s`.

## 17. Verify media file before display

Source: `p0299:c01`.

```python
if os.path.exists(file_path):
    file_size = os.path.getsize(
        file_path
    )

    logical_size = 1000

    if file_size > logical_size:
        display(
            Image(
                filename=file_path
            )
        )
```

The 1000-byte value is an example logical check, not a universal validation threshold.

## 18. Video Expert prompt

Sources: `p0301:c01–p0302:c01`.

The source system instruction asks GPT-4o to:
1. identify cognitive dissonances;
2. rewrite the comment logically/engagingly;
3. provide a label.

Retrieved comment becomes:

```python
prompt = text
response_content = (
    get_openai_response(prompt)
)
```

Class: external/billable workload.

## 19. Evaluation

Sources: `p0303:c01–p0304:c01`.

Source uses:
- human feedback comment as expected text;
- extracted rewritten GPT-4o comment;
- SentenceTransformer cosine similarity;
- retrieval score appended separately.

Conceptual code:

```python
text2 = extract_rewritten_comment(
    response_content
)

similarity_score3 = (
    calculate_cosine_similarity_with_embeddings(
        text1,
        text2,
    )
)

scores.append(
    similarity_score3
)

rscores.append(
    score
)
```

Source example:
- one similarity: `0.621`;
- aggregate mean: `0.65`.

These are experiment outputs, not production acceptance criteria.
