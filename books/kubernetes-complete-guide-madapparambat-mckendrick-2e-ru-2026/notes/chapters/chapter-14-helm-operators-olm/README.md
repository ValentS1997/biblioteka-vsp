# Глава 14. Работа с Helm-чартами и операторами

**Inventory:** 0033 · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **source_policy:** `rag_only`.

## Scope and provenance

- **Boundaries VERIFIED:** PDF/printed pages **474–514**, inclusively. Chapter title p0474, source section «Резюме» p0513–p0514, bibliography p0514, chapter 15 begins p0515; TOC pp16–17.
- **Chapter source:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0474:c01` – `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0514:c01`, **41 addressable PDF-page chunks**. RAG paths `rag/chunks/p0401-p0500/p0474-c01.md` through `p0500-c01.md`; `rag/chunks/p0501-p0600/p0501-c01.md` through `p0514-c01.md`. EPUB spine: Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index generation `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** previously passed book readiness CI `38394894818`; current acceptance/template v1.7 on `main` checked. No claim of executing readiness CLI now.
- **Evidence discipline:** chapter `rag_only`. No direct PDF, external URLs followed, or model-memory corrections. Unverified operating conditions **[Needs confirmation]**.

## Структура главы

| Тема | PDF | Предмет |
|---|---:|---|
| Зачем Helm, chart/repository/release | 474–477 | Управление пакетами, Go templates, values и dependencies, Helm 3 без Tiller |
| Установка клиента Helm | 477–479 | Fedora/DNF, Windows/Chocolatey, macOS/Homebrew, tarball |
| WordPress Helm chart | 479–487 | Artifact Hub, Bitnami repo, namespace, wp-values.yaml, NodePort, dry-run, WordPress/MariaDB, list/uninstall |
| Анатомия чарта | 487–489 | Chart.yaml, values.yaml, schema, templates/, charts/, crds/, NOTES.txt, зависимость MariaDB |
| Kubernetes Dashboard | 489–492 | Helm release, RBAC, ServiceAccount, token, local port-forward; elevated cluster-admin demonstration |
| Helm security | 493–495 | Trust source, dependency audit, RBAC, namespaced isolation and defaults |
| Operators / CRD / OLM | 495–501 | Reconciliation, custom resources, Operator SDK, OperatorHub, CatalogSource, CSV, Subscription |
| Операторы Prometheus и Grafana | 501–506 | OLM install, CSV success, Prometheus/Grafana custom resource manifests |
| Observability stack | 506–513 | Node Exporter DaemonSet, Service/ServiceMonitor, port-forward, Grafana Prometheus datasource/dashboard |
| Резюме и дополнительные источники | 513–514 | Итог и переход к GKE |

## Основные выводы

**Helm** группирует параметризованные Kubernetes-манифесты в *chart*, предоставляет хранилища *repository*, а установленный экземпляр именует *release*; values переопределяют шаблоны. В книге демонстрируется Bitnami WordPress с MariaDB (p0475–p0489) и Helm-установка Dashboard (p0489–p0492).

**Оператор Kubernetes** реализует application-specific controller, циклически сравнивающий желаемое состояние пользовательского ресурса с фактическим и вносящий изменения (p0495–p0499). **CRD** расширяет API типом пользовательского ресурса, **OLM** управляет установкой и обновлениями операторов через каталоги, Subscription и ClusterServiceVersion (p0500–p0504). Пример Prometheus/Grafana создаёт CR и управляемые операторами ресурсы, затем через ServiceMonitor подключает Node Exporter (p0505–p0513).

**Нельзя считать команды безопасным production runbook:** исходный пример Dashboard выдаёт `cluster-admin` через ClusterRoleBinding (p0490–p0493), values WordPress и Grafana manifest включают пароль открытым текстом (p0482, p0506), установка OLM выполняет удалённый `curl | bash` (p0502), а OperatorHub subscriptions применяются прямо с удалённых URL (p0503–p0504). Эти шаги не выполнялись. Для актуальной среды нужны supply-chain/RBAC/credentials проверки и согласованный rollback.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — problem, baseline, read-only, intervention, verification, rollback.
- [commands.md](commands.md) — source-grounded commands, snippets, side effects and warnings.
- [diagram.md](diagram.md) — Mermaid: Helm chart lifecycle, operator control loop, OLM, monitoring.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — краткая визуальная памятка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная памятка.
- [summary.md](summary.md) — исходный раздел «Резюме» pp513–514.
- [source-findings.md](source-findings.md) — расхождения/ограничения chapter source.

**Review questions/answers:** [Not applicable]; выделенного блока контрольных вопросов/упражнений на pp474–514 нет.

## Evidence

- [Helm concepts p0476](../../../rag/chunks/p0401-p0500/p0476-c01.md)
- [Helm 3 without Tiller p0477](../../../rag/chunks/p0401-p0500/p0477-c01.md)
- [Old stable repository caveat p0479](../../../rag/chunks/p0401-p0500/p0479-c01.md)
- [WordPress values/password p0482](../../../rag/chunks/p0401-p0500/p0482-c01.md)
- [Helm install p0483](../../../rag/chunks/p0401-p0500/p0483-c01.md)
- [WordPress NodePort inconsistency p0484](../../../rag/chunks/p0401-p0500/p0484-c01.md)
- [Uninstall and PVC caveat p0487](../../../rag/chunks/p0401-p0500/p0487-c01.md)
- [Dependencies/Go templates p0488](../../../rag/chunks/p0401-p0500/p0488-c01.md)
- [Dashboard Helm repo p0489](../../../rag/chunks/p0401-p0500/p0489-c01.md)
- [Dashboard elevated RBAC p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md)
- [Chart security p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)
- [Operator reconciliation p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)
- [OLM/CSV p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md)
- [OLM install script p0502](../../../rag/chunks/p0501-p0600/p0502-c01.md)
- [Subscription p0503](../../../rag/chunks/p0501-p0600/p0503-c01.md)
- [Prometheus CR p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)
- [Grafana plaintext admin p0506](../../../rag/chunks/p0501-p0600/p0506-c01.md)
- [ServiceMonitor p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)
- [Port-forward p0508](../../../rag/chunks/p0501-p0600/p0508-c01.md)
- [Grafana datasource p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md)
- [Chapter summary p0513](../../../rag/chunks/p0501-p0600/p0513-c01.md)

## Execution boundary

All platform installation, Helm, `kubectl`, remote installer and secret/token commands are **unexecuted**; no access to a live cluster. CLI output, charts, image versions, hostnames and OperatorHub links are historical as provided by chapter, not current validations. Production rollout, current chart availability and rollback **[Needs confirmation]**. Canonical PDF/LFS, RAG, registry, book metadata and reading status/progress/dates are unchanged.
