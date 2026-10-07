# Шпаргалка главы 8 — distributed-system failure model

## Symptom / problem framing

Проблема главы: remote node, network, clock и process pause создают uncertainty. Отсутствие ответа не говорит, что именно произошло.

Негативные сигналы:

- timeout трактуется как доказанный node failure;
- failover происходит при latency spike и удваивает нагрузку;
- request retry может выполнить operation дважды;
- wall-clock используется для elapsed timeout;
- LWW ordering полагается на clocks с неизвестной погрешностью;
- process после GC pause продолжает работать как прежний leader;
- lease считается достаточной защитой resource;
- algorithm correctness зависит от timing assumptions, которые нигде не зафиксированы;
- monitoring различает только healthy/dead и не видит slow/limping nodes.

## Baseline / context

### Partial failure

В distributed system:

- один node может работать, другой — нет;
- network path может быть asymmetric;
- request может потеряться;
- request может быть обработан, а response — потеряться;
- message может задержаться на произвольное время;
- process может остановиться и затем продолжить работу.

### Failure detection

Timeout дает только вывод:

`response not observed before deadline`

Он не доказывает:

- remote process died;
- request was not executed;
- response will never arrive.

### Clocks

**Real-time / time-of-day clock**

- дает calendar timestamp;
- обычно корректируется NTP;
- может прыгнуть назад/вперед;
- подходит для wall-clock events, но опасен для elapsed duration.

**Monotonic clock**

- движется вперед;
- подходит для duration/timeouts;
- абсолютное значение не переносимо между machines.

### Process pauses

Причины могут включать:

- stop-the-world GC;
- OS scheduling;
- page faults / swapping;
- synchronous I/O;
- virtualization pauses.

Во время pause другой quorum может признать node неработающим и передать его роль другому.

## Read-only checks

1. Зафиксировать все remote calls и их timeout/retry semantics.
2. Измерить RTT distribution, tail latency и jitter по длительному окну.
3. Проверить false-positive failure detection при load spike.
4. Проверить network loss, delay, duplication и asymmetric connectivity scenarios.
5. Проверить, что request success определяется application-level acknowledgment, а не только TCP delivery.
6. Для elapsed time проверить использование monotonic clock.
7. Для wall-clock timestamps проверить NTP/clock offset и допустимую uncertainty.
8. Найти business/replication ordering, основанный только на physical timestamps.
9. Проверить process-pause sensitivity lease/leader logic.
10. Проверить, есть ли fencing token downstream.
11. Проверить monotonicity fencing tokens.
12. Проверить, отклоняет ли resource stale token.
13. Зафиксировать quorum rules для leadership/lock ownership.
14. Зафиксировать system model: timing + node-failure assumptions.
15. Разделить acceptance properties на safety и liveness.

## Interpretation

- Timeout spike без node crash → failure detector false positive.
- После failover старый node продолжает писать → stale leader/lease-holder problem.
- Старый fencing token принят resource → fencing не реализован end-to-end.
- Wall-clock идет назад → elapsed-time code на wrong clock source.
- LWW теряет causally later write → physical timestamps не обеспечивают causal ordering.
- Slow node формально жив, но throughput резко упал → limping node; binary health model недостаточна.
- Алгоритм безопасен только при bounded delays, а production network таких bounds не обещает → model mismatch.
- Safety нарушилась хоть один раз → algorithm incorrect for stated model.
- Liveness временно не выполняется при partition, но восстанавливается после network recovery → возможно допустимо по specified model.

## Next action

1. Сформулировать failure scenario.
2. Зафиксировать system assumption, на котором основана текущая логика.
3. Выполнить read-only measurement/fault test.
4. Найти mismatch между assumption и наблюдаемым поведением.
5. Выбрать минимальное изменение: timeout policy, monotonic clock, fencing, quorum, validation.
6. Повторить тот же failure scenario.
7. Сохранить изменение только при выполнении safety/liveness acceptance criteria.

## Modifying action

Source-confirmed classes of changes:

- изменить timeout/failure detector policy;
- использовать adaptive failure detection;
- заменить wall-clock elapsed measurement на monotonic clock;
- настроить синхронизацию с несколькими NTP servers;
- добавить fencing token к lease/lock protocol;
- проверять monotonic token downstream;
- добавить checksum/input validation;
- изменить quorum/coordination rule.

Concrete product commands глава универсально не задает.

## Verification / acceptance checks

### Network/failure detection

- temporary latency spike не вызывает неконтролируемый cascading failover;
- system восстанавливается после network fault;
- duplicate execution обрабатывается согласно operation semantics;
- slow node обнаруживается observability layer.

### Time

- elapsed duration не зависит от wall-clock jumps;
- clock skew/uncertainty наблюдаемы;
- causal order не выводится только из ненадежных physical timestamps.

### Lease/fencing

- stale process после pause не может изменить protected resource;
- newer fencing token supersedes older token;
- resource rejects request with older token.

### Correctness model

- safety property не нарушается ни в одном tested failure scenario;
- liveness возвращается при выполнении stated recovery assumptions;
- timing/failure assumptions явно документированы.

## Rollback

- Timeout/failure-detector tuning: вернуть предыдущие thresholds/policy; concrete syntax `[Needs confirmation]`.
- Clock-source change: вернуть прежний implementation only after confirming timeout semantics; concrete syntax `[Needs confirmation]`.
- Fencing: удаление fencing снижает safety и не является безопасным operational rollback без отдельного design review.
- Read-only/fault-injection checks: `[Not applicable]`.

## Operational loop

`assumption → fault scenario → observe uncertainty → minimal control → repeat fault → verify safety/liveness`.
