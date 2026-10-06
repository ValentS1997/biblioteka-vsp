# Команды, алгоритмы и инструменты главы 6

Глава 6 не содержит shell-команд или универсального CLI-runbook. Ниже приведены только source-confirmed algorithms, tools, metrics, SQL example и agent actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды установки/запуска FAISS, Elasticsearch, AgentOps или иных библиотек: их CLI syntax в chapter RAG не приведен.

## Retrieval algorithms/tools

| Элемент | Класс | Роль |
|---|---|---|
| TF-IDF | read-only analysis/indexing logic | lexical relevance |
| BM25 | read-only / workload-generating retrieval | term-based retrieval baseline |
| Elasticsearch | workload-generating retrieval service | term-based search example |
| embedding search | workload-generating | semantic retrieval |
| k-NN | workload-generating | exact nearest-neighbor vector search |
| ANN | workload-generating | approximate vector search at scale |
| FAISS | workload-generating | vector search library |
| ScaNN | workload-generating | vector search library |
| Annoy | workload-generating | approximate nearest-neighbor library |
| Hnswlib | workload-generating | HNSW implementation |
| LSH | workload-generating | similarity search via hashing |
| HNSW | workload-generating | graph-based ANN |
| product quantization | state-changing if index persisted | compressed vector representation |
| IVF | state-changing if index persisted | clustered vector index |
| RRF | read-only ranking aggregation | fuse ranked lists |

## Retrieval metrics

Source-confirmed:

- context precision;
- context recall;
- NDCG;
- MAP;
- MRR;
- embedding quality;
- query latency;
- index creation time;
- index size;
- end-to-end RAG output quality.

## Chunking / retrieval modification actions

### Change chunk size / overlap

Класс: `state-changing`, если индекс перестраивается.

Effect: меняет число chunks, boundary preservation, index size и context packing.

Risk: слишком мелкие chunks теряют связность и увеличивают search space; слишком крупные тратят context budget.

Verification: retrieval metrics + end-to-end RAG quality + index size/latency.

Rollback: предыдущий индекс/chunk config — `[Needs confirmation]`.

### Query modification

Класс: `workload-generating`.

Purpose: превратить context-dependent user query в self-contained retrieval query.

Risk: rewrite model может выдумать отсутствующую информацию.

Verification: rewritten query должен сохранять intent и не вводить неподтвержденные entities.

Rollback: `[Not applicable]` для разового rewrite; persisted rewrite logic — `[Needs confirmation]`.

### Contextual retrieval

Класс: `state-changing`, если enriched chunks индексируются.

Purpose: добавить к chunk metadata/context, улучшающий retrieval.

Verification: сравнить retrieval metrics до/после на одном evaluation set.

Rollback: предыдущая index version — `[Needs confirmation]`.

## Source-confirmed SQL example for tabular retrieval

Класс: `read-only` по смыслу приведенного запроса (`SELECT`).

~~~sql
SELECT SUM(units) AS total_units_sold
FROM Sales
WHERE product_name = 'Fruity Fedora'
AND timestamp >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);
~~~

Глава использует его как пример получения контекста из tabular data.

## Multimodal retrieval

Source-confirmed example:

1. generate CLIP embeddings для text + images;
2. store them in vector database;
3. embed the query;
4. retrieve text/images with nearby embeddings.

Класс: indexing — state-changing; query — workload-generating.

## Agent tools/actions

### Tool inventory

Класс: `state-changing` configuration.

Tool types in the chapter:

- knowledge/context tools: text/image retrieval, SQL, web/API access;
- capability tools: calculators/code or specialized processors;
- environment actions: write/change operations.

Effect: расширяет action space агента.

Risk: больше tools усложняют planning; write tools увеличивают consequence of failure.

Verification:

- tool selection accuracy;
- parameter validity;
- independent tool tests;
- goal success.

Rollback: remove/disable tool from inventory — exact implementation `[Needs confirmation]`.

### Read-only vs write actions

Read-only examples: получение информации.

Write-action examples из главы:

- изменение/удаление таблицы через SQL-capable tool;
- отправка email;
- инициирование банковского перевода.

Они приведены как capability/risk examples, а не как команды к выполнению.

## Planning loop

Source-confirmed sequence:

~~~text
1. generate plan
2. reflect / correct
3. execute actions
4. reflect on results
5. re-plan if goal not reached
~~~

Класс: workload-generating.

## Agent diagnostics

Всегда логировать:

- tool name;
- parameters;
- parameter values;
- tool output.

Source example: `lbs_to_kg(lbs=40)`.

## Agent failure metrics

Source-confirmed questions/metrics:

1. доля допустимых сгенерированных планов;
2. среднее число планов до получения допустимого;
3. доля допустимых tool calls;
4. частота invalid tools;
5. частота invalid parameters;
6. частота wrong parameter values;
7. goal completion;
8. time/deadline compliance;
9. average steps;
10. average task cost;
11. action/task latency.

## Agent evaluation tools/benchmarks

Source-confirmed examples:

- Berkeley Function Calling Leaderboard;
- AgentOps evaluation platform;
- TravelPlanner.

CLI commands не приводятся.

## Memory actions

### Short-term → long-term transfer

Класс: `state-changing` memory operation.

Source-confirmed strategies:

- FIFO;
- summarization;
- entity-aware compression;
- reflection-based add/merge/replace.

Effect: освобождает limited context.

Risk: можно удалить раннюю, но критичную информацию.

Verification: long-horizon task success, memory retrieval quality, consistency.

Rollback: конкретный memory-store/versioning mechanism — `[Needs confirmation]`.

## Operational boundary

- Не добавлены CLI/API syntax из внешней документации.
- Write actions не превращены в runnable destructive examples.
- Все algorithms/tools/actions выше подтверждены chapter RAG.
