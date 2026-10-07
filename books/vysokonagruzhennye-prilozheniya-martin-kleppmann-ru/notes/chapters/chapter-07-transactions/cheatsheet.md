# Шпаргалка главы 7 — транзакции и isolation

## Symptom / problem framing

Проблема главы: несколько reads/writes должны сохранять application invariants несмотря на crashes и concurrency.

Негативные сигналы:

- частично выполненная multi-object operation оставляет inconsistency;
- transaction retry повторяет уже committed effect;
- один transaction читает uncommitted data другого;
- concurrent write затирает чужое изменение;
- multi-read видит данные из разных моментов времени;
- две transactions принимают решение на одинаковом snapshot и вместе нарушают invariant;
- predicate query возвращает «пусто», после чего concurrent transaction вставляет matching row;
- lock queue/deadlock резко ухудшает tail latency;
- SSI abort rate растет при contention.

## Baseline / context

### ACID

- Atomicity: при failure transaction aborts и ее partial writes должны быть отброшены.
- Consistency: application invariants должны оставаться истинными; в общем случае это ответственность приложения.
- Isolation: concurrent result должен соответствовать выбранной isolation guarantee; сильный эталон — serializability.
- Durability: committed data не должно теряться в рамках обещанной storage/replication model; абсолютной гарантии нет.

### Weak isolation

#### Read committed

Предотвращает:

- dirty reads;
- dirty writes.

Не предотвращает все read/write races.

#### Snapshot isolation

- transaction читает consistent snapshot;
- readers не блокируют writers и наоборот;
- обычно реализуется MVCC;
- предотвращает read skew;
- может допустить write skew и связанные phantom anomalies.

### Serializable

Результат эквивалентен некоторому serial execution.

Три подхода главы:

- actual serial execution;
- two-phase locking (2PL);
- serializable snapshot isolation (SSI).

## Read-only checks

1. Зафиксировать application invariants.
2. Определить transaction boundaries.
3. Классифицировать operations:
   - single-object;
   - multi-object;
   - read-only;
   - read-modify-write;
   - predicate read followed by write.
4. Определить фактический isolation level.
5. Проверить, предотвращаются ли dirty reads/writes.
6. Проверить consistent snapshot semantics.
7. Найти read-modify-write loops.
8. Проверить использование atomic DB operations.
9. Найти explicit `FOR UPDATE` locks.
10. Найти decisions, основанные на predicate query.
11. Проверить возможный write skew/phantoms.
12. Для 2PL измерить lock wait/deadlock rate.
13. Для SSI измерить serialization abort/retry rate.
14. Проверить retry policy: transient vs permanent errors.
15. Проверить external side effects и deduplication при ambiguous commit.

## Interpretation

- Видны uncommitted writes → dirty read.
- Write поверх uncommitted write → dirty write.
- В одной transaction повторный read дает logically incompatible snapshot → read skew/nonrepeatable read.
- Два read-modify-write loops дают один итоговый increment вместо двух → lost update.
- Transactions обновляют разные rows, но вместе нарушают общий invariant → write skew.
- Write меняет result set predicate query другой transaction → phantom.
- Snapshot isolation пропускает write skew → ожидаемое ограничение, не обязательно defect implementation.
- Lock wait растет → pessimistic concurrency ограничивает throughput/tail latency.
- SSI часто aborts → optimistic model столкнулся с высоким contention.

## Next action

1. Сформулировать invariant.
2. Воспроизвести конкретную anomaly concurrent test'ом.
3. Выбрать минимальный механизм:
   - atomic operation;
   - explicit lock;
   - stronger isolation.
4. Повторить тот же concurrency scenario.
5. Измерить correctness и performance.
6. Сохранить изменение только при выполнении acceptance criteria.

## Modifying action

Source-confirmed изменения:

- заменить read-modify-write на atomic DB update;
- добавить `SELECT ... FOR UPDATE`;
- использовать transaction boundaries `BEGIN TRANSACTION ... COMMIT`;
- повысить isolation до serializable;
- материализовать conflict для возможности lock;
- использовать stored procedure/serial execution model;
- перейти на 2PL/SSI в системах, где это поддерживается.

Конкретная настройка isolation/product syntax вне приведенных SQL examples: `[Needs confirmation]`.

## Verification / acceptance checks

### Atomicity

- partial failure не оставляет subset writes;
- aborted transaction можно безопасно повторить при transient error.

### Isolation

- dirty reads/writes отсутствуют;
- lost update scenario дает правильный результат;
- invariant не нарушается при write skew scenario;
- phantom scenario не создает duplicate/conflicting object;
- serializable execution проходит те же concurrency tests.

### Performance

- 2PL lock waits/deadlocks не превышают допустимый уровень;
- SSI abort/retry rate приемлем;
- transaction duration минимальна;
- retries не создают overload feedback loop.

## Rollback

- Explicit lock/isolation change: вернуть предыдущую application/query strategy; product-specific command `[Needs confirmation]`.
- State-changing SQL examples: восстановление данных зависит от transaction state и application semantics — `[Needs confirmation]`.
- Read-only anomaly tests: `[Not applicable]`.
- При staged change сначала остановить rollout при росте deadlocks/abort rate, затем вернуть прежнюю стратегию.

## Operational loop

`invariant → concurrent scenario → anomaly classification → minimal control → rerun scenario → keep/rollback`.
