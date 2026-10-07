# Шпаргалка главы 9 — consistency, ordering, consensus

## Symptom / problem framing

Проблема главы: replicas/nodes должны давать достаточно сильные guarantees для application invariants, но coordination имеет цену по latency и availability.

Негативные сигналы:

- приложение ожидает «одну актуальную copy», а БД дает только eventual convergence;
- linearizability и serializability используются как синонимы;
- uniqueness/leader election реализованы локальным check-then-write;
- physical timestamps используются как единственный total-order mechanism;
- Lamport order считается доказательством concurrency/non-concurrency;
- 2PC coordinator потерян, transactions остаются in-doubt и держат locks;
- service продолжает writes в minority partition, хотя invariant требует single decision;
- собственный election/consensus protocol строится без epochs/quorums/fencing;
- ZooKeeper/etcd используется как high-throughput application database.

## Baseline / context

### Eventual consistency

Если writes прекратятся и failures устранятся, replicas со временем converges.

До convergence guarantee слабая: fresh read не обещан.

### Linearizability

Снаружи система ведет себя так, как будто:

- существует одна copy;
- каждая operation действует атомарно в некоторый момент между request/response;
- после наблюдения нового value последующие reads не должны возвращаться к старому.

### Linearizability != serializability

- serializability — ordering transactions, затрагивающих несколько objects;
- linearizability — real-time recency guarantee отдельных register-like operations;
- вместе они образуют strict serializability.

### Causality

Если B зависит от A, система обязана наблюдать A before B.

Concurrent events не обязаны иметь meaningful order.

### Total-order broadcast

Требует:

- reliable delivery;
- одинакового total delivery order на всех nodes.

## Read-only checks

1. Сформулировать application invariant.
2. Определить текущую consistency guarantee каждого storage/coordination path.
3. Проверить, действительно ли нужен linearizable read/write/CAS.
4. Разделить transaction isolation и replica consistency.
5. Найти cross-channel dependency: write в одном channel → signal через другой → read.
6. Для causal workload определить dependencies и допустимые concurrent branches.
7. Проверить source of sequence numbers/timestamps.
8. Если используется Lamport timestamp, не выводить из него concurrency.
9. Проверить, есть ли gap-free/final total-order mechanism там, где решение должно быть окончательным.
10. Для 2PC проверить coordinator durability и in-doubt transactions.
11. Проверить lock retention во время coordinator outage.
12. Для consensus зафиксировать:
    - current term/epoch;
    - quorum size;
    - majority availability;
    - leader election behavior.
13. Проверить safety при minority isolation.
14. Проверить liveness после восстановления majority.
15. Для ZooKeeper/etcd определить, какие данные являются coordination metadata, а какие application data.

## Interpretation

- Реплики со временем сходятся, но fresh read не гарантирован → eventual consistency.
- После completed write другой client видит старое value → violation linearizability.
- Transactions serializable, но read snapshot intentionally stale → serializable, но not linearizable.
- Causal chain нарушена → causal inconsistency.
- Lamport timestamp задает порядок A < B, но это не доказывает, что A caused B.
- Total-order log имеет missing sequence entry → нельзя безопасно deliver later entry before gap resolved.
- 2PC participants prepared, coordinator unavailable → in-doubt/blocking state.
- Consensus lost majority → liveness may stop; safety должна сохраниться.
- Два leaders разных epochs → newer epoch must supersede stale leader.
- Coordination service хранит rapidly changing bulk state → misuse of intended model.

## Next action

1. Зафиксировать invariant и требуемую guarantee.
2. Найти минимальную coordination boundary.
3. Воспроизвести failure/concurrency scenario.
4. Проверить behavior under network partition / leader loss.
5. Выбрать mechanism: causal order, linearizable primitive, total-order broadcast, consensus service.
6. Повторить scenario.
7. Сохранить решение только при выполнении safety/liveness acceptance criteria.

## Modifying action

Source-confirmed classes of changes:

- использовать linearizable compare-and-set/register;
- перейти к total-order broadcast/state-machine style sequencing;
- применить 2PC для atomic distributed commit;
- использовать fault-tolerant consensus protocol;
- вынести lock/election/membership в ZooKeeper-like coordination service;
- использовать epoch/term/ballot + quorum majority;
- отказаться от global consensus там, где branches/merge допустимы.

Concrete product configuration commands глава не задает.

## Verification / acceptance checks

### Linearizability

- после completed write subsequent reads не возвращают older value;
- CAS decision выглядит atomic;
- network partition не создает две conflicting successful decisions.

### Causality/order

- causal predecessor всегда наблюдается before dependent event;
- total-order recipients deliver same messages in same order;
- missing sequence position не пропускается.

### 2PC

- participant after prepare obeys durable coordinator decision;
- coordinator restart восстанавливает decision log;
- in-doubt locks/transactions наблюдаемы;
- failure mode не маскируется как successful atomic commit.

### Consensus

- agreement: два nodes не decide разные values;
- integrity: node не decides дважды;
- validity: decided value был proposed;
- termination: healthy nodes eventually decide при stated quorum assumptions;
- stale leader from older epoch не способен overwrite newer decision.

## Rollback

- Consistency/consensus design rollback зависит от конкретного storage protocol — `[Needs confirmation]`.
- 2PC/XA rollback после prepare нельзя выполнять произвольно: participant связан protocol decision; recovery procedure `[Needs confirmation]`.
- Coordination-service migration назад требует сохранения single-owner/uniqueness invariants — `[Needs confirmation]`.
- Read-only consistency tests: `[Not applicable]`.

## Operational loop

`invariant → required order/decision → minimal coordination → partition/failure test → verify safety/liveness → keep/rollback`.
