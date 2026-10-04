# Сводная шпаргалка — «Kubernetes в действии»

Эта шпаргалка агрегирует source-grounded chapter artifacts книги. Она описывает модель Kubernetes в терминах и архитектуре источника и не является автоматически обновленной документацией современного Kubernetes.

## 1. Ментальная модель

```text
User / CI
   ↓ declarative objects
API Server
   ↓ persistence
etcd
   ↓ watches
Controllers ──→ desired state reconciliation
Scheduler   ──→ Pod → Node binding
Kubelet     ──→ containers on node
kube-proxy  ──→ Service traffic rules
```

Основной принцип всей книги:

> Пользователь описывает желаемое состояние; независимые control loops наблюдают API и приводят фактическое состояние к желаемому.

## 2. Core objects

| Задача | Основной объект/механизм | Ключевая мысль |
|---|---|---|
| Запустить containers | Pod | минимальная jointly-scheduled unit |
| Держать N взаимозаменяемых Pods | ReplicaSet/контроллер | reconciliation desired replicas |
| Декларативно обновлять stateless app | Deployment | rollout через ReplicaSets |
| Stateful replicas | StatefulSet | stable identity + per-Pod storage |
| Stable network endpoint | Service | decouples clients from Pod IPs |
| External HTTP routing | Ingress | внешний routing layer |
| Non-sensitive config | ConfigMap | config отдельно от image/Pod spec |
| Sensitive config | Secret | credential-bearing resource |
| Ephemeral shared files | emptyDir | живёт вместе с Pod |
| Durable storage request | PVC | workload requests storage |
| Cluster storage resource | PV | storage abstraction |
| Dynamic storage | StorageClass | provisioner + parameters |
| Workload identity | ServiceAccount | Pod API identity |
| Authorization | RBAC | Role/ClusterRole + Binding |
| Autoscale workload | HPA | desired replicas from metrics |
| Placement | nodeSelector/affinity | Pod → suitable topology |
| Exclusion | taints/tolerations | node repels non-tolerating Pods |
| API extension | CRD + controller | high-level object → native resources |

## 3. Pod lifecycle

```text
manifest accepted
  → scheduled
  → kubelet starts Pod
  → init containers
  → main containers
  → readiness gates Service traffic
  → liveness may restart unhealthy container
  → termination
       preStop
       SIGTERM
       grace period
       SIGKILL if needed
```

Разделяй:
- readiness = можно ли направлять traffic;
- liveness = нужно ли restart container;
- restart container ≠ recreate Pod;
- delete Pod под controller ≠ remove workload: controller может создать replacement.

## 4. Network path

```text
Client
  → Service / Ingress
  → Service virtual IP/rules
  → endpoint Pod IP
  → container port
```

Pod model:
- containers одного Pod разделяют network namespace;
- внутри Pod доступен `localhost`;
- Pod получает собственный IP;
- Service скрывает нестабильность Pod IP;
- NetworkPolicy ограничивает разрешенный traffic;
- kube-proxy/service rules обновляются асинхронно относительно Pod termination.

Operational implication: graceful shutdown должен учитывать distributed propagation routing state.

## 5. Storage decision

```text
Нужно пережить restart container?
  ├─ нет → writable container layer
  └─ да
      ↓
Нужно пережить deletion/recreation Pod?
  ├─ нет → emptyDir
  └─ да → PVC/PV/external persistent storage
```

Для stateful replicated workload:
```text
StatefulSet ordinal
   + stable DNS identity
   + volumeClaimTemplate
   = stable logical replica
```

Критическая граница: force-delete stateful Pod может создать второй экземпляр с той же logical identity/storage до фактической остановки старого.

## 6. Configuration

```text
Pod spec
  ├─ command / args
  ├─ env
  ├─ ConfigMap
  │    ├─ env
  │    └─ mounted files
  └─ Secret
       ├─ env
       └─ mounted files
```

Remember:
- Base64 ≠ encryption;
- Secret data — credential material;
- mounted config update ≠ application reload;
- source-era subPath behavior имеет ограничения.

## 7. Security model

```text
request
  → authentication
  → authorization
  → admission
  → validation
  → persistence
```

RBAC:
```text
Role         + RoleBinding        → namespace permissions
ClusterRole  + RoleBinding        → reusable permissions in one namespace
ClusterRole  + ClusterRoleBinding → cluster-wide scope
```

Принцип: separate ServiceAccounts + least privilege.

Node/container isolation controls:
- runAsUser / runAsNonRoot;
- privileged;
- Linux capabilities;
- hostNetwork / hostPID / hostIPC;
- readOnlyRootFilesystem;
- fsGroup / supplementalGroups;
- source-era PodSecurityPolicy.

