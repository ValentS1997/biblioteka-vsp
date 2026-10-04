# Команды главы 17

Source policy: RAG-only. Read-only, workload-changing and high-risk operations are separated.

## Observe crash-looping Pods

~~~bash
kubectl get po
kubectl describe rs crashing-pods
kubectl describe po crashing-pods-f1tcd
~~~

Read-only.

Source lesson:
ReplicaSet may report desired/current Pod count satisfied even while containers repeatedly crash.

## Inspect init container

~~~bash
kubectl get po
kubectl logs fortune-client -c init
~~~

Read-only.

Source status example:
Init:0/1 while prerequisite is unavailable.

## Diagnose failed postStart

Source recommends Pod events/describe.

Exact full command listing in excerpt is not given.

Operational command: [Needs confirmation].

Source also shows:

~~~bash
kubectl exec my-pod cat logfile.txt
~~~

Read-only if file is only read.

## Graceful delete override

~~~bash
kubectl delete po mypod --grace-period=5
~~~

STATE-CHANGING / workload deletion.

Effect:
Kubelet gets 5-second graceful termination budget.

## Force-delete Pod

~~~bash
kubectl delete po mypod --grace-period=0 --force
~~~

CRITICAL WORKLOAD STATE CHANGE.

Risk:
API object can be deleted before old containers are confirmed stopped.

StatefulSet:
may allow replacement with same logical identity/storage while old instance still runs.

Use only when old instance is known dead/fenced.

## Read termination reason

~~~bash
kubectl describe po
~~~

Read-only.

Source shows termination message in Last State / Message.

## Read file-based logs

~~~bash
kubectl exec <pod> cat <log-file>
~~~

Read-only if only cat is executed.

## Previous-container logs

Source states to use the --previous option with kubectl logs.

Exact complete command listing: [Needs confirmation].

## Copy file from Pod

~~~bash
kubectl cp foo-pod:/var/log/foo.log foo.log
~~~

READ from container / writes local filesystem.

## Copy file into Pod

~~~bash
kubectl cp localfile foo-pod:/etc/remotefile
~~~

STATE-CHANGING container filesystem write.

## Minikube Docker daemon

~~~bash
eval $(minikube docker-env)
~~~

LOCAL SHELL ENVIRONMENT CHANGE.

Effect:
subsequent Docker CLI commands target Docker daemon inside Minikube VM.

## Copy local image into Minikube Docker daemon

~~~bash
docker save <image> | (eval $(minikube docker-env) && docker load)
~~~

STATE-CHANGING image store in Minikube VM.

Source constraint:
Pod imagePullPolicy should not be Always, otherwise runtime may pull registry image instead.

## Render Ksonnet/Jsonnet manifest

~~~bash
jsonnet kubia.ksonnet
~~~

Read-only generation to stdout.

Source-era toolchain.

## Declarative deployment

Source describes using:

~~~text
kubectl apply
~~~

after committing manifests to VCS.

Exact target path/arguments are deployment-specific and not reconstructed.

## Source-mentioned but not fully specified

- minikube mount exact command: [Needs confirmation].
- kubectl proxy exact invocation: [Needs confirmation].
- exact kubectl logs --previous full command: [Needs confirmation].
- exact apply path/flags: [Needs confirmation].

## Risk matrix

| Operation | Class |
|---|---|
| kubectl get/describe/logs | read-only |
| kubectl exec ... cat | read-only if command only reads |
| kubectl cp Pod→local | local file write |
| kubectl cp local→Pod | container filesystem change |
| delete --grace-period=N | workload deletion |
| delete --grace-period=0 --force | critical forced deletion |
| eval minikube docker-env | local shell environment change |
| docker load into Minikube | image-store change |
| kubectl apply | cluster desired-state change |
