# Команды главы 9

Source policy: RAG-only. Commands separated into read-only, state-changing, destructive and obsolete/source-era.

## Initial Service test — read-only/workload-generating

~~~bash
kubectl get svc kubia
~~~

Read-only.

Source curls Service external IP in a loop. Operational form:

~~~bash
while true; do curl http://<service-external-ip>; done
~~~

Workload-generating. Replace source-specific IP with actual Service endpoint.

## Obsolete source-era rolling update

~~~bash
kubectl rolling-update kubia-v1 kubia-v2 --image=luksa/kubia:v2
~~~

STATE-CHANGING and explicitly obsolete in source.

Verbose form:

~~~bash
kubectl rolling-update kubia-v1 kubia-v2 --image=luksa/kubia:v2 --v 6
~~~

Source uses verbose logging to show kubectl API requests.

Read-only inspection:

~~~bash
kubectl describe rc kubia-v2
kubectl describe rc kubia-v1
kubectl get po --show-labels
~~~

## Destructive cleanup before Deployment demo

~~~bash
kubectl delete rc --all
~~~

DESTRUCTIVE / broad scope.

Effect:
- deletes all ReplicationControllers in current namespace;
- source uses it to clear old demo controllers before creating Deployment.

Preflight:
- list target namespace RCs first;
- verify no unrelated RC-managed workloads.

Rollback: [Needs confirmation] — source assumes recreation from manifests.

## Create Deployment

~~~bash
kubectl create -f kubia-deployment-v1.yaml --record
~~~

STATE-CHANGING.

Source says --record stores command in revision history change cause.

Read-only verification:

~~~bash
kubectl rollout status deployment kubia
kubectl get po
kubectl get replicasets
~~~

## Deployment modification methods

Source table lists:

~~~bash
kubectl edit deployment kubia
~~~

Interactive state change.

Patch example:

~~~bash
kubectl patch deployment kubia -p '{"spec": {"minReadySeconds": 10}}'
~~~

State-changing.

Apply:

~~~bash
kubectl apply -f kubia-deployment-v2.yaml
~~~

State-changing; can also create object if missing according to source.

Replace:

~~~bash
kubectl replace -f kubia-deployment-v2.yaml
~~~

State-changing; source requires object already exists.

Set image:

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v2
~~~

State-changing; changes Pod template and initiates rollout.

## Observe rollout

~~~bash
kubectl rollout status deployment kubia
kubectl get rs
kubectl get po
~~~

Read-only.

## Deploy intentionally bad v3 in source demo

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v3
kubectl rollout status deployment kubia
~~~

STATE-CHANGING.

Source v3 intentionally begins returning HTTP 500 after several requests.

This is failure demonstration, not production deployment guidance.

## Rollback

Previous revision:

~~~bash
kubectl rollout undo deployment kubia
~~~

STATE-CHANGING.

Specific revision:

~~~bash
kubectl rollout undo deployment kubia --to-revision=1
~~~

STATE-CHANGING.

History:

~~~bash
kubectl rollout history deployment kubia
~~~

Read-only.

## Pause/resume

Start new image:

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v4
~~~

Immediately pause:

~~~bash
kubectl rollout pause deployment kubia
~~~

State-changing.

Resume:

~~~bash
kubectl rollout resume deployment kubia
~~~

State-changing.

Source caveat:
- rollout undo does not undo a paused Deployment until resumed.

## Apply readiness-gated Deployment

~~~bash
kubectl apply -f kubia-deployment-v3-with-readinesscheck.yaml
~~~

STATE-CHANGING.

Source manifest includes:
- minReadySeconds: 10
- maxSurge: 1
- maxUnavailable: 0
- readinessProbe every 1 second
- image v3

Observe:

~~~bash
kubectl rollout status deployment kubia
kubectl get po
~~~

Expected source behavior:
- one v3 Pod exists but remains 0/1 Ready;
- Service traffic continues to healthy v2 Pods;
- rollout stops progressing.

## Diagnose blocked rollout

~~~bash
kubectl describe deploy kubia
~~~

Read-only.

Source condition example:

~~~text
Available=True
Progressing=False
Reason=ProgressDeadlineExceeded
~~~

## Abort bad rollout

~~~bash
kubectl rollout undo deployment kubia
~~~

STATE-CHANGING rollback.

## Important source-era apply caveat

Source warns:
if apply manifest contains replicas different from live desired replicas, apply can rescale Deployment.

Operational implication:
- inspect manifest before apply;
- omit replicas when source intent is image/config update without scaling.

## Risk matrix

| Operation | Class |
|---|---|
| get/describe/rollout status/history | read-only |
| curl loop | workload-generating |
| delete rc --all | destructive broad-scope |
| rolling-update | obsolete state-changing |
| create/patch/apply/replace/set image | state-changing |
| rollout pause/resume/undo | state-changing |
| intentional v3 rollout | failure demonstration |
