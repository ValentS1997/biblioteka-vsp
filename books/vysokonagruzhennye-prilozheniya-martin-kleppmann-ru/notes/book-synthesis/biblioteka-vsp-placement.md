# Место книги в biblioteka-vsp

## Canonical registry placement

Current inventory record:

- Inventory: 0035
- Title: «Высоконагруженные приложения: программирование, масштабирование, поддержка»
- Direction: Distributed Systems / Data
- Knowledge ID: vysokonagruzhennye-prilozheniya-martin-kleppmann-ru

Оценка: canonical direction менять не требуется. Distributed Systems / Data точно отражает предмет книги.

## Analytical role in the library

Ниже — synthesis/inference по текущему registry, не новый canonical field.

### Role: architecture bridge / conceptual spine

Книга связывает несколько направлений библиотеки, которые иначе легко изучать как независимые tools:

- Linux / OS;
- networking;
- databases;
- containers/Kubernetes;
- monitoring/operations;
- distributed systems;
- data/ML systems.

Она объясняет, почему production systems ведут себя определенным образом при replication lag, partitions, retries, timeouts, schema changes и partial failure.

Это делает ее скорее системообразующей архитектурной книгой, чем специализированным manual.

## Связи с конкретными книгами registry

### Foundations before/alongside

#### 0007 — UNIX и Linux. Руководство системного администратора

Связь:

- operability;
- failures;
- storage/network/service operation;
- monitoring mindset.

Разница:

- SysAdmin handbook отвечает «как эксплуатировать системы»;
- Клеппман отвечает «какие distributed/data guarantees вообще возможны и какой ценой».

Эти книги дополняют друг друга.

#### 0003 / 0004 — Компьютерные сети

Связь:

- latency;
- packet loss;
- partitions;
- queues;
- distributed failure detection.

Клеппман использует network uncertainty как архитектурную данность, но не заменяет глубокое изучение protocols/routing.

#### 0034 — Внутреннее устройство Linux

Связь:

- process scheduling;
- I/O;
- filesystems;
- memory;
- process pauses;
- local failure behavior.

Linux internals дает механизм одного node; Клеппман показывает, что происходит, когда таких nodes много.

#### 0039 — Сети Linux. Модели и приложения

Связь особенно прямая для перехода от local networking primitives к behavior distributed applications.

### Direct companion

#### 0009 — Распределенные системы. Паттерны проектирования

Это наиболее прямой companion.

Разделение ролей:

- Клеппман — fundamentals, failure/consistency/data semantics;
- Burns — reusable distributed-system patterns и practical composition, особенно вокруг container/Kubernetes environment.

Recommended relation:

~~~text
Kleppmann fundamentals
→ distributed-systems patterns
→ concrete platform implementation
~~~

### Database complement

#### 0008 — SQL. Карманный справочник

SQL reference помогает писать queries.

Клеппман объясняет:

- data models;
- indexes/storage engines;
- isolation;
- transactions;
- replication;
- OLTP/OLAP.

Это разные abstraction levels: syntax vs architecture/semantics.

### Platform/containers

#### 0014 — Docker без секретов
#### 0001 / 0033 — Kubernetes books

Containers/orchestrators решают packaging/scheduling/service-operation problems.

Они не решают автоматически:

- consistency;
- replication correctness;
- transaction isolation;
- exactly-once effects;
- data partitioning;
- consensus design.

Клеппман — conceptual correction против предположения «распределили pods = получили надежную distributed system».

### Observability

#### 0020 — Zabbix 7
#### 0040 — Запускаем Prometheus

Книга дает смысл метрикам:

- latency percentiles;
- replication lag;
- partition skew;
- consumer lag;
- retries;
- lock waits;
- abort rate;
- failure detector behavior.

Monitoring books дают инструменты наблюдения; Клеппман помогает выбрать, что наблюдать и почему.

### Data/ML systems

#### 0031 — Проектирование систем машинного обучения
#### 0029 — AI-инженерия

Связь через:

- data pipelines;
- derived state;
- batch/stream processing;
- event logs;
- data quality/integrity;
- reproducibility;
- materialized views.

Для ML/AI systems главы 10–12 особенно полезны как фундамент data infrastructure.

## What this book contributes uniquely

В registry уже есть книги про Linux, networks, containers, monitoring, programming и SQL.

Уникальная роль Клеппмана — соединить component-level knowledge в reasoning о system-wide correctness.

Она отвечает на вопросы вида:

- Почему retry может быть опасен?
- Почему healthy nodes все равно могут disagree?
- Почему wall-clock timestamp не означает causal order?
- Почему quorum не всегда дает freshness?
- Почему transaction isolation level меняет business correctness?
- Почему cache/search index должен считаться derived state?
- Почему replay/log architecture упрощает recovery and migration?

## Suggested library graph

~~~mermaid
flowchart TD
    L["Linux / SysAdmin<br/>0007 · 0034"] --> K["Kleppmann 0035<br/>Distributed Systems / Data"]
    N["Networks<br/>0003 · 0004 · 0039"] --> K
    SQL["SQL / Databases<br/>0008"] --> K

    K --> D["Distributed-system patterns<br/>0009"]
    K --> C["Containers / Kubernetes<br/>0014 · 0001 · 0033"]
    K --> O["Observability<br/>0020 · 0040"]
    K --> ML["ML / AI systems<br/>0031 · 0029"]
~~~

This does not mean every arrow is a strict reading prerequisite. It shows conceptual dependency/benefit.

## Priority assessment

There is no canonical registry priority field, so this is analytical only.

For an infrastructure/operations trajectory, the book has:

- High conceptual value
- Medium direct command/runbook value
- High architecture/reliability value
- High incident-analysis value
- High long-term reread/reference value

The most reusable chapters for operations are 1, 4–9, 11–12.

The chapters most likely to need complementary practical labs are 3, 5–9 and 11.

## What should not be changed in registry

No change is recommended to:

- inventory number;
- knowledge_id;
- direction;
- bibliographic metadata;
- reading lifecycle state.

Reason: book-level synthesis adds knowledge artifacts, not new inventory facts.

## Final placement verdict

Within biblioteka-vsp, this book should be treated as a core architecture bridge between infrastructure operations and distributed/data-system engineering.

It is not the endpoint of the library path. It is the conceptual layer that makes subsequent Kubernetes, observability, distributed systems, databases and data/ML systems easier to reason about correctly.
