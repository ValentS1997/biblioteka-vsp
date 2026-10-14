# Глава 21. Продвинутые возможности Kubernetes

**Книга:** №0033 · `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · второе русское издание (2026).  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source mode:** `rag_only`.

## Scope and evidence

- **Boundary VERIFIED:** глава начинается PDF/печатной страницей **705** (`p0705:c01`) и завершается **749** (`p0749:c01`); итоговое «Резюме» **747–748**, дополнительные источники 748–749. p0751–p0752 — рекламные материалы следующих книг, **не содержание главы**; p0750 в RAG не найден. Всего **45** page-addressable locators 705–749 (каждый `p####:c01`), папка `rag/chunks/p0701-p0800/`.
- **Canonical source:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`. EPUB spine Not applicable.
- **Book RAG:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index generation `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** previously PASS in GitHub Actions `38394894818`. Acceptance and template v1.7 verified from main; no claim of re-running readiness locally.
- **Source discipline:** facts and commands **only from chapter RAG**; do not read canonical PDF, external sites or model-memory corrections. Unknown or disputed: **[Needs confirmation]**. None of the book examples was executed against Kubernetes, cloud or etcd.

## Chapter map

| Topic | PDF | Key material |
|---|---:|---|
| Prerequisites, Service types, Ingress | 705–710 | L4 vs L7, path/host rules, Ingress needs controller |
| ingress-nginx / minikube | 710–716 | Controller deployment, 3 application Services, `k8sbible.local` and /video, /shopping, / |
| Multiple IngressClass and Azure AGIC | 716–720 | Default class, App Gateway direct routing, AKS example with **contradictory resource names** |
| Gateway API, EndpointSlice | 720–724 | GatewayClass/Gateway/HTTPRoute, endpoints at 100 per slice (source default) |
| Ecosystem technologies | 724–727 | Knative, OpenFaaS, Kubeflow, KubeVirt, concepts only |
| Day-2: etcd backup and restore | 727–730 | `etcdctl snapshot save`, `etcdutl snapshot status/restore`, IaC/CaC/GitOps |
| Upgrade and multi-cluster | 730–734 | Backups, `drain`/control plane/workers/`uncordon`, Rancher, ArgoCD/Fleet, Lens, cloud services |
| Security baseline | 734–739 | API, kubelet, least privilege, network, encryption-at-rest, audit |
| Troubleshooting and debugging | 739–747 | get/describe/events/logs/explain/exec/cp/debug, ephemeral containers, Pending/CrashLoop/PVC/Ingress issues |
| Chapter-end resume + references | 747–749 | Final synthesis and external reading URLs (URLs not accessed) |

## Central analysis

**Ingress as routing rules, not a controller.** An Ingress with `networking.k8s.io/v1` maps HTTP host `k8sbible.local` and paths `/video`, `/shopping`, `/` to three ClusterIP Services; a separately deployed controller actually enforces the paths (pp708–715). Minikube example starts 3 nodes, enables ingress addon, deploys `ingress/`, shows `portal-ingress` and asks to map minikube IP to name in `/etc/hosts`. Source intentionally exposes **HTTP without TLS** (p715). There is a source discrepancy: YAML p708 sets `host`, but prose p709 says `host` is not used. Nginx Ingress Controller (F5) and community ingress-nginx deployment URL are discussed together (pp710–711), without unambiguous equivalence.

**AGIC on AKS.** Application Gateway can connect to private Pod IP addresses, reducing some proxy layers (pp717–720). **Critical:** p719 prose specifies `k8sforbeginners-rg/k8sforbeginners-aks-agic`, the `az aks create` sample uses `myResourceGroup/myAKSCluster`, while `az aks get-credentials` returns to the prose names; expected App Gateway name also differs (`MyAppGateway` vs `AksApplicationGateway`). Never claim this exact CLI sequence is executable as a single cluster.

**Gateway API ≠ ready replacement deployment.** Source includes `GatewayClass` controllerName `example.net/gateway-controller`, `Gateway` and `HTTPRoute` (pp720–722), but **does not deploy a matching gateway controller**. Source path `gateway-api/gateway_api/gateway.yaml` differs in nesting from surrounding `gateway-api/` examples. EndpointSlice supports smaller collections of endpoint addresses (pp723–724), not a source-tested performance benchmark.

**Day-2 operation and operational risks.** `etcdctl` snapshot, `etcdutl` inspect/restore, staged upgrades and GitOps-style IaC/CaC are core practices. **Critical:** p728 saves `/tmp/snapshot-pre-patch.db`, while `etcdutl snapshot status snapshot.db` (p728) and `etcdutl ... snapshot restore snapshot.db` (p729) refer to another name; no rename/move in source. Do not run a production restore by copying unverified paths. Restore may require coordinated API-server shutdown and recovery; snapshot may contain secrets (pp727–729). `kubectl drain` can evict workloads, upgrades can break API compatibility (pp730–732). No restore rehearsal, backup encryption or verified rollback occurs.

