# Приложение D — cheatsheet

## Symptom / problem framing

Один Kubernetes cluster не должен быть единственным failure domain, если требуется переживать потерю целого дата-центра/availability zone.

## Baseline / context

```text
Federation control plane
  ├─ etcd
  ├─ federated API server
  └─ federated controller manager
             ↓
       member clusters
```

## Read-only checks

В приложении нет конкретных source-confirmed operational CLI checks для построения federation.

Read-only commands: **[Not applicable]**.

## Interpretation

- Federation abstractly заменяет worker nodes на whole clusters.
- Federated resources являются desired state верхнего уровня.
- Controllers проецируют это состояние в member clusters.
- Replication direction: federation → cluster only.
- Replica counts могут распределяться, а не дублироваться.
- Federated Ingress создает multi-cluster global entry point.
- Pods остаются cluster-local с точки зрения listing в source.

## Next action

Если применять концепцию source-era:
1. определить member clusters;
2. развернуть federation control plane;
3. зарегистрировать clusters;
4. создавать federated resources;
5. проверять resulting resources в каждом member cluster.

Конкретные setup commands в источнике отсутствуют: **[Needs confirmation]**.

## Modifying action

Source не приводит команд настройки federation.

**[Not applicable / Needs confirmation]**

## Verification / acceptance checks

Source-grounded acceptance conceptual:
- federated Namespace/ConfigMap/Secret и т.п. появляются в member clusters;
- Deployment/ReplicaSet desired replicas суммарно соответствуют federated desired replicas;
- изменения federated object распространяются вниз;
- обратная синхронизация из member cluster отсутствует.

## Rollback

Source не дает procedure: **[Needs confirmation]**.
