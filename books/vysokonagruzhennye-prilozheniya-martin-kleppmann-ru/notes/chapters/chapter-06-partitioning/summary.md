# Резюме главы 6

Источник: раздел 6.6 «Резюме», `p0259:c01`–`p0260:c01`, PDF 259–260.

Глава рассматривает способы разбить большой dataset на partitions, когда его уже нельзя эффективно хранить и обрабатывать на одной машине.

## Цель

Partitioning должен равномерно распределить:

- data volume;
- read load;
- write load.

Неравномерность создает skew, а partition с непропорциональной нагрузкой становится hot spot.

## Основные подходы

### Range partitioning

Keys сортируются, и каждая partition получает непрерывный key range.

Плюс — эффективные range queries.

Минус — близкие по sort order keys могут концентрировать load и создавать hot spots.

Обычно range partitions можно динамически split/merge при изменении размера.

### Hash partitioning

Для key вычисляется hash; partitions соответствуют hash ranges.

Плюс — более равномерное распределение keys.

Минус — теряется natural ordering и ухудшаются range queries.

При hash partitioning часто используется fixed number of partitions с перемещением whole partitions между nodes во время rebalance.

### Hybrid

Composite key может использовать одну часть для выбора partition и другую для сортировки внутри partition.

## Secondary indexes

Два базовых подхода:

- document-partitioned/local index: write касается одной partition, но read может потребовать scatter/gather по всем partitions;
- term-partitioned/global index: read для term может обслуживаться одной index partition, но write затрагивает несколько partitions.

## Rebalancing

При добавлении/удалении nodes или росте load данные нужно перераспределять.

Хороший rebalance:

- делает load равномернее;
- сохраняет availability для reads/writes;
- перемещает не больше data, чем необходимо.

Глава отдельно предупреждает против `hash(key) mod N`: изменение `N` приводит к массовому remapping.

## Routing

После partitioning client должен знать, где находится нужная partition.

Варианты:

- отправить request любому node и позволить forwarding;
- использовать routing tier;
- сделать client partition-aware.

Metadata о placement должна обновляться вместе с rebalancing; source приводит coordination services и gossip как разные способы распространения этой информации.

## Итог

Partitioning масштабирует data и query throughput за счет независимости partitions, но переносит сложность в выбор key, secondary indexes, rebalancing и routing.

Следующая глава по boundary evidence `p0265:c01` переходит к транзакциям и проблеме операций, затрагивающих несколько objects/partitions.
