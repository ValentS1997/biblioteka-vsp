# Шпаргалка: autoscaling Pods и nodes

## 1. HPA control loop

~~~text
Pod metrics
  ↓
HPA controller
  ↓ desired replicas
Scale subresource
  ↓
Deployment / ReplicaSet / RC / StatefulSet
  ↓
Pods
~~~

Source stages:
1. collect metrics;
2. calculate replica count;
3. update Scale subresource.

## 2. Source-era metric pipeline

~~~text
containers
  ↓
cAdvisor in Kubelet
  ↓
Heapster
  ↓
HorizontalPodAutoscaler
~~~

Important:
metrics propagate periodically, so scaling is not instant.

## 3. CPU utilization basis

HPA CPU percentage is based on:

~~~text
actual CPU usage / CPU request
~~~

Not:
- node CPU capacity;
- CPU limit.

Therefore CPU requests must exist.

Example:
request = 100m
usage = 108m
utilization = 108%

## 4. Create CPU HPA

~~~bash
kubectl autoscale deployment kubia   --cpu-percent=30   --min=1   --max=5
~~~

Source target:
- average CPU utilization ≈ 30%;
- never below 1;
- never above 5.

## 5. Inspect HPA

~~~bash
kubectl get hpa
kubectl describe hpa
kubectl get hpa.v2beta1.autoscaling kubia -o yaml
~~~

Events may show:
- SuccessfulRescale;
- metrics below target;
- CPU utilization above target.

## 6. Simplified replica calculation

One metric:

~~~text
desired replicas
≈ sum(current metric values) / target value
~~~

Source example:

~~~text
108% / 30% = 3.6 → 4 replicas
~~~

Multiple metrics:
- calculate desired replicas for each metric;
- choose the largest result.

## 7. Scaling target selection

Source advice:
autoscale Deployment, not underlying ReplicaSet.

Reason:
Deployment creates a new ReplicaSet on rollout; HPA should follow workload abstraction across revisions.

## 8. Load generation

Source pattern:

~~~bash
kubectl run -it --rm --restart=Never loadgenerator   --image=busybox   -- sh -c "while true; do wget -O - -q http://kubia.default; done"
~~~

Creates sustained traffic.

Stop with Ctrl+C.
--rm removes temporary Pod.

## 9. Scale timing source-era

Source limits:
- scale-up does not immediately repeat after a recent rescale;
- scale-down is even less frequent;
- source states approximately 3 minutes for scale-up and 5 minutes for scale-down.

Preserve as historical/source-era behavior.

## 10. Change HPA target

Source exercise:
change target CPU 30% → 60%.

~~~bash
kubectl edit hpa kubia
~~~

Edit:
~~~text
targetAverageUtilization: 60
~~~

This changes scaling policy.

## 11. Metric types

Source v2beta1 HPA types:

### Resource

Example:
CPU utilization.

### Pods

Per-Pod custom metric.

Example:
QPS.

~~~text
targetAverageValue: 100
~~~

### Object

Metric from another API object.

Example:
Ingress latencyMillis target 20.

## 12. Good autoscaling metric

Good metric approximately behaves:

~~~text
replicas ×2
→ per-replica metric ≈ /2
~~~

Source good example:
QPS.

Source problematic example:
memory consumption.

## 13. Scale to zero

Source-era HPA:
~~~text
minReplicas cannot be 0
~~~

So HPA cannot idle workload to zero in source model.

## 14. Vertical autoscaling

Source-era:
- cannot change requests/limits of existing running Pod;
- full vertical Pod autoscaling unavailable.

Experimental InitialResources:
- sets requests on newly created Pods;
- uses historical consumption tied to container image/tag.

## 15. Cluster Autoscaler scale-up

~~~text
unschedulable Pod
  ↓
Cluster Autoscaler
  ↓
find node group type that could fit Pod
  ↓
increase node group
  ↓
new Node registers
  ↓
scheduler can place Pod
~~~

## 16. Cluster Autoscaler scale-down

Source checks include:
- low requested CPU/memory;
- no blocking system-only workload;
- no unmanaged Pod;
- no local-storage workload;
- Pods can be recreated elsewhere.

Before deletion:
- mark node unschedulable;
- evict movable Pods.

## 17. Manual node lifecycle

~~~bash
kubectl cordon <node>
kubectl drain <node>
kubectl uncordon <node>
~~~

cordon:
- no new Pods scheduled.

drain:
- cordon + eviction;
- service-impacting.

uncordon:
- restores scheduling.

## 18. Enable source GKE Cluster Autoscaler

~~~bash
gcloud container clusters update kubia   --enable-autoscaling   --min-nodes=3   --max-nodes=5
~~~

Cloud infrastructure state change.

## 19. PodDisruptionBudget

Source:

~~~bash
kubectl create pdb kubia-pdb   --selector=app=kubia   --min-available=3
~~~

Meaning:
voluntary evictions must preserve at least 3 selected Pods.

Inspect:

~~~bash
kubectl get pdb kubia-pdb -o yaml
~~~

Source note:
maxUnavailable available starting Kubernetes 1.7.

## 20. PDB boundary

PDB protects against:
- Cluster Autoscaler voluntary node removal;
- kubectl drain.

PDB does not protect against:
- unexpected node failure.

## Acceptance model

For HPA:
- CPU requests exist when using CPU utilization;
- min/max replicas explicit;
- metric reacts predictably to replica count;
- HPA events/desired replicas observed;
- load test removed afterward.

For Cluster Autoscaler:
- unschedulable reason confirmed;
- node group bounds reviewed;
- cloud cost impact understood;
- movable workloads identified;
- PDB protects required availability.

For drain:
- node and workloads identified;
- PDB/availability checked;
- rollback point is uncordon if drain is aborted before node removal.
