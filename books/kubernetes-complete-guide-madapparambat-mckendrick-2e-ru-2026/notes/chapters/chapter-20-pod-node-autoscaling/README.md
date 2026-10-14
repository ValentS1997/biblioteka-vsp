# Глава 20. Автоматическое масштабирование подов и узлов в Kubernetes

**Inventory:** `0033` · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source policy:** `rag_only`.

## Scope / provenance / readiness

- **Chapter boundary VERIFIED:** PDF/печатные страницы **668–704** включительно; заголовок `p0668:c01`, «Резюме» `p0703:c01`–`p0704:c01`, дополнительные источники `p0704:c01`; глава 21 начинается на p0705 (TOC p0020:c01).
- **Addressable chunks:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0668:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0704:c01`, 37 страниц RAG: `rag/chunks/p0601-p0700/p0668-c01.md` … `p0700-c01.md`, затем `rag/chunks/p0701-p0800/p0701-c01.md` … `p0704-c01.md`. EPUB spine: Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **Full-book RAG:** `ACCEPTED`, `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** previously PASS, GitHub Actions run `38394894818`. Book acceptance/template verified on main before chapter work; no newly executed readiness command claimed.
- **Evidence mode:** only chapter RAG. No direct PDF, external documentation verification, model-memory correction, actual GCP/Azure/EKS access or live Kubernetes execution. Unsupported: **[Needs confirmation]**.

## Chapter map

| Section | PDF pages | Content |
|---|---:|---|
| Autoscaling dimensions and prerequisites | 668–669 | VPA: resources; HPA: replicas; CA: nodes; GKE cluster and kubectl |
| Resource requests and limits | 669–673 | CPU vs memory, millicores, Mi, 5-replica nginx, Pending from 2000m |
| VPA and setup | 674–678 | Recommender/Updater/Admission, GKE, VPA install script, metrics-server |
| VPA workload experiment | 678–683 | hamster 5 Pods, requests 100m, CPU ~500m, Off recommendation 587m, Auto recreates |
| HPA workload experiment | 683–690 | Todo Deployment, ClusterIP + port-forward, HPA target CPU 80%, hey load, 1→3 replicas |
| CA fundamentals and platforms | 691–696 | Cluster Autoscaler, request-driven nodes, GKE, EKS reference, AKS, delays |
| HPA + CA coupled demo | 696–700 | elastic-hamster RBAC, HPA up to 25 Pods, GKE nodes up to 10 and down to 2 |
| KEDA and Karpenter | 701–703 | Event-driven Pod scaling and node provisioning; conceptual only |
| Summary and references | 703–704 | Source chapter-end «Резюме» and documentation |

## Main model

**Vertical Pod Autoscaler (VPA)** корректирует requests контейнеров с учётом метрик, может оставаться в режиме `Off` для рекомендаций или применять изменения с пересозданием Pod в показанном `Auto` (pp674–683). В Source демонстрации hamster 5 реплик запрашивают 100m CPU, измеренная нагрузка 450–489m, VPA target 587m, после смены режима происходит Terminating/ContainerCreating. Исторические замечания о стабильности InPlacePodVerticalScaling/Auto надо трактовать с учётом противоречивых сносок, не распространять на актуальные кластеры.

**Horizontal Pod Autoscaler (HPA)** меняет число реплик в зависимости от метрик. Источник использует `autoscaling/v2` для `todo-hpa`, минимум 1/максимум 5, цель 80% CPU (pp685–690). Для процентной CPU-метрики требуется `resources.requests.cpu`; `hey -z 4m -c 25` в книге увеличивает число Pod до 3. **Исходный Todo Deployment YAML содержит неверно/неоднозначно вложенный `resources` и противоречивые имена образов** — см. findings; сам манифест нельзя считать проверенной рабочей копией.

**Cluster Autoscaler (CA)** управляет числом узлов, когда HPA увеличивает число Pod, а планировщик не находит свободных ресурсов (pp691–700). В GKE-сценарии установлен диапазон 2–10 узлов; HPA `elastic-hamster` желает до 25 реплик по 500m CPU, CA достигает 10 узлов, затем при `maxReplicas=2` исходный вывод показывает возвращение к 2 узлам. **Стоимость и разрушительность:** создание облачного кластера, изменение Node Pool, HPA, IAM/RBAC, удаление узлов и ресурсов могут влиять на реальные сервисы и счета; это не сертифицированный production-runbook.

