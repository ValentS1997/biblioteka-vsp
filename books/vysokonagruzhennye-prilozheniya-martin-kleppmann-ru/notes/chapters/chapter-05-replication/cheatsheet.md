# Шпаргалка главы 5 — replication

## Symptom / problem framing

Проблема главы: копии одних данных находятся на нескольких узлах, но writes, failures и network delays происходят независимо. Система должна определить, как эти копии сходятся и какие аномалии допустимы.

Негативные сигналы:

- follower заметно отстает, а приложение читает из него как из актуального источника;
- promoted follower не содержит последних writes старого leader;
- два узла одновременно считают себя leader;
- user не видит собственную только что выполненную запись;
- повторное чтение «откатывается назад во времени»;
- causal order нарушается;
- multi-leader writes конфликтуют без deterministic policy;
- leaderless quorum трактуется как абсолютная consistency guarantee;
- LWW используется там, где silent data loss недопустим.

## Baseline / context

### Single-leader

- writes идут leader;
- leader отправляет replication log followers;
- reads могут обслуживаться leader или followers;
- replication может быть synchronous или asynchronous.

### Multi-leader

- несколько leaders принимают writes;
- лидеры реплицируют изменения друг другу;
- повышается availability/geo-locality, но появляются write conflicts.

### Leaderless

- client/координатор пишет сразу в несколько replicas;
- reads выполняются с нескольких replicas;
- version information помогает определить более новые/concurrent values.

## Read-only checks

1. Определить replication topology: single-leader, multi-leader или leaderless.
2. Зафиксировать synchronous/asynchronous paths.
3. Проверить, когда write считается successful.
4. Измерить replication lag.
5. Проверить follower log position относительно leader.
6. Зафиксировать failover policy и election/promote criteria.
7. Проверить split-brain prevention.
8. Определить read guarantees:
   - read-after-write;
   - monotonic reads;
   - consistent prefix reads.
9. Для multi-leader проверить:
   - conflict detection;
   - conflict resolution;
   - replication topology;
   - causal ordering.
10. Для leaderless зафиксировать `n`, `w`, `r`.
11. Проверить, используется strict или sloppy quorum.
12. Проверить read repair / anti-entropy.
13. Определить conflict strategy: LWW, merge, siblings/version vectors.
14. Проверить tombstones для удалений при merge.
15. Проверить staleness monitoring.

## Interpretation

- Async follower lag растет → reads могут быть stale; eventual consistency window увеличивается.
- User пишет в leader и сразу читает lagging follower → нарушается read-after-write.
- Последовательные reads попадают на replicas с разным lag → возможно нарушение monotonic reads.
- Causally related events применены в разном порядке → нарушается consistent prefix.
- Failover promotes stale follower → возможна потеря acknowledged writes.
- Multi-leader принимает concurrent updates → требуется conflict resolution.
- `w + r > n` → множества read/write обычно пересекаются, но это не абсолютная гарантия свежести во всех сценариях.
- Sloppy quorum пишет во временные non-home nodes → write availability выше, immediate visibility ниже.
- LWW выбирает одно значение → convergence достигается, но concurrent writes могут быть отброшены.
- Version vectors показывают causal history → система может различать overwrite и concurrency.

## Next action

1. Снять topology и replication mode.
2. Измерить lag / replica freshness.
3. Сформулировать требуемую user-visible consistency guarantee.
4. Выбрать минимальное изменение.
5. Проверить failure case или lag case контролируемо.
6. Повторить те же чтения/записи и measurements.
7. Сохранить изменение только при выполнении acceptance criteria.

## Modifying action

Source-confirmed виды изменений:

- переключение synchronous/asynchronous replication policy;
- добавление follower через snapshot + catch-up;
- promotion follower в leader при failover;
- изменение routing reads/writes;
- настройка quorum parameters `n/w/r`;
- применение hinted handoff;
- применение read repair/anti-entropy;
- изменение conflict-resolution strategy.

Конкретный product syntax в главе не приводится.

## Verification / acceptance checks

### Single-leader

- follower catch-up подтвержден по replication position;
- failover не создает два active leaders;
- новый leader имеет ожидаемую свежесть данных;
- clients действительно пишут в новый leader;
- replication lag остается наблюдаемым.

### Read semantics

- user видит собственную запись;
- после более нового read не наблюдается более старое состояние;
- causal dependencies не наблюдаются в обратном порядке.

### Leaderless

- успешный write получил минимум `w` подтверждений;
- read получил минимум `r` ответов;
- repair/anti-entropy возвращают replicas к convergence;
- stale values и concurrent values различаются по version metadata.

### Conflict handling

- concurrent writes не теряются без явной policy;
- merge дает ожидаемый application result;
- delete semantics используют tombstones, если простое удаление может воскресить значение.

## Rollback

- Replication topology/config rollback: конкретные команды `[Needs confirmation]`.
- Failover: возврат прежнего leader без проверки divergence небезопасен; source не дает универсальной rollback procedure — `[Needs confirmation]`.
- Quorum parameter rollback: вернуть предыдущие `n/w/r`; конкретный syntax `[Needs confirmation]`.
- Read-only checks: `[Not applicable]`.

## Operational loop

`topology → lag/failure model → consistency target → controlled change → verify → keep/rollback`.
