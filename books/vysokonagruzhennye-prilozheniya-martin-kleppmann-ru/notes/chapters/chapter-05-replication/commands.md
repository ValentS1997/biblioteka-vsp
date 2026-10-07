# Команды и инструменты главы 5

## Статус

Глава описывает replication algorithms, guarantees и operational mechanisms, но не дает универсальных ready-to-run CLI-команд для конкретной СУБД.

Поэтому ниже фиксируются только source-confirmed параметры, механизмы и tools.

## Quorum parameters

Источник: `p0217:c01`–`p0218:c01`, PDF 217–218.

- `n` — число replicas, на которых хранится значение;
- `w` — минимальное число подтверждений write;
- `r` — минимальное число ответов read;
- базовое quorum condition: `w + r > n`.

Пример источника:

~~~text
n = 3
w = 2
r = 2
~~~

Тип: configuration model, не команда.

Risk: уменьшение `w`/`r` повышает availability/снижает latency, но увеличивает вероятность stale reads.

Verification: проверить фактическое число подтверждений и поведение при недоступной replica.

Rollback: вернуть предыдущие значения; product-specific syntax `[Needs confirmation]`.

## New follower procedure

Источник: `p0190:c01`, PDF 190.

Source-confirmed последовательность:

1. сделать consistent snapshot leader;
2. скопировать snapshot на новый follower;
3. связать snapshot с replication-log position;
4. запросить изменения после snapshot;
5. дождаться catch-up.

Тип: state-changing procedure.

Verification: follower достиг текущей replication position и продолжает применять новые changes.

Rollback: `[Needs confirmation]`.

## Failover procedure

Источник: `p0191:c01`–`p0192:c01`, PDF 191–192.

Source-confirmed логика:

1. определить недоступность leader;
2. выбрать/promote новый leader;
3. перенаправить writes клиентов;
4. перевести вернувшийся old leader в follower.

Тип: state-changing / availability-critical.

Risks:

- потеря нереплицированных writes;
- split brain;
- слишком агрессивный или слишком медленный failure timeout.

Verification: единственный active leader; clients пишут в него; followers реплицируются от него.

Rollback: универсальной процедуры глава не дает — `[Needs confirmation]`.

## Read repair

Источник: `p0216:c01`, PDF 216.

Тип: state-changing repair mechanism.

Effect: read нескольких replicas выявляет stale response, после чего более новое value записывается обратно в stale replica.

Verification: повторный read показывает convergence соответствующих replicas.

Rollback: `[Not applicable]` как обычная repair semantics; исправление ошибочно выбранного value зависит от application/version history — `[Needs confirmation]`.

## Anti-entropy

Источник: `p0216:c01`, PDF 216.

Тип: background state-changing repair mechanism.

Effect: background process сравнивает replicas и копирует отсутствующие данные.

Verification: divergence между replicas со временем уменьшается.

Rollback: `[Needs confirmation]`.

## Sloppy quorum / hinted handoff

Источник: `p0221:c01`–`p0222:c01`, PDF 221–222.

Тип: state-changing availability mechanism.

Effect:

- временно записывает значение на доступные non-home nodes;
- после восстановления связи передает данные home replicas.

Verification: hinted values в конечном итоге доставлены home replicas.

Risk: `w + r > n` при sloppy quorum не гарантирует немедленное чтение актуального значения из home set.

Rollback: `[Needs confirmation]`.

## Source-confirmed tools/technologies

Упомянуты как реализации/контекст, но без универсального CLI syntax:

- PostgreSQL;
- MySQL;
- Oracle Data Guard / GoldenGate;
- SQL Server AlwaysOn Availability Groups;
- MongoDB;
- RethinkDB;
- Espresso;
- Kafka;
- RabbitMQ;
- DRBD;
- Databus;
- Bucardo;
- Tungsten Replicator;
- BDR;
- Riak;
- Cassandra;
- Voldemort.

## Что не добавлено

- commands promotion/demotion;
- vendor-specific replication setup;
- SQL statements управления replication;
- Cassandra/Riak quorum CLI/API calls;
- monitoring queries;
- repair commands.

В chapter RAG их конкретного operational syntax нет.
