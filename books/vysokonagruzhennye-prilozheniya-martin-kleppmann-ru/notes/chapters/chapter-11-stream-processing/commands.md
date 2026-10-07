# Source-confirmed APIs, mechanisms and tools — глава 11

Глава в основном концептуальная. Универсальных shell/admin commands она не дает. Ниже только source-confirmed mechanisms, APIs, protocols и named tools.

## Consumer offset in a log-based broker

Источник: `p0516:c01`–`p0518:c01`, PDF 516–518.

Conceptual model:

~~~text
partition log:
offset 0, 1, 2, ... N

consumer stores:
last processed / next offset
~~~

Тип: state-management mechanism.

Source point:

- сообщения до current consumer offset считаются обработанными;
- после consumer failure partition может быть назначена другому consumer;
- processing resumes from last recorded offset;
- если message был обработан, но offset не успел сохраниться, message может быть обработан повторно.

Verification:

- restart resumes from expected position;
- replay from older offset reproduces intended output;
- lag does not exceed retained log history.

Rollback: изменение offset может вызвать replay/duplicate effects; concrete procedure `[Needs confirmation]`.

## Log replay

Источник: `p0518:c01`, PDF 518.

Conceptual action:

~~~text
start a consumer from an older offset
read historical events again
write rebuilt output elsewhere
~~~

Тип: workload-generating / potentially state-changing at sink.

Effect: повторно обрабатывает retained history without modifying source log.

Verification: rebuilt output matches expected state for the replayed range.

Rollback: discard rebuilt derived output or switch back to previous known-good projection; concrete switch mechanism `[Needs confirmation]`.

## Change Data Capture (CDC)

Источник: `p0521:c01`–`p0525:c01`, PDF 521–525.

Conceptual pipeline:

~~~text
database write
  -> replication/change log
  -> CDC
  -> log broker / stream
  -> search index / cache / warehouse / other derived system
~~~

Тип: state-changing integration mechanism.

Source-confirmed implementations/examples:

- LinkedIn Databus;
- Facebook Wormhole;
- Yahoo! Sherpa;
- Bottled Water for PostgreSQL;
- Maxwell for MySQL;
- Debezium for MySQL;
- Mongoriver for MongoDB;
- Oracle GoldenGate;
- Kafka Connect.

Verification:

- changes are consumed in source order required by the projection;
- derived system converges to source DB state;
- consumer can recover after restart.

Rollback: product-specific `[Needs confirmation]`.

## Initial snapshot + change-log position

Источник: `p0523:c01`, PDF 523.

Conceptual bootstrap:

~~~text
1. capture consistent database snapshot
2. record corresponding log position / offset
3. load snapshot into new derived system
4. consume changes after that position
5. catch up to current log head
~~~

Тип: state-changing bootstrap procedure.

Verification: after catch-up, derived system matches source database state.

Rollback: discard incomplete derived copy and restart from a verified snapshot/position pair; concrete procedure `[Needs confirmation]`.

## Log compaction

Источник: `p0523:c01`–`p0524:c01`, PDF 523–524.

Conceptual rule:

~~~text
for each key:
  retain latest value
delete/tombstone:
  represents removed key
~~~

Тип: state-changing retention/storage mechanism.

Source-confirmed implementation: Apache Kafka supports log compaction.

Verification:

- compacted history retains latest value for every live key;
- new consumer from offset 0 can reconstruct current database-like state.

Rollback: previous uncompacted history cannot be recreated from compacted data alone — `[Needs confirmation]`.

## Event sourcing

Источник: `p0525:c01` onward.

Conceptual model:

~~~text
domain command
  -> immutable domain event
  -> append event to log
  -> project event into current/read state
~~~

Тип: state-changing application architecture.

Source distinction:

- CDC derives low-level change events from database writes;
- event sourcing makes domain events the primary application record.

Verification: replaying event history reconstructs the intended current projection.

Rollback: append compensating event where domain semantics allow; true historical deletion is a separate problem — `[Needs confirmation]`.

## Window types

Источник: `p0542:c01`–`p0543:c01`, PDF 542–543.

Source-confirmed window models:

- tumbling window;
- hopping window;
- sliding window;
- session window.

Тип: stream-processing configuration/model.

Verification:

- each event is assigned according to the chosen event-time/window rules;
- overlap/non-overlap semantics match the intended analysis;
- late-event behavior is explicit.

Rollback: revert processor/window configuration and replay retained input where safe — concrete syntax `[Needs confirmation]`.

## Stream joins

Источник: `p0543:c01`–`p0545:c01`, summary `p0552:c01`–`p0553:c01`.

### Stream–stream join

Two activity/event streams joined within a time window.

### Stream–table join

Activity stream enriched from table state; source describes maintaining a local copy via database change stream to avoid remote lookup per event.

### Table–table join

Two change streams maintain a materialized view of joined tables.

Тип: workload-generating stateful operators.

Verification: output reflects intended temporal/state semantics and recovers consistently after restart.

Rollback: previous processor version + replay from known offset/checkpoint where source history is retained.

## Idempotent processing with message offset

Источник: `p0549:c01`–`p0550:c01`, PDF 549–550.

Conceptual pattern:

~~~text
external state stores:
  business value
  last applied message offset

when processing message:
  if offset already applied -> skip duplicate
  else apply update + record offset
~~~

Тип: state-changing deduplication mechanism.

Source assumptions:

- replay reproduces the same messages/order;
- processing is deterministic;
- another node does not concurrently update the same value without additional coordination/fencing.

Verification: replaying the same message does not change final state twice.

Rollback: application-specific `[Needs confirmation]`.

## Stateful recovery

Источник: `p0550:c01`–`p0551:c01`, PDF 550–551.

Source-confirmed mechanisms/examples:

- Flink snapshots operator state to durable storage such as HDFS;
- Samza and Kafka Streams replicate state changes into a compacted Kafka topic;
- state can sometimes be rebuilt directly from replayable input;
- VoltDB example uses redundant processing on multiple nodes.

Тип: state-management / fault-recovery mechanisms.

Verification:

- recovered state corresponds to the resumed input offset;
- downstream output remains logically consistent after recovery.

Rollback: restore previous checkpoint/state and corresponding offset only as a matched pair; concrete mechanism `[Needs confirmation]`.

## Named technologies explicitly present in the chapter

- JMS;
- AMQP;
- Apache Kafka;
- Amazon Kinesis;
- DistributedLog;
- PostgreSQL / MySQL / MongoDB / Oracle change logs through CDC examples;
- Kafka Connect;
- Druid;
- Pistachio;
- RethinkDB;
- Firebase;
- CouchDB;
- VoltDB;
- Storm / Trident;
- Samza;
- Kafka Streams;
- Flink.

## Что не добавлено

- Kafka CLI;
- consumer-group reset commands;
- Debezium connector configuration;
- Flink checkpoint commands;
- Samza/Kafka Streams deployment syntax;
- broker retention configuration commands.

Concrete operational syntax этих systems не подтвержден chapter RAG.
