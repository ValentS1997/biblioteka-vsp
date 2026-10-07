# Команды и примеры главы 3

Включены только команды и запросы, явно подтвержденные chapter RAG. Современные product-specific команды настройки storage engines не добавлялись.

## Bash: простейшее key-value storage

Источник: `p0098:c01`, PDF 98.

~~~bash
#!/bin/bash

db_set () {
    echo "$1,$2" >> database
}

db_get () {
    grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
~~~

### `db_set key value`

Тип: state-changing.

Effect: дописывает новую строку `key,value` в конец файла `database`.

Риск:

- файл растет при каждом update;
- старые значения остаются в журнале;
- пример не содержит concurrency/recovery protection настоящей БД.

Verification:

~~~bash
db_get <key>
~~~

или source-confirmed inspection:

~~~bash
cat database
~~~

Rollback: в главе не описан — `[Needs confirmation]`.

### `db_get key`

Тип: read-only / workload-generating.

Effect: сканирует файл, выбирает строки по ключу, удаляет prefix `key,` и возвращает последнее значение.

Source observation: поиск требует scan всего файла и имеет порядок сложности `O(n)`.

Rollback: `[Not applicable]`.

## Source examples

~~~bash
db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}'
db_set 42 '{"name":"San Francisco","attractions":["Golden Gate Bridge"]}'
db_get 42
~~~

Ожидаемый source result:

~~~json
{"name":"San Francisco","attractions":["Golden Gate Bridge"]}
~~~

После нового значения:

~~~bash
db_set 42 '{"name":"San Francisco","attractions":["Exploratorium"]}'
db_get 42
cat database
~~~

Последний `db_get 42` возвращает последнее записанное значение, а `cat database` показывает как старую, так и новую запись.

## `cat database`

Тип: read-only.

Effect: выводит append-only file целиком.

Verification: все дописанные строки видимы в порядке записи.

Rollback: `[Not applicable]`.

## SQL: analytical query

Источник: `p0127:c01`, PDF 127.

~~~sql
SELECT
  dim_date.weekday, dim_product.category,
  SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
  JOIN dim_date    ON fact_sales.date_key   = dim_date.date_key
  JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk
WHERE
  dim_date.year = 2013 AND
  dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY
  dim_date.weekday, dim_product.category;
~~~

Тип: read-only analytical query.

Что показывает:

- query касается большого количества fact rows;
- реально использует ограниченный набор columns;
- joins связывают fact table с dimensions;
- aggregation выполняется по weekday/category.

Verification: result содержит aggregated `quantity_sold` по комбинациям weekday/category для заданных фильтров.

Rollback: `[Not applicable]`.

## Source-confirmed structures/tools

Глава обсуждает, но не дает универсальных admin-команд для:

- hash indexes;
- Bitcask;
- SSTables / MemTable;
- LSM-trees;
- Bloom filters;
- LevelDB / RocksDB / Cassandra / HBase;
- B-trees и WAL;
- clustered / covering indexes;
- Lucene full-text indexes;
- in-memory databases;
- ETL;
- star/snowflake schemas;
- column stores;
- materialized views;
- OLAP cubes.

## Что не добавлено

- `CREATE INDEX` / `DROP INDEX`;
- compaction commands;
- RocksDB/Cassandra tuning flags;
- WAL recovery commands;
- database backup/restore;
- warehouse ETL tooling commands.

Chapter RAG описывает механизмы и trade-offs, но не дает единый operational syntax для этих действий.
