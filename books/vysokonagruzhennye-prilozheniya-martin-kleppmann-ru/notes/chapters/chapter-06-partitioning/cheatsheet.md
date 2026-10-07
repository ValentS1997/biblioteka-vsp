# Шпаргалка главы 6 — partitioning

## Symptom / problem framing

Проблема главы: dataset или request volume перестает помещаться на одной машине. Простое разделение данных бесполезно, если отдельные partitions становятся hot spots или request routing не знает актуального placement.

Негативные сигналы:

- один partition получает непропорционально много data или requests;
- timestamp-first key направляет все текущие writes в одну partition;
- range query после hash partitioning вынуждена обращаться ко всем partitions;
- secondary-index query делает scatter/gather по всему кластеру;
- изменение количества nodes заставляет перемещать почти все keys;
- rebalancing перегружает сеть и nodes;
- automatic failure detection запускает rebalancing на просто медленном node;
- client использует устаревшую partition map.

## Baseline / context

### Range partitioning

- partition соответствует диапазону key values;
- keys внутри partition можно хранить sorted;
- эффективны range scans;
- границы partitions должны соответствовать реальному distribution;
- sequential/time-based access может создать hot spot.

### Hash partitioning

- hash(key) определяет partition;
- load распределяется равномернее;
- key order теряется;
- range query по partition key становится неэффективной.

### Composite key

- первая часть может определять partition;
- остальные части — sort order внутри partition;
- источник приводит Cassandra как пример такого компромисса.

### Secondary indexes

- document-partitioned/local: write затрагивает одну partition, read может требовать scatter/gather;
- term-partitioned/global: read идет к partition нужного term, write может обновлять несколько index partitions.

## Read-only checks

1. Определить dataset size и request volume.
2. Зафиксировать текущий partition key.
3. Измерить data distribution по partitions.
4. Измерить request distribution по partitions.
5. Найти hot partitions/hot keys.
6. Проверить тип запросов:
   - point lookup;
   - range scan;
   - secondary-index lookup;
   - analytical multi-partition query.
7. Проверить, где нужен sorted key order.
8. Для secondary indexes определить local или global strategy.
9. Проверить долю scatter/gather reads.
10. Проверить текущий rebalancing model:
    - fixed partitions;
    - dynamic split/merge;
    - partitions proportional to nodes.
11. Проверить, не используется ли `hash(key) mod N`.
12. Проверить автоматизацию rebalancing и failure detection.
13. Проверить актуальность partition→node metadata.
14. Проверить routing path: node forwarding, routing tier или partition-aware client.

## Interpretation

- Один partition горячий по data volume → data skew.
- Data распределены равномерно, но один key очень популярен → request skew/hot key.
- Timestamp-first range partition перегружает текущий time range → partition key создает write hot spot.
- Hash partitioning устраняет range locality → это ожидаемый trade-off, а не дефект.
- Local secondary index → write проще, read дороже из-за scatter/gather.
- Global secondary index → read проще, write становится distributed и может быть asynchronous.
- Modulo N при изменении N → массовое remapping keys и дорогой rebalance.
- Auto-rebalance начинается на перегруженном node → риск positive feedback/cascading failure.
- Routing component имеет stale map → запрос может уйти не в тот node.

## Next action

1. Снять partition/load distribution.
2. Классифицировать hot spot: data skew, request skew или hot key.
3. Проверить access patterns и secondary indexes.
4. Выбрать минимальную partition/rebalancing hypothesis.
5. Выполнить контролируемое изменение.
6. Повторить те же workload measurements.
7. Оставить изменение только при выполнении acceptance criteria.

## Modifying action

Source-confirmed изменения:

- изменить partition boundaries;
- перейти между range/hash strategy;
- изменить composite key design;
- распределить hot key на несколько synthetic keys;
- split/merge dynamic partition;
- переместить whole partitions между nodes;
- добавить/remove node и выполнить rebalance;
- переключить local/global secondary-index strategy;
- изменить routing/partition metadata mechanism.

Конкретный product CLI syntax глава не предоставляет.

## Verification / acceptance checks

### Partition balance

- data volume распределен приемлемо;
- request load распределен приемлемо;
- hot spot устранен или контролируем;
- range-query performance не ухудшилась сверх цели.

### Rebalancing

- reads/writes продолжают обслуживаться;
- перемещается минимально необходимый объем data;
- network/disk load остается в приемлемых пределах;
- после rebalancing partitions распределены равномернее.

### Secondary index

- local-index scatter/gather latency приемлема;
- global-index write cost приемлем;
- asynchronous global-index staleness соответствует application semantics.

### Routing

- partition map актуальна;
- request попадает в правильный node;
- routing metadata обновляется после node/partition changes.

## Rollback

- Partition-key/schema rollback: конкретная migration procedure `[Needs confirmation]`.
- Rebalancing: вернуть прежнее placement возможно только product-specific способом — `[Needs confirmation]`.
- Routing change: вернуть предыдущий routing mechanism; конкретный syntax `[Needs confirmation]`.
- Read-only measurements: `[Not applicable]`.

## Operational loop

`distribution → hot-spot classification → partition hypothesis → controlled rebalance/change → remeasure → keep/rollback`.
