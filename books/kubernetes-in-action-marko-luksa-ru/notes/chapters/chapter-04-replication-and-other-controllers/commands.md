# Команды главы 4

Source policy: только RAG главы 4. Команды разделены на read-only, state-changing, failure-injection и destructive.

## Read-only — liveness и Pod

~~~bash
kubectl get po kubia-liveness
~~~

Проверяет status и `RESTARTS`.

~~~bash
kubectl logs <pod-name> --previous
~~~

Read-only. Source рекомендует для логов предыдущего container instance после restart.

~~~bash
kubectl describe po kubia-liveness
~~~

Read-only. Показывает liveness configuration, restart count, exit details и events.

## Liveness manifest fragments

Source поддерживает три механизма:
- HTTP GET;
- TCP socket;
- Exec.

HTTP example:

~~~text
livenessProbe:
  httpGet:
    path: /
    port: 8080
  initialDelaySeconds: 15
~~~

Source-observed defaults/examples:
- timeout 1s;
- period 10s;
- restart after 3 consecutive failures.

## ReplicationController — create/read

Source manifest file: `kubia-rc.yaml`.

~~~bash
kubectl create -f kubia-rc.yaml
~~~

State-changing: создаёт ReplicationController.

Verification:

~~~bash
kubectl get pods
kubectl get rc
kubectl describe rc kubia
~~~

## Delete one managed Pod

~~~bash
kubectl delete pod <pod-name>
~~~

Destructive для конкретного Pod.

Expected source behavior: ReplicationController замечает уменьшение matching Pods и создаёт replacement.

Verification:

~~~bash
kubectl get pods
~~~

## Node-failure exercise — intentional failure injection

### Preflight

Source требует выбрать node, на котором работает хотя бы один test Pod; для поиска placement используется wide output.

`kubectl get pods -o wide` поддерживается surrounding text главы как способ выбрать node.

### SSH

~~~bash
gcloud compute ssh <node-name>
~~~

Interactive access.

### Failure injection

~~~bash
sudo ifconfig eth0 down
~~~

HIGH RISK / state-changing / network outage.

Effect: сетевой интерфейс worker node выключается; SSH session перестаёт отвечать.

### Verification из другого terminal

~~~bash
kubectl get node
kubectl get pods
~~~

Expected:
- node → `NotReady`;
- Pod на потерянном node позже → `Unknown`;
- controller создаёт replacement Pod.

### Recovery

~~~bash
gcloud compute instances reset <node-name>
~~~

State-changing infrastructure action.

Acceptance: node после перезагрузки возвращается в `Ready`; source говорит, что Pod со статусом Unknown затем удаляется.

## Moving Pod in/out of controller scope

### Add unrelated label

~~~bash
kubectl label pod <pod-name> type=special
~~~

State-changing metadata.

### Change selector-matching label

~~~bash
kubectl label pod <pod-name> app=foo --overwrite
~~~

State-changing.

Verification:

~~~bash
kubectl get pods --show-labels
kubectl get pods -L app
~~~

Expected: Pod перестаёт соответствовать RC selector; RC создаёт replacement matching Pod.

## Edit ReplicationController

~~~bash
kubectl edit rc kubia
~~~

State-changing.

Source exercise: добавить label в Pod template.

Important: existing Pods не меняются; replacement Pods, созданные позже, используют изменённый template.

### Configure editor

~~~bash
export KUBE_EDITOR="/usr/bin/nano"
~~~

Shell-session state change.

## Scale ReplicationController

~~~bash
kubectl scale rc kubia --replicas=10
kubectl scale rc kubia --replicas=3
~~~

State-changing desired state.

Verification:

~~~bash
kubectl get rc
kubectl get pods
~~~

Rollback: вернуть `spec.replicas` к предыдущему значению.

## Delete RC but preserve Pods

~~~bash
kubectl delete rc kubia --cascade=false
~~~

State-changing/destructive for controller object, but source says Pods remain running.

Use case: replace controller type without interrupting existing Pods.

## ReplicaSet

Source manifest: `kubia-replicaset.yaml`.

Source explicitly says ReplicaSet is created from YAML using `kubectl create`, but exact full command line is not present in the retrieved command excerpt; it is not reconstructed here.

Read-only:

~~~bash
kubectl get rs
kubectl describe rs
~~~

Destructive cleanup:

~~~bash
kubectl delete rs kubia
~~~

Source says deleting ReplicaSet deletes its Pods.

## ReplicaSet selectors

Source `matchExpressions` operators:

~~~text
In
NotIn
Exists
DoesNotExist
~~~

Multiple expressions and `matchLabels` + `matchExpressions` are combined as AND.

## DaemonSet

Create:

~~~bash
kubectl create -f ssd-monitor-daemonset.yaml
~~~

State-changing.

Read-only:

~~~bash
kubectl get ds
kubectl get po
kubectl get node
~~~

Add matching node label:

~~~bash
kubectl label node <node-name> disk=ssd
~~~

State-changing. Expected: DaemonSet creates daemon Pod on matching node.

Change node classification:

~~~bash
kubectl label node <node-name> disk=hdd --overwrite
~~~

State-changing. Expected source result: daemon Pod on that node enters `Terminating`.

Exact DaemonSet delete command is not present in retrieved command lines, although the prose says the object can be deleted; command is not invented.

## Job

Source manifest uses:
- `apiVersion: batch/v1`;
- `kind: Job`;
- `restartPolicy: OnFailure`;
- image `luksa/batch-job`.

Source says Job is created using `kubectl create`, but exact command line is not present in the retrieved excerpt.

Read-only:

~~~bash
kubectl get jobs
kubectl get po
kubectl get po -a
kubectl logs <job-pod-name>
kubectl get job
~~~

## Job parallelism

Source properties:

~~~text
completions: 5
parallelism: 2
~~~

Dynamic parallelism change:

~~~bash
kubectl scale job multi-completion-batch-job --replicas 3
~~~

State-changing. Source interprets this as increasing Job `parallelism` from 2 to 3.

## Job runtime limits

Source fields:

~~~text
activeDeadlineSeconds
spec.backoffLimit
~~~

Source says default `backoffLimit` is 6 when not explicitly set.

## CronJob

Source manifest:
- `apiVersion: batch/v1beta1`;
- `kind: CronJob`;
- `schedule: "0,15,30,45 * * * *"`;
- `jobTemplate`;
- `restartPolicy: OnFailure`.

No exact `kubectl create ...` command line for CronJob is present in the retrieved chapter command excerpt, so it is not invented.

Source scheduling fields:

~~~text
schedule
jobTemplate
startingDeadlineSeconds
~~~

Reliability note from source:
- duplicate Job creation may occur;
- a scheduled Job may also be missed;
- Jobs should be idempotent;
- later run should account for work missed by a previous run.

## Destructive / risk summary

| Command | Risk |
|---|---|
| `kubectl delete pod <pod>` | destroys Pod; controller may recreate |
| `kubectl delete rc kubia --cascade=false` | removes controller, preserves Pods |
| `kubectl delete rs kubia` | removes ReplicaSet and source says Pods too |
| `sudo ifconfig eth0 down` | intentionally disconnects worker node |
| `gcloud compute instances reset <node>` | resets VM/node |

Failure-injection and destructive commands must not be chained into opaque one-liners.
