# Commands and YAML — Глава 20: Pod/Node autoscaling

**Strict source:** RAG p0668:c01–p0704:c01, PDF 668–704. Commands drawn from chapter text, not executed. Read-only vs state-changing marked; no credentials supplied or invented corrections to source YAML.

## Requests/limits and nginx Pending (p671–673)

Source fragment:
```yaml
# resource-limit/nginx-deployment.yaml (partial)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-example
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: nginx
          image: nginx:1.17
          resources:
            requests:
              cpu: 100m
              memory: 50Mi
            limits:
              cpu: 200m
              memory: 60Mi
```

**Note:** excerpt omits Deployment `selector` and Pod metadata: **not a standalone runnable YAML**. Source then changes both `requests.cpu` and `limits.cpu` to `2000m`.

```bash
kubectl apply -f resource-limit/nginx-deployment.yaml
kubectl describe node minikube-m03
kubectl get pod
kubectl describe pod nginx-deployment-example-69bd6d55b4-n2mzq
```

**Classification:** `apply` workload-changing, other commands read-only. **Effect:** new 5-Pod Deployment and later a rolling rollout with large CPU requests. **Risk:** 2000m may exceed node allocatable, cause Pending and stalled rollout; 60Mi memory limit may terminate memory-hungry processes. **Verification:** node allocatable/requests plus FailedScheduling; **source event includes both `Insufficient cpu` and `untolerated taint machine-check-exception:memory`** (p673). **Rollback:** return to prior manifest values suggested in concept; exact source CLI/recorded previous rollout [Needs confirmation].

## VPA install and metrics (pp675–678)

```bash
minikube start --feature-gates=InPlacePodVerticalScaling=true
gcloud container clusters update <имя_кластера> --enable-vertical-pod-autoscaling
gcloud container clusters create k8sforbeginners --num-nodes=2 --zone=us-central1-a --enable-vertical-pod-autoscaling
git clone https://github.com/kubernetes/autoscaler
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
kubectl get pods -n kube-system | grep vpa
minikube addons enable metrics-server
```

**Classification:** `get pods` read-only; `cd` changes local shell directory; `git clone` writes unpinned remote repo content; remaining commands state-changing. **Effect:** minikube cluster/features, billable GKE change or create, installation of VPA CRD, Admission/Updater/Recommender controllers and metrics server. **Risks:** historical alpha/stable notes conflict across versions, control-plane restart p676, unreviewed remote install script, API admission changes, workloads and cloud costs. **Verification:** three `vpa-*` Pod Ready (p677); current CRD/metrics/API policy [Needs confirmation]. **Rollback:** no complete supported VPA uninstall or GKE feature disable command in chapter [Needs confirmation].

Source also instructs editing `/etc/kubernetes/manifests/kube-apiserver.yaml` with `--feature-gates=InPlacePodVerticalScaling=true` (p676). **CONTROL-PLANE DISRUPTIVE:** editing static API server manifest can restart API; source p676 calls feature alpha but footnote claims stable at v1.35, so do not apply without version-specific verification, backup and authority.

## VPA hamster experiment (pp678–683)

Source Deployment in `vpa-demo` includes 5 replicas `hamster`, `image: ubuntu:20.04`, request `cpu: 100m`, `memory: 50Mi`, loop `while true; do timeout 0.5s yes >/dev/null; sleep 0.5s; done`, no explicit limits (pp678–679). VPA:
```yaml
# vpa/hamster-vpa.yaml (core excerpt; source)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: hamster-vpa
  namespace: vpa-demo
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hamster
  updatePolicy:
    updateMode: 'Off'
  resourcePolicy:
    containerPolicies:
      - containerName: '*'
        minAllowed: {cpu: 100m, memory: 50Mi}
        maxAllowed: {cpu: 1, memory: 500Mi}
        controlledResources: [cpu, memory]
```
**Mode `Off` must be quoted in source** so YAML tooling does not interpret it as a boolean (p681). In phase 2 source replaces `Off` with `Auto` (p682).

