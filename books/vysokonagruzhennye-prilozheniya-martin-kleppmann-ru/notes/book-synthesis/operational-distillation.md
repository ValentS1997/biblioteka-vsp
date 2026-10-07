# Operational distillation — Infrastructure / Operations practice

Это не новый источник по продуктам. Ниже — book-derived engineering rules, сформулированные как operational checks.

## 1. Начинать с load model

Проверить:

- request/read/write rate;
- key distribution;
- data growth;
- p50/p95/p99 latency;
- concurrency;
- burst behavior;
- failure/recovery objectives.

Не принимать architecture decision только по среднему response time или общей CPU utilization.

## 2. Отделять fault от user-visible failure

Fault может быть:

- disk/node failure;
- software bug;
- operator error;
- slow dependency;
- packet loss/delay;
- process pause.

Acceptance criterion: fault не должен автоматически превращаться в corrupted state или uncontrolled outage.

## 3. Делать contracts versioned

Для API/schema/message/storage format проверять отдельно:

- backward compatibility;
- forward compatibility;
- unknown-field preservation;
- old/new version coexistence.

Operational rule:

~~~text
contract delta → compatibility test → staged rollout → observe → keep/rollback
~~~

## 4. Наблюдать replication как процесс, а не boolean health

Минимальные signals:

- replication lag;
- replica position;
- leader/follower state;
- failover history;
- stale-read window;
- conflict/repair metrics.

Failover acceptance: exactly one active writer where topology requires it, expected data freshness and known handling of unreplicated writes.

## 5. Измерять skew

Для partitioned systems смотреть не только aggregate load, но и per-partition/per-key distribution.

Signals:

- hottest partition;
- hottest key;
- partition size spread;
- request-rate spread;
- rebalance data movement;
- routing metadata freshness.

## 6. Формулировать invariant до transaction mechanism

Reasoning:

~~~text
invariant → concurrent scenario → anomaly → minimal control
~~~

Контроль может быть:

- atomic DB operation;
- explicit lock;
- stronger isolation;
- serialized partition/queue;
- consensus boundary.

## 7. Timeout — это suspicion

Timeout не доказывает:

- что remote node dead;
- что request не executed;
- что response никогда не придет.

Перед tuning:

- измерить latency distribution;
- учесть queueing/jitter;
- проверить retry amplification;
- проверить false failover.

## 8. Использовать правильные clocks

- elapsed duration / timeout → monotonic clock;
- calendar timestamps → real-time clock;
- causal ordering → не выводить только из wall-clock timestamps.

Clock/NTP status — source of uncertainty, а не доказательство exact order.

## 9. Fencing для stale actors

Если lease/lock holder после pause может повредить resource, lease alone недостаточен.

Проверка:

- token monotonically increases;
- resource remembers newer token;
- stale token is rejected at the protected resource.

## 10. Coordination платить только за invariant

Linearizability/consensus нужны не «для надежности вообще», а для конкретных decisions:

- unique owner/leader;
- uniqueness;
- membership;
- one irreversible decision;
- total ordered replicated state machine.

Если branching/merge acceptable, weaker causal/eventual semantics могут быть правильнее.

## 11. Делать computation replayable

Batch principle:

~~~text
immutable input → deterministic/retryable transform → separate output
~~~

Преимущества:

- rollback by output selection;
- rebuild after code fix;
- audit/reconciliation;
- migration by parallel projection.

## 12. Делать streams recoverable

Для stateful stream processing зафиксировать:

- partition/order guarantee;
- consumer offset;
- retention horizon;
- event-time policy;
- state checkpoint;
- sink dedup/idempotency.

Recovery must restore state + matching offset.

## 13. Не доверять marketing "exactly once"

Проверять end-to-end:

- source;
- processor;
- state backend;
- network retry;
- external sink;
- client/request retry.

Exactly-once framework processing может закончиться duplicate business effect.

## 14. Distinguish timeliness from integrity

Timeliness problem:

- state stale;
- lagging cache/index;
- delayed projection.

Integrity problem:

- lost/duplicated operation;
- broken invariant;
- corrupt derived state.

Staleness часто лечится catch-up. Integrity требует detection/repair.

## 15. Build independent verification

Для critical data paths полезны:

- reconciliation;
- checksums;
- replay comparison;
- source-vs-derived consistency checks;
- audit trail/provenance.

Operational principle: trust but verify.

## 16. Rollback-first architecture

The book repeatedly favors designs where rollback is structurally possible:

- old/new schemas coexist;
- immutable input retained;
- derived state replaceable;
- projection rebuilt in parallel;
- rollout staged;
- source of truth remains unchanged.

This directly supports controlled operations.

## Compact incident checklist

When a distributed/data incident occurs:

1. What is the authoritative state?
2. Is the problem availability, timeliness or integrity?
3. Which node/version/partition owns the affected state?
4. What ordering guarantee is expected?
5. Is there lag, replay or duplicate processing?
6. Could timeout/failover be a false positive?
7. Is a stale actor still able to write?
8. Can the derived state be rebuilt?
9. What is the rollback point?
10. Which invariant proves recovery is complete?

## Acceptance mindset

A change is not accepted because "service is up".

Acceptance should include:

- expected invariant holds;
- stale/divergent state is bounded;
- recovery path tested;
- rollback remains possible;
- monitoring can detect recurrence.
