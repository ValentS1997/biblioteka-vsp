# Резюме главы 3

Источник: раздел 3.4 «Резюме», `p0135:c01`–`p0136:c01`, PDF 135–136.

Глава рассматривает, как БД сохраняют данные и затем извлекают их по запросу.

На высоком уровне storage systems разделяются на две широкие категории:

- оптимизированные для transaction processing (OLTP);
- оптимизированные для analytics (OLAP).

## OLTP

OLTP-системы обслуживают большое количество пользовательских запросов. Один запрос обычно затрагивает небольшое количество records и находит их через index.

Глава рассматривает две основные storage philosophies.

### Log-structured

Данные дописываются в files/segments, а устаревшие segments позднее сливаются и удаляются.

К этому семейству относятся идеи, представленные через Bitcask, SSTables, LSM-trees, LevelDB, HBase и Lucene.

Основная идея: превращать random writes в преимущественно sequential writes через append, sorted immutable segments и background compaction.

### Page-oriented

Диск представляется набором pages фиксированного размера, которые можно обновлять на месте.

Ключевой пример — B-tree, широко применяемый в relational и многих non-relational databases.

B-tree требует WAL для recovery при частично выполненных page updates.

## Дополнительные индексы

Глава также рассматривает secondary/clustered/covering indexes, multi-dimensional indexes, full-text/fuzzy search и in-memory databases.

Общий принцип остается тем же: index ускоряет определенные reads, но требует дополнительных storage/write resources.

## OLAP и warehouses

Analytical systems выполняют меньше запросов, но каждый query обычно просматривает очень большой объем данных и вычисляет aggregates.

Поэтому bottleneck отличается от OLTP:

- OLTP: важен быстрый переход к небольшому числу records;
- OLAP: важна пропускная способность sequential scan и минимизация объема данных, который приходится читать.

Отдельный data warehouse позволяет выполнять analytical workload без влияния на production OLTP. Данные поступают в warehouse через ETL.

Star/snowflake schemas организуют факты и измерения для аналитического доступа.

## Column-oriented storage

Если query использует только небольшое число columns из очень wide table, column storage позволяет читать только нужные columns.

Дополнительные механизмы:

- column compression;
- sort order;
- vectorized processing;
- in-memory write buffer с последующим merge;
- materialized views;
- OLAP cubes.

Materialized aggregates ускоряют заранее известные query patterns, но увеличивают стоимость updates.

## Итог

Storage engine нельзя выбирать вне контекста workload. Знание внутренних механизмов позволяет понять, почему изменение index, compaction, page layout, column layout или warehouse architecture влияет на performance.

Следующая глава по boundary evidence `p0143:c01` переходит к кодированию данных, evolution и compatibility.