```bash
kubectl apply -f vpa/vpa-demo-ns.yaml
kubectl apply -f vpa/hamster-deployment.yaml
kubectl get po -n vpa-demo
kubectl top pod -n vpa-demo
kubectl apply -f vpa/hamster-vpa.yaml
kubectl describe vpa hamster-vpa -n vpa-demo
kubectl get po -n vpa-demo -w
kubectl describe pod hamster-7fb7dbff7-24p89 -n vpa-demo
```

**Classification:** `apply` mutates namespace/Deployment/CRD instance and can delete/recreate Pod when Auto; `get/top/describe/watch` read-only. **Effect:** 5 CPU-consuming hamster Pod; VPA calculates target CPU 587m/memory 262144k and in Auto recreates Pod with revised requests. **Risk:** CPU saturation, outages, scheduling failure if requests exceed node resources; source warns of experimental maturity (pp675–678). **Verification:** `top` CPU 451–489m; `describe vpa` RecommendationProvided; `get -w` Terminating/ContainerCreating; `describe pod` new 587m. **Rollback:** switch VPA updateMode back to `Off` is an inference not explicitly tested as rollback; full safe restore [Needs confirmation].

## HPA Todo and synthetic load (pp685–690)

```bash
minikube addons enable metrics-server
kubectl apply -f hpa/hpa-demo-ns.yaml
kubectl apply -f hpa/todo-deployment.yaml
kubectl get po -n hpa-demo
kubectl apply -f hpa/todo-service.yaml
kubectl get svc -n hpa-demo
kubectl port-forward svc/todo-app -n hpa-demo 8081:8081
kubectl apply -f hpa/todo-hpa.yaml
kubectl get hpa -n hpa-demo
hey -z 4m -c 25 http://localhost:8081
watch 'kubectl get po -n hpa-demo; kubectl top pods -n hpa-demo'
kubectl describe deployments.apps todo-app -n hpa-demo
kubectl delete namespaces hpa-demo
```

**Classification:** `addons/apply/port-forward/hey/delete` state-affecting (port-forward local network connection, hey workload-generating, namespace delete destructive); `get/top/describe/watch` read-only. **Effect:** one Pod Todo app, internal Service `8081→3000`, HPA min1/max5 target 80% CPU, 25 concurrent clients for 4 minutes; sample shows **3 replicas**. **Risk:** mutable/quay images, high CPU, local TCP exposure, ingress/load, metering, and source Todo YAML mismatch; namespace deletion removes *all* contents. **Verification:** HPA metrics, Pod top/describe scale event; **Rollback:** only source `kubectl delete namespaces hpa-demo`, destructive and no app-data restore.

Source HPA manifest (p689):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-hpa
  namespace: hpa-demo
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: todo-app}
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 80}
```

**CRITICAL source defect p686:** prose says Todo runs image `quay.io/iamgini/one-page-web:1.0`, but YAML sets `quay.io/ginigangadharan/todo-app:2.0`. `resources.requests/limits` in excerpt appears indented beneath `ports[0]`/misaligned. Do not silently fix or claim that exact YAML was independently validated. p688 manual scale example refers to `one-page-web`, not actual `todo-app` (see findings). Alternative in-cluster load source command (p688):
```bash
kubectl run -n hpa-demo -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://todo-app; done"
```
**CLASS:** workload-generating, potentially continuous traffic until interrupted; not verified. Source `--rm` requests cleanup, but no completed output shown. Web access `http://localhost:8081` only during port-forward.

## Cluster Autoscaler — cloud resource mutations (pp693–695)

```bash
gcloud container clusters create k8sbible --enable-autoscaling --num-nodes 3 --min-nodes 2 --max-nodes 10 --region=us-central1-a
gcloud container clusters update k8sforbeginners --enable-autoscaling --min-nodes=2 --max-nodes=10 --zone=us-central1-a --node-pool=nodepool1
gcloud container node-pools describe default-pool --cluster=k8sdemo
az aks create --resource-group k8sforbeginners-rg --name k8sforbeginners-aks --node-count 1 --enable-cluster-autoscaler --min-count 1 --max-count 10 --vm-set-type VirtualMachineScaleSets --load-balancer-sku standard --generate-ssh-keys
az aks update --resource-group k8sforbeginners-rg --name k8sforbeginners-aks --enable-cluster-autoscaler --min-count 2 --max-count 10
```

