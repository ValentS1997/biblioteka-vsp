# Команды и инструменты главы 6

## Статус

Глава описывает partitioning algorithms, rebalancing и routing mechanisms, но не дает универсальных ready-to-run CLI-команд.

Ниже зафиксированы только source-confirmed parameters, formulas, mechanisms и named tools.

## Hash partitioning

Источник: `p0243:c01`–`p0245:c01`, PDF 243–245.

Conceptual mapping:

~~~text
partition = range_of(hash(key))
~~~

Тип: configuration/data-placement model.

Source warning: встроенные process-local hash functions могут быть непригодны, если один и тот же key получает разные hash values в разных processes.

Verification: одинаковый key должен стабильно отображаться в одну и ту же partition в пределах выбранной distributed hash scheme.

Rollback: `[Needs confirmation]`.

## Не использовать hash(key) mod N для изменяемого N

Источник: `p0250:c01`–`p0251:c01`, PDF 250–251.

Source example:

~~~text
hash(key) = 123456
123456 mod 10 = 6
123456 mod 11 = 3
123456 mod 12 = 0
~~~

Тип: design example / non-executing.

Effect: изменение числа nodes `N` remap'ит большую часть keys, что делает rebalancing дорогим.

Verification: при добавлении node сравнить долю keys, которые должны сменить placement.

Rollback: `[Not applicable]` для вычисления; migration design `[Needs confirmation]`.

## Fixed partition count

Источник: `p0251:c01`–`p0252:c01`.

Source example:

~~~text
10 nodes
1000 partitions
100 partitions per node
~~~

Тип: configuration model.

Effect: при добавлении node whole partitions передаются между nodes, а key→partition mapping не меняется.

Verification: после rebalance partitions распределены равномернее; reads/writes продолжаются во время перемещения.

Rollback: placement rollback `[Needs confirmation]`.

## Dynamic partitioning

Источник: `p0252:c01`–`p0253:c01`.

Тип: state-changing background mechanism.

Source-confirmed behavior:

- partition, выросшая выше threshold, split на две;
- слишком маленькие соседние partitions могут merge;
- часть split partition может быть перенесена на другой node;
- empty database может потребовать pre-splitting.

Verification: partition sizes остаются в заданных системой пределах; load распределяется после split/move.

Rollback: `[Needs confirmation]`.

## Hot-key spreading

Источник: `p0246:c01`, PDF 246.

Conceptual example:

~~~text
hot_key + random two-digit suffix
→ up to 100 derived keys
~~~

Тип: state-changing application data-model technique.

Effect: writes для одного hot key распределяются по нескольким keys/partitions.

Risk: reads должны читать и объединять derived keys; нужно отслеживать, какие keys были split.

Verification: write load распределен, а merged read дает исходно ожидаемый logical result.

Rollback: migration back to one key `[Needs confirmation]`.

## Request routing mechanisms

Источник: `p0255:c01`–`p0258:c01`.

Source-confirmed варианты:

1. client обращается к любому node, node при необходимости forwards request;
2. dedicated routing tier направляет request нужному node;
3. partition-aware client обращается напрямую.

Named tools/services:

- ZooKeeper;
- Helix;
- MongoDB config servers / mongos;
- gossip protocols;
- moxi;
- DNS.

Тип: routing/control-plane mechanisms.

Verification: routing component знает актуальное partition→node mapping.

Rollback: product-specific `[Needs confirmation]`.

## Что не добавлено

- MongoDB sharding commands;
- Cassandra token commands;
- Elasticsearch reroute API calls;
- ZooKeeper CLI;
- HBase split commands;
- Couchbase rebalance commands.

Concrete operational syntax отсутствует в chapter RAG и не добавлен из model memory.
