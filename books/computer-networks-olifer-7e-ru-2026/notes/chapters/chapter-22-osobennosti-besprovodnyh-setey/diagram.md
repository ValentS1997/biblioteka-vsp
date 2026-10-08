# Diagram — Глава 22. Беспроводные сети

RAG: PDF pages 662–686, p0662:c01–p0686:c01, strict rag_only. Mermaid представляет **аналитическую схему по тексту**. Это не реальная топология и не воссоздание авторских рисунков 22.1–22.7.

## Радиосреда, покрытие и логические связи

~~~mermaid
flowchart TD
  ENV["Радиосреда: шум, препятствия, интерференция"] --> PHY["Изменяемые параметры PHY и качества линии"]
  PHY --> COV["RF coverage / взаимная досягаемость"]
  COV --> P["Физически возможные связи"]
  P --> LOG["Логические связи: политика/режим сети"]
  LOG --> S["Infrastructure Wi-Fi: AP и клиенты, звезда"]
  LOG --> M["Mesh: многошаговые маршруты"]
  ENV --> MAC["Разделяемый канал / арбитраж доступа"]
  MAC --> H["Hidden station: риск одновременной передачи к одному приёмнику"]
  MAC --> E["Exposed station: передача откладывается, хотя может не мешать"]
~~~

[p0664](../../../rag/chunks/p0601-p0700/p0664-c01.md)–[p0670](../../../rag/chunks/p0601-p0700/p0670-c01.md). Конкретная буквенная топология hidden station на p0668 конфликтует с её же описанием: source-findings.md.

## Infrastructure, infrastructureless и Ad Hoc

~~~mermaid
flowchart TD
  N["Беспроводная сеть"] --> I{"Предустановленная инфраструктура?"}
  I -->|Есть| INF["AP/BS/route services, централизованные роли"]
  I -->|Нет| PEER["Конечные узлы координируются самостоятельно"]
  PEER --> Q{"Спонтанная самоорганизация?"}
  Q -->|Да| A["Ad Hoc: discovery, association, self config, routing"]
  Q -->|Нет| P["Плановая infrastructureless сеть"]
  A --> C["MANET / VANET / FANET / некоторые WSN"]
  N --> HY["Гибридные архитектуры возможны"]
~~~

[p0671](../../../rag/chunks/p0601-p0700/p0671-c01.md)–[p0676](../../../rag/chunks/p0601-p0700/p0676-c01.md), [p0684](../../../rag/chunks/p0601-p0700/p0684-c01.md).

## Mobility, security, energy: разные ограничения

~~~mermaid
flowchart TD
  D["Передвижение / изменение радиоусловий"] --> X["PHY, IP, transport или приложение компенсирует изменения"]
  X --> Z["Цель: поддержать требуемый сервис"]
  R["Радио за пределами контролируемого помещения"] --> SEC["Прослушивание / rogue AP / jamming"]
  SEC --> AU["Разделить шифрование, authentication и availability"]
  B["Батарейный узел"] --> SLEEP["Sleep / ограничение времени активности"]
  B --> PWR["TX power vs retries"]
  B --> ROUTE["Routing учитывает hops, остаточный заряд, aggregation"]
~~~

[p0677](../../../rag/chunks/p0601-p0700/p0677-c01.md)–[p0683](../../../rag/chunks/p0601-p0700/p0683-c01.md).

**Verification:** фактические RSSI/SNR, wireless auth, retries, channel utilization, маршруты/заряд и время жизни сети не предоставлены: [Needs confirmation]. **Rollback:** [Needs confirmation]. Схемы не предлагают state-changing конфигураций.
