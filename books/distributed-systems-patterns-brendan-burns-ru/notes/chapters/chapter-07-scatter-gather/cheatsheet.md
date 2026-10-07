# Шпаргалка: глава 7 — Scatter/Gather

## Symptom / problem framing

Один запрос можно разбить на независимые части и выполнить параллельно.

## Baseline / context

Root распределяет работу между leaf nodes и затем объединяет partial results.

## Read-only checks

- проверить способ декомпозиции;
- проверить aggregation semantics;
- измерить fan-out overhead и tail latency;
- проверить поведение при недоступности leaf/shard.

## Interpretation

Больше parallelism уменьшает полезную работу на node, но увеличивает coordination overhead и вероятность straggler.

## Next action

Измерить end-to-end latency при нескольких вариантах fan-out и выбрать минимальную достаточную степень параллелизма.

## Modifying action

[Not applicable] — глава не содержит explicit CLI/config modification sequence.

## Verification / acceptance checks

Проверить полноту результата, корректность aggregation и доступность replicated shards.

## Rollback

[Needs confirmation] — source rollback procedure отсутствует.
