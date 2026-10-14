# Глава 17. Запуск кластера на платформе Microsoft Azure с помощью Azure Kubernetes Service

**Inventory:** `0033` · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Edition:** второе, русское (2026)  
**Template:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source policy:** `rag_only`.

## Provenance and readiness

- **Chapter boundary VERIFIED:** PDF/печатные страницы **561–586** включительно; заголовок p0561, «Резюме» p0585–p0586, «Дополнительные источники информации» p0586, глава 18 начинается p0587. TOC `p0018:c01`.
- **RAG source locator:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0561:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0586:c01`, **26 page-addressable PDF chunks** in `rag/chunks/p0501-p0600/p####-c01.md`. Format: PDF; EPUB spine: Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index generation `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Book readiness:** previously passed GitHub Actions run `38394894818`. Latest acceptance and template v1.7 checked at `main` before work; this is not a claim to have rerun the readiness script.
- **Evidence restriction:** no direct PDF access, external URL validation, model-memory corrections, Azure account access or live Kubernetes execution. Unsupported claims **[Needs confirmation]**.

## Chapter map

| Section | PDF | Subject |
|---|---:|---|
| Azure, AKS and prerequisites | 561–564 | History Windows Azure, ACS→AKS, Container Apps; Azure account and billing |
| Azure CLI installation | 565–567 | brew on macOS; Linux script; MSI/Chocolatey on Windows |
| Login and Cloud Shell | 567–569 | `az login`, device code, `az account show`, Cloud Shell storage for persistent kubeconfig |
| AKS creation and credentials | 569–572 | Resource group `eastus`, 2 worker nodes, monitoring addon, `--generate-sshkeys`, `az aks get-credentials` |
| Guestbook on AKS | 572–573 | Reuse 6 remote YAML manifests for Redis Leader, Redis Follower and frontend; public IP with HTTP |
| Azure Portal | 573–582 | Namespaces, Workloads, logs, Events, Services, storage, Run command, node pools, Insights/Log Analytics, backups |
| Delete and historical costs | 582–583 | `az aks delete` **then** `az group delete` in disposable lab; VM sizes and estimated monthly costs |
| Compare GKE/EKS/AKS | 583–585 | Table 17.1, provider tradeoffs, author's preference AKS→GKE→EKS |
| Summary and references | 585–586 | Source chapter-end resume, transition to Kubernetes security |

## Principal source-grounded conclusions

**AKS lifecycle.** Source `az group create --name rg-myfirstakscluster-eus --location eastus -o table` creates a Resource Group (p0569). `az aks create --resource-group rg-myfirstakscluster-eus --name aksmyfirstakscluster-eus --node-count 2 --enable-addons monitoring --generate-sshkeys -o yaml` creates a 2-worker AKS cluster and enables Azure monitoring in the lab (p0570). `az aks get-credentials` changes local kubeconfig and `kubectl get nodes` verifies nodes (p0571).

**Guestbook portability.** The same six Kubernetes YAML URLs as chapters 15–16 create three Deployment/Service pairs for Redis Leader, Redis Follower and PHP frontend (p0572). The frontend's public IP is opened using **HTTP**, explicitly without configured TLS (p0573). Source manifests are referenced by the mutable GitHub branch `main`, with no complete YAML embedded in this chapter; current trust, content and availability **[Needs confirmation]**.

**Observability is configured, not proof of full DR.** Azure Portal exposes workloads, Live logs, Events, Services, Run command, node pools, Backup and Insights. In the sample, `--enable-addons monitoring` sends metrics/logs to Azure Log Analytics for Insights (pp0575–0582). The chapter describes backup features but does **not** perform or verify a workload restore.

**Cleanup and cost.** `az aks delete --resource-group rg-myfirstakscluster-eus --name aksmyfirstakscluster-eus` removes the AKS cluster, but does **not** delete its resource group; `az group delete --name rg-myfirstakscluster-eus` deletes the **whole** group (p0582) and is not a safe generic cleanup instruction for a shared group. Costs (~$213, ~$286, ~$140/month; historical profiles p0583) are not current price quotes.

**Provider comparison.** Table 17.1 (p0584) evaluates versions/upgrades, usability, integrations, scaling, security, cost, multizone/private/serverless capabilities. The end-of-chapter order **AKS → GKE → EKS** is the **authors' subjective assessment at the book's historical point in time**, not an independently verified 2026 ranking (p0585).

## Artifacts

- [cheatsheet.md](cheatsheet.md) — baseline, read-only, interpretation, action, verification and rollback.
- [commands.md](commands.md) — source-backed Azure/Kubernetes commands, classifications, risk/effect/verification/rollback.
- [diagram.md](diagram.md) — resource group/cluster, guestbook, monitoring and cleanup Mermaid diagrams.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [summary.md](summary.md) — RAG-grounded chapter closing «Резюме», pp0585–p0586.
- [source-findings.md](source-findings.md) — source mismatches and unresolved boundaries.

**Review questions/answers:** [Not applicable]; no standalone review/control questions or exercises in chapter RAG pp561–586.

## Evidence anchors

- [Requirements and billable warning p0561](../../../rag/chunks/p0501-p0600/p0561-c01.md)
- [AKS and Azure Container Apps p0563](../../../rag/chunks/p0501-p0600/p0563-c01.md)
- [Historical Azure free account p0564](../../../rag/chunks/p0501-p0600/p0564-c01.md)
- [Linux installer p0566](../../../rag/chunks/p0501-p0600/p0566-c01.md)
- [Login / device code / Cloud Shell p0567](../../../rag/chunks/p0501-p0600/p0567-c01.md)
- [AKS resource group p0569](../../../rag/chunks/p0501-p0600/p0569-c01.md)
- [AKS creation and SSH p0570](../../../rag/chunks/p0501-p0600/p0570-c01.md)
- [Credentials / node check p0571](../../../rag/chunks/p0501-p0600/p0571-c01.md)
- [Guestbook remote YAML p0572](../../../rag/chunks/p0501-p0600/p0572-c01.md)
- [Public HTTP and portal naming p0573](../../../rag/chunks/p0501-p0600/p0573-c01.md)
- [Workloads/Namespaces p0574](../../../rag/chunks/p0501-p0600/p0574-c01.md)
- [Live logs p0576](../../../rag/chunks/p0501-p0600/p0576-c01.md)
- [Run command p0578](../../../rag/chunks/p0501-p0600/p0578-c01.md)
- [Control plane/version and KEDA p0580](../../../rag/chunks/p0501-p0600/p0580-c01.md)
- [Insights p0581](../../../rag/chunks/p0501-p0600/p0581-c01.md)
- [Delete group and cluster p0582](../../../rag/chunks/p0501-p0600/p0582-c01.md)
- [Costs and VM options p0583](../../../rag/chunks/p0501-p0600/p0583-c01.md)
- [Three-cloud table p0584](../../../rag/chunks/p0501-p0600/p0584-c01.md)
- [Authors' conclusion p0585](../../../rag/chunks/p0501-p0600/p0585-c01.md)

## Safety and non-interference

No Azure subscription/resource or cluster was accessed or changed; source `curl | bash` and `kubectl apply -f` remote manifests **were not executed**. Azure resource group deletion is destructive; CLI login/device credentials, Cloud Shell storage, SSH generation, public load balancer and Log Analytics charges require approval. **Unchanged:** PDF/LFS, RAG, registry, book metadata, reading status/progress/dates.
