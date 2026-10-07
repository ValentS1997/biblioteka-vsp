# Шпаргалка главы 10 — batch processing

## Symptom / problem framing

Проблема главы: нужно воспроизводимо обработать большой bounded dataset на одном или многих nodes так, чтобы failures, retries и code changes не повреждали source data и не превращали workflow в набор необратимых side effects.

Негативные сигналы:

- batch job модифицирует source data in place;
- retry может повторно выполнить внешний side effect;
- каждый stage materializes huge intermediate dataset без необходимости;
- join strategy не учитывает relative sizes/partitioning inputs;
- один reducer/partition становится bottleneck из-за skew;
- recovery требует полного manual restart и неизвестно, какие outputs валидны;
- operator недетерминирован, но framework рассчитывает lost partitions;
- workflow смешивает transport, storage и transformation logic;
- coordination between jobs зависит от ad hoc paths и ручного запуска.

## Baseline / context

### Unix model

- small programs;
- text/record streams;
- `stdin` → transform → `stdout`;
- pipelines compose independent tools;
- input обычно immutable;
- intermediate output можно inspect/save/reuse.

### MapReduce model

1. read bounded input records;
2. map → emit key/value;
3. partition + shuffle + sort by key;
4. reduce grouped values;
5. write durable output.

Framework берет на себя:

- partitioning;
- network movement;
- scheduling;
- retries;
- failed-task output discard.

### HDFS

- distributed shared-nothing filesystem;
- file blocks stored across nodes;
- metadata tracked centrally by NameNode;
- scheduler может run computation close to data.

### Dataflow engines

Spark/Tez/Flink:

- моделируют whole workflow as operators/DAG;
- pipeline intermediate data;
- avoid mandatory sort/materialization where not needed;
- recompute lost state or restore checkpoints;
- benefit from deterministic transformations.

## Read-only checks

1. Зафиксировать bounded input snapshot/files.
2. Проверить, изменяется ли input job'ом.
3. Зафиксировать stage DAG и materialization points.
4. Для каждого operator проверить external side effects.
5. Проверить determinism при одинаковом input.
6. Измерить input/output/intermediate sizes.
7. Измерить partition/key skew.
8. Для join определить:
   - размеры обоих inputs;
   - join key;
   - existing partitioning;
   - необходимость sort.
9. Проверить retry behavior при failure отдельной task/node.
10. Проверить, что failed/speculative task output не становится одновременно visible.
11. Проверить data locality/network shuffle volume.
12. Проверить stage barriers и idle time stragglers.
13. Для Spark/Flink/Tez определить recovery source: lineage, previous intermediate state или checkpoint.
14. Проверить final output publication/selection mechanism.
15. Сравнить job result с предыдущим known-good run.

## Interpretation

- Input immutable, output separate → job легко rerun/rollback.
- Failure одной map/reduce task лечится retry без corruption → framework abstraction работает.
- Small side input целиком помещается в memory каждого worker → broadcast hash join candidate.
- Both inputs partitioned одинаково → partitioned hash join candidate.
- Need group/sort all records by key → sort-merge/shuffle path.
- Каждый intermediate stage записывается в replicated HDFS → высокая recoverability, но большой I/O cost.
- Intermediate state local/in-memory + deterministic lineage → faster dataflow engine with recomputation trade-off.
- Rerun дает разные derived output при одном input → investigate nondeterminism.
- Один key концентрирует большую часть shuffle → data skew/hot reducer.
- Job пишет directly во внешнюю transactional system → safe retry assumption нарушена.

## Next action

1. Зафиксировать immutable input и expected output contract.
2. Нарисовать DAG stages/operators.
3. Измерить sizes, skew, shuffle и materialization.
4. Выбрать минимальную optimization hypothesis:
   - join strategy;
   - partitioning;
   - remove unnecessary materialization/sort;
   - make operator deterministic.
5. Выполнить controlled run.
6. Сравнить result + throughput + recovery behavior.
7. Оставить изменение только при acceptance criteria.

## Modifying action

Source-confirmed classes of changes:

- заменить monolithic program на composable pipeline;
- изменить mapper/reducer logic;
- изменить reducer partitioning/number;
- использовать sort-merge, broadcast hash или partitioned hash join;
- materialize/reuse derived dataset;
- перейти от chained MapReduce jobs к Spark/Tez/Flink-style dataflow;
- сделать operator deterministic;
- materialize expensive intermediate state вместо recomputation;
- использовать higher-level declarative interface/query optimizer.

Concrete cluster/vendor CLI syntax глава универсально не задает.

## Verification / acceptance checks

### Correctness

- одинаковый bounded input дает ожидаемый logical output;
- rerun после transient failure не создает duplicate/corrupted result;
- failed task output не публикуется как final;
- join output соответствует expected cardinality/content.

### Recoverability

- worker/task failure восстанавливается retry/recomputation/checkpoint;
- source input остается unchanged;
- known-good output можно вернуть без reverse mutation source data.

### Performance

- no uncontrolled partition skew;
- network shuffle/materialization соответствуют выбранному algorithm;
- stragglers не определяют disproportionate runtime;
- throughput улучшился без нарушения correctness.

## Rollback

- Batch code change: вернуть previous code version и rerun from immutable input.
- Derived output: вернуть consumer на previous known-good output dataset, если publication mechanism это позволяет; concrete switch syntax `[Needs confirmation]`.
- Join/partitioning strategy: вернуть previous job configuration and rerun.
- Read-only measurements: `[Not applicable]`.

## Operational loop

`immutable input → inspect DAG/data distribution → controlled transformation → validate derived output → publish/rollback`.
