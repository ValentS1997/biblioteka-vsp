# Cheatsheet — Глава 20: автоматическое масштабирование Pod и Node

**RAG-only:** PDF 668–704, `p0668:c01`–`p0704:c01`. Команды/облака не запускались. Исходные версии, реальная IAM-конфигурация и цена [Needs confirmation].

## Symptom / problem framing

Рабочая нагрузка испытывает недостаток CPU/памяти, число реплик не соответствует нагрузке, либо дополнительные Pod остаются Pending при отсутствии ёмкости узлов. В книге три плоскости автомасштабирования: **VPA изменяет requests**, **HPA изменяет replicas**, **CA добавляет/удаляет nodes** (pp668–669). Решение требует правильных `requests`/`limits`, метрик и контроля расходов.

## Baseline / context

- Кластер Kubernetes, желательно многоузловой; `kubectl`, для VPA/CA демонстраций GKE; источник предлагает отдельные `vpa-demo`, `hpa-demo`, `ca-demo` namespaces (p669, 678, 685, 697).
- `resources.requests` участвует в решении scheduler; CPU обычно ограничивается throttling, превышение memory limit может приводить к OOM/рестарту (pp670–671). Sample nginx requests CPU `100m`/memory `50Mi`, limits `200m`/`60Mi`; изменение CPU request на `2000m` вызывает Pending при недостатке capacity (pp671–673).
- VPA — отдельный CRD/controller, в sample компоненты `vpa-recommender`, `vpa-updater`, `vpa-admission-controller`; требуется server of metrics (pp674–678). Source distinguishes `Off`, `Initial`, `Recreate`, `Auto`, with footnote describing later deprecation of Auto (p680), version and current meaning [Needs confirmation].
- HPA встроен в Kubernetes, но CPU-based utilization требует Metrics Server и заданного CPU request; `todo-hpa` `autoscaling/v2`, target 80%, min1/max5 (pp685–690). Source Todo Deployment **невалидирован как YAML**; его блок `resources` имеет спорные отступы, а текст и YAML называют разные container images (p686).
- CA требует cloud node allocation/IAM and node pool bounds (GKE/AKS source) and acts on Pods Pending for lack of capacity; node count 2–10 (pp691–700). Real accounts, clusters, limits and billing **[Needs confirmation]**.
- KEDA/Karpenter source gives only conceptual orientation without lab operations (pp701–703).

## Read-only checks

```bash
kubectl describe node minikube-m03
kubectl get pod
kubectl describe pod nginx-deployment-example-69bd6d55b4-n2mzq
kubectl get pods -n kube-system | grep vpa
kubectl get po -n vpa-demo
kubectl top pod -n vpa-demo
kubectl describe vpa hamster-vpa -n vpa-demo
kubectl get hpa -n hpa-demo
kubectl get svc -n hpa-demo
kubectl describe deployments.apps todo-app -n hpa-demo
kubectl get po -n ca-demo
kubectl get nodes
```

**Evidence:** pp672–673, 677, 679, 681, 687, 689–690, 699–700. Read-only API and CLI requests but observations may reveal system details; `watch 'kubectl get po -n hpa-demo; kubectl top pods -n hpa-demo'` p690 runs these repeatedly, without changing resources. The command `kubectl top pod -n ca-demo` in p699 displays **node names and CPU% columns**; do not mistake this for a verified Pod metrics output.

## Interpretation

| Observation in source | Diagnosis | Evidence |
|---|---|---|
| CPU request 2000m leads new nginx Pending | insufficient node allocatable CPU **and** one node still tainted `machine-check-exception:memory` in scheduler events | 672–673 |
| Hamster requests 100m, CPU top 451–489m | VPA identifies underprovisioned requested CPU | 678–681 |
| VPA Off target CPU 587m, memory 262144k | recommendation present but no Pod mutation yet | 680–681 |
| Change VPA to Auto, Pod Terminating / ContainerCreating | updater/admission recreates Pods with updated requests | 682 |
| HPA initially `cpu:<unknown>/80%`, replicas 0 in quick output | metrics/initial reconciliation not ready; no steady-state proof | 689 |
| `hey -z 4m -c 25`, later 3 Todo Pods | HPA scaled source Deployment from 1 to 3 | 689–690 |
| `elastic-hamster` HPA asks for many CPU-requesting Pods and many remain Pending | CA scales nodes to configured cap 10; remaining Pending possible | 698–699 |
| Patch HPA maxReplicas 2 | pods become 2; after delay GKE nodes shown as 2 | 700 |

