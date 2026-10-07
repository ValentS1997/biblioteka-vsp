# Шпаргалка: глава 11 — Событийно-ориентированная пакетная обработка

## Symptom / problem framing

One task queue is insufficient when batch processing:
- has several transformations;
- branches into several outputs;
- filters/reroutes items;
- later recombines streams.

~~~text
queue → event → queue → event → queue
~~~

## Baseline / context

System becomes a DAG of batch stages.

Core patterns:

| Pattern | Stream effect |
|---|---|
| Copier | 1 → many identical streams |
| Filter | keep matching subset |
| Splitter | route into different subsets |
| Sharder | partition across equivalent shards |
| Merger | many → 1 combined stream |

## Read-only checks

1. Is the full DAG documented?
2. Which stages duplicate work?
3. Which predicates discard work?
4. Can one item go to multiple Splitter branches?
5. What sharding key/function is used?
6. How does routing change after shard failure?
7. Does Merger require completeness or only stream union?
8. How is data transported between stages?
9. Are topics durable?
10. How are replication factor and partitions sized?
11. What happens when one downstream branch is slow/unavailable?

## Interpretation

### Copier

~~~text
item
→ all output branches
~~~

### Filter

~~~text
item
→ predicate
→ keep or drop
~~~

### Splitter

~~~text
item
→ routing criteria
→ one or more selected branches
~~~

### Sharder

~~~text
item
→ sharding function
→ one healthy shard
~~~

### Merger

~~~text
several sources
→ one combined source
~~~

Merger does not itself guarantee all parallel work is complete.

## Next action

1. Draw the DAG.
2. Label each edge with data/event semantics.
3. Classify each fan-out/fan-in operation.
4. Define filter/split/shard rules.
5. Define failure behavior per branch/shard.
6. Select durable transport.
7. Map pipeline outputs to topics.
8. Measure per-topic/per-stage backlog.
9. Verify end-to-end event flow.
10. Keep stage ownership and observability explicit.

## Modifying action

Source-supported modifications:
- Helm initialization/repository setup;
- Kafka installation;
- topic creation;
- publishing test messages;
- consuming test messages.

Exact inventory: `commands.md`.

Risk:
- cluster state changes;
- source commands target historical toolchain;
- malformed topic-creation loop must not be run as-is.

## Verification / acceptance checks

Verify:
- Copier sends item to every intended branch;
- Filter passes only matching items;
- Splitter routes to correct branch(es);
- Sharder excludes failed shards and continues with healthy ones;
- Merger exposes inputs as one stream;
- Kafka topic exists before publish;
- produced message can be consumed from intended topic.

Exact modern diagnostic commands: `[Needs confirmation]`.

## Rollback

Chapter provides no complete rollback workflow.

- Kafka deployment rollback: `[Needs confirmation]`;
- topic rollback/deletion: `[Needs confirmation]`;
- pipeline topology rollback: application-specific;
- shard remapping rollback: `[Needs confirmation]`.

Do not infer delete/uninstall commands.
