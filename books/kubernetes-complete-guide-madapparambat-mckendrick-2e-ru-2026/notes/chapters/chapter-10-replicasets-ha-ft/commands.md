# Source-confirmed commands — Глава 10

**RAG PDF:** 366–383 (`p0366:c01`–`p0383:c01`). Все команды взяты из главы, но **не исполнялись**. Не выполнять `delete`, `drain`, `exec rm` и `kind create` в действующей инфраструктуре без отдельного допуска, backup и rollback.

## Read-only / observation

| Команда из RAG | Назначение / ограничение | Стр. |
|---|---|---:|
| `kubectl get nodes` | готовность нескольких узлов kind | 372 |
| `kubectl describe replicaset/nginx-replicaset-example -n rs-ns` | `4 current / 4 desired` и статус Pod | 374 |
| `kubectl get pods -n rs-ns` | состояние выбранного Namespace | 374, 379 |
| `kubectl describe pod <Id_пода>` | labels и `Controlled By`; placeholder нужно заменить | 374 |
| `kubectl describe rs/nginx-replicaset-example -n rs-ns` | события `SuccessfulCreate` и `SuccessfulDelete` | 375–376, 379 |
| `watch -n 1 kubectl get pods -n rs-ns` | повторное наблюдение из сноски | 375 |
| `kubectl get pods` | контекстно-зависимый namespace; указан без `-n` | 376, 381 |
| `kubectl get po -n rs-ns -o wide` | Pod IP и Node | 377–378 |
| `curl localhost:8080` | HTTP read с локального port-forward; network diagnostic | 377–378 |
| `kubectl describe pod/nginx-replicaset-livenessprobe-example-lgvqv` | `Unhealthy`, `Killing`, контейнерные перезапуски | 381 |

`get` и `describe` читают состояние API, но могут показывать инфраструктурные/сетевые сведения. `watch` создаёт долгоживущий процесс чтения. `curl` генерирует сетевой запрос, даже если локальный адрес. `kubectl get pods` без `-n rs-ns` нельзя считать доказательством состояния rs-ns: текущий контекст в источнике не подтверждён.

## Workload-generating — создать учебный кластер и ReplicaSet

```bash
kind create cluster --config Chapter03/kind_cluster --image kindest/node:v1.31.0
kubectl get nodes
kubectl create -f ns-rs.yaml
kubectl apply -f nginx-replicaset-example.yaml
kubectl describe replicaset/nginx-replicaset-example -n rs-ns
```

Source p0372–p0374. **Effect:** создание kind кластера, изменение локального kubeconfig, создание Namespace `rs-ns` и ReplicaSet с четырьмя Pod. **Risk:** локальная инфраструктура, ресурсы и конфликт текущего Kubernetes context. **Verification:** `get nodes` Ready, `describe rs` 4 desired/4 current. **Rollback:** полный lifecycle kind cluster, возврат kubeconfig и восстановление ресурсов в книге **[Needs confirmation]**.

Манифест p0372:
```yaml
# nginx-replicaset-example.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset-example
  namespace: rs-ns
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx
      environment: test
  template:
    metadata:
      labels:
        app: nginx
        environment: test
    spec:
      containers:
        - name: nginx
          image: nginx:1.17
          ports:
            - containerPort: 80
```

`replicas` задаёт число подов, `selector` — принадлежность, `template` — создаваемый Pod (p0373). Источник отдельно подчёркивает совпадение `spec.template.metadata.labels` с `spec.selector` (p0374).

Пример `nginx-replicaset-expressions.yaml` p0374 — **неполный YAML**, только фрагмент:
```yaml
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx
    matchExpressions:
      - key: environment
        operator: In
        values: [test, dev]
```
Не объявлять его полноценным манифестом или готовой командой `apply`: template опущен исходником.

## Destructive experiments — заменить Pod и проверить adoption

```bash
kubectl delete po nginx-replicaset-example-6qc9p -n rs-ns
kubectl describe rs/nginx-replicaset-example -n rs-ns
kubectl apply -f nginx-pod-bare.yaml
kubectl describe rs/nginx-replicaset-example -n rs-ns
```

p0375–p0376. **Effect:** удаляет конкретный Pod, ReplicaSet создаёт замену; создание bare Pod с совпадающими метками способно вызвать adoption/удаление контроллером. **Risk:** сбой доступа, непреднамеренное удаление Pod при пересечении селекторов. **Verification:** `SuccessfulCreate`, `SuccessfulDelete`, `get pods`. **Rollback:** восстановление старого Pod/его данных/identity не описано — [Needs confirmation].

Манифест bare Pod p0376:
```yaml
# nginx-pod-bare.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod-bare-example
  namespace: rs-ns
  labels:
    app: nginx
    environment: test
spec:
  containers:
    - name: nginx
      image: nginx:1.17
      ports:
        - containerPort: 80
```

