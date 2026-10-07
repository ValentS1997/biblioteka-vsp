# Book-level synthesis — «Высоконагруженные приложения»

Книга: **Мартин Клеппман — «Высоконагруженные приложения: программирование, масштабирование, поддержка»**.

Book ID: `vysokonagruzhennye-prilozheniya-martin-kleppmann-ru`.

Inventory: `0035`.

Registry direction: `Distributed Systems / Data`.

## Статус

- Все 12 numbered chapters имеют merged chapter-level analysis.
- Chapter artifacts: `notes/chapters/`.
- Canonical source SHA-256: `495e75f185c758a8223ca25b0fb35a8e6db693b06fb78c102e624a01ff852685`.
- RAG: `READY_WITH_KNOWN_LIMITATIONS`.
- Reading lifecycle: не изменяется этим synthesis; canonical state остается в `reading/progress.yaml`.
- Этот каталог — аналитический book-local layer. Отдельного canonical BOOK-SYNTHESIS template в `templates/` на момент создания нет.

## Source policy

### Book-derived synthesis

Основан на merged chapter artifacts глав 1–12, которые были построены в режиме `rag_only`.

External sources и model-memory факты не используются для дополнения содержания книги.

### biblioteka-vsp placement

Оценка места книги основана отдельно на:

- `registry/books.yaml`;
- `registry/ARCHITECTURE.md`;
- текущем составе библиотеки и ее `direction` classifications.

Это library-level analysis, а не утверждение исходного текста книги.

## Главный вывод книги

Книга не столько про «высокую нагрузку», сколько про **управление состоянием и неопределенностью в data-intensive systems**.

Повторяющаяся логика всей книги:

`workload/invariant → data model → storage/encoding → replication/partitioning → failure model → consistency/coordination → replayable derived state`

Главная инженерная идея: нельзя получить надежность, масштабируемость или корректность выбором одного продукта. Эти свойства возникают из явных contracts между компонентами и из понимания trade-offs.

## Три части как единая архитектурная линия

### Часть I — Foundations of data systems

Главы 1–4 отвечают на вопрос: **как представить, хранить и изменять данные так, чтобы система оставалась operable и evolvable?**

- Глава 1: reliability, scalability, maintainability.
- Глава 2: data models and query languages.
- Глава 3: storage engines, indexes, OLTP/OLAP.
- Глава 4: encoding, schema evolution, backward/forward compatibility.

Главный результат: данные и interfaces нужно проектировать как долгоживущие contracts, а performance — как функцию workload, а не как абстрактное число.

### Часть II — Distributed data

Главы 5–9 отвечают на вопрос: **что происходит, когда одно логическое состояние распределено между несколькими nodes и failures становятся partial?**

- Глава 5: replication.
- Глава 6: partitioning.
- Глава 7: transactions and isolation.
- Глава 8: network/clock/process uncertainty.
- Глава 9: consistency, ordering, consensus.

Главный результат: распределенная система не знает глобальную истину автоматически. Нужно явно определить ordering, failure assumptions, consistency guarantee и границу coordination.

### Часть III — Derived data

Главы 10–12 отвечают на вопрос: **как строить и эволюционировать производное состояние поверх authoritative data?**

- Глава 10: bounded batch dataflow.
- Глава 11: unbounded streams, CDC, replay, state.
- Глава 12: integration, integrity, auditability and responsibility.

Главный результат: derived state следует делать replaceable/rebuildable, transformations — replayable, а synchronous coordination использовать только там, где нарушение invariant действительно неприемлемо.

## Двенадцать глав — двенадцать operational questions

| Глава | Вопрос, который стоит задавать в реальной системе |
|---|---|
| 1 | Как мы измеряем нагрузку, tail latency, reliability и operability? |
| 2 | Соответствует ли data model реальным relationships и query patterns? |
| 3 | Почему storage/index layout подходит именно этому workload? |
| 4 | Могут ли old/new writers и readers безопасно сосуществовать? |
| 5 | Что будет видно/потеряно при lag, failover и concurrent writes? |
| 6 | Где появятся skew, hot partitions и routing/rebalancing cost? |
| 7 | Какой invariant защищает transaction и какие anomalies еще возможны? |
| 8 | Что на самом деле означает timeout и что node реально может знать? |
| 9 | Где действительно требуется одно global decision/order? |
| 10 | Можно ли вычисление безопасно повторить из immutable input? |
| 11 | Можно ли восстановить state из log + offset/checkpoint без duplicate effect? |
| 12 | Где authoritative data, можно ли rebuild derived state и как verify integrity end-to-end? |

