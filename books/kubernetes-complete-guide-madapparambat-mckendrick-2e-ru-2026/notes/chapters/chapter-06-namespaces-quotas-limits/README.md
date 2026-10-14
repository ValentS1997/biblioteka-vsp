# Глава 6. Пространства имен, квоты и лимиты для реализации мультитенантности в Kubernetes

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 06  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · **Source policy:** `rag_only`

## Scope / provenance

- **Chapter boundary: VERIFIED.** Глава 6 занимает PDF/печатные страницы **218–247** включительно. На p0247 завершается «Резюме» и расположен раздел «Дополнительные источники информации». Глава 7 начинается на **248**.
- **Boundary evidence:** RAG-оглавление p0010–p0011; `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0218:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0246:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0247:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0248:c01`.
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0218:c01` … `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0247:c01` (30 PDF-страниц); source locator 218–247; printed 218–247; EPUB spine: Not applicable. Chunk files `rag/chunks/p0201-p0300/p####-c01.md`.
- **Canonical source:** `source/book.pdf`; SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG ingestion:** `ACCEPTED`, `failed_checks: []`; corpus ID `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index ID `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Precondition:** source SHA/manifest and template v1.7 match current main; previous `Validate book readiness` run 38394894818 PASS. A fresh readiness CLI run is not claimed.
- **Method:** chapter RAG only; no direct PDF reading, no external verification and no memory-derived source corrections.

## Карта главы

| Подраздел | PDF | Главные идеи |
|---|---:|---|
| Namespace и изоляция | 218–223 | Логическое разделение, четыре типичных системных пространства, общекластерные объекты, права и сети |
| Создание, удаление и target namespace | 224–230 | `kubectl create ns`, `apply -f`, `delete`, `-n`, `config set-context`, имя в пределах namespace |
| DNS и практики мультитенантности | 231–233 | FQDN `service.namespace.svc.cluster.local`; RBAC, NetworkPolicy, имена и организация |
| Requests и limits | 233–240 | CPU millicores, Mi/Gi memory, scheduler, Pending, события FailedScheduling, throttling/OOM |
| ResourceQuota | 240–244 | Hard caps на CPU, RAM, количество объектов, PVC/storage; admission error при превышении |
| LimitRange | 244–246 | `default`, `defaultRequest`, `min`, `max` для контейнеров, просмотр и удаление |
| Резюме и дополнительные источники | 246–247 | Итоги и переход к ConfigMap/Secret в главе 7 |

## Главный принцип

**Namespace** задаёт логическую область ресурсов и имён, но сам не является полной изоляцией сети или вычислительной нагрузки. **ResourceQuota** определяет совокупный бюджет в namespace; **LimitRange** — значения и границы для отдельных контейнеров; **requests/limits** участвуют в размещении и ограничении выполнения (p0219–p0236, p0240–p0246).

В исходнике прямо сказано, что связь между namespace может быть разрешена по умолчанию; для безопасности необходимо дополнение RBAC и сетевыми политиками (p0221, p0231–p0233).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — symptom, baseline, read-only, interpretation, actions, verification и rollback.
- [commands.md](commands.md) — только подтверждённые команды/YAML главы, с классификацией и рисками.
- [diagram.md](diagram.md) — Mermaid-карта и диагностический flow.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — обязательная компактная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — обязательная подробная схема.
- [summary.md](summary.md) — исходный раздел «Резюме», p0246–p0247.
- [source-findings.md](source-findings.md) — конфликтующие формулировки `-n`, `get all`, описания безопасности и прочие границы.

Отдельных контрольных вопросов/упражнений в RAG p0218–p0247 **нет**: `review-questions.md` и `review-answers.md` — [Not applicable].

## RAG source references

- [Namespace и область действия, p0219](../../../rag/chunks/p0201-p0300/p0219-c01.md)
- [Стандартные пространства, p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md)
- [Создание Namespace, p0224](../../../rag/chunks/p0201-p0300/p0224-c01.md)
- [Удаление и риск, p0225](../../../rag/chunks/p0201-p0300/p0225-c01.md)
- [Указание metadata.namespace, p0226](../../../rag/chunks/p0201-p0300/p0226-c01.md)
- [Смена контекста, p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md)
- [Cluster-scoped и область имен, p0230](../../../rag/chunks/p0201-p0300/p0230-c01.md)
- [DNS и границы, p0231](../../../rag/chunks/p0201-p0300/p0231-c01.md)
- [Requests CPU/memory, p0235](../../../rag/chunks/p0201-p0300/p0235-c01.md)
- [Scheduling failure, p0239](../../../rag/chunks/p0201-p0300/p0239-c01.md)
- [ResourceQuota YAML, p0241](../../../rag/chunks/p0201-p0300/p0241-c01.md)
- [Quota rejection, p0242](../../../rag/chunks/p0201-p0300/p0242-c01.md)
- [LimitRange YAML, p0245](../../../rag/chunks/p0201-p0300/p0245-c01.md)
- [Summary, p0247](../../../rag/chunks/p0201-p0300/p0247-c01.md)

## Operational safety / limitations

Выполнение упражнений требует авторизованного Kubernetes-кластера и `kubectl` (p0218). **Удаление Namespace уничтожает находящиеся в нём ресурсы**; обратимость и сохранность persistent storage в главе не гарантированы. `kubectl config set-context` изменяет локальную конфигурацию и область последующих команд. `ResourceQuota`, `LimitRange` и `requests/limits` могут приводить к отказу admission или Pending. Реальных запусков/измерений нет; актуальные версии и семантика конфликтующих утверждений [Needs confirmation]. Источник, RAG, registry, status/progress чтения не изменяются.
