# Шпаргалка главы 11 — stream processing

## Symptom / problem framing

Проблема главы: input не заканчивается, events могут приходить late/out-of-order, consumers могут падать и replay'ить данные, а state/output должны оставаться корректными.

Негативные сигналы:

- producer пишет отдельно в DB и search index/cache;
- consumer offset неизвестен или теряется при restart;
- consumer lag приближается к retention boundary;
- retry одного event создает duplicate external effect;
- processing time используется как event time без явного contract;
- late event silently discarded;
- stream-table join выполняет remote DB query на каждый event и перегружает source DB;
- stateful operator теряет local state после node failure;
- replay produces different state because processing nondeterministic;
- framework заявляет exactly-once, но external sink semantics не проверены.

## Baseline / context

### Messaging

**AMQP/JMS-like broker**

- message delivered to consumer;
- consumer acknowledges;
- broker usually removes acknowledged message;
- good fit for task queue/asynchronous RPC;
- replay old history обычно не является основной моделью.

**Log-based broker**

- append events to partitioned log;
- ordered within partition;
- consumer tracks offset;
- history retained by policy;
- replay = reset/start from older offset.

### Database streams

- replication log = ordered stream of database writes;
- CDC exposes change stream for derived systems;
- snapshot + log position bootstraps a new consumer;
- compaction keeps latest value per key;
- event sourcing stores domain events explicitly.

### Stream processing

Processor may:

1. update database/cache/index;
2. notify a user/human;
3. transform input streams into derived output streams.

## Read-only checks

1. Зафиксировать topic/stream partitions and ordering guarantee.
2. Проверить retention policy.
3. Измерить consumer lag per partition.
4. Проверить persisted consumer offset/checkpoint.
5. Проверить rebalance/restart behavior.
6. Зафиксировать source-of-truth system.
7. Найти dual-write paths.
8. Для CDC проверить:
   - initial snapshot;
   - snapshot log position;
   - schema-change handling;
   - replay/compaction semantics.
9. Для event sourcing проверить projection rebuild path.
10. Для windows определить:
    - event timestamp source;
    - processing time;
    - allowed lateness;
    - window type.
11. Для joins определить stream-stream / stream-table / table-table.
12. Для stateful operators определить state backend/recovery source.
13. Проверить duplicate handling external sink.
14. Проверить deterministic replay.
15. Проверить exactly-once statement end-to-end, включая sink.

## Interpretation

- Consumer lag растет быстрее processing rate → consumer risks leaving retention window.
- Offset committed before effect durable → message may be lost logically after crash.
- Effect durable before offset commit → event may be replayed and effect duplicated.
- DB+index dual write partially fails → systems diverge.
- CDC consumer slow → source DB может быть healthy, но derived view stale.
- Same event replay changes result → nondeterministic processor or non-idempotent sink.
- Late event belongs to closed window → window correction/retraction policy required.
- Remote lookup per event dominates latency → local replicated table/state may be preferable.
- Table-table updates produce derived change stream → materialized-view maintenance.
- State recovered but offset mismatched → state/event history inconsistency.

## Next action

1. Зафиксировать source-of-truth stream and ordering scope.
2. Снять offsets, lag, retention and state-recovery model.
3. Reproduce restart/replay scenario.
4. Classify problem: ordering, lag, time/window, join, state, duplicate effect.
5. Apply minimal change.
6. Replay same scenario.
7. Keep only if correctness + recovery acceptance pass.

## Modifying action

Source-confirmed classes of changes:

- move integration from dual writes to CDC/change stream;
- persist/reposition consumer offset;
- adjust partitioning/consumer group topology;
- use log compaction;
- build/rebuild derived projection from history;
- choose event-time window semantics;
- change stream join strategy;
- add state checkpoint/replication;
- make sink idempotent using offset/dedup metadata;
- use transactions/microbatch/checkpoint mechanism supported by processor.

Concrete vendor CLI/config syntax: `[Needs confirmation]`.

## Verification / acceptance checks

### Delivery/replay

- consumer restart resumes from expected offset;
- replay yields same logical derived state;
- consumer lag remains within retention safety margin;
- partition ordering assumptions hold.

### CDC/projections

- new consumer can bootstrap from snapshot + log;
- search index/cache converges to database state;
- projection can be rebuilt without mutating source data.

### Time/windows

- event-time windows handle out-of-order/late events according to documented policy;
- processing-time delays do not silently change business meaning;
- window closure/correction semantics are testable.

### Stateful processing

- state + offset recover consistently after failure;
- duplicate input does not create duplicate visible effect where exactly/effectively-once is required;
- local state can be restored from checkpoint/log/source.

## Rollback

- CDC/projection change: return consumers to previous derived view/pipeline only after verifying source-of-truth remains unchanged; concrete procedure `[Needs confirmation]`.
- Offset change/replay: restore previous offset only if duplicate/replay semantics are understood; otherwise `[Needs confirmation]`.
- Window/join semantics rollback: revert processor version and replay from known offset/checkpoint where safe.
- Read-only checks: `[Not applicable]`.

## Operational loop

`event log → ordering/offset/time contract → stateful transform → replay/failure test → verify derived state → keep/rollback`.