**Source defect:** p0375 пишет о целевом числе **трёх**, хотя предыдущий YAML на p0372 задаёт **четыре** и вывод на p0376 содержит три оставшихся RS Pod + один bare `Terminating`. Не восстанавливать скрытые изменения `replicas` по памяти; см. findings.

## Service + node failover — HIGH RISK, state-changing

```bash
kubectl apply -f nginx-service.yaml
kubectl port-forward svc/nginx-service 8080:80 -n rs-ns
curl localhost:8080
kubectl get po -n rs-ns -o wide
kubectl cordon kind-worker
kubectl drain kind-worker --ignore-daemonsets
kubectl delete node kind-worker
kubectl get po -n rs-ns -o wide
```

p0377–p0378. `apply` создаёт Service, `port-forward` открывает локальный порт, `cordon` запрещает новый scheduling на узел, `drain` вытесняет Pod, `delete node` удаляет объект узла. **Risk:** очень высокий: нарушение доступности других приложений, потеря capacity, проблемы с DaemonSet/PDB/хранилищем и ролью узла (возможности в реальной среде **[Needs confirmation]**). **Verification:** `get po -o wide` показывает распределение четырёх реплик между оставшимися worker, `curl localhost:8080` проверяет сервис. **Rollback:** в source нет процедуры обратного добавления/разблокировки узла; [Needs confirmation]. Это только лабораторная демонстрация, не production runbook.

## Scaling — state-changing

p0378–p0379 показывает изменение `spec.replicas` в файле на **5**, затем на **2**:
```bash
kubectl apply -f ./nginx-replicaset-example.yaml
kubectl get pods -n rs-ns
kubectl describe rs/nginx-replicaset-example -n rs-ns
kubectl scale rs/nginx-replicaset-example --replicas=5
```
`scale` — указанная авторами императивная альтернатива и рекомендована ими главным образом для учебных/отладочных сценариев. **Effect:** создание/удаление экземпляров Pod. **Risk:** изменение capacity и распределения запросов, потеря ephemeral state. **Verification:** `get pods`/`describe rs` показывают заданное число. **Rollback:** вернуть ранее подтверждённое число реплик через источник YAML; если неизвестно, [Needs confirmation]. **Source mismatch:** в тексте для уменьшения replicas упомянут файл `nginx-replicaset.yaml`, но применяется `nginx-replicaset-example.yaml` (p0379).

## Liveness — workload-generating, destructive simulation

p0380:
```yaml
# nginx-replicaset-livenessprobe.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset-livenessprobe-example
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
      environment: test
  template:
    metadata:
      labels:
        app: nginx
        environment: test
    spec:
      containers:
        - name: nginx
          image: nginx:1.17
          ports:
            - containerPort: 80
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 2
            periodSeconds: 2
```

```bash
kubectl apply -f ./nginx-replicaset-livenessprobe.yaml
kubectl get pods
kubectl exec -it nginx-replicaset-livenessprobe-example-lgvqv -- rm /usr/share/nginx/html/index.html
kubectl describe pod/nginx-replicaset-livenessprobe-example-lgvqv
```

p0381. **Effect:** создаёт новый ReplicaSet в текущем namespace, затем удаляет HTML-файл в одном контейнере. **Risk:** **destructive**, приложение начнёт возвращать ошибку; liveness может вызвать рестарты. **Verification:** источник приводит `Liveness probe failed: HTTP ... 403`, `Killing`, `Started`; перезапуск делает kubelet, а не RS. **Rollback:** восстановление файла и прекращение restart loop в source [Needs confirmation]. В разных Namespace риск пересечения labels зависит от контекста — [Needs confirmation]. Имена Pod с суффиксом из книги не гарантированы.

## Destructive ReplicaSet deletion — две взаимоисключающие альтернативы

```bash
kubectl delete rs/nginx-replicaset-livenessprobe-example
kubectl delete rs/nginx-replicaset-livenessprobe-example --cascade=orphan
```

p0382. **Первая** команда удаляет ReplicaSet и управляемые Pod (default cascade); **вторая** оставляет Pod, но снимает управление, после чего возможен захват другим RS. **НЕ выполнять обе подряд.** Verification: список Pod после операции — описан автором концептуально, точная команда проверки здесь не приведена; `kubectl get pods` встречается в p0381. Rollback ресурсов, сетевой доступности и workload identity [Needs confirmation].

## Scope and operational safety

Source не предоставляет полноценного безопасного плана production HA, восстановления удалённого Node или DR. Репликация Pod не обеспечивает сохранность данных. Текущие RBAC/namespace, Service selector, topology, probes и version compatibility **[Needs confirmation]**. Не использовать `drain`, `delete node`, `exec rm`, `--cascade=orphan` как «безопасную диагностику».
