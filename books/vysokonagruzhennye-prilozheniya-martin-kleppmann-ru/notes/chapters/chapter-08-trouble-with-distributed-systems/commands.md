# Source-confirmed APIs, pseudocode and tools — глава 8

Глава концептуальная и не дает универсальных shell/admin commands. Ниже только явно подтвержденные APIs, protocols, algorithms и pseudocode.

## Real-time clock APIs

Источник: `p0339:c01`–`p0340:c01`, PDF 339–340.

~~~text
clock_gettime(CLOCK_REALTIME)
System.currentTimeMillis()
~~~

Тип: read-only time API.

Смысл:

- возвращают wall-clock / calendar time;
- могут зависеть от clock synchronization;
- wall clock может прыгнуть назад/вперед;
- не подходят для надежного измерения elapsed duration.

Verification: не использовать difference wall-clock values как единственный elapsed-time source при возможной clock correction.

Rollback: `[Not applicable]`.

## Monotonic clock APIs

Источник: `p0340:c01`, PDF 340.

~~~text
clock_gettime(CLOCK_MONOTONIC)
System.nanoTime()
~~~

Тип: read-only time API.

Смысл:

- предназначены для измерения duration;
- гарантированно движутся вперед в пределах предоставляемой system abstraction;
- absolute values между machines сравнивать бессмысленно.

Verification: timeout/duration вычисляется как difference двух readings одного monotonic clock.

Rollback: `[Not applicable]`.

## NTP

Источник: `p0339:c01`, `p0360:c01`.

Тип: synchronization protocol / operational dependency.

Source-confirmed points:

- NTP синхронизирует time-of-day clocks с внешними time servers;
- точность ограничена network delay, local oscillator drift и source accuracy;
- source рекомендует несколько NTP servers и majority agreement, чтобы один ошибочный server можно было исключить.

Concrete NTP configuration command в chapter RAG отсутствует.

Verification: clock uncertainty/offset должен быть наблюдаем; наличие NTP само по себе не доказывает точность timestamps.

Rollback: concrete config rollback `[Needs confirmation]`.

## Lease pseudocode

Источник: `p0348:c01`, PDF 348.

Source pseudocode описывает цикл:

~~~text
receive request
check remaining lease time
renew lease if near expiry
process request only if lease is valid
~~~

Тип: state-changing control-flow example.

Risk:

- lease expiry может проверяться по несинхронизированному wall clock;
- process может pause после проверки lease и возобновиться уже после expiry;
- старый holder способен продолжить работу после передачи lease другому node.

Verification: lease protection должна тестироваться с long process pause и failover.

Rollback: `[Needs confirmation]`.

## Fencing token

Источник: `p0356:c01`, PDF 356.

Conceptual protocol:

~~~text
lock/lease grant → monotonically increasing fencing token
client write → include token
resource → remember highest token seen
resource → reject lower/older token
~~~

Тип: state-changing coordination mechanism.

Source example:

~~~text
client 1 token = 33
client 2 token = 34
later write with token 33 → reject
~~~

Verification:

- token monotonically increases;
- downstream resource enforces ordering;
- stale lease holder cannot modify protected resource.

Rollback: removal of fencing weakens safety; universal rollback procedure `[Needs confirmation]`.

## Phi Accrual failure detector

Источник: `p0335:c01`, PDF 335.

Тип: adaptive failure-detection mechanism.

Source point: вместо fixed timeout можно непрерывно измерять response time/jitter и адаптировать suspicion threshold к observed latency distribution.

Source examples: Akka и Cassandra.

Concrete configuration syntax в chapter RAG отсутствует.

## Chaos Monkey

Источник: `p0331:c01`, PDF 331.

Тип: fault-injection tool/concept.

Source use: deliberately provoke failures to verify system recovery instead of assuming the error path works.

Concrete invocation/configuration chapter RAG не приводит.

## Checksums and input validation

Источник: `p0360:c01`, PDF 360.

Тип: validation mechanisms.

Source-confirmed examples:

- application-level checksum can catch corruption missed by lower layers;
- validate input ranges and string lengths;
- protocol parsing should reject malformed values.

Concrete implementation command: `[Needs confirmation]`.

## Named mechanisms/tools

- TCP / UDP;
- ICMP;
- NTP;
- Phi Accrual failure detector;
- Chaos Monkey;
- ZooKeeper;
- TrueTime;
- GPS receiver / atomic clock as precise time sources.

## Что не добавлено

- `ping`, `traceroute`;
- `chronyc`, `ntpq`, `timedatectl`;
- Linux `tc/netem`;
- ZooKeeper CLI;
- Cassandra/Akka failure-detector configuration;
- cloud fault-injection commands.

Они не подтверждены chapter RAG.