**Source gaps affecting reproducibility:** Todo image name mismatch and YAML indentation (p686); CA RoleBinding SA namespace `default` despite SA in `ca-demo` (p697); CA sample `autoscaling/v1` but HPA manifest includes `metrics` v2 shape (p698); `kubectl top pod` with node rows and percentages (p699). These examples cannot be endorsed as successfully replayable without review.

## Next action

Verify actual kube context, resource budget, Metrics Server, valid Deployment manifests, readiness, Pod events, cluster limits, provider identity/quota, autoscaler controllers and rolling/eviction policies. Start with **recommendation-only VPA Off** on disposable test application; isolate HPA load test from public services and isolate CA experiment in a pre-approved account with cost ceilings. Do not treat a sampled result as a production SLO, SLA or current cloud price.

## Modifying action — source-only examples, NOT EXECUTED

```bash
kubectl apply -f resource-limit/nginx-deployment.yaml
minikube addons enable metrics-server
kubectl apply -f vpa/vpa-demo-ns.yaml
kubectl apply -f vpa/hamster-deployment.yaml
kubectl apply -f vpa/hamster-vpa.yaml
kubectl apply -f hpa/hpa-demo-ns.yaml
kubectl apply -f hpa/todo-deployment.yaml
kubectl apply -f hpa/todo-service.yaml
kubectl apply -f hpa/todo-hpa.yaml
kubectl port-forward svc/todo-app -n hpa-demo 8081:8081
hey -z 4m -c 25 http://localhost:8081
```

pp672, 677–682, 685–690. **Effect:** deployment/namespace workloads, VPA CRD-related controls, service, horizontal replicas and local traffic generation; metrics add-on mutates cluster. **Risk:** CPU saturation, VPA Pod replacement/unavailability, HPA instability, resources and billing; unverified source YAML; local port-forward temporary accessibility. **Verification:** `get/describe/top` outputs above. **Rollback:** book explicitly shows `kubectl delete namespaces hpa-demo` (p690) for HPA; VPA and Metrics Server cleanup not specified, [Needs confirmation].

```bash
gcloud container clusters create k8sbible --enable-autoscaling --num-nodes 3 --min-nodes 2 --max-nodes 10 --region=us-central1-a
gcloud container clusters update k8sforbeginners --enable-autoscaling --min-nodes=2 --max-nodes=10 --zone=us-central1-a --node-pool=nodepool1
az aks create --resource-group k8sforbeginners-rg --name k8sforbeginners-aks --node-count 1 --enable-cluster-autoscaler --min-count 1 --max-count 10 --vm-set-type VirtualMachineScaleSets --load-balancer-sku standard --generate-ssh-keys
az aks update --resource-group k8sforbeginners-rg --name k8sforbeginners-aks --enable-cluster-autoscaler --min-count 2 --max-count 10
kubectl apply -f ca/
kubectl patch hpa elastic-hamster-hpa -n ca-demo -p '{"spec":{"maxReplicas":2}}'
```

pp693–695, 698–700. **Cloud state-changing, billable and potentially destructive**; create/update distinct source clusters/node pools and modify autoscalers/workloads. The GKE source uses `--region=us-central1-a` while API response and text reveal a **zone**; don't run without adjudication of location flag. **Verification:** actual `gcloud container node-pools describe ...`, `kubectl get nodes`, `get po`; current quotas/cloud outputs [Needs confirmation]. **Rollback:** p700 says clean cluster/disable CA, not exact safe commands; patch HPA max2 is a change of policy, not full undo. No verified cloud teardown commands in chapter, [Needs confirmation].

## Verification / acceptance checks

Expected book evidence: requests 100m vs measured hamster 450–489m; recommendation VPA target 587m; Auto replacement and new requests; HPA Todo 1→3 under hey; CA 2→10→2 nodes around HPA changes. A **successful runtime verification is not claimed**: source contains incompatible manifests and inconsistent observations; specific timing, prices, Kubernetes versions and cloud account state unknown.

## Rollback

- Source-supported deletion: `kubectl delete namespaces hpa-demo` (p690) deletes HPA study resources **and all other resources in that namespace**; destructive, verify ownership.
- Source `kubectl patch hpa ... maxReplicas=2` (p700) reduces Pod count and enables CA to scale down, not reverse complete experiment.
- VPA CRD/controller uninstall, source mTLS/runtime, `vpa-demo`/ `ca-demo` cleanup, GKE/AKS cloud node-pool teardown, data restore, cloud billing audit **[Needs confirmation]**. No deletion command invented.
