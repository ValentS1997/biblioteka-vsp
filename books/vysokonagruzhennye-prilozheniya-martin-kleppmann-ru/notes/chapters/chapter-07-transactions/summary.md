# Резюме главы 7

Источник: раздел 7.4 «Резюме», `p0314:c01`–`p0316:c01`, PDF 314–316.

Транзакции — это слой абстракции, позволяющий приложению не обрабатывать вручную часть hardware/software failures и concurrency problems.

Широкий класс ошибок сводится к transaction abort, после которого приложение может повторить operation. Для простых access patterns транзакции могут быть необязательны, но при сложных multi-object operations они значительно уменьшают число возможных failure scenarios.

## Anomalies

Глава рассматривает несколько типов concurrency anomalies.

### Dirty read

Один client читает data, записанные другой transaction до ее commit.

Read committed и более сильные уровни предотвращают dirty reads.

### Dirty write

Один client перезаписывает uncommitted write другого.

Практически все transactional implementations предотвращают dirty writes.

### Read skew / nonrepeatable read

Client видит разные части БД по состоянию на разные моменты.

Snapshot isolation дает consistent snapshot и обычно реализуется через MVCC.

### Lost update

Два clients выполняют read-modify-write; поздняя запись затирает изменение первой.

Меры включают atomic operations, explicit locks и automatic lost-update detection в некоторых systems.

### Write skew

Transactions читают одни и те же исходные данные, но записывают разные objects и вместе нарушают invariant.

Snapshot isolation само по себе write skew не предотвращает. Требуется serializability или carefully designed locking/materialized conflict.

### Phantom

Одна transaction выполняет predicate query, а другая write меняет множество rows, которые этому predicate соответствуют.

Для serializable 2PL применяются predicate/index-range locks; SSI обнаруживает опасные serialization dependencies оптимистически.

## Serializable isolation

Глава рассматривает три подхода.

1. **Actual serial execution.** Transactions выполняются по одной. Подходит, если transactions короткие и active data можно быстро обработать; throughput ограничен execution capacity одного thread/partition.
2. **Two-phase locking (2PL).** Readers/writers блокируют конфликтующие operations. Сильная защита ценой lock waits, deadlocks и нестабильной tail latency.
3. **Serializable snapshot isolation (SSI).** Использует MVCC snapshot reads и optimistic conflict detection. Transactions не блокируются заранее; если перед commit обнаружена non-serializable history, transaction aborts.

SSI особенно зависит от contention и длительности read-write transactions: высокий conflict rate увеличивает число abort/retries.

## ACID

Глава отдельно уточняет смысл ACID:

- atomicity — abortability при partial failure;
- consistency — application invariants, а не магическая гарантия БД;
- isolation — защита от concurrency anomalies;
- durability — сохранение committed data в рамках storage/replication mechanisms, но не абсолютная физическая гарантия.

## Итог

Слабый isolation level может быть корректным выбором, если приложение знает оставшиеся anomalies и явно их предотвращает. Если reasoning о races становится сложным, serializable isolation уменьшает пространство возможных ошибок.

Следующая глава по boundary evidence `p0323:c01` переходит к failures, uncertainty и timing problems распределенных систем.
