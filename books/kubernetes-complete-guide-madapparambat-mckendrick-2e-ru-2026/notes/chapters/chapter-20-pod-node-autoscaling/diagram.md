# Диаграммы главы 20 — VPA, HPA, CA и event-driven scaling

**Provenance:** RAG-only pp668–704. Mermaid depicts book concepts and demo observations, not original PDF screenshots.

## Resource requests and Pending

```mermaid
flowchart TD
  BASE["Pod resources: requests vs limits"]
  REQUESTS["requests drive scheduler reservation"]
  LIMITS["limits bound CPU or memory behavior"]
  DEMO["nginx requests CPU 2000m"]
  PENDING["No fitting node, Pending / FailedScheduling"]
  BASE --> REQUESTS --> DEMO --> PENDING
  BASE --> LIMITS
```

p670–673. Event also lists leftover `machine-check-exception:memory` taint; CPU shortage is not sole scheduler reason in example.

## VPA recommendation and Pod replacement

```mermaid
flowchart TD
  LOAD["hamster 5 Pod; 100m requested, about 500m used"]
  METRICS["Metrics Server / observed CPU"]
  REC["VPA Recommender target 587m"]
  OFF["updateMode Off: recommendations only"]
  AUTO["updateMode Auto in source"]
  UPD["VPA Updater evicts older Pods"]
  ADM["Admission adjusts requests on newly created Pods"]
  LOAD --> METRICS --> REC --> OFF
  OFF --> AUTO --> UPD --> ADM
```

pp674–682. Source says in-place resizing experimental, with v1.35 stable footnote. Do not treat this specific legacy Auto flow as current API contract.

## HPA load-test loop

```mermaid
flowchart TD
  D["todo-app Deployment: 1 replica, CPU request"]
  SERV["ClusterIP port 8081 -> Pod 3000"]
  PF["kubectl port-forward"]
  HEY["hey 4 minutes, concurrency 25"]
  HPA["HPA autoscaling/v2, goal 80 CPU, min1 max5"]
  THREE["Book sees 3 replicas"]
  D --> SERV --> PF --> HEY --> HPA --> THREE
```

pp685–690. Actual Todo YAML contains conflicting image and indentation; diagram expresses intended model, not proof its source manifest is valid.

## Horizontal Pod scaling drives Node scaling

```mermaid
flowchart TD
  HPA["HPA creates more elastic-hamster replicas"]
  NEED["New Pods request 500m CPU each"]
  PENDING["Insufficient allocatable node capacity -> Pending"]
  CA["Cluster Autoscaler scales GKE up"]
  MAX["Source maximum 10 nodes"]
  PATCH["Patch HPA maxReplicas from 25 to 2"]
  DELAY["Scale-down delay / consolidate"]
  TWO["Source returns to 2 nodes"]
  HPA --> NEED --> PENDING --> CA --> MAX --> PATCH --> DELAY --> TWO
```

pp691–700. CA RBAC/SA and HPA API versions are inconsistent in source; treat as conceptual flow until manifests are corrected via explicit external verification.

## KEDA and Karpenter

```mermaid
flowchart TD
  EVENT["External events / queues / app metrics"]
  KEDA["KEDA event-driven Pod replicas; HPA integration"]
  CAPACITY["Unschedulable Pod / capacity demand"]
  KARPENTER["Karpenter node provisioning and capacity optimization"]
  EVENT --> KEDA
  CAPACITY --> KARPENTER
```

pp701–703. No installation, ScaledObject YAML, Karpenter NodePool or live testing in chapter.

## Operational check

```mermaid
flowchart TD
  A["Baseline: context, requests, limits, metrics"]
  B{"Workload Pending, high CPU, or underutilized?"}
  OBS["Inspect Pod Events, VPA target, HPA replicas, nodes"]
  GUARD["Approve permissions, disruption risk and spending limits"]
  CHANGE["Controlled changes: VPA/HPA/CA"]
  VERIFY["Remeasure Pod readiness, node count, cost"]
  STOP["Stop without a safe change"]
  A --> B --> OBS --> GUARD
  GUARD -->|"No"| STOP
  GUARD -->|"Yes"| CHANGE --> VERIFY
```

As a safety interpretation of source pp673, 678, 692, 700, rather than an executed runbook.
