# Шпаргалка: requests, limits, QoS и quotas

## 1. Requests

Container:

~~~text
resources:
  requests:
    cpu: 200m
    memory: 10Mi
~~~

Meaning in source:
- scheduler reserves capacity based on requests;
- Pod request = sum of container requests;
- CPU request also influences CPU-time share during contention.

200m CPU = 0.2 CPU core.

## 2. Capacity vs allocatable

~~~text
Node capacity
  - resources reserved for system/Kubernetes
  = Node allocatable
~~~

Scheduler uses allocatable.

Read-only:

~~~bash
kubectl describe nodes
~~~

## 3. Pending because of insufficient request capacity

Source example:
- running requests consume allocatable CPU;
- new Pod asks for 1 CPU;
- scheduler cannot place it;
- Pod remains Pending.

Diagnose:

~~~bash
kubectl describe po requests-pod-3
~~~

Expected source event:
Insufficient cpu.

## 4. CPU request fairness

If two CPU-hungry containers request:

~~~text
Pod A: 200m
Pod B: 1000m
~~~

then under CPU contention unused CPU is divided approximately 1:5 according to source example.

If one workload is idle, the other may consume more CPU when no limit blocks it.

## 5. Extended Resources

Source-era model:
- custom resource is added to Node capacity;
- example name: example.org/my-resource;
- amount must represent integer units;
- scheduler places Pods only where enough units remain.

Example use case:
GPU count.

Exact PATCH command is not reproduced in chapter artifact: [Needs confirmation].

## 6. Limits

~~~text
resources:
  limits:
    cpu: 1
    memory: 20Mi
~~~

If requests are omitted in source example, requests default to limits.

## 7. CPU vs memory limit

CPU:
~~~text
over limit → throttled
container stays running
~~~

Memory:
~~~text
over limit → OOM kill
possible restart
possible CrashLoopBackOff
~~~

Inspect:

~~~bash
kubectl describe pod
~~~

Source indicator:

~~~text
Reason: OOMKilled
Exit Code: 137
~~~

## 8. Limits may be overcommitted

~~~text
sum(requests) ≤ schedulable allocatable
sum(limits) may exceed node capacity
~~~

If everyone tries to consume their memory limits simultaneously, memory pressure can require process termination.

## 9. Source-era visibility caveat

Source demonstrates:

~~~bash
kubectl exec -it limited-pod top
~~~

and explains that ordinary tools in the container may see node-level CPU/memory rather than configured container limits.

This behavior is preserved as source-era statement.

## 10. QoS classes

### BestEffort

All containers:
- no CPU requests/limits;
- no memory requests/limits.

### Guaranteed

Every container:
- CPU request set;
- CPU limit set;
- memory request set;
- memory limit set;
- request == limit for each resource.

Source notes that setting limits alone may cause requests to default to the same values.

### Burstable

Everything else.

## 11. Memory-pressure priority

Source ordering:

~~~text
BestEffort
  ↓ killed first
Burstable
  ↓
Guaranteed
  ↓ killed last
~~~

Within same QoS class, source says OOM score and memory usage relative to request influence victim selection.

## 12. LimitRange

Namespace policy for individual objects.

Can define:
- min;
- max;
- defaultRequest;
- default limits;
- max limit/request ratio;
- source also shows PVC storage constraints.

Example behavior:
Pod requests 2 CPU while maximum is 1 → admission rejects Pod.

Defaults:
Pod with no resources can receive automatically injected requests/limits.

## 13. ResourceQuota

Namespace aggregate policy.

CPU/memory example source fields:

~~~text
requests.cpu
requests.memory
limits.cpu
limits.memory
~~~

Inspect:

~~~bash
kubectl describe quota
~~~

Shows:
- Used;
- Hard.

## 14. LimitRange vs ResourceQuota

~~~text
LimitRange
  → one Pod/container/PVC

ResourceQuota
  → sum across namespace
~~~

Recommended source relationship:
ResourceQuota + LimitRange defaults.

Why:
quota may reject Pods that omit requests/limits.

## 15. Storage quota

Source fields include:

~~~text
requests.storage
<storageclass>.storageclass.storage.k8s.io/requests.storage
~~~

Use:
- total PVC requested storage;
- per StorageClass requested storage.

## 16. Object-count quotas

Source examples:
- pods;
- replicationcontrollers;
- secrets;
- configmaps;
- persistentvolumeclaims;
- services;
- services.loadbalancers;
- services.nodeports;
- per-StorageClass PVC count.

This list is source-era and not modernized.

## 17. Quota scopes

Source scopes:
- BestEffort;
- NotBestEffort;
- Terminating;
- NotTerminating.

Example:
BestEffort + NotTerminating quota can limit number of matching Pods.

## 18. Monitoring pipeline

Source-era:

~~~text
Kubelet/cAdvisor
  ↓
Heapster
  ├─ kubectl top
  └─ InfluxDB → Grafana
~~~

Current usage:

~~~bash
kubectl top node
kubectl top pod --all-namespaces
~~~

Historical analysis:
InfluxDB + Grafana in source.

## 19. Tuning rule

If actual CPU usage routinely exceeds request:
- source recommends increasing CPU request to secure needed CPU under contention.

If actual memory usage is far below request:
- source recommends lowering memory request so reserved memory can be used by other workloads.

## Acceptance model

For each workload verify:
- CPU request reflects contention requirement;
- memory request reflects normal expected usage;
- CPU limit does not over-throttle workload;
- memory limit leaves safe headroom;
- QoS class is understood;
- namespace LimitRange/ResourceQuota will admit intended manifest;
- metrics are reviewed over time, not from one sample.
