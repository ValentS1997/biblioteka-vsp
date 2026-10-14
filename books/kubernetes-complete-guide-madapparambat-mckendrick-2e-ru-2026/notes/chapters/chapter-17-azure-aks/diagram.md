# Диаграммы главы 17 — Microsoft Azure / AKS

**Source:** RAG-only PDF pp561–586, `p0561:c01`–`p0586:c01`. Mermaid reconstructs the chapter text, not direct PDF screenshots. The referenced Azure account/cluster has not been accessed.

## Resource hierarchy / lifecycle

```mermaid
flowchart TD
  AZ["Azure subscription + billing"]
  RG["Resource Group rg-myfirstakscluster-eus, eastus"]
  AKS["AKS aksmyfirstakscluster-eus, 2 nodes"]
  MON["Monitoring addon → Log Analytics / Insights"]
  CFG["az aks get-credentials → kubeconfig"]
  CL["kubectl get nodes; apply Guestbook"]
  AZ --> RG --> AKS
  AKS --> MON
  AKS --> CFG --> CL
```

RAG p0567–p0571 and p0581. `az group delete` removes the whole resource group; `az aks delete` removes the cluster but not the group. Source p0573 uses a different portal cluster spelling: `aks-myfirstakscluster-eus` [Needs confirmation].

## Guestbook traffic

```mermaid
flowchart TD
  U["Internet browser: HTTP, no SSL in book"]
  LB["Azure LoadBalancer / frontend public IP"]
  FRONT["PHP frontend Deployment / Service"]
  LEAD["Redis Leader Service + Deployment"]
  FOL["Redis Follower Service + Deployment"]
  U --> LB --> FRONT
  FRONT --> LEAD
  FRONT --> FOL
```

Source pp572–573. Only the six remote URL manifests are listed, not their complete content; no TLS/security or data persistence verified.

## Azure Portal observation and management

```mermaid
flowchart TD
  AZ["AKS cluster portal"]
  WORK["Kubernetes resources: Namespaces, Workloads, Services"]
  EVENTS["YAML / Events / Live logs"]
  RUN["Run command: can mutate cluster"]
  NODES["Node pools and cluster configuration"]
  INS["Monitoring addon → Azure Log Analytics → Insights"]
  AZ --> WORK --> EVENTS
  AZ --> RUN
  AZ --> NODES
  AZ --> INS
```

Source pp573–582. Viewing is observation; clicking a modification control or invoking Run command can change resource state. Backup is discussed, but a restore is not demonstrated.

## Controlled cleanup

```mermaid
flowchart TD
  START["Identify subscription, resource group, cluster"]
  CHECK{"Owned disposable RG and backup confirmed?"}
  STOP["Stop: Needs confirmation"]
  DELAKS["az aks delete --resource-group ... --name ..."]
  DELRG{"Delete entire resource group authorized?"}
  GROUP["az group delete --name ..."]
  AUDIT["Review residual resources and costs"]
  START --> CHECK
  CHECK -->|"No"| STOP
  CHECK -->|"Yes"| DELAKS --> DELRG
  DELRG -->|"No"| AUDIT
  DELRG -->|"Yes"| GROUP --> AUDIT
```

Source p0582. Data recovery and verified zero remaining billable assets are [Needs confirmation].

## Cross-cloud conclusion in source

```mermaid
flowchart TD
  GKE["GKE: chapter 15"]
  EKS["EKS: chapter 16"]
  AKS["AKS: chapter 17"]
  YAML["Same Guestbook Kubernetes manifests"]
  AUTHORS["Authors prefer AKS, then GKE, then EKS"]
  GKE --> YAML
  EKS --> YAML
  AKS --> YAML
  YAML --> AUTHORS
```

p0583–p0585. The authors' preference reflects their historical experience, not an objective or verified current ranking. Full workload portability (storage/IAM/network/security) was not established.
