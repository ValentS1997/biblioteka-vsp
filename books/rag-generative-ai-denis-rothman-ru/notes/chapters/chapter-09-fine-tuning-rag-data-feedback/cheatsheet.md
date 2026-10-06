# Cheatsheet — глава 9

Provenance: `p0253:c01–p0270:c01`.

## Symptom / problem framing

A growing RAG corpus can become expensive to process, store and retrieve. When part of the corpus is stable for long periods, the chapter considers converting some non-parametric RAG knowledge into model parameters through fine-tuning.

## Baseline / context

| Stage | Source implementation |
|---|---|
| Prepare data | SciQ from Hugging Face |
| Transform | prompt + detailed answer in chat-message structure |
| Persist training data | JSONL-style local file |
| Upload | OpenAI training file |
| Train | GPT-4o-mini fine-tuning job |
| Monitor | OpenAI job list + metrics UI |
| Validate | prompt fine-tuned model with known science question |

## Read-only checks

1. Confirm SciQ loads.
2. Confirm filtered row count.
3. Inspect retained columns.
4. Inspect generated chat-message structure.
5. Re-open the JSONL-style file and verify records.
6. Inspect uploaded OpenAI file object.
7. Inspect fine-tuning job status.
8. Inspect errors before retrying failed jobs.
9. Confirm a non-empty fine-tuned model identifier exists.
10. Inspect generated answer against expected science content.
11. Inspect training loss and trained-token metrics.
12. Inspect usage/cost before repeating training cycles.

## Interpretation

### When fine-tuning is considered

The chapter’s threshold is project-specific and based on:
- RAG data volume;
- processing cost;
- storage/retrieval cost;
- overlap/redundancy;
- resource management burden;
- stability of the data.

### Static vs dynamic

Dynamic data continues to favor RAG because it changes frequently.

Stable/static data may be a candidate for fine-tuning because it can be encoded into model weights and no longer needs to be retrieved on every query.

### Training data structure

Each example contains:
- system instruction;
- user science question;
- assistant answer with explanation.

### Fine-tuning job

Source base model:
- `gpt-4o-mini-2024-07-18`

Source hyperparameters:
- epochs: `auto`;
- batch size: `auto`;
- learning-rate multiplier: `auto`.

### Evaluation

The chapter validates the fine-tuned model with a question already represented in the science dataset and then inspects OpenAI metrics.

Training loss is used as an indicator of training performance, not a universal final quality threshold.

## Next action

1. Decide whether data is stable enough for fine-tuning.
2. Retrieve and inspect source data.
3. Filter/clean rows.
4. Build chat-format examples.
5. Write and inspect training file.
6. Upload training file.
7. Create fine-tuning job.
8. Monitor status/errors.
9. Wait for a usable fine-tuned model identifier.
10. Query the model with representative questions.
11. Compare outputs with expected source answers.
12. Inspect training metrics and usage cost.
13. Adjust data/parameters if output is unsatisfactory.

## Modifying action

State-changing/external operations:
- package installs;
- Drive mount;
- API-key environment assignment;
- local training-file writes;
- OpenAI file upload;
- fine-tuning job creation;
- fine-tuned model generation.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported:
- filtered dataset contains `10481` supported Q/A rows;
- training records use system/user/assistant messages;
- uploaded file status reaches processed;
- fine-tuning job status can be monitored;
- a fine-tuned model ID becomes available;
- generation succeeds only when a model ID exists;
- response resembles the expected science answer;
- training loss and usage metrics are inspectable.

No universal acceptance threshold is defined.

## Rollback

The chapter does not provide formal rollback for:
- local file overwrite;
- uploaded OpenAI training files;
- fine-tuning jobs;
- resulting models;
- billable API operations.

Rollback: `[Needs confirmation]`.
