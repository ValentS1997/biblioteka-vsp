# Диаграммы главы 12 — StatefulSet, PVC, DNS и upgrade

**Источник:** RAG PDF 420–456, `p0420:c01`–`p0456:c01`. Диаграммы синтезированы из текста главы, не являются копией PDF-рисунков.

## Идентичность Pod и отдельные PVC

```mermaid
flowchart TD
  S["StatefulSet mysql-stateful replicas=3"]
  H["Headless Service: mysql-headless clusterIP None"]
  S --> A["Pod mysql-stateful-0"]
  S --> B["Pod mysql-stateful-1"]
  S --> C["Pod mysql-stateful-2"]
  H -.-> A
  H -.-> B
  H -.-> C
  A --> PA["PVC mysql-data-mysql-stateful-0"]
  B --> PB["PVC mysql-data-mysql-stateful-1"]
  C --> PC["PVC mysql-data-mysql-stateful-2"]
  PA --> VA["PV 0: backend"]
  PB --> VB["PV 1: backend"]
  PC --> VC["PV 2: backend"]
```

p0424–p0436. Каждый ordinal имеет **собственный** PVC. Подсистема StatefulSet не синхронизирует данные между PV/Pod (p0427). DNS-имена стабильны, IP могут меняться.

## OrderedReady vs Parallel

```mermaid
flowchart TD
  A["OrderedReady: Pod 0 готов"] --> B["Создать Pod 1"]
  B --> C["Pod 1 готов"] --> D["Создать Pod 2"]
  D --> E["Scale up: создать Pod 3"]
  E --> F["Scale down: удалить Pod 3"]
  F --> G["Затем удалить Pod 2"]
  P["Parallel policy"] --> Q["Масштабирование параллельно"]
  Q -.-> X["Не меняет порядок RollingUpdate"]
```

p0425, p0440–p0441. Для неизвестного кластера успешность Ready и время зависят от приложения и storage [Needs confirmation].

## Поэтапный rollout StatefulSet

```mermaid
flowchart TD
  A["3 Pod: MySQL 8.3.0"]
  B["Шаблон MySQL 8.4.0, partition=3"]
  C["Pod не обновляются"]
  D["partition=2"]
  E["Обновить только mysql-stateful-2"]
  F["Проверить mysql-stateful-2 Ready и состояние"]
  G{"Проверка успешна?"}
  H["partition=0: обновить mysql-stateful-1, затем -0"]
  I["Остановить выкатывание, анализ состояния"]
  A --> B --> C --> D --> E --> F --> G
  G -->|"Да"| H
  G -->|"Нет"| I
```

p0444–p0451. `partition` не является механизмом automatic data migration, reconciliation или backup; если обновление повреждает DB schema, обратный образ может быть несовместим (p0452).

## Reclaim / data-safety decision

```mermaid
flowchart TD
  A["План: уменьшить replicas или удалить StatefulSet"]
  B{"Retention policy проверена?"}
  C["Сверить whenScaled/whenDeleted, PV reclaim, backup"]
  D{"Есть подтверждённая процедура восстановления?"}
  E["Контролируемо изменять StatefulSet и повторно проверять Pod/PVC"]
  F["Блокировать разрушительные действия"]
  A --> B
  B -->|"Нет"| C --> D
  B -->|"Да"| D
  D -->|"Да"| E
  D -->|"Нет"| F
```

p0426–p0427, p0442–p0443, p0452–p0454. `kubectl delete pvc` при `reclaimPolicy: Delete` может уничтожить данные, **не** является rollback.

## Verification boundary

Книга показывает `ststest` после пересоздания `mysql-stateful-0`, но **не** проверяет данные на `-1`/`-2`, автоматическую репликацию, multi-node failure или disaster restore. Claim о сохранности одного тома нельзя расширять на состояние распределённой БД.
