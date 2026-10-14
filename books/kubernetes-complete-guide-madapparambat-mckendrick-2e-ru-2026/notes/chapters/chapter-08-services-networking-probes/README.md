# Глава 8. Публикация подов с помощью сервисов

**Книга:** «Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.»  
**Inventory:** 0033 · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 08  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **source_policy:** `rag_only`.

## Provenance и границы

- **Глава VERIFIED:** PDF/печатные страницы **281–325** включительно; следующая глава 9 «Постоянное хранилище в Kubernetes» начинается на **326**. Evidence: оглавление RAG `p0012:c01`–`p0013:c01`, начало `p0281:c01`, «Резюме» `p0324:c01`–`p0325:c01`, следующий заголовок `p0326:c01`.
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0281:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0325:c01` (45 PDF page chunks). Source locator: PDF page 281–325; printed pages 281–325; EPUB spine: Not applicable.
- **Source:** `source/book.pdf` SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** canonical source, manifest, acceptance and collection template v1.7 checked against main; prior readiness CI run `38394894818` PASS. No new readiness CLI execution is claimed.
- Source content derived **only** from chapter RAG; no direct PDF access, external sources or model-memory corrections to examples.

## Карта главы

| Тематика | PDF/printed | Содержание |
|---|---:|---|
| Зачем нужен Service и сетевая модель | 281–290 | Динамический Pod IP; CNI, service mesh; связь по label selector; DNS; балансировка |
| Service discovery и debug Pod | 290–298 | DNS `service.namespace.svc.cluster.local`, `kubectl run --expose`, `describe`/Endpoints, `port-forward`, `k8sutils` |
| NodePort | 299–305 | `nodePort`, `port`, `targetPort`, `app=whoami`, диапазон портов и риски внешней публикации |
| ClusterIP / headless | 306–312 | Внутрикластерный сервис; declarative YAML; `clusterIP: None` для прямого обнаружения endpoints |
| LoadBalancer / ExternalName | 312–316 | Облачный балансировщик, `loadBalancerClass`, внешний DNS ресурс |
| Проверки состояния | 316–324 | `readinessProbe`, `livenessProbe`, `startupProbe`: HTTP, TCP, exec, gRPC и жизненный цикл |
| Резюме и дополнительные источники | 324–325 | Стабильная точка входа и направление запросов только на готовые приложения |

## Главный принцип

Pod может быть заменён и получить новый IP, поэтому **не закреплять Pod IP в коде** (p0285–p0288). Service — абстракция адресации: его селектор соответствует меткам Pod, а DNS/ClusterIP обеспечивает стабильную точку обращения (p0288–p0297). `readinessProbe` определяет готовность принимать трафик, `livenessProbe` контролирует работоспособность и может инициировать перезапуск, `startupProbe` даёт время медленному старту (p0316–p0324).

## Файлы

- [cheatsheet.md](cheatsheet.md) — диагностический workflow, безопасные проверки, интерпретация, действия, verification и rollback.
- [commands.md](commands.md) — точные source-confirmed команды и YAML с классификацией воздействия.
- [diagram.md](diagram.md) — Mermaid: Service/selector/DNS, порты, probes.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная памятка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная памятка.
- [summary.md](summary.md) — заключительный текст раздела «Резюме», p0324–p0325.
- [source-findings.md](source-findings.md) — неоднозначности источника без самостоятельного исправления.

**Review questions/exercises:** [Not applicable] — самостоятельного блока контрольных вопросов и упражнений между p0281–p0325 не обнаружено. Поэтому `review-questions.md`/`review-answers.md` не создаются.

## Evidence index

- [Pod IP и пример nginx, p0285](../../../rag/chunks/p0201-p0300/p0285-c01.md)
- [Изменение Pod IP, p0286](../../../rag/chunks/p0201-p0300/p0286-c01.md)
- [Service/selector, p0288](../../../rag/chunks/p0201-p0300/p0288-c01.md)
- [Балансировка: оговорка, p0290](../../../rag/chunks/p0201-p0300/p0290-c01.md)
- [Service DNS, p0291](../../../rag/chunks/p0201-p0300/p0291-c01.md)
- [k8sutils DNS/curl, p0295](../../../rag/chunks/p0201-p0300/p0295-c01.md)
- [NodePort YAML, p0300](../../../rag/chunks/p0201-p0300/p0300-c01.md)
- [NodePort port fields, p0301](../../../rag/chunks/p0301-p0400/p0301-c01.md)
- [ClusterIP YAML, p0310](../../../rag/chunks/p0301-p0400/p0310-c01.md)
- [Headless, p0311](../../../rag/chunks/p0301-p0400/p0311-c01.md)
- [LoadBalancer, p0312](../../../rag/chunks/p0301-p0400/p0312-c01.md)
- [ExternalName, p0315](../../../rag/chunks/p0301-p0400/p0315-c01.md)
- [Readiness, p0317](../../../rag/chunks/p0301-p0400/p0317-c01.md)
- [Liveness, p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)
- [Startup, p0323](../../../rag/chunks/p0301-p0400/p0323-c01.md)
- [Summary, p0324](../../../rag/chunks/p0301-p0400/p0324-c01.md)

## Safety boundary

Ни один Kubernetes-кластер не менялся. `kubectl apply/run/expose/delete` и `port-forward` могут менять ресурсы или доступ к ним; `NodePort` и `LoadBalancer` расширяют сетевую поверхность и иногда создают облачные расходы. YAML с незаполненными health-check endpoints нельзя считать production-ready. Полный rollback и фактическая совместимость зависят от среды: **[Needs confirmation]**. Canonical PDF/LFS, RAG, registry, metadata и статус/прогресс чтения остаются без изменений.
