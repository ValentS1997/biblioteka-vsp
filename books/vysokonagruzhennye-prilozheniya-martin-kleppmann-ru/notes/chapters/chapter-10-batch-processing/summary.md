# Резюме главы 10

Источник: раздел 10.4 «Резюме», `p0494:c01`–`p0496:c01`, PDF 494–496.

Глава рассматривает batch processing как обработку bounded input dataset с генерацией отдельного derived output.

## Unix philosophy

Разбор начинается с Unix tools:

- небольшие programs делают одну задачу;
- data передаются через standardized streams/files;
- tools легко compose в pipeline;
- input files обычно не изменяются;
- intermediate output можно inspect, save и reuse.

Эта модель дает transparency и experimentability: ошибочную transformation можно исправить и повторить без изменения source input.

## MapReduce and distributed filesystem

MapReduce переносит те же идеи на cluster.

Map function обрабатывает records независимо и генерирует key/value pairs.

Framework:

- partitions data;
- выполняет shuffle;
- сортирует by key;
- направляет одинаковые keys в один reducer;
- retries failed tasks;
- скрывает часть distributed failure mechanics от application code.

HDFS/distributed filesystem становится стандартным interface между jobs: input и final/intermediate output представлены files/directories.

## Partitioning and joins

Глава выделяет несколько join patterns.

### Sort-merge join

Оба inputs map'ятся по join key, затем shuffle/sort co-locates одинаковые keys у reducer.

### Broadcast hash join

Если один input мал, его можно полностью передать каждому worker и держать в local hash table/index while scanning large input.

### Partitioned hash join

Если оба datasets уже partitioned совместимо по join key, join можно выполнить независимо per partition.

Все эти patterns иллюстрируют главный partitioning rule: related data должны оказаться в одном execution location.

## Derived data and reproducibility

Batch outputs часто являются не reports, а новыми data structures — например, search indexes.

Особенно важна separation:

- source input immutable;
- output создается separately;
- failed/incorrect output можно отбросить;
- исправленный job можно rerun.

Это обеспечивает сильную tolerance к code/human errors.

Безопасные retries основаны на предположении, что mapper/reducer callbacks не имеют externally visible side effects кроме generated output.

## MapReduce vs MPP databases

MPP databases оптимизируют parallel analytical SQL и tightly integrated execution.

Hadoop/MapReduce делает ставку на:

- arbitrary files/formats;
- schema-on-read;
- arbitrary application code;
- shared cluster для разных processing models;
- task-level recovery.

MapReduce materializes intermediate state чаще и лучше переносит long-running/failure-prone workloads, но платит за это disk/network I/O.

## Beyond MapReduce

Spark, Tez и Flink рассматривают workflow как единый dataflow/operator graph.

Преимущества:

- не нужно mandatory sort между каждым map/reduce-like stage;
- operators могут начинать работу по мере поступления input;
- intermediate state можно держать in memory/local disk;
- scheduler видит dependencies целиком;
- redundant map/materialization stages можно убрать.

Цена: при потере intermediate state его приходится recompute или восстанавливать из checkpoint.

Spark использует lineage/RDD concept; Flink сохраняет operator state. Deterministic operators особенно важны для корректного recomputation.

## Graph processing

Pregel-style systems применяют iterative vertex-centric processing:

- vertex receives messages;
- updates local state;
- sends messages to other vertices;
- next iteration starts after barrier;
- checkpoints provide fault recovery.

## Declarative interfaces

Higher-level APIs and query optimizers позволяют framework выбирать join algorithm, reorder joins и использовать efficient storage/execution techniques.

По мере этого batch systems становятся похожи на MPP databases, а MPP platforms становятся более programmable.

## Итог

Глава сводит distributed batch processing к двум основным задачам:

1. **Partitioning** — связанные records должны оказаться в одной execution partition.
2. **Fault tolerance** — computation должно быть repeatable после task/node failure.

Ключевая semantics batch job:

`bounded immutable input → retryable transformation → separate derived output`.

На `p0505:c01` глава 11 переходит к unbounded input streams, где job больше не может дождаться «конца input».
