# Команды главы 14

Source policy: RAG-only. Commands separated into read-only, state-changing and policy-impacting actions.

## Inspect resource usage inside request Pod

~~~bash
kubectl exec -it requests-pod top
~~~

Read-only process/resource inspection inside container.

## Inspect node capacity and allocatable

~~~bash
kubectl describe nodes
~~~

Read-only.

Source distinction:
- Capacity = total node resources;
- Allocatable = resources scheduler may allocate to Pods.

## Create Pod with 800m CPU request

Source-era:

~~~bash
kubectl run requests-pod-2 --image=busybox --restart Never   --requests='cpu=800m,memory=20Mi'   -- dd if=/dev/zero of=/dev/null
~~~

STATE-CHANGING.

## Create Pod with 1 CPU request

~~~bash
kubectl run requests-pod-3 --image=busybox --restart Never   --requests='cpu=1,memory=20Mi'   -- dd if=/dev/zero of=/dev/null
~~~

STATE-CHANGING.

Verify:

~~~bash
kubectl get po requests-pod-3
kubectl describe po requests-pod-3
~~~

Expected source result:
- Pending;
- FailedScheduling / Insufficient cpu.

## Free requested capacity

~~~bash
kubectl delete po requests-pod-2
~~~

STATE-CHANGING / workload deletion.

Then:

~~~bash
kubectl get po
~~~

Source result:
requests-pod-3 becomes Running after enough requested CPU is freed.

## Inspect allocated requests/limits on node

~~~bash
kubectl describe node
~~~

Read-only.

Useful section:
Allocated resources / Non-terminated Pods.

## Create limited Pod

~~~bash
kubectl create -f limited-pod.yaml
~~~

STATE-CHANGING.

Inspect:

~~~bash
kubectl exec -it limited-pod top
~~~

Read-only.

## Diagnose OOMKilled / CrashLoopBackOff

~~~bash
kubectl get po
kubectl describe pod
~~~

Read-only.

Source indicators:
- CrashLoopBackOff;
- Reason: OOMKilled;
- Exit Code: 137.

## LimitRange rejection demonstration

~~~bash
kubectl create -f limits-pod-too-big.yaml
~~~

STATE-CHANGING request expected to be REJECTED.

Source example:
Pod requests 2 CPU when Pod/container maximum is 1 CPU.

## LimitRange defaulting demonstration

~~~bash
kubectl create -f ../Chapter03/kubia-manual.yaml
kubectl describe po kubia-manual
~~~

First STATE-CHANGING, second read-only.

Source result after LimitRange:
- Limits: cpu 200m, memory 100Mi;
- Requests: cpu 100m, memory 10Mi.

## Inspect ResourceQuota

~~~bash
kubectl describe quota
~~~

Read-only.

Source output compares Used vs Hard for:
- requests.cpu;
- requests.memory;
- limits.cpu;
- limits.memory.

## Quota rejection when requests/limits missing

Source demonstration:

~~~bash
kubectl create -f ../Chapter03/kubia-manual.yaml
~~~

With ResourceQuota and without LimitRange defaults, expected:
Forbidden because CPU/memory requests and limits must be specified.

This is admission-policy behavior, not scheduler failure.

## Extended Resource modification

Source says Node capacity can be modified through an HTTP PATCH to advertise custom resources.

Exact PATCH command: [Needs confirmation].

Do not reconstruct from memory.

## Source cleanup before monitoring section

Source asks to remove all ResourceQuota and LimitRange resources created in examples.

Exact broad cleanup command: [Needs confirmation].

Do not invent namespace-wide delete syntax.

## Enable source-era Heapster in Minikube

~~~bash
minikube addons enable heapster
~~~

STATE-CHANGING add-on enablement.

Source-era only.

## Read current usage

~~~bash
kubectl top node
kubectl top pod --all-namespaces
~~~

Read-only metric queries.

Source warns metrics may be unavailable for several minutes after enabling Heapster.

Container-level source tip:
use --containers with top Pod command.

## Discover Grafana endpoint

~~~bash
kubectl cluster-info
~~~

Read-only.

## Open source-era Grafana in Minikube

~~~bash
minikube service monitoring-grafana -n kube-system
~~~

Opens/proxies Service through Minikube workflow.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl get/describe/top | read-only |
| kubectl exec ... top | read-only workload inspection |
| kubectl run/create Pod | state-changing |
| kubectl delete Pod | workload deletion |
| LimitRange/ResourceQuota creation | namespace admission-policy change |
| custom Node resource PATCH | node scheduling-capacity state change |
| minikube addons enable heapster | cluster add-on state change |
