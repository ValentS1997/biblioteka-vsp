# Глава 8. Создание динамических RAG с помощью Chroma и Hugging Face Llama

Status: `RAG_GROUNDED`

## Scope

- Book ID: `rag-generative-ai-denis-rothman-ru`
- RAG chunk range: `p0227:c01–p0252:c01`
- PDF pages: `227–252`
- Printed page range: `[Needs confirmation]`
- Next chapter starts at PDF page `253`: «Улучшение моделей ИИ: тонкая настройка данных RAG и обратная связь»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

Source policy: strict `rag_only`. No external web/model-memory fallback used.

## Chapter map

1. Dynamic RAG concept:
   - short-lived, meeting-specific data;
   - temporary Chroma collection;
   - avoid long-term storage when data quickly loses relevance.
2. Environment:
   - Hugging Face token;
   - `datasets`, `transformers`, `accelerate`;
   - Llama 2 chat model;
   - Chroma;
   - ONNX Runtime;
   - spaCy model.
3. SciQ data preparation:
   - load `sciq`;
   - keep non-empty `support` and `correct_answer`;
   - drop distractors;
   - build `completion = correct_answer + support`;
   - 10,481 prepared rows.
4. Chroma:
   - ephemeral local client;
   - create/check collection;
   - add documents and metadata;
   - default embedding path via Chroma/ONNX.
5. Retrieval:
   - query all questions;
   - `n_results=1`;
   - inspect retrieved document.
6. Evaluation:
   - spaCy `en_core_web_md`;
   - cosine-style vector similarity;
   - threshold example `>0.7`;
   - aggregate accuracy.
7. Meeting-time RAG:
   - query Chroma with a prompt;
   - use retrieved document to augment Llama input;
   - generate a short summary.
8. Lifecycle:
   - optional collection deletion;
   - measure session preparation time.
9. Explicit summary and 8 review questions.

## Main principle

Dynamic RAG is treated as a time-bounded data system: prepare a fresh, relevant collection shortly before a meeting, validate it, use it during the event, and discard it afterward if long-term retention is unnecessary. The source optimizes for speed, low cost and operational simplicity rather than persistence.

## Operational boundaries

- Hugging Face token is a secret-bearing runtime input.
- Google Drive mount changes runtime state.
- Package installation changes the notebook environment.
- Dataset/model downloads are external workloads and local cache writes.
- Chroma collection creation/addition changes local runtime state.
- Chroma collection deletion is destructive local state-changing.
- Llama generation can be GPU/resource intensive.
- Source recommends GPU but permits CPU at slower speed.
- Similarity threshold `0.7` is an example criterion, not a universal acceptance threshold.
- The source repeatedly states that human supervision remains necessary as prompts drift from the original dataset.
- No persistence/backup rollback scheme is defined because the intended Chroma collection is temporary.

## Source issues

### Transformers import typo

`p0232:c01` shows:

`import tranformers`

while the following code calls `transformers.pipeline(...)`.

Status: `[Source code issue]`.

### Session-time variable mismatch

`p0250:c01` computes:

`end_time = time.time() - session_start_time`

but then prints:

`response_time`

for “Session preparation time”.

Status: `[Source code mismatch]`.

### Collection deletion is commented

`p0250:c01` shows:

`#client.delete_collection(collection_name)`

The chapter documents manual deletion, but the displayed line is commented and therefore does not execute as shown.

Status: `[Source execution-state note]`.

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [summary.md](./summary.md)
- [review-questions.md](./review-questions.md)
- [review-answers.md](./review-answers.md)

## Provenance

- Concept / architecture: `p0227:c01–p0230:c01`
- Environment: `p0231:c01–p0235:c01`
- SciQ / Chroma preparation: `p0236:c01–p0240:c01`
- Retrieval / evaluation: `p0241:c01–p0245:c01`
- Llama generation / lifecycle: `p0246:c01–p0250:c01`
- Summary / questions: `p0251:c01–p0252:c01`
