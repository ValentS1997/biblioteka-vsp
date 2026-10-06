# Глава 9. Улучшение моделей ИИ: тонкая настройка данных RAG и обратная связь

Status: `RAG_GROUNDED`

## Scope

- Book ID: `rag-generative-ai-denis-rothman-ru`
- RAG chunk range: `p0253:c01–p0270:c01`
- PDF pages: `253–270`
- Printed page range: `[Needs confirmation]`
- Next chapter starts at PDF page `271`: «RAG для создания стоковых видео с помощью Pinecone и OpenAI»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

Source policy: strict `rag_only`. No external web/model-memory fallback used.

## Chapter map

1. Fine-tuning threshold:
   - static RAG data can become expensive to store/retrieve;
   - some stable data can be moved from non-parametric RAG storage into model parameters.
2. RAG ecosystem components:
   - D1/D2: download and prepare SciQ;
   - E2: human feedback as a quality signal;
   - T2: fine-tune GPT-4o-mini;
   - G3/G4: prompt engineering and generation;
   - E1: metrics.
3. Environment:
   - OpenAI API key;
   - `openai==1.42.0`;
   - `jsonlines==4.0.0`;
   - `datasets==2.20.0`.
4. Dataset preparation:
   - load SciQ train split;
   - filter non-empty `support` and `correct_answer`;
   - drop distractors;
   - build prompt/answer examples.
5. Fine-tuning dataset:
   - chat-format messages;
   - system/user/assistant roles;
   - JSONL-style write.
6. OpenAI fine-tuning:
   - upload training file;
   - create fine-tuning job;
   - base model `gpt-4o-mini-2024-07-18`;
   - auto epochs/batch/LR multiplier.
7. Monitoring:
   - list jobs;
   - status/error/training file/fine-tuned model;
   - inspect latest usable model.
8. Generation:
   - query fine-tuned model;
   - `temperature=0.0`;
   - inspect answer against source dataset.
9. Metrics / cost:
   - status;
   - trained tokens;
   - epochs;
   - batch size;
   - LR multiplier;
   - seed;
   - training loss;
   - usage/cost UI.
10. Explicit summary and 10 review questions.

## Main principle

The chapter distinguishes dynamic data from stable/static RAG data. When static RAG content becomes expensive or cumbersome to process, store and retrieve, fine-tuning can move some of that knowledge into model parameters. The source does not claim that all RAG data should be fine-tuned; the decision is project-specific and depends on data stability, volume, retrieval overhead and cost.

## Operational boundaries

- OpenAI API key is a secret-bearing runtime input.
- Package installation changes notebook state.
- JSON/JSONL dataset creation writes local files.
- OpenAI file upload creates remote state.
- Fine-tuning job creation is remote state-changing and billable.
- Fine-tuned model generation is an external/billable workload.
- Training metrics are observational; the source does not define universal production thresholds.
- Static data still may require later updates; “static” is treated as long-lived/stable, not immutable forever.
- Human feedback is framed as important to data quality, especially for scientific question/answer material.

## Source issues

### Malformed Colab import

`p0256:c01` extracts:

`from google.colab import`
`drive drive.mount('/content/drive')`

Status: `[Source extraction issue]`.

### DataFrame variable mismatch

`p0258:c01` creates `df_view = pd.DataFrame(filtered_dataset)`, then shows:

`df_view = df.drop(columns=columns_to_drop)`

Status: `[Source code mismatch]`.

### JSON vs JSONL naming

The chapter says the training data is prepared in JSONL format and writes with `jsonlines.open(...)`, but the filename is:

`QA_prompts_and_completions.json`

Status: `[Source format/naming mismatch]`.

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

- Concept / architecture: `p0253:c01–p0256:c01`
- Environment / dataset prep: `p0256:c01–p0259:c01`
- Fine-tuning / monitoring: `p0260:c01–p0264:c01`
- Generation / metrics: `p0264:c01–p0269:c01`
- Questions: `p0270:c01`
