# Резюме главы 5

Source section: явное «Резюме» в `p0101:c01`.

Это структурированная передача source meaning, а не дословная копия.

## Основные тезисы

- Глава начинает с простого replicated stateless service за load balancer.
- Затем basic pattern расширяется дополнительными replicated/load-balanced layers.
- Cache layer добавляется для повышения performance.
- SSL bridge layer добавляется для защищенного client connection.
- Полная source architecture содержит три independently replicated tiers.
- В Kubernetes глава представляет эту структуру через три Deployment objects и три load-balancing Service objects.

## Provenance

- chunk: `distributed-systems-patterns-brendan-burns-ru:p0101:c01`
- PDF page: `101`
- Source SHA-256: `d4529f6267d0fe16d411c912a1ecc7ab4924530c376103ce5f16067aca337aa5`
