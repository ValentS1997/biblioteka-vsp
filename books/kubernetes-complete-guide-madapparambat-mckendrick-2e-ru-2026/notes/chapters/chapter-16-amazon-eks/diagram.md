# Диаграммы главы 16 — Amazon EKS, CloudFormation и Guestbook

**Evidence:** RAG-only p0537:c01–p0560:c01, PDF pp537–560. Концептуальные схемы по тексту главы, не скриншоты оригинального PDF.

## Account → EKS

```mermaid
flowchart TD
  A["AWS account + billing"]
  I["IAM user ekscluster + programmatic key (high privilege in source)"]
  CLI["aws configure, default region"]
  EK["eksctl create cluster"]
  CF["AWS CloudFormation"]
  CONTROL["Managed EKS control plane stack"]
  GROUP["Managed nodegroup stack"]
  EC2["2 m5.large EC2 workers"]
  KUB["kubeconfig updated; kubectl get nodes"]
  A --> I --> CLI --> EK --> CF
  CF --> CONTROL
  CF --> GROUP --> EC2
  CONTROL --> KUB
  EC2 --> KUB
```

Source pp540–549. p547 describes region `us-west-1` while terminal shows `us-west-2`; all creation is billable. Login with `AdministratorAccess` is **not** a least-privilege example.

## EKS and cloud endpoints

```mermaid
flowchart TD
  BROWSER["Browser / user"]
  ELB["AWS ELB: external DNS hostname"]
  FRONT["Guestbook PHP frontend Service and Deployment"]
  LEAD["Redis leader ClusterIP Service and Deployment"]
  FOLLOW["Redis follower ClusterIP Service and Deployment"]
  BROWSER --> ELB --> FRONT
  FRONT --> LEAD
  FRONT --> FOLLOW
```

Source pp549–551, 555. The six YAML files are remote `raw.githubusercontent.com/.../main` resources and are not fully included in the chapter; no TLS or data-backup workflow is demonstrated.

## AWS Console authorization

```mermaid
flowchart TD
  CLI["AWS CLI principal ekscluster"]
  EKS["EKS cluster created by eksctl"]
  OTHER["Other AWS Console principal"]
  DENIED["EKS resource view: Access denied"]
  IAM["Source suggests enabling Console access for ekscluster"]
  VIEW["EKS Resources / Compute / Access and CloudFormation"]
  CLI --> EKS
  OTHER --> DENIED
  DENIED --> IAM --> VIEW
```

Source pp552–556. Enabling console access creates **more credentials**; it is not a validated safe fix for a real production IAM/RBAC problem. Access levels of a real environment **[Needs confirmation]**.

## Cleanup and residual cost

```mermaid
flowchart TD
  A["Confirm actual cluster name, AWS account, region"]
  B{"Backup / delete authority confirmed?"}
  STOP["STOP: Needs confirmation"]
  DELETE["eksctl delete cluster --name ..."]
  LB["Attempt cleanup of AWS load balancers"]
  GROUP["Delete nodegroup CloudFormation stack"]
  CONTROL["Delete EKS control-plane stack"]
  AUDIT["Inspect EC2, EKS, CloudFormation, ELB"]
  BILLS["Check residual billable assets"]
  A --> B
  B -->|"No"| STOP
  B -->|"Yes"| DELETE
  DELETE --> LB --> GROUP --> CONTROL --> AUDIT --> BILLS
```

Source pp557–559. Deletion is destructive. The chapter's success log and recommendation to audit orphan resources do not amount to a guaranteed zero-cost teardown, and no disaster restore plan is presented.

## Data-flow and operational assumptions

The source's sample cluster API endpoint is publicly accessible and CloudWatch cluster logging is off (p548). Both facts are **sample output**, not asserted current settings of a target cluster. CloudFormation IaC constructs the cluster but does not guarantee application health, monitoring, authentication hardening or safe rollback.
