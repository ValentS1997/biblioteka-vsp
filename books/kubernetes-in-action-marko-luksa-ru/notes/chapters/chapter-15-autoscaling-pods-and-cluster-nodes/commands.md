# Команды главы 15

Source policy: RAG-only. Read-only, workload-changing and infrastructure-changing actions are separated.

## Create HPA

~~~bash
kubectl autoscale deployment kubia   --cpu-percent=30   --min=1   --max=5
~~~

STATE-CHANGING.

Effect:
creates HorizontalPodAutoscaler and allows controller to modify Deployment replica count between 1 and 5.

## Inspect HPA

~~~bash
kubectl get hpa
kubectl describe hpa
kubectl get hpa.v2beta1.autoscaling kubia -o yaml
~~~

Read-only.

Source may initially show:

~~~text
TARGETS: <unknown> / 30%
~~~

until metrics propagate.

## Inspect target Deployment

~~~bash
kubectl get deployment
~~~

Read-only.

Use to compare HPA desired behavior with Deployment replica count.

## Expose Deployment for load test

~~~bash
kubectl expose deployment kubia --port=80 --target-port=8080
~~~

STATE-CHANGING.

Creates Service kubia.

## Observe HPA and Deployment

~~~bash
watch -n 1 kubectl get hpa,deployment
~~~

Read-only polling.

Source notes platform alternatives to watch.

## Generate sustained load

~~~bash
kubectl run -it --rm --restart=Never loadgenerator   --image=busybox   -- sh -c "while true; do wget -O - -q http://kubia.default; done"
~~~

STATE-CHANGING / LOAD-GENERATING.

Effects:
- creates temporary Pod;
- continuously sends requests;
- intentionally raises target workload CPU usage;
- Ctrl+C stops command;
- --rm removes temporary Pod.

Do not run against production unless load impact is intended.

## Change HPA target — explicit chapter exercise

~~~bash
kubectl edit hpa kubia
~~~

STATE-CHANGING SCALING POLICY.

Source change:

~~~text
targetAverageUtilization: 30
→
targetAverageUtilization: 60
~~~

Verification:

~~~bash
kubectl get hpa
kubectl describe hpa
~~~

Expected:
target reflects 60%;
future replica decisions use new target.

## Delete/recreate HPA

Source states deleting HPA disables autoscaling while leaving target workload at its current replica count.

Exact delete command is not explicitly shown in the verified chapter excerpt.

Command: [Needs confirmation].

Do not reconstruct from memory.

## Custom metrics / Object metrics

Source provides HPA manifest fragments, not a complete adapter installation or metric-provider command sequence.

Operational setup commands: [Needs confirmation].

## Vertical autoscaling

Source-era full vertical autoscaling for running Pods is unavailable.

No VPA command sequence is provided.

Do not invent one.

## Manual node scheduling control

~~~bash
kubectl cordon <node>
~~~

STATE-CHANGING scheduler placement.

Effect:
marks node unschedulable; existing Pods remain.

~~~bash
kubectl drain <node>
~~~

HIGH-IMPACT STATE CHANGE.

Effect:
marks node unschedulable and evicts Pods.

Pre-checks:
- identify workloads on node;
- check PDBs;
- confirm replacement capacity;
- understand local/unmanaged workload constraints.

Source recovery:

~~~bash
kubectl uncordon <node>
~~~

STATE-CHANGING.

Restores scheduling to node.

## Enable Cluster Autoscaler on source GKE cluster

~~~bash
gcloud container clusters update kubia   --enable-autoscaling   --min-nodes=3   --max-nodes=5
~~~

CLOUD INFRASTRUCTURE STATE CHANGE.

Effects:
- autoscaler may add/delete cloud nodes;
- changes capacity and cost envelope.

Verify source status concept:
Cluster Autoscaler writes status to ConfigMap cluster-autoscaler-status in kube-system.

Exact kubectl command to inspect this ConfigMap is not explicitly shown in chapter excerpt: [Needs confirmation].

## Source GCE environment settings

Source lists:

~~~text
KUBE_ENABLE_CLUSTER_AUTOSCALER=true
KUBE_AUTOSCALER_MIN_NODES=3
KUBE_AUTOSCALER_MAX_NODES=5
~~~

These are source-era kube-up.sh settings, not generalized beyond source.

## Create PodDisruptionBudget

~~~bash
kubectl create pdb kubia-pdb   --selector=app=kubia   --min-available=3
~~~

STATE-CHANGING availability policy.

Verify:

~~~bash
kubectl get pdb kubia-pdb -o yaml
~~~

Read-only.

Expected source fields:
- minAvailable: 3;
- selector matchLabels app: kubia.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl get/describe HPA | read-only |
| watch kubectl get | read-only polling |
| kubectl autoscale | scaling policy state change |
| kubectl expose | Service creation |
| loadgenerator Pod | workload creation + intentional load |
| kubectl edit hpa | scaling policy state change |
| kubectl cordon | scheduler placement change |
| kubectl drain | high-impact workload eviction |
| kubectl uncordon | scheduler placement change |
| gcloud enable autoscaling | cloud capacity/cost state change |
| create PDB | availability policy change |
