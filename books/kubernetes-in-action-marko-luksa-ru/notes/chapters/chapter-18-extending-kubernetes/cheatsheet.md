# Глава 18 — cheatsheet

## Symptom / problem framing

Нужно выразить предметную сущность выше уровня стандартных Kubernetes resources или автоматизировать создание набора стандартных объектов из одной декларации.

Пример главы: пользователь создает объект `Website`, а система должна автоматически создать `Deployment` и `Service`.

## Baseline / context

Базовая схема главы:

```text
CRD
  → custom resource instance
  → custom controller
  → Deployment / Service / другие стандартные resources
```

Альтернативная схема:

```text
APIService
  → aggregated custom API server
  → отдельные API resources
```

Service Catalog:

```text
ClusterServiceBroker
  → ClusterServiceClass
  → ServiceInstance
  → ServiceBinding
  → Secret
  → workload
```

## Read-only checks

Source-confirmed проверки:

```bash
kubectl get websites
kubectl get website kubia -o yaml
kubectl logs website-controller-2429717411-q43zs -c main
kubectl get deploy,svc,po
kubectl get serviceclass postgres-database -o yaml
kubectl get secret postgres-secret -o yaml
```

Имена Pod/ресурсов в примерах source-specific; перед использованием в другом кластере они требуют **[Needs confirmation]**.

## Interpretation

### CRD без контроллера

CRD дает API server возможность хранить пользовательские объекты. Наличие объекта само по себе не гарантирует side effect.

### CRD + controller

Контроллер наблюдает custom resources и приводит фактическое состояние к состоянию, описанному высокоуровневым объектом.

### Aggregated API server

Если возможностей CRD недостаточно, дополнительный API server можно интегрировать с главным Kubernetes API через API aggregation и ресурс `APIService`.

### Service Catalog

Service Catalog абстрагирует provisioning внешней службы:

- broker — поставщик;
- class — тип службы;
- instance — конкретно provisioned service;
- binding — связь клиента со службой;
- Secret — учетные данные для доступа.

### PaaS поверх Kubernetes

OpenShift и Deis Workflow показаны как системы, добавляющие build/deploy abstractions и developer workflow поверх Kubernetes.

### Helm

Source-era Helm использует:

```text
Chart + Config → Release → Tiller → Kubernetes resources
```

## Next action

Для source-era учебного сценария:

1. Зарегистрировать CRD.
2. Создать экземпляр custom resource.
3. Проверить, что API server сохраняет объект.
4. Развернуть controller.
5. Проверить controller logs.
6. Проверить созданные стандартные resources.

Для применения на современном Kubernetes сначала проверить актуальность API versions и архитектуры компонентов: **[Needs confirmation]**.

## Modifying action

Source-confirmed state-changing examples:

```bash
kubectl create -f website-crd-definition.yaml
kubectl create -f kubia-website.yaml
kubectl delete website kubia
kubectl create serviceaccount website-controller
kubectl create clusterrolebinding website-controller \
  --clusterrole=cluster-admin \
  --serviceaccount=default:website-controller
helm install --name my-database stable/mysql
```

### Критическая граница RBAC

Глава использует `cluster-admin` для демонстрационного контроллера. Это дает очень широкие полномочия. Source не предоставляет least-privilege role для этого примера.

Production-safe RBAC: **[Needs confirmation]**.

## Verification / acceptance checks

CRD acceptance:

```text
kubectl get websites
→ экземпляр Website виден
```

Controller acceptance:

```text
controller log
→ ADDED event
→ 201 Created для Service
→ 201 Created для Deployment

kubectl get deploy,svc,po
→ связанные объекты существуют
```

Service Catalog acceptance:

```text
ServiceInstance provisioned
→ ServiceBinding создан
→ Secret с connection data существует
```

Helm acceptance из source: после `helm install` должны быть созданы необходимые для MySQL Deployments, Services, Secrets и PVC.

## Rollback

- Удаление экземпляра `Website` показано явно: `kubectl delete website kubia`.
- Удаление CRD, ClusterRoleBinding, ServiceAccount, Service Catalog resources и Helm release в проверенном source fragment не описано: **[Needs confirmation]**.
