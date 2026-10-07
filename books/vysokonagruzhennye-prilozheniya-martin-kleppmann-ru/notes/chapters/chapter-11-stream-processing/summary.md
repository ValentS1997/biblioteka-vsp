# Резюме главы 11

Источник: раздел 11.4 «Резюме», `p0551:c01`–`p0553:c01`, PDF 551–553.

Глава рассматривает event streams как unbounded counterpart batch datasets.

## Messaging models

Source compares two broad broker models.

### AMQP/JMS-like broker

Broker delivers messages to consumers, consumers acknowledge successful processing, and acknowledged messages are normally removed.

This model fits asynchronous RPC/task queues when exact historical replay and strict event order are not primary requirements.

### Log-based broker

Events are appended to a partitioned durable log.

Consumers:

- read a partition in order;
- track progress with an offset;
- can replay retained historical events;
- operate independently from other consumers.

Parallelism comes from partitions. If a consumer fails, another consumer can resume from the recorded offset.

This log model resembles replication logs in databases and immutable input files in batch processing.

## Database changes as streams

A database replication log is itself a stream of writes.

CDC exposes this stream to derived systems such as:

- search indexes;
- caches;
- analytics/warehouse systems;
- other databases.

This avoids unreliable ad hoc dual writes by establishing one ordered source of changes.

For a new derived system, source describes the combination:

`consistent snapshot + known change-log position + catch-up`.

Log compaction can retain the latest value per key so a consumer can rebuild database-like current state without storing the full write history forever.

## Event sourcing and derived views

Event sourcing stores application/domain events directly as the authoritative log rather than deriving events after ordinary database mutations.

Current application state becomes a projection of that immutable history.

One event history can produce multiple read-optimized views. This relates to CQRS: write representation and read representation do not need to have the same shape.

The main trade-off is asynchronous propagation: a user may write an event and temporarily not see it in a derived view.

Immutability also has limits. Privacy, legal or operational requirements may force actual deletion, and removing information from all copies/backups is difficult.

## Stream processing

A stream processor can:

1. write data into a store/index/cache;
2. deliver notifications to people;
3. transform one or more input streams into derived output streams.

The third case is the main focus of processing frameworks.

## Time and windows

Unbounded input means aggregation needs explicit time boundaries.

Chapter distinguishes event time from processing time and discusses late/out-of-order events.

Source lists four window types:

- tumbling;
- hopping;
- sliding;
- session.

Choosing a window is part of application semantics, not merely a performance setting.

## Stream joins

Three join classes are identified.

### Stream–stream

Both sides are event streams; matching usually has a time window.

### Stream–table

An event stream is enriched using current table state. A local copy of table state can be maintained by consuming its change stream, avoiding a remote DB request per event.

### Table–table

Both inputs are table change streams. Each update changes a materialized view of the join, producing another change stream.

## Fault tolerance and exactly-once semantics

Stream jobs run indefinitely and emit output continuously, so recovery cannot simply discard the entire output and rerun from the beginning.

Source discusses finer-grained mechanisms:

- microbatches;
- checkpoints;
- transactions;
- idempotent writes;
- deduplication;
- replayable logs.

An idempotent or deduplicated sink can use message offsets/metadata to recognize an update already applied.

Stateful processors must also restore operator state consistently with input progress.

Examples in the source include:

- Flink state snapshots;
- Samza/Kafka Streams state replication through compacted Kafka topics;
- rebuilding state from replayable input.

## Итог

The central stream-processing abstraction is:

`unbounded event log → stateful/replayable transformation → continuously maintained derived state/output`.

Batch and stream processing share partitioning, deterministic transformation and fault-recovery ideas. The major difference is that stream input has no end, which makes time, state, offsets and continuous output part of the correctness model.

На `p0563:c01` начинается заключительная глава 12 «Будущее информационных систем».