## 8. Resource management

Scheduler использует requests для placement.

```text
requests → scheduling reservation model
limits   → upper runtime boundary
usage    → observed consumption
```

CPU:
- compressible resource;
- limit может приводить к throttling.

Memory:
- incompressible;
- превышение memory limit связано с termination/OOM behavior.

QoS и eviction зависят от requests/limits и давления на node.

## 9. Autoscaling

```text
Metrics
  → HPA
  → desired Pod replicas

Unschedulable Pods
  → Cluster Autoscaler
  → node group size
```

PDB ограничивает voluntary disruptions, но не предотвращает физический failure.

## 10. Scheduling

Taint/toleration:
```text
Node taint = repel
Pod toleration = allowed to stay/schedule
```

Важно: toleration не притягивает Pod к node.

Affinity:
- node affinity → properties of node;
- pod affinity → рядом с matching Pods;
- pod anti-affinity → разнести matching Pods;
- topologyKey определяет failure/placement domain;
- required = hard;
- preferred = soft.

## 11. Deployment safety

```text
change Pod template
  → new ReplicaSet
  → rolling transition
  → readiness gates availability
  → rollout status
  → rollback if required
```

Key knobs:
- `maxSurge`;
- `maxUnavailable`;
- `minReadySeconds`;
- `progressDeadlineSeconds`;
- rollout pause/resume;
- revision history.

## 12. Control-plane internals

```text
Deployment
  ↓ Deployment controller
ReplicaSet
  ↓ ReplicaSet controller
Pod
  ↓ Scheduler
Pod bound to Node
  ↓ Kubelet
running containers
```

Controllers не обязаны directly call друг друга; coordination идёт через API objects/watch events.

etcd — persistent state store, API server — security/validation boundary.

## 13. Operational troubleshooting loop

```text
kubectl get
  ↓
kubectl describe
  ↓
events / conditions
  ↓
kubectl logs
  ↓
inspect YAML/spec/status
  ↓
localize layer:
  object / controller / scheduler / kubelet / network / storage / app
```

Перед изменением:
1. зафиксировать current state;
2. определить owner/controller объекта;
3. понять desired state;
4. менять минимальный scope;
5. re-check status/events;
6. rollback, если acceptance criteria не достигнуты.

## 14. Application contract with Kubernetes

Application должна:
- переживать Pod recreation;
- не полагаться на stable Pod IP;
- корректно реагировать на SIGTERM;
- сигнализировать readiness только после реальной готовности;
- сохранять durable state вне writable container layer;
- писать operational logs в stdout/stderr;
- не зависеть от гарантированного порядка старта независимых resources;
- использовать versioned artifacts/manifests.

Graceful HTTP shutdown в модели главы 17:

```text
SIGTERM
  → короткая задержка для propagation routing changes
  → stop accepting new connections
  → close idle keep-alive
  → wait active requests
  → exit
```

## 15. Extensibility

```text
CRD
  → Custom Resource
  → Custom Controller
  → Deployment / Service / Secret / other native resources
```

Более глубокое расширение:
- aggregated API server через APIService;
- source-era Service Catalog;
- PaaS layers (OpenShift / Deis in source);
- Helm package abstraction.

## 16. Appendices — что оставить в голове

A. kubeconfig:
```text
context = cluster + user + namespace
```
Всегда проверять current context перед modifying command.

B. kubeadm:
```text
node prerequisites → kubeadm init → join → CNI → Ready
```
Source-era host commands требуют отдельной современной проверки.

C. runtimes:
```text
Kubelet → CRI → runtime implementation
```

D. federation:
```text
higher-level desired state
  → federation controllers
  → member clusters
```
Historical source-era architecture.

## 17. Самые опасные ошибки

| Ошибка | Почему опасно |
|---|---|
| Force-delete StatefulSet Pod без подтверждения shutdown | split-brain / duplicate identity |
| Выдать `cluster-admin` workload | потеря security boundary |
| Считать Base64 Secret шифрованием | ложная защита credentials |
| Использовать liveness как readiness | restart вместо traffic gating |
| Полагаться на Pod IP | Pod replacement ломает identity |
| Хранить durable state в container layer | данные исчезнут при restart/recreate |
| Hard affinity там, где достаточно preference | Pending Pods при нехватке topology |
| Игнорировать requests | scheduler не видит реальную capacity need |
| Удалить Pod вместо owner/controller | workload будет воссоздан |
| Работать kubectl не проверив context | изменение не того cluster/namespace |

## 18. Книга одной строкой

```text
Declarative desired state
+ API-centered control loops
+ ephemeral compute
+ explicit network/storage/security contracts
= Kubernetes operational model
```
