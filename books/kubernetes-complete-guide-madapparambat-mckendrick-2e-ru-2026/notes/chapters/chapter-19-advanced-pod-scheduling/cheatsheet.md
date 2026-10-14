# Cheatsheet — Глава 19: Продвинутые методы планирования Pod

**Provenance:** RAG-only PDF pp641–667, chunks `p0641:c01`–`p0667:c01`. No commands executed; versions and expected output are **historical book examples**, not live observations.

## Symptom / problem framing

Pod застрял в `Pending`, Deployment не завершает rollout либо Pod размещается на неподходящем узле. Требуется диагностировать решения scheduler с учётом labels, `nodeSelector`, жёсткой/мягкой `nodeAffinity`, taints/tolerations, а также отличать Pod, который обрабатывает kube-scheduler, от статического Pod (pp642–644, 651, 657–663).

## Baseline / context

- Многоузловой кластер Kubernetes и `kubectl`, желательно отдельный lab (p641). Источник создаёт `minikube` на 3 узла (один control plane + 2 worker) с VirtualBox, Calico, containerd, Kubernetes v1.30.0 (p644). Версии в позднейших выводах отличаются [Needs confirmation].
- `kube-scheduler` filter → score → bind; kubelet на выбранном узле запускает Pod, уже работающие Pod сами не переносятся при изменении affinity/label (pp642–644).
- **Прямое nodeName** = привязка к одному конкретному узлу, без scheduler; **nodeSelector** = обязательное совпадение labels; **required nodeAffinity** = обязательный критерий; **preferred affinity** = взвешенное пожелание (pp645–655).
- **Taint** принадлежит узлу: `NoSchedule` запрещает новые Pod без допуска, `PreferNoSchedule` мягкое ограничение, `NoExecute` вытесняет запущенные Pod при отсутствии/истечении допуска (pp656–662). **Toleration** разрешает размещение/пребывание, но сам по себе **не притягивает** Pod к узлу.
- Реальные имена/роли узлов, labels, taints, cluster policy, права и доступность управляющего слоя **[Needs confirmation]**. В AKS/EKS доступ к kube-scheduler config в книге ограничен (p642).

## Read-only checks

```bash
kubectl get nodes
kubectl describe nodes minikube
kubectl get nodes --show-labels | grep superfast
kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
kubectl describe pod <имя_pod>
```

p644–649, 650–651, 655–662, p648 (describe event). **Read-only:** API queries of node state, labels, Pod phase, selected node and scheduling events. Source `describe pod` appears for absent `Scheduled` event under nodeName, not as an actual transcript. Source `kubectl logs` for kube-scheduler mentioned p647 but access/log-path and namespace not provided. **Do not invent runnable scheduler log command**.

## Interpretation

| Book symptom | Cause shown in source | Evidence |
|---|---|---|
| Five nginx replicas distributed among minikube, m02, m03 | standard scheduler filter and score without placement constraints | 646 |
| Five replicas all on m02 | source added `template.spec.nodeName: minikube-m02`, bypassing scheduler | 647–648 |
| Five replicas only on m02/m03 | custom `node-type=superfast` labels and `nodeSelector` | 649–650 |
| Three Pending Pods plus four Running old Pods | `nodeSelector.node-type=slow` does not match any node; rolling update stalls | 650–651 |
| Preferred fast/superfast; required NotIn extremelyslow | two favored nodes; fallback to slow if needed | 652–656 |
| Five Pending after NoExecute taint of sole eligible node | hard affinity excludes m02/m03, NoExecute prevents viable placement on minikube | 660 |
| Pod repeatedly uses minikube then is evicted | matching NoExecute toleration with `tolerationSeconds=60`; no separate NoSchedule | 661 |
| Replicas relocate to m02/m03 | add NoSchedule to minikube while not tolerating that effect | 661–662 |

**Deployment rollout detail:** p651 shows 3 new Pending + 4 old Running and calls this a 7-Pod intermediate result; defaults `maxSurge=25%` (ceil to 2 for 5) and `maxUnavailable=25%` (floor to 1) discussed. This is a **specific rolling-update snapshot**, not proof rollout succeeds. Source suggests rollback to previous Deployment version, matching selector, additional node or label, but **does not give exact safe rollback command**.

