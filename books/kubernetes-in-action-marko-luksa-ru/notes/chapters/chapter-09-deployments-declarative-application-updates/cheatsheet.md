# Шпаргалка: Deployment rollout и rollback

## 1. Старый client-driven rolling update

Source-era:

~~~bash
kubectl rolling-update kubia-v1 kubia-v2 --image=luksa/kubia:v2
~~~

Модель:

~~~text
kubectl client
  ↓ creates/modifies
old ReplicationController
new ReplicationController
  ↓ gradual scale down/up
Pods v1 → Pods v2
~~~

Проблема source framing:
- orchestration выполняет kubectl client;
- process сложнее и хрупче;
- command объявлен устаревшим.

## 2. Deployment model

~~~text
Deployment
  ├─ ReplicaSet revision 1 → Pods v1
  ├─ ReplicaSet revision 2 → Pods v2
  └─ ReplicaSet revision 3 → Pods v3
~~~

Deployment не управляет Pods напрямую; ReplicaSet делает это за него.

## 3. Create / observe

Source-era create:

~~~bash
kubectl create -f kubia-deployment-v1.yaml --record
~~~

Read-only:

~~~bash
kubectl rollout status deployment kubia
kubectl get po
kubectl get replicasets
kubectl describe deployment kubia
~~~

## 4. What triggers rollout

Изменение Pod template.

Source methods:

~~~text
kubectl edit
kubectl patch
kubectl apply
kubectl replace
kubectl set image
~~~

Пример:

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v2
~~~

Изменение только minReadySeconds не изменяет существующие Pods и само по себе не запускает новый rollout.

## 5. Rollback

Previous revision:

~~~bash
kubectl rollout undo deployment kubia
~~~

Specific revision:

~~~bash
kubectl rollout undo deployment kubia --to-revision=1
~~~

History:

~~~bash
kubectl rollout history deployment kubia
~~~

Не удалять old ReplicaSets вручную, если нужны rollback revisions.

## 6. RollingUpdate speed

Source fragment:

~~~text
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
~~~

maxSurge:
- additional Pods above desired replicas.

maxUnavailable:
- allowed reduction in available Pods relative to desired replicas.

## 7. Pause / resume

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v4
kubectl rollout pause deployment kubia
~~~

После проверки:

~~~bash
kubectl rollout resume deployment kubia
~~~

Source uses this as canary-like demonstration.

Caveat:
- undo does not take effect while Deployment remains paused.

## 8. Blocking bad rollout

Source safety combination:

~~~text
readinessProbe
+
minReadySeconds: 10
+
maxUnavailable: 0
~~~

Effect:
- failing new Pod removed from Service endpoints;
- Pod never becomes available;
- rollout cannot continue replacing healthy old Pods.

## 9. Failed rollout condition

Read-only:

~~~bash
kubectl describe deploy kubia
~~~

Source condition:

~~~text
Progressing=False
Reason=ProgressDeadlineExceeded
~~~

Controlled by:

~~~text
progressDeadlineSeconds
~~~

Source-era cleanup:

~~~bash
kubectl rollout undo deployment kubia
~~~

## 10. Recreate vs RollingUpdate

### Recreate

~~~text
delete all old Pods
then create new Pods
~~~

Risk: downtime.

### RollingUpdate

~~~text
incrementally create new
incrementally remove old
~~~

Designed for continued availability, subject to readiness and strategy limits.

## 11. Destructive/state-changing boundaries

### Destructive setup reset

~~~bash
kubectl delete rc --all
~~~

Deletes all ReplicationControllers in current namespace; source uses it only before switching demo to Deployment.

### State-changing rollout commands

- kubectl set image
- kubectl patch
- kubectl apply
- kubectl rollout undo
- kubectl rollout pause
- kubectl rollout resume

## Acceptance model

Before rollout:
- current revision known;
- health/readiness mechanism exists;
- maxSurge/maxUnavailable understood;
- rollback path/history retained;
- desired image/template verified.

During rollout:
- rollout status progresses;
- expected number of available Pods maintained;
- Service traffic avoids unready Pods.

After rollout:
- all desired replicas available;
- expected revision active;
- no stuck ProgressDeadlineExceeded condition.
