# Команды, инструменты и действия главы 8

Глава 8 не содержит shell-команд или универсального CLI-runbook. Ниже приведены только source-confirmed tools, processing methods and operational actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды установки/запуска Faker, deduplication libraries или других tools: CLI syntax в chapter RAG не приведен.

## Data-generation tools

| Tool / method | Class | Role |
|---|---|---|
| Faker | workload-generating | generate structured fake/test data |
| Chance | workload-generating | generate structured fake/test data |
| rule/template generation | workload-generating | create structured synthetic examples |
| perturbation | workload-generating | generate noisy/robustness variants |
| CARLA | workload-generating | simulation example for autonomous driving |
| simulation | workload-generating | generate scenarios/actions without real-world cost/risk |
| AI paraphrasing | workload-generating | augment linguistic variants |
| AI translation | workload-generating | expand languages/code languages |
| self-play | workload-generating | generate interaction/strategy data |
| AI instruction generation | workload-generating | synthesize instruction/response examples |

## Synthetic-data verification

Source-confirmed patterns:

- parser checks;
- linter checks;
- unit tests;
- AI judge / specialized verifier;
- factual-consistency checking;
- anomaly detection;
- heuristic filters;
- back-translation consistency;
- downstream model improvement.

Class: read-only analysis or workload-generating, depending on whether model/tool calls are required.

Important operational pattern from the chapter:

~~~text
generate
→ validate
→ if failed, repair/regenerate
→ keep only examples that pass
~~~

## Back-translation check

Класс: workload-generating.

Source logic:

~~~text
X --translate--> Y --translate back--> X'
compare X with X'
~~~

Large divergence between `X` and `X'` is a signal that translation `Y` may be poor.

## Annotation workflow actions

### Create labeling guidelines

Class: state-changing dataset-process artifact.

Effect: defines what counts as good/bad labels and how scores are distinguished.

Risk: ambiguous guidelines create inconsistent labels.

Verification:

- multiple annotators label same examples;
- measure disagreement;
- review conflicting labels.

Rollback: prior guideline version — `[Needs confirmation]`.

### Human/manual inspection

Class: read-only.

Source emphasizes that tooling does not replace manual data review.

Checks include:

- examples make sense;
- factual correctness;
- labels are plausible;
- strange distributions/outliers;
- annotator-specific patterns.

## Dataset inspection

Source-confirmed distributions:

- token frequencies;
- input lengths;
- output lengths;
- ratings;
- topic/language distributions;
- source;
- time;
- annotator.

Class: read-only.

## Deduplication methods

| Method | Class | Notes |
|---|---|---|
| exact comparison | read-only analysis | exact duplicates |
| n-gram overlap | read-only analysis | lexical near-duplicates |
| fuzzy matching | read-only analysis | approximate duplicate detection |
| semantic similarity | workload-generating/read-only analysis | embedding/similarity-based |
| pairwise comparison | read-only/workload-generating | expensive at large scale |
| hashing / blocking | read-only processing | compare within buckets |
| MinHash | read-only processing | hashing-based dedup |
| Bloom filter | read-only processing | hashing/filter-based |
| dimensionality reduction + comparison | workload-generating | scale similarity search |

Source-confirmed dedup libraries:

- dupeGuru;
- Dedupe;
- datasketch;
- TextDistance;
- TheFuzz;
- deduplicate-text-datasets;
- lazyNLP.

No CLI syntax is provided.

## Cleaning and filtering

Class: state-changing when persisted.

Source-confirmed actions:

- remove unnecessary HTML/Markdown/formatting tokens;
- remove PII/disallowed fields;
- remove confidential/copyrighted/toxic data when policies require;
- filter low-quality examples;
- use active learning / importance sampling when only a subset can be afforded;
- inspect removed examples manually.

Effect: changes training distribution.

Risk: excessive filtering may remove useful rare cases.

Verification:

- sample removed records;
- compare distributions;
- run downstream evaluation.

Rollback: previous immutable dataset snapshot — `[Needs confirmation]`.

## Formatting

Class: state-changing.

Source-confirmed rule: serialize data in the format expected by target tokenizer/chat template.

For supervised finetuning, common source pattern:

~~~text
instruction → answer
~~~

Instructions can be decomposed into system/user prompts when required.

Risk: mismatched train/inference format can cause unexpected behavior.

Verification:

- inspect serialized examples;
- confirm tokenizer/chat-template compatibility;
- use matching inference prompts.

Rollback: previous formatted dataset version — `[Needs confirmation]`.

## Processing-pipeline safety

Source-confirmed operational rules:

1. Order processing steps to minimize time/compute.
2. Run trial jobs before processing the full dataset.
3. Do not mutate source data in place.
4. Keep copies of original data.

Class:
- trial run: workload-generating;
- persisted processing: state-changing.

## Synthetic-data limits

Source-confirmed risks:

- low-quality generated data;
- shallow imitation;
- recursive model collapse;
- bias amplification;
- hidden data provenance;
- licensing restrictions on teacher-model outputs.

## Distillation

Class: workload-generating / state-changing training workflow.

Source concept:

~~~text
teacher model
→ generate training outputs
→ train student model
→ evaluate whether student preserves useful behavior
~~~

Not every model can legally/contractually serve as teacher; license terms may prohibit using outputs to train other models.

## Operational boundary

- No external CLI/API syntax added.
- No tool versions are updated beyond chapter content.
- Exact compliance rules are application/jurisdiction specific and remain outside chapter-level inference.
- All listed tools/actions are source-confirmed by chapter RAG.
