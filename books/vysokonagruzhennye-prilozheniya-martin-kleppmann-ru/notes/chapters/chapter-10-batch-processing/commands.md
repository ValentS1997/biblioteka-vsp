# Source-confirmed commands and tools — глава 10

Включены только команды, примеры и инструменты, явно присутствующие в chapter RAG.

## Unix pipeline: top 5 URLs

Источник: `p0452:c01`, PDF 452.

~~~bash
cat /var/log/nginx/access.log |
  awk '{print $7}' |
  sort |
  uniq -c |
  sort -r -n |
  head -n 5
~~~

Тип: read-only transformation относительно source log.

Эффект:

1. читает access log;
2. извлекает седьмое поле — URL;
3. сортирует URL;
4. считает одинаковые соседние значения;
5. сортирует counts по убыванию;
6. оставляет top 5.

Source example output:

~~~text
4189 /favicon.ico
3631 /2013/05/24/improving-security-of-ssh-private-keys.html
2124 /2012/12/05/schema-evolution-in-avro-protocol-buffers-thrift.html
1369 /
915 /css/typography.css
~~~

Verification: output содержит не более пяти строк и упорядочен по descending numeric count.

Rollback: `[Not applicable]`.

## Exclude CSS URLs

Источник: `p0453:c01`, PDF 453.

~~~bash
awk '$7 !~ /\.css$/ {print $7}'
~~~

Тип: read-only filtering transformation.

Effect: выводит seventh field только для строк, где URL не заканчивается на `.css`.

Verification: output не содержит URLs, оканчивающихся на `.css`.

Rollback: `[Not applicable]`.

## Extract client IP instead of URL

Источник: `p0453:c01`, PDF 453.

~~~bash
awk '{print $1}'
~~~

Тип: read-only projection.

Effect: выводит первое поле access log — client IP в source example.

Verification: структура output соответствует first-field values source log.

Rollback: `[Not applicable]`.

## Source-confirmed Unix tools

Источник: `p0452:c01`–`p0453:c01`.

- `cat`;
- `awk`;
- `sort`;
- `uniq`;
- `head`;
- `sed`;
- `grep`;
- `xargs`.

Глава использует их как composable data-processing primitives.

## MapReduce primitives

Источник: `p0460:c01`–`p0462:c01`.

Conceptual sequence:

~~~text
input records
  -> map(record) => key/value pairs
  -> partition/shuffle/sort by key
  -> reduce(key, values)
  -> output files
~~~

Тип: workload-generating distributed batch-processing model.

Source guarantees/assumptions:

- map records обрабатываются независимо;
- framework собирает одинаковые keys у одного reducer;
- shuffle/sort выполняются framework;
- failed tasks can be retried;
- application logic не должна зависеть от hidden mutable state между records.

Verification:

- records одного key оказываются в одном reducer partition;
- final output соответствует bounded input;
- transient task failure не меняет logical result.

Rollback: вернуть previous job code/config and rerun from immutable input; concrete platform syntax `[Needs confirmation]`.

## Join strategies

Источник: `p0468:c01`, `p0471:c01`, `p0495:c01`.

### Sort-merge join

~~~text
map both inputs by join key
-> shuffle/sort
-> co-locate same key
-> reduce/join
~~~

Тип: workload-generating.

### Broadcast hash join

Условие: один input достаточно мал, чтобы полностью загрузиться в memory/index каждого worker.

~~~text
small input -> local hash table on every mapper
large input -> scan each partition
lookup join key in local hash table
~~~

Тип: workload-generating.

### Partitioned hash join

Условие: inputs partitioned compatible way by same join key/hash/partition count.

Тип: workload-generating.

Verification для всех join strategies: output cardinality/content соответствует source datasets и intended join semantics.

Rollback: previous algorithm/config + rerun — concrete syntax `[Needs confirmation]`.

## Dataflow engines and recovery primitives

Источник: `p0484:c01`–`p0487:c01`.

Source-confirmed systems:

- Spark;
- Tez;
- Flink.

Source-confirmed mechanisms:

- operator DAG/dataflow;
- repartition without mandatory sort where possible;
- broadcast to all join partitions;
- local/in-memory intermediate state;
- recomputation after loss;
- Spark RDD lineage;
- Flink operator state/checkpointing.

Тип: workload-generating / state-management mechanisms.

Verification:

- lost intermediate state is recovered from lineage/checkpoint/source;
- deterministic rerun produces compatible data for downstream operators.

Rollback: platform-specific `[Needs confirmation]`.

## Pregel-style graph processing

Источник: `p0488:c01`–`p0490:c01`.

Conceptual primitives:

~~~text
vertex state
message(vertex_id, payload)
iteration barrier
checkpoint
repeat until termination condition
~~~

Тип: workload-generating iterative batch model.

Verification:

- messages from iteration N are processed in iteration N+1 according to source model;
- failed processing can restart from checkpoint;
- partition placement is transparent to vertex logic.

Rollback: checkpoint/job-specific `[Needs confirmation]`.

## Что не добавлено

- `hdfs dfs` commands;
- Hadoop/YARN administrative CLI;
- Spark submit commands;
- Flink CLI;
- Tez configuration;
- HDFS replication commands;
- scheduler tuning commands.

Concrete operational syntax этих систем отсутствует в использованных chapter chunks.
