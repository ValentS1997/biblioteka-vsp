# Commands and manifests — Chapter 19 advanced Pod scheduling

**Strict evidence:** RAG `p0641:c01`–`p0667:c01` (PDF 641–667). **No commands executed.** Classify observational, local-cluster-changing, cluster-state-changing, workload-generating, disruptive; no invented cleanup.

## Three-node minikube / kube-scheduler (p644–646)

```bash
minikube start --driver=virtualbox --nodes 3 --cni calico --cpus=2 --memory=2g --kubernetes-version=v1.30.0 --container-runtime=containerd
kubectl get nodes
```
**Effect:** starts/changes local Kubernetes lab, three Nodes, control plane and two workers; network and resources allocated. **Risk:** impact existing minikube profile, drivers, CPU/RAM consumption, mismatched versions. **Verification:** three Ready nodes `minikube`, `minikube-m02`, `minikube-m03` in source. **Rollback:** source gives no cluster delete/previous-state restoration [Needs confirmation]. `kubectl get nodes` read-only. Source p647 mentions `kubectl logs` and `/var/log/kube-scheduler.log` for self-hosted control plane without concrete command; no executable logs command invented.

Read-only view (p646–648):
```bash
kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
kubectl describe pod <имя_pod>
```
The latter is mentioned for checking whether a `Scheduled` event exists when `nodeName` bypasses scheduler. No live output checked.

## Direct binding using nodeName (p646–648)

Source `01_nodename/nginx-deployment.yaml` initial Deployment: `metadata.name: nginx-app`, `replicas: 5`, `image: nginx:1.17`, Pod labels `app: nginx`, `environment: test`. After first apply, five replicas spread across all three nodes; source then changes Pod template:
```yaml
# Fragment from 01_nodename/nginx-deployment.yaml
spec:
  template:
    spec:
      nodeName: minikube-m02
```
```bash
kubectl apply -f 01_nodename/nginx-deployment.yaml
```
**Effect:** creates/updates Deployment and ReplicaSets, replaces Pods, binds all five new Pods to m02 without scheduler choice. **Risk:** capacity exhaustion, node disappearance, loss of scheduling flexibility, disruption; `nginx:1.17` historical image. **Verification:** all 5 Running at m02 in p647. **Rollback:** undo of template/Deployment discussed conceptually but exact working rollback not shown [Needs confirmation].

## nodeSelector and missing label (p649–651)

```bash
kubectl describe nodes minikube
kubectl label nodes minikube-m02 node-type=superfast
kubectl label nodes minikube-m03 node-type=superfast
kubectl get nodes --show-labels | grep superfast
```
`describe` and `get` **read-only**; `label` **node-state-changing** and may affect other scheduling rules. Source nodeSelector:
```yaml
spec:
  template:
    spec:
      nodeSelector:
        node-type: superfast
```
Source p650 has a line-wrapped/space-corrupted path `02_nodeselector/nginx deployment.yaml` but identifies file `02_nodeselector/nginx-deployment.yaml` in YAML heading; command bytes for that specific apply line **[Needs confirmation]**. **Effect if applied:** new Pod placement only m02/m03. **Verification:** source five Pods, 3 on m02 and 2 on m03. **Rollback:** original Deployment selector/restoring labels not provided as full procedure.

A separate source file `02_nodeselector/nginx-deployment-slow.yaml` sets `nodeSelector.node-type: slow`, a label no nodes have:
```bash
kubectl apply -f 02_nodeselector/nginx-deployment-slow.yaml
```
**Effect:** starts rolling Deployment with unschedulable new Pods. **Risk:** availability and hung rollout; source shows **3 Pending + 4 Running**, with `maxSurge` and `maxUnavailable` behavior (p651). **Verification:** Pod table; no matching node. **Rollback:** change selector to matching label or return to previous Deployment revision; no specific rollback command [Needs confirmation].

## nodeAffinity: soft preferred, hard required (p652–656)

```bash
kubectl label nodes --overwrite minikube node-type=slow
kubectl label nodes --overwrite minikube-m02 node-type=fast
kubectl label nodes --overwrite minikube-m03 node-type=superfast
```
**Effect:** change shared Node labels; can affect other Pods. Source example `03_affinity/nginx-deployment.yaml`:
```yaml
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: NotIn
                    values: [extremelyslow]
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values: [fast, superfast]
```
```bash
kubectl apply -f 03_affinity/nginx-deployment.yaml
```
**Effect:** requires NOT extremelyslow, prefers fast/superfast, schedules only m02/m03 in source. **Risk:** if hard condition excludes all nodes, new Pods Pending; existing Pod placements remain until recreated. **Verification:** Pod NODE table in p655. **Rollback:** restore previous labels and/or Deployment template; no tested exact procedure [Needs confirmation].

