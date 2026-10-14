# Глава 16. Запуск кластера на платформе Amazon Web Services с помощью Amazon Elastic Kubernetes Service

**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source mode:** `rag_only`.

## Scope / provenance

- **Boundary VERIFIED:** PDF/печатные страницы **537–560**, заголовок `p0537:c01`; раздел «Резюме» `p0559:c01`; дополнительные источники `p0560:c01`; следующая глава 17 начинается со стр. 561 по TOC `p0018:c01`.
- **Addressable source:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0537:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0560:c01`, 24 page-addressable RAG chunks; paths `rag/chunks/p0501-p0600/p####-c01.md`. Format PDF, EPUB spine Not applicable.
- **Canonical source:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Book readiness:** prior GitHub Actions workflow `38394894818` PASS. RAG acceptance and canonical template checked on `main`; new direct readiness CLI run is **not** claimed.
- **Evidence restriction:** chapter `rag_only`; no direct PDF, external sources, cloud account access or model-memory corrections. Unknown facts **[Needs confirmation]**.

## Chapter map

| Section | PDF | Contents |
|---|---:|---|
| EKS, AWS and requirements | 537–540 | AWS history, EKS integration (IAM, Route 53, EBS, EC2 Auto Scaling, multi-AZ), billing warnings |
| Account and AWS CLI | 540–545 | Free Tier at writing time, AWS CLI macOS/Linux/Windows, IAM user, access key, `aws configure`, region |
| eksctl and CloudFormation | 545–546 | Install eksctl via brew/Chocolatey/tar archive, IaC stacks |
| Create Amazon EKS | 546–549 | `eksctl create cluster`, managed node group, public API endpoint, kubeconfig, 2 EC2 nodes |
| Guestbook application | 549–551 | Six remote YAML, Redis leader/follower, PHP frontend and AWS load balancer |
| AWS Console exploration | 551–557 | Region, IAM access issue, EKS, EC2, ELB, CloudFormation, tabs/metrics/permissions |
| Delete / costs | 557–559 | `eksctl delete cluster`, stacks/ELB, orphan resources check, historical cost |
| Conclusion / references | 559–560 | Summary, EKS documentation and pricing link |

## Main principle

**`eksctl` abstracts multi-step EKS creation with AWS CloudFormation**, provisioning a control-plane stack and a managed node-group stack. In the source, `eksctl create cluster` deploys **two m5.large EC2 worker nodes**, a VPC and managed EKS control plane (pp545–549). On completion it changes the local `kubeconfig`; `kubectl get nodes` reads the Kubernetes nodes.

**Critical conflict:** the prose on p0547 says region `us-west-1`, while the sample output on p0547–p0549 and console p0551 consistently use **`us-west-2`**. The source also selects `us-west-2` for `aws configure` (p0545). Do not silently select either region or assert deterministic default `eksctl` settings. Both variants are preserved in [source-findings.md](source-findings.md).

**Guestbook** repeats the same six `kubectl apply -f https://raw.githubusercontent.com/.../main/quickstarts/guestbook/...` commands as chapter 15, now against EKS (p0550). AWS assigns a **hostname/URL** for the frontend load balancer, in contrast with a directly displayed IP in the previous GKE example (p0550–p0551). The manifests themselves are absent from the chapter RAG and their current version/security are [Needs confirmation].

**Security and cost:** for the educational account, the author creates IAM user `ekscluster`, attaches **`AdministratorAccess`**, issues an **access key stored in CSV**, and later enables Console access (pp543–544, 552–553). This is **not a production least-privilege configuration**. The cluster output shows `publicAccess=true`, `privateAccess=false` and CloudWatch control-plane logging disabled (p0548). Deletion through `eksctl` can destroy workloads, and resources left behind may continue generating charges (pp557–558). The text's **$0.10/hour EKS and ~$213/month for 2 EC2 nodes + EKS** are historical estimates (pp558–559), not present-day rates.

## Artifacts

- [cheatsheet.md](cheatsheet.md) — problem, baseline, observation, interpretations, modifications, verification and rollback.
- [commands.md](commands.md) — chapter-supported CLI and six manifest references, classified by effects and risk.
- [diagram.md](diagram.md) — Mermaid EKS lifecycle, AWS resource tree, Guestbook and cleanup.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact SVG summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed SVG summary.
- [summary.md](summary.md) — source-grounded condensed chapter-end «Резюме», p0559.
- [source-findings.md](source-findings.md) — source contradictions and unverified operational claims.

**Review questions/answers:** [Not applicable]; chapter p0537–p0560 has no standalone review question or exercise section.

## Selected RAG evidence

- [AWS market and prerequisites p0537](../../../rag/chunks/p0501-p0600/p0537-c01.md)
- [EKS integrations p0539](../../../rag/chunks/p0501-p0600/p0539-c01.md)
- [Account and Free Tier p0540](../../../rag/chunks/p0501-p0600/p0540-c01.md)
- [AWS CLI packages p0541](../../../rag/chunks/p0501-p0600/p0541-c01.md)
- [Access keys and AdministratorAccess p0543](../../../rag/chunks/p0501-p0600/p0543-c01.md)
- [Credential CSV p0544](../../../rag/chunks/p0501-p0600/p0544-c01.md)
- [aws configure / region p0545](../../../rag/chunks/p0501-p0600/p0545-c01.md)
- [eksctl install p0546](../../../rag/chunks/p0501-p0600/p0546-c01.md)
- [Region mismatch p0547](../../../rag/chunks/p0501-p0600/p0547-c01.md)
- [Public endpoint and disabled logging p0548](../../../rag/chunks/p0501-p0600/p0548-c01.md)
- [EKS ready p0549](../../../rag/chunks/p0501-p0600/p0549-c01.md)
- [Guestbook YAML p0550](../../../rag/chunks/p0501-p0600/p0550-c01.md)
- [Console access p0553](../../../rag/chunks/p0501-p0600/p0553-c01.md)
- [AWS console views p0554](../../../rag/chunks/p0501-p0600/p0554-c01.md)
- [CloudFormation p0556](../../../rag/chunks/p0501-p0600/p0556-c01.md)
- [Delete command p0557](../../../rag/chunks/p0501-p0600/p0557-c01.md)
- [Orphan/cost checks p0558](../../../rag/chunks/p0501-p0600/p0558-c01.md)
- [Summary & cost p0559](../../../rag/chunks/p0501-p0600/p0559-c01.md)

## Safety / non-interference

**No** `aws`, `eksctl`, `kubectl`, installers, IAM or AWS Console changes were performed. Account/billing, region, CLI identity, RBAC, service public exposure, CloudFormation stacks and teardown **[Needs confirmation]**. No source PDF/LFS, RAG, registry, metadata or reading status/progress/dates changed.
