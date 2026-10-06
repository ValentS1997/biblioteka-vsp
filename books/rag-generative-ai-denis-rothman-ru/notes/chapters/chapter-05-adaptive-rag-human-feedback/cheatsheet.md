# Cheatsheet — глава 5

Provenance: `rag-generative-ai-denis-rothman-ru:p0136:c01–p0160:c01`.

## Symptom / problem framing

Automatic metrics may look good while users still judge the answer as wrong or unhelpful. The chapter uses this gap to motivate adaptive RAG with human feedback.

## Baseline / context

Pipeline components:

| Component | Role |
|---|---|
| Retriever | collect/clean Wikipedia documents; retrieve by keyword |
| Generator | choose augmentation mode; call GPT-4o |
| Evaluation | response time, cosine similarity, user rating, expert feedback |

Adaptive behavior is driven by human evaluation rather than one fixed retrieval strategy.

## Read-only checks

1. Inspect the user query.
2. Inspect matched keyword.
3. Inspect retrieved text before augmentation.
4. Inspect current `ranking`.
5. Inspect current `text_input`.
6. Inspect generated answer.
7. Compute response time.
8. Compute cosine similarity.
9. Inspect user-rating history.
10. Confirm whether expert-feedback conditions are actually satisfied.
11. Inspect expert feedback before feeding it back into retrieval/generation.

## Interpretation

### Rating 1–2

Source intent:
- disable RAG;
- use `user_input` directly.

### Rating 3–4

Source intent:
- use expert feedback / didactic card as augmentation;
- ordinary retrieval is not used.

Source code only enables `hf=True` for `ranking == 4`; this is a preserved contradiction.

### Rating 5

- run keyword retrieval;
- cap retrieved text in the example at `max_words=100`;
- use retrieved text as `text_input`.

### Evaluation

Automatic:
- response time;
- TF-IDF cosine similarity.

Human:
- user rating 1–5;
- expert thumbs up/down + text feedback.

The chapter explicitly distinguishes similarity from correctness: a high cosine score does not prove factual accuracy or usefulness.

## Next action

Source-grounded flow:

1. collect/clean source documents;
2. parse user query;
3. determine current ranking;
4. choose adaptive branch;
5. construct `text_input`;
6. verify `text_input` before generation;
7. call GPT-4o;
8. measure response time;
9. compute cosine similarity;
10. ask user for rating;
11. update feedback statistics;
12. when the configured trigger requires it, request expert evaluation;
13. save expert feedback;
14. feed corrected expert material into future retrieval/augmentation.

## Modifying action

State-changing/source-external operations:
- `pip install`;
- HTTP scraping;
- helper/assets downloads;
- Google Drive mount;
- environment-variable assignment;
- local feedback file writes;
- GPT-4o API calls.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported checks:
- matched keyword exists;
- retrieved text exists or fallback path activates;
- intended adaptive branch matches rating;
- GPT-4o returns a response;
- response time recorded;
- similarity score computed;
- user rating validated as 1–5;
- expert-feedback UI activates only when its trigger fires;
- saved feedback file exists and contains entered feedback.

No source-defined production SLO, accuracy threshold, or universal ranking policy is provided.

## Rollback

Formal rollback is not provided for:
- package changes;
- Drive mount;
- environment-variable changes;
- downloaded helper/assets;
- overwritten `expert_feedback.txt`;
- external API calls.

Rollback: `[Needs confirmation]`.