Second phase:
```bash
kubectl label nodes --overwrite minikube node-type=slow
kubectl label nodes --overwrite minikube-m02 node-type=extremelyslow
kubectl label nodes --overwrite minikube-m03 node-type=extremelyslow
kubectl rollout restart deployment nginx-app
```
**Effect:** changes Node labels and forces a rolling replacement; source new five Pods all on `minikube` (p656). **Risk:** forced rescheduling/downtime with insufficient node resources, effect on other workloads. **Verification:** Pod-to-NODE listing. **Rollback:** source does not supply a restored-state snapshot or rollback command [Needs confirmation]. Source output last node truncated as `mi` p656 (see findings).

## Taints and tolerations: interruption-sensitive (p657–662)

Three effects: `NoSchedule` (hard placement prohibition), `PreferNoSchedule` (soft), `NoExecute` (scheduling prohibition and eviction unless tolerated). The source shows:
```bash
kubectl taint node minikube machine-check-exception=memory:NoExecute
kubectl taint node minikube machine-check-exception=memory:NoSchedule
```
**Effect:** mutate node taints; `NoExecute` can **evict active Pods**, `NoSchedule` can halt replacement. **Risk:** application outage and possible data loss; cannot assume a disposable node. **Verification:** p660 five Pending; p661 temporary placement followed by eviction after 60 s; with NoSchedule, all five eventually on m02/m03. **Rollback:** effect-specific `kubectl taint node minikube machine-check-exception=memory:NoExecute-` provided p658, but full two-effect teardown p662 text corrupted [Needs confirmation].

Source p658 also shows:
```bash
kubectl taint node minikube machine-check-exception=memory:NoExecute-
kubectl taint node minikube machine-check-exception:NoExecute-
```
Both are **state-changing removal**, potentially permit formerly excluded workloads; verify before/after. Exact command in source p662 to remove **both** taints is corrupted as `kubectl taint node minikube machine-check-exception-node/ minikube untainted` (line-break/export artifact) and must **NOT** be copied as a working command.

Toleration fragment p660:
```yaml
spec:
  template:
    spec:
      tolerations:
        - key: machine-check-exception
          operator: Equal
          value: memory
          effect: NoExecute
          tolerationSeconds: 60
```
```bash
kubectl apply -f 04_taints/nginx-deployment.yaml
kubectl rollout restart deployment nginx-app
```
**Effect:** replace Pod template removing old affinity and admitting tainted minikube for 60 s; can lead to re-placement/eviction churn until NoSchedule applied. **Verification:** p661 shows Pod on minikube then p661/662 without it after NoSchedule and time interval. **Rollback:** no full source-supported cleanup; p662 command broken. **Needs confirmation.**

Note source generic taint syntax p658 is printed as `kubectl taint node =:<имяУзла> <ключ>=<значение>:<эффект>`; the `=:` segment is not supported by the nearby working example; do not present generic expression as an executable recipe.

## Static Pod and advanced scheduler (p663–666)

Static Pod local file/remote URL watched by kubelet; mirror Pod exposed through API; **no source command to create one**. Managed/cloud control-plane access not provided. No external static Pod setup introduced.

Scheduler file supports profiles and plugins with extension points; `NodeRestriction` and Node authorizer discussed for protected labels. `percentageOfNodesToScore` controls sampled candidate nodes. p666 supplies **truncated/historical illustrative snippet**:
```yaml
apiVersion: kubescheduler.config.k8s.io/v1alpha1
kind: KubeSchedulerConfiguration
algorithmSource:
  provider: DefaultProvider
# ...source fragment omitted...
percentageOfNodesToScore: 50
```
**Classification:** illustration only, **not a verified runnable configuration**. p664 says older policies were replaced at v1.23 by scheduler configuration; juxtaposition with `v1alpha1` and `algorithmSource` is a source version inconsistency. Source does not show apply/restart/proof of this file. Avoid using it to reconfigure a live scheduler. Actual API schema and rollback **[Needs confirmation]**.

## Acceptance boundary

Source confirms its own sample Pod placements and evictions, **not** generalized production behavior with another scheduler, CNI, node set, taint defaults, descheduler or resource pressure. No CLI tested in current cluster, no external source corrected, no real workloads changed.