**Class:** all `create/update` cloud resource state-changing/billable (GKE/AKS and managed node pools); `describe` read-only. **Risks:** GKE create uses `--region=us-central1-a` yet result says `zones/us-central1-a`; text calls a zone a region (p693). The `update` targets k8sforbeginners/nodepool1 while `describe` targets k8sdemo/default-pool (p694), **not verification of same cluster**. IAM/quota and active prices unverified. **Verification:** `kubectl get nodes`, GKE node-pool/AKS status. **Rollback:** no GKE/AKS delete or scale-disable commands in this chapter; source p700 merely asks to clean cluster/disable CA, [Needs confirmation].

For EKS, chapter p694 gives documentation link only: no verified `eksctl`/IAM deployment commands for CA; **[Not applicable]** as runnable source.

## Coupled HPA + CA (pp696–700)

Source states `elastic-hamster` Deployment under `ca-demo`, `image: quay.io/iamgini/elastic-hamster:1.0`, requests `cpu: 500m`, `memory: 50Mi`, env `TOTAL_HAMSTER_USAGE=1.0`; a script reads replica count via Kubernetes API. Files `ca/ca-demo-ns.yaml`, `ca/deployment-reader-role.yaml`, `ca/elastic-hamster-serviceaccount.yaml`, `ca/read-deployments-rolebinding.yaml`, `ca/elastic-hamster-deployment.yaml`, `ca/elastic-hamster-hpa.yaml`.

**SOURCE BLOCKERS — DO NOT DEPLOY UNREVIEWED:**
- p697 SA `elastic-hamster` is in `ca-demo`, RoleBinding subject namespace **`default`**, though intended Pod runs in `ca-demo`; effective RBAC not proven.
- p698 HPA **`apiVersion: autoscaling/v1`** with `spec.metrics`/v2-style Resource target; actual schema acceptance [Needs confirmation].
- p699 `kubectl top pod -n ca-demo` shows names of `gke-...` **nodes**, CPU%, MEMORY%, rather than described Pod list; cannot confirm node count from that exact command.

```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,CPU_ALLOCATABLE:.status.allocatable.cpu,MEMORY_ALLOCATABLE:.status.allocatable.memory
kubectl apply -f ca/
kubectl get po -n ca-demo
kubectl top pod -n ca-demo
kubectl patch hpa elastic-hamster-hpa -n ca-demo -p '{"spec":{"maxReplicas":2}}'
kubectl get pod -n ca-demo
kubectl get nodes
```

**Classification:** `get/top` read-only; `apply ca/` deploys Namespace, Role/RoleBinding/SA, CPU-consuming Deployment and HPA (workload/authorization state-changing); `patch` modifies HPA to shrink max 25 to 2, leading to workload removal and potential node scale-down. **Effect per source narrative:** scale-out GKE cluster from 2 toward **10** nodes under insufficient CPU; after patch, scale-in to **2**; **actual manifest validity not verified**. **Risk:** cloud spending, RBAC failures, high load, eviction, permanent data loss on incorrect node drain. **Verification:** source screenshots/output and `get nodes` after waiting; no independent reliability/price measure. **Rollback:** no source-complete IAM, GKE cluster, Namespace or controller teardown [Needs confirmation].

## KEDA and Karpenter

pp701–703 concept only: **no source installation, ScaledObject, NodePool, authorization or metric query commands**. Installation/production claims [Not applicable] to chapter command collection.

**Source constraints:** p676/version footnote conflicts with alpha warning; p680 Auto mode historical deprecation; input YAML/image mismatch; and CA demo cannot be asserted runnable. No live runtime/billing tests completed.
