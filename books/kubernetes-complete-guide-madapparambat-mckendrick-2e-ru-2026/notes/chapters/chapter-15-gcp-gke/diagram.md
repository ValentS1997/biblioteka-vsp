# Схемы главы 15 — GCP / GKE

**Source:** only chapter RAG PDF pp515–536; Mermaid reflects text, not original screenshot reconstruction.

## GKE lifecycle and local context

```mermaid
flowchart TD
  A["GCP account + billing enabled"]
  B["Choose Project ID"]
  C["gcloud init / set project"]
  D["Enable container.googleapis.com"]
  E["Install gke-gcloud-auth-plugin"]
  F["Create GKE cluster in us-central1-a"]
  G["kubeconfig / get-credentials"]
  H["kubectl current-context / get nodes"]
  I["Deploy Guestbook"]
  J["Remove frontend Service and cluster"]
  K["Audit console for orphaned billable resources"]
  A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K
```

Evidence p0515, p0518–p0527, p0533. Billing, permissions and missing backups prevent this being a production procedure. `gcloud` project and `kubectl` context are distinct targets; verify both.

## Guestbook components

```mermaid
flowchart TD
  U["External browser: HTTP port 80"]
  LB["frontend Service: external LoadBalancer"]
  F["PHP frontend Deployment"]
  L["redis-leader Service: ClusterIP"]
  LD["Redis Leader Deployment"]
  R["redis-follower Service: ClusterIP"]
  RD["Redis Follower Deployment"]
  U --> LB --> F
  F --> L --> LD
  F --> R --> RD
```

Evidence p0527–p0531. The text demonstrates three deployments/services but contains no reviewed full manifest YAML. Public IP and node port are environment-dependent; backend data durability, secret handling and SSL not demonstrated.

## Zonal versus regional nodes

```mermaid
flowchart TD
  X["GKE create with --num-nodes=2"]
  CH{"Location scope?"}
  Z["--zone=us-central1-a"]
  Z2["2 total nodes in 1 zone"]
  REG["--region=us-central1"]
  REG3["3 zones by book's default"]
  REG6["2 nodes x 3 zones = 6"]
  FOUR["--node-locations a,b,c,f"]
  EIGHT["2 nodes x 4 zones = 8"]
  X --> CH
  CH --> Z --> Z2
  CH --> REG --> REG3 --> REG6
  REG --> FOUR --> EIGHT
```

Evidence p0533–p0536. Counts are from *the chapter's examples*, not a guaranteed current GKE default. Regional cluster not equivalent to proven app HA/SLO.

## Cost and cleanup guardrails

```mermaid
flowchart TD
  A["Plan experiment"]
  B{"Project, IAM, region, cost approved?"}
  STOP["Stop: Needs confirmation"]
  C["Create monitored lab"]
  D["Workloads + external LoadBalancer"]
  E["Delete frontend Service"]
  F["Delete cluster using correct zone or region"]
  G["Inspect GCP console for remaining resources"]
  A --> B
  B -->|"No"| STOP
  B -->|"Yes"| C --> D --> E --> F --> G
```

Evidence p0515, p0530–p0535. Resource deletion can destroy state and is not a substitute for a validated recovery plan.