## Сквозные идеи

### 1. Workload first

Нет «быстрой базы», «масштабируемой архитектуры» или «правильного индекса» вне конкретного load model.

Нужно знать:

- read/write ratio;
- key distribution;
- access pattern;
- latency percentiles;
- data lifetime;
- failure tolerance;
- consistency requirements.

### 2. Fault != failure

Hardware, software, operator, network и timing faults неизбежны.

Цель инженерии — не отсутствие faults, а ограничение blast radius и предотвращение user-visible failure.

### 3. Data contracts live longer than code

Schemas, field tags, logs, APIs и stored records переживают отдельные deployments.

Поэтому compatibility — часть deployment architecture.

### 4. Replication trades certainty for availability/latency

Replication lag, stale reads, failover и concurrent writes — нормальные состояния, а не edge cases.

### 5. Partitioning is a workload-distribution problem

Нужно распределять не только bytes, но и read/write pressure. Hot key способен разрушить красивую hash scheme.

### 6. Transactions protect invariants, not business meaning automatically

ACID label не заменяет понимание isolation level, lost update, write skew, phantoms и retry semantics.

### 7. Distributed systems operate under uncertainty

Timeout не доказывает failure. Wall clock не доказывает causal order. Lease holder может быть stale после process pause.

### 8. Strong consistency has a coordination price

Linearizability/consensus полезны там, где требуется одна shared truth. Их не следует распространять на state, который может безопасно branch/merge или converge asynchronously.

### 9. Replay is a reliability primitive

Immutable input/log + deterministic transformation позволяет:

- retry;
- rebuild;
- migrate;
- audit;
- repair;
- create new projections.

### 10. Integrity is end-to-end

Exactly-once внутри одного layer не гарантирует exactly-once business effect.

Request/operation identity, deduplication, reconciliation and provenance должны доходить до конечного durable effect.

## Где книга особенно сильна

1. **Vocabulary.** Дает точные имена распространенным проблемам: replication lag, write skew, fencing token, linearizability, causal order, quorum, total-order broadcast, CDC, replay.
2. **Trade-off reasoning.** Почти каждая техника описывается через цену и failure mode, а не как product feature.
3. **Layer bridging.** Связывает storage internals, networking uncertainty, transactions, consensus и data pipelines в одну mental model.
4. **Failure thinking.** Учит рассматривать retries, pauses, partitions, stale state и partial failure как штатные режимы.
5. **Evolution thinking.** Совместимость, replay и replaceable derived state превращают изменения системы в controlled migration rather than big-bang change.

## Где книга не заменяет другие источники

Это не runbook и не vendor handbook.

Она не заменяет:

- Linux internals;
- практическую network administration;
- Kubernetes/container operations;
- SQL syntax/reference;
- конкретную database administration;
- monitoring tooling;
- incident response/runbooks;
- IaC/automation.

Книга дает **архитектурную модель, по которой нужно понимать поведение этих инструментов**, но не их operational syntax.

## Итоговая оценка

В `biblioteka-vsp` это одна из наиболее системообразующих книг уровня architecture/reliability.

Ее ценность не в конкретных Hadoop/Kafka/ZooKeeper examples, часть которых исторична, а в устойчивых abstractions:

- logs;
- immutable/replayable data;
- ordering;
- idempotency;
- replication;
- partitioning;
- transactions;
- partial failure;
- consensus;
- derived state;
- end-to-end integrity.

См. также:

- [knowledge-map.md](knowledge-map.md)
- [operational-distillation.md](operational-distillation.md)
- [biblioteka-vsp-placement.md](biblioteka-vsp-placement.md)
- [visual-synthesis.svg](visual-synthesis.svg)
