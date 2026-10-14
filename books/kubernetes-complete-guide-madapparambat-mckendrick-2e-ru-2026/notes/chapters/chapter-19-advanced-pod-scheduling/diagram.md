# Диаграммы главы 19 — планирование Pod

**RAG:** pp641–667, `p0641:c01`–`p0667:c01`. Схемы синтезированы по исходному тексту, а не реконструированы с рисунков PDF.

## Scheduler filter → score → node binding

```mermaid
flowchart TD
  API["kube-apiserver: Pod without spec.nodeName"]
  FILTER["kube-scheduler filter: viable nodes"]
  NONE["No suitable nodes → Pending"]
  SCORE["Score viable nodes by preferences"]
  BIND["Bind Pod to chosen nodeName"]
  KUBELET["kubelet on selected node starts containers"]
  API --> FILTER
  FILTER -->|"None"| NONE
  FILTER -->|"One or more"| SCORE --> BIND --> KUBELET
```

p642–p644. Source notes scheduling decision not continuously revisited after Pod is running. Direct `spec.nodeName` bypasses scheduler choice (pp645–648).

## Placement constraint hierarchy

```mermaid
flowchart TD
  P["Pod scheduling configuration"]
  DIRECT["nodeName: named node, bypass selection"]
  SELECTOR["nodeSelector: required label equality"]
  REQUIRED["nodeAffinity required: hard expression"]
  PREFERRED["nodeAffinity preferred: weighted soft expression"]
  TAINTS["Node taints + Pod tolerations"]
  P --> DIRECT
  P --> SELECTOR
  P --> REQUIRED
  P --> PREFERRED
  P --> TAINTS
```

pp645–659. Tolerations are permissions to tolerate, not a command to target a specific node. Soft preference still allows fallback.

## Matching vs rollout Pending

```mermaid
flowchart TD
  DEP["Deployment nginx-app, 5 replicas"]
  LABELS["Nodes m02 and m03 labelled superfast"]
  MATCH["nodeSelector superfast → Running on m02/m03"]
  SLOW["nodeSelector slow, no node has label"]
  ROLL["New Pods Pending; old Pods remain Running"]
  FIX["Source proposes selector change / more matching nodes / rollback"]
  DEP --> LABELS --> MATCH --> SLOW --> ROLL --> FIX
```

p649–651. Source p651 shows 3 Pending and 4 old Running in one rollout snapshot; do not generalize exact count to all Deployment configurations.

## Hard and soft affinity

```mermaid
flowchart TD
  A["nodeAffinity: required NotIn extremelyslow"]
  B["Preferred In fast or superfast, weight 1"]
  GOOD["Initially m02 fast and m03 superfast"]
  SWITCH["Relabel m02/m03 extremelyslow, m01 slow"]
  RESTART["rollout restart nginx-app"]
  FALLBACK["All 5 new Pods on m01 slow, if resource capacity"]
  A --> B --> GOOD --> SWITCH --> RESTART --> FALLBACK
```

p652–656. Already running Pods are not automatically migrated merely because labels changed.

## NoExecute and NoSchedule

```mermaid
flowchart TD
  T["Taint on m01: NoExecute memory"]
  PENDING["All 5 Pending while hard affinity excludes other nodes"]
  TOL["Change Deployment to tolerate NoExecute for 60 sec"]
  CHURN["Temporarily scheduled to m01; later evicted"]
  NS["Also add NoSchedule on m01, not tolerated"]
  OK["5 replicas on m02/m03"]
  T --> PENDING --> TOL --> CHURN --> NS --> OK
```

p660–662. Taints can evict running workloads; do not reproduce on non-disposable nodes. Source two-taint cleanup command p662 is malformed.

## Static Pod and scheduler configs

```mermaid
flowchart TD
  STATIC["Local file / configured remote URL"]
  KUBELET["kubelet manages static Pod"]
  MIRROR["API server mirror Pod for observation"]
  CONFIG["kube-scheduler config: profiles, plugin extension points"]
  NR["Node authorizer + NodeRestriction labels"]
  PERF["percentageOfNodesToScore balance"]
  STATIC --> KUBELET --> MIRROR
  CONFIG --> NR
  CONFIG --> PERF
```

p663–666. No static Pod runtime test, profile deployment or scheduler config verification is supplied. `v1alpha1/algorithmSource` fragment is not production-ready evidence.
