# Шпаргалка: Pod и организация Kubernetes resources

Цель: быстро локализовать задачу главы 3 — от состава Pod до labels, scheduling, namespaces и lifecycle deletion.

## Baseline

~~~text
Pod
├─ one or more tightly coupled containers
├─ always one worker node
├─ shared Network / UTS / IPC context
├─ one Pod IP / one port namespace
└─ scaling unit = whole Pod
~~~

### Когда containers должны быть в одном Pod

Задайте три вопроса из главы:

1. Они должны работать вместе на одном host?
2. Они представляют единое целое или независимые компоненты?
3. Они должны масштабироваться вместе или отдельно?

Если совместное размещение не требуется — тяготеть к отдельным Pods.

## Read-only checks

| Что проверить | Source-confirmed command | Смысл |
|---|---|---|
| Pods | `kubectl get pods` | состояние Pod |
| Full YAML | `kubectl get po <pod> -o yaml` | spec + runtime fields |
| Full JSON | `kubectl get po <pod> -o json` | тот же object в JSON |
| API fields | `kubectl explain pods` | поля Pod |
| Pod spec fields | `kubectl explain pod.spec` | детализация `spec` |
| Logs | `kubectl logs <pod>` | stdout/stderr single-container Pod |
| Container logs | `kubectl logs <pod> -c <container>` | logs выбранного container |
| Labels | `kubectl get po --show-labels` | все labels |
| Selected label columns | `kubectl get po -L creation_method,env` | отдельные label columns |
| Pods by selector | `kubectl get po -l <selector>` | filtered resources |
| Nodes by label | `kubectl get nodes -l gpu=true` | candidate nodes |
| Node label column | `kubectl get nodes -L gpu` | label values |
| Annotations | `kubectl describe pod <pod>` | annotations/details |
| Namespaces | `kubectl get ns` | namespace list |
| Pods in namespace | `kubectl get po --namespace <ns>` | scoped resource list |

## Interpretation

### Multiple processes

- Несвязанные processes → разные containers.
- Независимые components → обычно разные Pods.
- Main process + tightly coupled supporting process → возможно несколько containers в одном Pod.

### Networking

Контейнеры одного Pod:
- один Pod IP;
- одно port space;
- `localhost` между containers;
- port collision возможен внутри Pod.

Pods:
- отдельные Pod IP;
- в модели главы — flat inter-Pod network.

### Labels vs annotations

~~~text
Label
→ short identifying metadata
→ selectable
→ grouping / filtering / scheduling

Annotation
→ larger non-identifying metadata
→ no annotation selector
→ tooling / descriptions / auxiliary data
~~~

### Namespace

Namespace:
- scope имён;
- группировка resources;
- позволяет одинаковые resource names в разных namespaces.

Namespace сам по себе не гарантирует network isolation.

## Modifying actions

### Create Pod/resource from manifest

~~~bash
kubectl create -f <manifest.yaml>
~~~

Verification:

~~~bash
kubectl get pods
kubectl get po <pod> -o yaml
~~~

Rollback для Pod — `kubectl delete po <pod>`, если Pod не будет автоматически воссоздан controller.

### Add/change labels

~~~bash
kubectl label po <pod> <key>=<value>
kubectl label po <pod> <key>=<new-value> --overwrite
~~~

Verification:

~~~bash
kubectl get po --show-labels
~~~

### Label node and constrain placement

~~~bash
kubectl label node <node-name> gpu=true
kubectl get nodes -l gpu=true
~~~

Pod spec использует `nodeSelector` с `gpu: "true"`.

Acceptance: созданный Pod должен быть назначен node, соответствующему selector.

Rollback label/selector removal: `[Needs confirmation]` — команда удаления label в главе не приведена.

### Add annotation

~~~bash
kubectl annotate pod <pod> mycompany.com/someannotation="foo bar"
~~~

Verification:

~~~bash
kubectl describe pod <pod>
~~~

Rollback annotation removal: `[Needs confirmation]`.

### Create namespace

~~~bash
kubectl create -f custom-namespace.yaml
~~~

или:

~~~bash
kubectl create namespace custom-namespace
~~~

Verification:

~~~bash
kubectl get ns
~~~

### Create resource in namespace

~~~bash
kubectl create -f kubia-manual.yaml -n custom-namespace
~~~

Verification:

~~~bash
kubectl get po --namespace custom-namespace
~~~

## Destructive actions

### Delete one Pod

~~~bash
kubectl delete po <pod>
~~~

Source behavior:
- SIGTERM;
- default grace period 30 seconds;
- затем SIGKILL, если process не завершился.

Risk: Pod может быть автоматически воссоздан controller.

### Delete Pods by label

~~~bash
kubectl delete po -l creation_method=manual
kubectl delete po -l rel=canary
~~~

Risk: selector может затронуть несколько resources сразу.

### Delete namespace

~~~bash
kubectl delete ns custom-namespace
~~~

High impact: удаляет namespace и resources в нём.

### Delete all Pods in current namespace

~~~bash
kubectl delete po --all
~~~

High impact. Если Pods управляются controller, они могут появиться снова.

### Delete almost all resources in current namespace

~~~bash
kubectl delete all --all
~~~

Very high impact.

Source caveats:
- `all` не включает абсолютно все resource types;
- пример удаляет ReplicationController и Services;
- Service `kubernetes` также удаляется и, по источнику, должна быть автоматически воссоздана.

## Acceptance model

После главы должно быть возможно ответить:

- почему два containers находятся в одном Pod;
- какой Pod IP/port space они разделяют;
- какой resource manifest задаёт desired spec;
- какие labels описывают resource;
- каким selector выбрано подмножество;
- почему placement задан через свойства node, а не конкретный hostname;
- в каком namespace находится object;
- кто контролирует Pod и не создаст ли его снова после delete.
