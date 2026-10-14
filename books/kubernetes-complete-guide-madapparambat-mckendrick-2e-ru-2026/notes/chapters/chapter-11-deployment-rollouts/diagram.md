# Диаграммы главы 11 — Deployment / Service / rollout

**RAG-only:** PDF/printed p0384–p0419, chunks p0384:c01–p0419:c01. Mermaid концептуально воспроизводит извлечённый текст, не точные рисунки PDF.

## Контроллеры и Service

```mermaid
flowchart TD
  G["Git/YAML: Deployment desired state"] --> D["Deployment"]
  D --> R["ReplicaSet: replicas=N, pod-template-hash"]
  R --> A["Pod A"]
  R --> B["Pod B"]
  R --> C["Pod C"]
  S["Service: selector app=nginx, environment=test"] --> A
  S --> B
  S --> C
  Q["ReadinessProbe: /ready"] --> A
  Q --> B
  Q --> C
  X["Client / cluster DNS"] --> S
```

RAG p0387–p0395, p0397–p0402. Стрелки Service → Pod означают пригодные по labels **и готовности** endpoints; при failed readiness Pod остаётся Running, но исключается из Service endpoints. Реальный target cluster/Service admission [Needs confirmation].

## RollingUpdate: изменение шаблона

```mermaid
flowchart TD
  A["Deployment: replicas=3, nginx:1.17"]
  B["Изменение image на nginx:1.18"]
  C["Новый ReplicaSet: initially 0 replicas"]
  D["maxSurge=1: до 4 Pod"]
  E["maxUnavailable=1: не более 1 недоступного из 3"]
  F["Проверка ready и minReadySeconds=10"]
  G["Новый RS: 3 Pod, старый RS: 0 Pod"]
  H["rollout status + history"]
  A --> B --> C --> D --> E --> F --> G --> H
```

RAG p0405–p0409. `Recreate` в книге завершает все старые Pod до создания новых и допускает downtime; **не** объявлять RollingUpdate гарантией измеренного нулевого простоя.

## Диагностика readiness

```mermaid
flowchart TD
  A["kubectl describe svc nginx-service-example"]
  B{"Все ожидаемые Endpoints готовы?"}
  C["kubectl describe pod: Readiness failed?"]
  D["Проверить /ready в приложении"]
  E["Source test: rm ready в одном Pod"]
  F["Endpoints: 3 → 2; Pod Running, NotReady"]
  G["Source restore: touch ready"]
  H["Повторная проверка Endpoints и curl"]
  A --> B
  B -->|"Нет"| C --> D
  B -->|"Да"| H
  D --> E --> F --> G --> H
```

p0397–p0402. `rm` и `touch` внутри контейнера — **state-changing, destructive test**, не безопасная диагностика реального workload. Имена Pod и IP источника — не идентификаторы текущего кластера.

## Rollout / rollback / canary

```mermaid
flowchart TD
  A["Git manifest или set image"] --> B["Deployment: новая ревизия"]
  B --> C["rollout status; проверка Pod/Service"]
  C --> D{"Новая версия проходит критерии?"}
  D -->|"Нет"| E["Git revert + apply или rollout undo"]
  D -->|"Да"| F["Оставить новую ревизию"]
  E --> G["rollout status / history"]
  F --> H["Canary: stable 3 и canary 1"]
  H --> I["Service selector app+tier; обе версии"]
  I --> J["Metrics ошибок, задержек, отзывы"]
```

p0409–p0413. Из соотношения 3:1 и общего Service не выводится подтверждённый процент трафика, 10% — отдельный пример с дополнительной маршрутизацией. Полный production rollback [Needs confirmation].
