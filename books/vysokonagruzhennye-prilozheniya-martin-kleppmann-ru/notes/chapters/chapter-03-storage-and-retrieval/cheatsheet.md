# Шпаргалка главы 3 — storage engines и retrieval

## Symptom / problem framing

Проблема главы: одна и та же БД должна сохранять данные и потом быстро находить их, но оптимизация записи, точечного чтения и аналитического сканирования требует разных структур.

Негативные сигналы:

- append-only storage пишет быстро, но поиск деградирует до полного scan;
- индексы ускоряют чтение, но делают запись дороже;
- storage engine выбран без representative workload;
- аналитические запросы конкурируют с OLTP;
- wide row storage читает множество ненужных столбцов;
- recovery path не соответствует модели записи.

## Baseline / context

### Log-structured

- новые данные дописываются;
- immutable segments могут сливаться и уплотняться;
- SSTable хранит пары key/value в sorted order;
- MemTable — sorted in-memory structure;
- WAL защищает данные MemTable от потери при crash;
- LSM-tree объединяет SSTables через background compaction;
- Bloom filter уменьшает лишние чтения при запросе отсутствующего ключа.

### B-tree

- storage разбит на fixed-size pages;
- дерево balanced;
- update существующего ключа приводит к изменению page;
- page split поддерживает рост дерева;
- WAL/redo log записывает изменения до изменения pages;
- concurrent access требует synchronization/latches.

### OLTP

- много запросов;
- каждый query обычно касается небольшого количества records;
- lookup по ключу/индексу;
- важна low latency.

### OLAP

- запросов меньше;
- каждый query просматривает очень много records;
- часто используются aggregate functions;
- bottleneck чаще связан с объемом читаемых данных и disk bandwidth.

## Read-only checks

1. Определить workload: OLTP, OLAP или смешанный.
2. Зафиксировать read/write ratio.
3. Определить query shape:
   - point lookup;
   - range scan;
   - full-text/fuzzy search;
   - wide analytical scan;
   - aggregation.
4. Проверить существующие indexes и их назначение.
5. Проверить, какие writes дополнительно требуют обновления indexes.
6. Для LSM-подобной системы оценить:
   - MemTable;
   - количество/уровни SSTables;
   - compaction;
   - Bloom filters;
   - WAL/recovery path.
7. Для B-tree оценить:
   - page access;
   - splits;
   - WAL;
   - clustered/secondary/covering indexes.
8. Для analytics проверить:
   - сколько columns реально читает типичный query;
   - нужен ли отдельный warehouse;
   - schema: star/snowflake;
   - column compression;
   - sort order;
   - materialized aggregates.
9. Benchmark выполнять на конкретной рабочей нагрузке: глава прямо предупреждает, что общие оценки LSM vs B-tree недостаточны.

## Interpretation

- Append path быстрый, lookup делает O(n) scan → нужен index.
- Набор ключей помещается в RAM и нужен direct key lookup → hash index может быть уместен.
- Нужны sorted range queries и высокий write throughput → LSM/SSTable architecture предоставляет соответствующие свойства.
- Read path вынужден проверять много SSTables → compaction/Bloom-filter behavior становится важным.
- Нужны предсказуемые indexed reads → B-tree является основным page-oriented вариантом.
- B-tree write требует WAL и coordinated page update → crash recovery нельзя отделять от storage layout.
- OLTP и OLAP имеют одинаковый SQL surface, но разный access pattern → одинаковая storage architecture не обязана быть оптимальной.
- Query читает 4–5 columns из wide fact table → column storage уменьшает объем чтения.
- Одни aggregates повторяются часто → materialized view/cube может ускорить reads ценой дополнительных writes.

## Next action

1. Снять representative workload.
2. Классифицировать запросы по access pattern.
3. Найти реальный bottleneck.
4. Сформулировать storage/index hypothesis.
5. Выполнить минимальное контролируемое изменение.
6. Повторить тот же benchmark/query set.
7. Сохранить изменение только при выполнении acceptance criteria.

## Modifying action

Source-confirmed изменения:

- `db_set` добавляет новую key/value запись в append-only файл;
- добавление/удаление индекса меняет performance/storage overhead, но не основное содержимое данных;
- MemTable flush создает новый SSTable segment;
- compaction создает новые merged segments и удаляет устаревшие;
- B-tree update меняет pages и предварительно требует WAL;
- ETL загружает transformed data в warehouse;
- materialized view хранит физическую копию query result.

Для production-команд этих операций глава не дает конкретного универсального синтаксиса.

## Verification / acceptance checks

### Index/storage change

- тот же representative query set выполняется быстрее или стабильнее;
- write overhead не превысил допустимый уровень;
- recovery path остается корректным;
- данные после crash/restart доступны согласно выбранной durability model.

### OLTP

- point/key lookups соответствуют latency target;
- write throughput соответствует нагрузке;
- indexes не создают неоправданный write overhead.

### OLAP

- query читает только необходимые columns;
- scan volume уменьшен;
- compression/sort order соответствует query pattern;
- warehouse workload не мешает production OLTP;
- materialized aggregates действительно ускоряют целевые запросы.

## Rollback

- Read-only queries: `[Not applicable]`.
- Добавленный index: source допускает удаление индексов; конкретная команда `[Needs confirmation]`.
- `db_set`: удаление/возврат записи в Bash-примере не описаны — `[Needs confirmation]`.
- Compaction/LSM/B-tree internal changes: rollback как ручная операция не описан — `[Needs confirmation]`.
- ETL/materialized view: конкретный rollback `[Needs confirmation]`.

## Operational loop

`workload → access pattern → storage/index hypothesis → benchmark → controlled change → remeasure → keep/rollback`.
