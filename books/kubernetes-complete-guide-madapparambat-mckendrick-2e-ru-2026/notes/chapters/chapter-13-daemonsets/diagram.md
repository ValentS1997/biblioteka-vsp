# Диаграммы главы 13 — DaemonSet

**Источник:** RAG PDF/printed 457–473, `p0457:c01`–`p0473:c01`. Mermaid реконструирует **текст** главы; оригинальные изображения напрямую не просматривались.

## DaemonSet и eligibility узлов

```mermaid
flowchart TD
  DS["DaemonSet: selector + Pod template"]
  NODE["Kubernetes nodes / Node affinity, selectors, tolerations"]
  N1["Узел A подходит"]
  N2["Узел B подходит"]
  N3["Узел C НЕ подходит"]
  P1["Pod агента на A"]
  P2["Pod агента на B"]
  DS --> NODE
  NODE --> N1 --> P1
  NODE --> N2 --> P2
  NODE --> N3
```

p0457–p0460, p0464, p0468. Формулировка «один на каждом» относится к **подходящим** узлам, не ко всем независимо от политики scheduling.

## Поток узловых логов: Fluentd source example

```mermaid
flowchart LR
  HOST["/var/log хостового узла"]
  V["volume.hostPath: /var/log"]
  POD["Fluentd Pod, один на eligible node"]
  END["elasticsearch-logging:9200"]
  HOST --> V --> POD -->|"Концептуально: отправка логов"| END
```

p0463–p0465. В учебном RAG endpoint `elasticsearch-logging` **не создаётся** и доставки логов нет в проверенных output. Исходный YAML объявляет DaemonSet в `kube-system`, а команды/Pod выводы используют `logging` — это **source mismatch**, не исполнимая верифицированная схема.

## RollingUpdate vs OnDelete

```mermaid
flowchart TD
  A["Изменить spec.template.image: v4.7 → v4.7.5"]
  B{"updateStrategy.type"}
  C["RollingUpdate: Pod заменяются постепенно"]
  D["OnDelete: ждать ручного удаления Pod"]
  E["rollout status / describe ds"]
  F["Проверить READY/AVAILABLE и events"]
  A --> B
  B --> C --> E
  B --> D --> E
  E --> F
```

p0467–p0469. В книге `RollingUpdate` применяется по умолчанию; наблюдаемый пример 2/3→3/3. `kubectl rollout undo daemonset` описан, но без live проверки rollback, особенно при конфликте namespaces.

## Операционная оценка перед изменением

```mermaid
flowchart TD
  START["План изменения DaemonSet"]
  NS{"Namespace YAML и команды совпадают?"}
  STOP["Остановить изменение; source finding"]
  SEC{"Это CNI / kube-proxy / критичный агент?"}
  REVIEW["Проверить окно изменений и влияние на все nodes"]
  STORAGE["Проверить hostPath, priority, resources, endpoint"]
  APPLY["Контролируемое обновление и rollout status"]
  START --> NS
  NS -->|"Нет"| STOP
  NS -->|"Да"| SEC
  SEC -->|"Да"| REVIEW --> STORAGE
  SEC -->|"Нет"| STORAGE
  STORAGE --> APPLY
```

Source p0461–p0469. В главе нет полного approval/rollback plan; реальная готовность к production **[Needs confirmation]**.

## Альтернативы

p0472–p0473: sidecar для сопровождения отдельного Pod, `CronJob` для расписания, systemd для узлового демона без Kubernetes, static Pod для специальных задач kubelet. Выбор зависит от того, требуется ли **один агент на каждый узел**, а не только выполнение задачи.
