# Диаграммы главы 6 — namespace, ResourceQuota, LimitRange

**Источник:** PDF/printed p0218–p0247, RAG chunks `p0218:c01`–`p0247:c01`. Диаграммы реконструированы из текста главы; исходные иллюстрации напрямую не просматривались.

## Ресурсные области и бюджеты

```mermaid
flowchart TD
  C["Kubernetes cluster"]
  C --> NS1["Namespace: custom-ns"]
  C --> NS2["Namespace: quota-ns"]
  C --> SYS["Namespace: kube-system"]
  C --> CL["Cluster-scoped resources: Node, PV"]
  NS1 --> POD1["Pod nginx"]
  NS2 --> POD2["Pod с requests/limits"]
  NS2 --> RQ["ResourceQuota: общий бюджет"]
  NS2 --> LR["LimitRange: per-container defaults / bounds"]
  RQ -->|"Ограничивает суммарные запросы"| POD2
  LR -->|"Default / min / max"| POD2
```

Namespace упорядочивает ресурсы, но **не гарантирует сетевой изоляции**; доступ между разными namespaces через Service DNS, ограничения посредством дополнительных NetworkPolicy/RBAC обсуждаются в p0221 и p0231–p0233. Cluster-scoped объекты описаны в p0230–p0231.

## Диагностическая цепочка для Pod в namespace

```mermaid
flowchart TD
  A["Подтвердить кластер, context, namespace"]
  B["kubectl get pods -n quota-ns"]
  C{"Pod создан?"}
  D["Admission: ResourceQuota / LimitRange"]
  E["Forbidden: exceeded quota"]
  F["Pod Pending"]
  G["kubectl describe po ... -n quota-ns"]
  H["FailedScheduling: Insufficient memory"]
  I["Pod Running"]
  J["kubectl top pod -n quota-ns"]
  K["Контролируемое изменение requests/limits<br/>только после оценки влияния"]
  A --> B --> C
  C -->|"Нет"| D --> E
  C -->|"Да"| F
  F -->|"Нет, Ready"| I --> J
  F -->|"Да"| G --> H --> K --> B
```

Пример отрицательного результата по quota: p0241–p0243; scheduling `Pending` и `Insufficient memory`: p0238–p0240. Процедуры восстановления при отказах приложения вне главы: **[Needs confirmation]**.

## Safety / lifecycle

```mermaid
flowchart TD
  A["Создание Namespace"]
  B["Поместить Pod / ConfigMap"]
  C["Назначить ResourceQuota и LimitRange"]
  D["Наблюдать Used/Hard и Pod"]
  E["Удаление Namespace"]
  F["Удаление всех ресурсов namespace<br/>деструктивная операция"]
  A --> B --> C --> D
  D -->|"Только после допуска"| E --> F
```

p0224–p0225: `kubectl delete namespaces` необратим по описанию автора; не использовать как штатный rollback. `kubectl config set-context` p0228–p0229 изменяет локальную конфигурацию и может перенаправить последующие команды в другой namespace.
