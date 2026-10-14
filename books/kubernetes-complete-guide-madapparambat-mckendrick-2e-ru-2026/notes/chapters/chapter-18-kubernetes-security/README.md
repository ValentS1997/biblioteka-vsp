# Глава 18. Безопасность в системе Kubernetes

**Inventory:** `0033` · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Edition:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source mode:** `rag_only`.

## Source provenance and prerequisites

- **Chapter boundary VERIFIED:** PDF/печатные страницы **587–640** включительно; заголовок `p0587:c01`, заключительное «Резюме» `p0639:c01`–`p0640:c01`; глава 19 начинается на p0641 (RAG TOC `p0019:c01`).
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0587:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0640:c01`, 54 source-page chunks, по одному `-c01` на страницу. Каталоги `rag/chunks/p0501-p0600` (587–600) и `rag/chunks/p0601-p0700` (601–640). EPUB spine: Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **Full-book RAG:** `ACCEPTED`, `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Book readiness:** ранее PASS, GitHub run `38394894818`; шаблон v1.7 и RAG acceptance повторно прочитаны на `main`. Не заявляется выполнение CLI readiness заново.
- **Policy:** только RAG главы; **не** открывать напрямую PDF, внешнюю документацию, приложенные по URL Chapter18 YAML, не устранять пробелы знанием модели. Если сведения не подтверждены — **[Needs confirmation]**.

## Карта главы

| Раздел | PDF pages | Evidence |
|---|---:|---|
| Обзор безопасности, prerequisites | 587–589 | Identity/authorization, admission, Pod and runtime isolation |
| Этапы доступа к API | 589–593 | Authentication → authorization → admission → audit; 401 vs 403; ServiceAccount and ordinary users |
| Статические токены и ServiceAccount | 593–601 | Non-production token-auth-file, JWT TokenRequest, `example-ns`/SA + Role + Binding |
| X.509, OIDC и другие способы | 602–611 | Client CA, CSR approval, kubeconfig, OIDC Discovery/IdP, proxy/webhook, bootstrap token |
| Механизмы RBAC | 611–619 | Role/ClusterRole, RoleBinding/ClusterRoleBinding, default-deny, pod-logger `403 → PodList → 403` |
| Admission controllers | 619–623 | Mutating then validating; `--enable-admission-plugins`, source version caveats |
| securityContext | 623–628 | runAsUser/group, capabilities, privileged, read-only rootfs; `id`/`touch` |
| NetworkPolicy | 628–634 | CNI Calico, two namespaces, ingress default deny, attempted cross-namespace allow |
| TLS/mTLS, runtimes | 634–638 | etcd and service links; gVisor, Kata and RuntimeClass |
| Registry Secret / final summary | 638–640 | `docker-registry`, `imagePullSecrets`, chapter closing |

## Main idea and operational boundary

Kubernetes security is **layered**. Authentication establishes identity; authorization (typically RBAC) decides requested operations; admission controllers can mutate or reject write requests; audit records operations (p0589–p0592). Practical RBAC in p0614–p0619 makes a Pod's ServiceAccount unable to list Pods (HTTP 403), then explicitly permits `get/watch/list` for Pods in one namespace via RoleBinding and removes the permission. This demonstrates *least privilege*, not administrator escalation.

The `securityContext` example runs as UID/GID 1000 with read-only root filesystem and writable `emptyDir` at a specific path (p0627–p0628). NetworkPolicy example demonstrates no rule → success, default-deny ingress → blocked, and an additional allow rule → success, with **major source semantics discrepancy**: two separate items under `ingress[].from` (one `namespaceSelector`, one `podSelector`) are interpreted in the prose as a conjunction for precisely Pod `nginx1` from namespace `web1`. The actual YAML presents two independent entries; this cannot be treated as evidence of that exact restrictive conjunction (p0633–p0634). The policy resource name in the output also differs from YAML. **Do not deploy this source YAML as an approved isolation rule.**

Other important limitations: `--token-auth-file` is explicitly discouraged (pp593–595); kubeconfig token and CSR key handling are sensitive (pp598–605); `CAP_NET_ADMIN` and `privileged: true` are deliberately unsafe examples (p0625); modifying `kube-apiserver.yaml`/admission plugins can restart control plane (p0622); private registry passwords placed in `--docker-password` can leak, and p0638 overstates automatic encryption-at-rest guarantees. RuntimeClass `kata-containers` is a source example; no runtime installation/availability demonstrated. Actual CNI, privileges, policies, TLS, Secret encryption and production rollback **[Needs confirmation]**.

## Artifact collection

- [cheatsheet.md](cheatsheet.md) — symptom, baseline, read-only, interpretation, next action, modifying action, verification and rollback.
- [commands.md](commands.md) — RAG-supported commands/manifests; classify risks, effects and verification.
- [diagram.md](diagram.md) — request security pipeline, RBAC, admission, network policies, container and runtime isolation.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact SVG memory aid.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed SVG memory aid.
- [summary.md](summary.md) — chapter-end source-grounded summary pp639–640.
- [source-findings.md](source-findings.md) — documented source contradictions, command/text mismatches and uncertain claims.

**Review questions/answers:** [Not applicable] — отдельного заключительного блока контрольных вопросов и упражнений pp587–640 нет; практические пошаговые упражнения входят в commands/cheatsheet.

## Key source anchors

- [Chapter intro and prerequisites p0587](../../../rag/chunks/p0501-p0600/p0587-c01.md)
- [Authentication sequence p0590](../../../rag/chunks/p0501-p0600/p0590-c01.md)
- [Ordinary users and SA p0592](../../../rag/chunks/p0501-p0600/p0592-c01.md)
- [Static token file p0593](../../../rag/chunks/p0501-p0600/p0593-c01.md)
- [Role/RoleBinding p0598](../../../rag/chunks/p0501-p0600/p0598-c01.md)
- [401/403 p0612](../../../rag/chunks/p0601-p0700/p0612-c01.md)
- [CSR creation p0604](../../../rag/chunks/p0601-p0700/p0604-c01.md)
- [CSR approval and kubeconfig p0605](../../../rag/chunks/p0601-p0700/p0605-c01.md)
- [OIDC options p0610](../../../rag/chunks/p0601-p0700/p0610-c01.md)
- [RBAC pod example p0616](../../../rag/chunks/p0601-p0700/p0616-c01.md)
- [Admission configuration p0622](../../../rag/chunks/p0601-p0700/p0622-c01.md)
- [SecurityContext p0627](../../../rag/chunks/p0601-p0700/p0627-c01.md)
- [NetworkPolicy CNI prerequisite p0629](../../../rag/chunks/p0601-p0700/p0629-c01.md)
- [NetworkPolicy source mismatch p0633](../../../rag/chunks/p0601-p0700/p0633-c01.md)
- [TLS and mTLS p0635](../../../rag/chunks/p0601-p0700/p0635-c01.md)
- [gVisor/Kata p0636](../../../rag/chunks/p0601-p0700/p0636-c01.md)
- [Registry secrets p0638](../../../rag/chunks/p0601-p0700/p0638-c01.md)
- [Original chapter resume p0639](../../../rag/chunks/p0601-p0700/p0639-c01.md)
- [Conclusion p0640](../../../rag/chunks/p0601-p0700/p0640-c01.md)

## Non-interference

No Kubernetes command, shell, cluster, CA signing, TokenRequest, manifest, privilege escalation, CNI or API-server change was executed. PDF/LFS, RAG/index, registry/metadata, and reading status, dates or progress **not modified**.