**KEDA / Karpenter** описаны только концептуально; упражнений по их установке или runtime-acceptance в главе нет (pp701–703).

## Artifact collection

- [cheatsheet.md](cheatsheet.md): problem, baseline, read-only checks, interpretation, next action, modifying actions, verification and rollback.
- [commands.md](commands.md): RAG-sourced commands and YAML fragments, risk/effect/check/rollback classification.
- [diagram.md](diagram.md): VPA/HPA/CA flows, requests and coupled scaling, Mermaid.
- [visual-cheatsheet.svg](visual-cheatsheet.svg): compact graphic.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg): detailed graphic.
- [summary.md](summary.md): source-grounded paraphrase of closing «Резюме», pp703–704.
- [source-findings.md](source-findings.md): evidence-indexed mismatches and unsupported claims.

**Review Q&A:** [Not applicable] — отдельного заключительного раздела вопросов/упражнений нет. Встроенные практические упражнения охвачены commands/cheatsheet.

## Evidence anchors

- [Three scaling dimensions p0668](../../../rag/chunks/p0601-p0700/p0668-c01.md)
- [Prerequisites p0669](../../../rag/chunks/p0601-p0700/p0669-c01.md)
- [Requests/limits p0670](../../../rag/chunks/p0601-p0700/p0670-c01.md)
- [Resource YAML p0671](../../../rag/chunks/p0601-p0700/p0671-c01.md)
- [Scheduling Pending p0673](../../../rag/chunks/p0601-p0700/p0673-c01.md)
- [VPA components p0675](../../../rag/chunks/p0601-p0700/p0675-c01.md)
- [In-place/GKE p0676](../../../rag/chunks/p0601-p0700/p0676-c01.md)
- [VPA installation p0677](../../../rag/chunks/p0601-p0700/p0677-c01.md)
- [Hamster load p0679](../../../rag/chunks/p0601-p0700/p0679-c01.md)
- [VPA Off p0680](../../../rag/chunks/p0601-p0700/p0680-c01.md)
- [VPA target p0681](../../../rag/chunks/p0601-p0700/p0681-c01.md)
- [VPA recreate p0682](../../../rag/chunks/p0601-p0700/p0682-c01.md)
- [HPA prerequisites p0685](../../../rag/chunks/p0601-p0700/p0685-c01.md)
- [Todo YAML p0686](../../../rag/chunks/p0601-p0700/p0686-c01.md)
- [Service and forwarding p0687](../../../rag/chunks/p0601-p0700/p0687-c01.md)
- [HPA workload p0689](../../../rag/chunks/p0601-p0700/p0689-c01.md)
- [Scale result p0690](../../../rag/chunks/p0601-p0700/p0690-c01.md)
- [CA conditions p0691](../../../rag/chunks/p0601-p0700/p0691-c01.md)
- [CA GKE configuration p0693](../../../rag/chunks/p0601-p0700/p0693-c01.md)
- [AKS command p0695](../../../rag/chunks/p0601-p0700/p0695-c01.md)
- [CA example RBAC p0697](../../../rag/chunks/p0601-p0700/p0697-c01.md)
- [CA example HPA p0698](../../../rag/chunks/p0601-p0700/p0698-c01.md)
- [Mismatch: kubectl top and node counts p0699](../../../rag/chunks/p0601-p0700/p0699-c01.md)
- [CA scale-down p0700](../../../rag/chunks/p0601-p0700/p0700-c01.md)
- [KEDA p0701](../../../rag/chunks/p0701-p0800/p0701-c01.md)
- [Karpenter / summary p0703](../../../rag/chunks/p0701-p0800/p0703-c01.md)
- [Summary p0704](../../../rag/chunks/p0701-p0800/p0704-c01.md)

## Boundary

No package installation, `kubectl`/`minikube`, `gcloud`, `az`, workload generation, autoscaler deployment or resource deletion performed. Do not reuse sample scripts or inconsistent manifests without a specific review and environment check. Canonical PDF/LFS, RAG, registry/metadata and reading status/dates/progress unchanged.
