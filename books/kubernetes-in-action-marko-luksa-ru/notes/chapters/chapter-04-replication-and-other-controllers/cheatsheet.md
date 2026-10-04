# Шпаргалка: controllers и self-healing

## 1. Два уровня self-healing

### Container-level

~~~text
livenessProbe fails repeatedly
          ↓
Kubelet kills unhealthy container
          ↓
new container is created in the Pod
~~~

Probe types из главы:

- HTTP GET;
- TCP socket;
- Exec.

### Pod-level / cluster-level

~~~text
desired replicas = N
       ↓
controller counts matching Pods
       ↓
actual < N → create
actual > N → delete
actual = N → no change
~~~

Directly created Pod не имеет controller, который восстановит его после node failure.

## 2. Read-only checks

| Цель | Команда |
|---|---|
| Проверить Pod/restarts | `kubectl get po kubia-liveness` |
| Посмотреть предыдущий container log | `kubectl logs <pod> --previous` |
| Liveness/events/restart reason | `kubectl describe po kubia-liveness` |
| Pods | `kubectl get pods` |
| ReplicationController | `kubectl get rc` |
| RC details | `kubectl describe rc kubia` |
| Nodes | `kubectl get node` |
| Labels Pods | `kubectl get pods --show-labels` |
| Label column | `kubectl get pods -L app` |
| ReplicaSet | `kubectl get rs` |
| ReplicaSet details | `kubectl describe rs` |
| DaemonSet | `kubectl get ds` |
| Jobs | `kubectl get jobs` / `kubectl get job` |
| Completed Job Pods | `kubectl get po -a` |
| Job logs | `kubectl logs <job-pod>` |

## 3. Liveness interpretation

Default/source-observed settings в примере:

- initial delay: 0s, если не задан;
- timeout: 1s;
- period: 10s;
- failure threshold: 3.

Source рекомендует `initialDelaySeconds`, чтобы приложение успело стартовать.

Пример:

~~~text
livenessProbe:
  httpGet:
    path: /
    port: 8080
  initialDelaySeconds: 15
~~~

## 4. ReplicationController

Три ключевые части:

~~~text
replicas
selector
Pod template
~~~

### Scale

~~~bash
kubectl scale rc kubia --replicas=10
kubectl scale rc kubia --replicas=3
~~~

Это изменение desired state, а не команда «создать/удалить конкретные Pods».

### Template change

~~~bash
kubectl edit rc kubia
~~~

Existing Pods не меняются. Новая template применяется к future replacement Pods.

### Preserve Pods while removing RC

~~~bash
kubectl delete rc kubia --cascade=false
~~~

Controller удаляется, Pods остаются.

## 5. ReplicaSet

ReplicaSet выполняет ту же reconciliation-задачу, но selector выразительнее.

`matchExpressions` operators:

- `In`;
- `NotIn`;
- `Exists`;
- `DoesNotExist`.

Multiple expressions → AND semantics.

## 6. DaemonSet

~~~text
desired state:
one daemon Pod on each matching node
~~~

Example node classification:

~~~bash
kubectl label node <node-name> disk=ssd
~~~

DaemonSet с `nodeSelector: disk=ssd` создаёт Pod на matching node.

Изменение:

~~~bash
kubectl label node <node-name> disk=hdd --overwrite
~~~

Source example показывает Pod в `Terminating`.

## 7. Job

Job предназначен для заканчиваемой работы.

~~~text
restartPolicy: OnFailure | Never
completions: required successful completions
parallelism: allowed simultaneous Pods
activeDeadlineSeconds: max runtime
backoffLimit: retry limit
~~~

Пример динамического изменения parallelism:

~~~bash
kubectl scale job multi-completion-batch-job --replicas 3
~~~

## 8. CronJob

~~~text
CronJob
  ↓ schedule
Job
  ↓ template
Pod(s)
~~~

Source schedule examples:

~~~text
0,15,30,45 * * * *   → каждые 15 минут
0,30 * 1 * *         → 0 и 30 минут каждого часа первого дня месяца
0 3 * * 0            → 03:00 каждое воскресенье
~~~

`startingDeadlineSeconds` ограничивает допустимую задержку старта.

## 9. Open risks

### Failure injection

~~~bash
sudo ifconfig eth0 down
~~~

Это намеренно отключает сеть worker node. Не diagnostic read-only action.

Перед экспериментом:
- убедиться, что это не production;
- выбрать node с test workload;
- иметь независимый terminal/session;
- иметь доступ к source-supported recovery.

Recovery из главы:

~~~bash
gcloud compute instances reset <node-name>
~~~

### Destructive controller deletion

~~~bash
kubectl delete rs kubia
~~~

Source говорит, что ReplicaSet и его Pods удаляются.

Для destructive operations сначала проверять target object и matching Pods.