**IgnoredDuringExecution** means node label/affinity changes do **not** evict current Pods. `kubectl rollout restart` explicitly creates a new allocation and is disruptive if capacity/readiness lacking (pp653–656). No universal zero-downtime guarantee established.

**Static Pod:** kubelet watches local file/URL rather than scheduler; API contains mirror Pods only; cannot be managed through mirror API and cannot reference Secret/ConfigMap (p663). Source describes but **does not create** one.

## Next action

Before modifying a shared cluster: confirm intended context and namespace, inspect all candidate nodes/labels/taints, scheduling events and resource pressure. Determine whether constraint is **hard** vs **soft**, whether Pod is new or already running, and whether pending replicas are from rollout. For NoExecute, establish required eviction tolerance and workload disruption budget. Verify capacity of candidate nodes; do not taint/remove labels from production nodes as a blind test.

## Modifying action (source lab only; NOT EXECUTED)

```bash
minikube start --driver=virtualbox --nodes 3 --cni calico --cpus=2 --memory=2g --kubernetes-version=v1.30.0 --container-runtime=containerd
kubectl apply -f 01_nodename/nginx-deployment.yaml
kubectl label nodes minikube-m02 node-type=superfast
kubectl label nodes minikube-m03 node-type=superfast
kubectl apply -f 02_nodeselector/nginx-deployment-slow.yaml
kubectl label nodes --overwrite minikube node-type=slow
kubectl label nodes --overwrite minikube-m02 node-type=fast
kubectl label nodes --overwrite minikube-m03 node-type=superfast
kubectl apply -f 03_affinity/nginx-deployment.yaml
kubectl rollout restart deployment nginx-app
```

pp644–656. **Effect:** local cluster resources, Deployment, new ReplicaSets/Pods and node labels are changed; `restart` replaces Pods. **Risk:** wrong cluster, workload downtime, resource pressure, label targeting other workloads, historical image tag `nginx:1.17`. **Verification:** node lists, Pod-to-node mapping. **Rollback:** source recommends previous revision or re-labeling, but does not provide complete tested cleanup/rollback [Needs confirmation]. Some source files are fragmentary in chapter RAG, not guaranteed runnable.

Taint experiment:
```bash
kubectl taint node minikube machine-check-exception=memory:NoExecute
kubectl apply -f 04_taints/nginx-deployment.yaml
kubectl taint node minikube machine-check-exception=memory:NoSchedule
```

pp660–662. **Effect:** may evict Pod and block replacement until toleration/affinity permits; `NoExecute` with 60 sec toleration allows temporary residence, the additional NoSchedule prevents re-admission in the book. **Verification:** first Pending, then one scheduled on tainted minikube, then all five on m02/m03. **Rollback:** p658 shows effect-qualified `kubectl taint node minikube machine-check-exception=memory:NoExecute-`; p662's claimed *remove both* command is malformed in RAG and not safe to copy; complete validated 2-taint cleanup **[Needs confirmation]**.

## Verification / acceptance checks

- `kubectl get nodes` reflects expected three nodes, labels consistent with selector; Pod table shows chosen NODE and Pending state.
- `nodeName` all five on m02; matching `nodeSelector` on m02/m03; missing selector demonstrates stalled rollout; affinity demonstrates 2 favored nodes then slow fallback.
- `NoExecute` eviction seen in source, after `NoSchedule` no Pod left on minikube, without NoSchedule temporary placement causes churn (p661).
- No source proof of performance SLO, resource admission beyond sample, real descheduler operation, static Pod deployment or scheduler profile config.

## Rollback

For source-supported reversal, p658 provides taint removal for a **single effect**; p651 suggests restoring previous Deployment revision but no exact command, and p662 intended cleanup both effects includes corrupted command. **[Needs confirmation]** before any node taint cleanup. `kubectl rollout restart` is not an undo. Label restoration depends on previous values not captured by source. Explicitly validate deployment owners, Pod availability and taints before any destructive change.