**Troubleshooting loop.** `kubectl get/describe` → Events/logs → `explain` → optional `exec`/`cp`/`debug` for targeted inspection (pp739–746). `kubectl debug` injects ephemeral container into an existing Pod and is **state-changing**, despite prose claiming no configuration change (pp744–745). Source `exec ... -- env` shows possible environment credentials; don't persist them in notes. Namespace is missing from first p742 `exec` example even though Pod is in `trouble-ns` (p742).

## Artifacts

- [cheatsheet.md](cheatsheet.md) — symptom, baseline, read-only, interpretation, next action, modification, verification and rollback.
- [commands.md](commands.md) — chapter-sourced CLI and YAML excerpts with side effects and verification.
- [diagram.md](diagram.md) — Mermaid traffic flows, Gateway API, etcd backup/restore, troubleshooting.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual synthesis.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual synthesis.
- [summary.md](summary.md) — source-grounded paraphrase of chapter-end «Резюме», pp747–748.
- [source-findings.md](source-findings.md) — source contradictions, extraction defects and unverified operations.

**Review questions/answers:** [Not applicable]. There is no standalone source review/control-question section at chapter end; built-in examples are included in the operational artifacts.

## Selected RAG anchors

- [Chapter opening p0705](../../../rag/chunks/p0701-p0800/p0705-c01.md)
- [Ingress YAML p0708](../../../rag/chunks/p0701-p0800/p0708-c01.md)
- [host contradiction p0709](../../../rag/chunks/p0701-p0800/p0709-c01.md)
- [controller p0710](../../../rag/chunks/p0701-p0800/p0710-c01.md)
- [minikube addon p0712](../../../rag/chunks/p0701-p0800/p0712-c01.md)
- [portal rules p0713](../../../rag/chunks/p0701-p0800/p0713-c01.md)
- [apply and DNS p0714](../../../rag/chunks/p0701-p0800/p0714-c01.md)
- [HTTP/TLS warning p0715](../../../rag/chunks/p0701-p0800/p0715-c01.md)
- [IngressClass p0717](../../../rag/chunks/p0701-p0800/p0717-c01.md)
- [AGIC resource-name mismatch p0719](../../../rag/chunks/p0701-p0800/p0719-c01.md)
- [AGIC output p0720](../../../rag/chunks/p0701-p0800/p0720-c01.md)
- [GatewayClass p0721](../../../rag/chunks/p0701-p0800/p0721-c01.md)
- [Gateway/HTTPRoute p0722](../../../rag/chunks/p0701-p0800/p0722-c01.md)
- [EndpointSlice p0724](../../../rag/chunks/p0701-p0800/p0724-c01.md)
- [Kubeflow/KubeVirt p0726](../../../rag/chunks/p0701-p0800/p0726-c01.md)
- [etcd backup p0728](../../../rag/chunks/p0701-p0800/p0728-c01.md)
- [etcd restore p0729](../../../rag/chunks/p0701-p0800/p0729-c01.md)
- [upgrades p0731](../../../rag/chunks/p0701-p0800/p0731-c01.md)
- [multi-cluster p0733](../../../rag/chunks/p0701-p0800/p0733-c01.md)
- [kubelet access p0735](../../../rag/chunks/p0701-p0800/p0735-c01.md)
- [audit config p0737](../../../rag/chunks/p0701-p0800/p0737-c01.md)
- [security table p0738](../../../rag/chunks/p0701-p0800/p0738-c01.md)
- [events/logs p0740](../../../rag/chunks/p0701-p0800/p0740-c01.md)
- [logs p0741](../../../rag/chunks/p0701-p0800/p0741-c01.md)
- [exec p0742](../../../rag/chunks/p0701-p0800/p0742-c01.md)
- [cp p0743](../../../rag/chunks/p0701-p0800/p0743-c01.md)
- [ephemeral debug p0744](../../../rag/chunks/p0701-p0800/p0744-c01.md)
- [failure matrix p0746](../../../rag/chunks/p0701-p0800/p0746-c01.md)
- [conclusion p0747](../../../rag/chunks/p0701-p0800/p0747-c01.md)
- [conclusion p0748](../../../rag/chunks/p0701-p0800/p0748-c01.md)

## Non-interference

No Ingress/AGIC/Gateway resource, cloud billing, kubeconfig, etcd secret/certificate, Pod, node, role, cluster upgrade or CLI executed. Canonical PDF/LFS, RAG, registry/book metadata and **reading status, dates and progress remain unchanged**.
