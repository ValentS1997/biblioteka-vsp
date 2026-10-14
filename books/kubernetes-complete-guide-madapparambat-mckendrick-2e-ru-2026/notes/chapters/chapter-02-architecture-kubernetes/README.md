# Глава 2. Архитектура Kubernetes: от образов контейнеров к работающим подам

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** 0033 · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 02  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · **Source mode:** `rag_only`

## Scope / provenance

- **Boundary VERIFIED:** глава 2 начинается на PDF/печатной стр. **71** и завершается на стр. **114** (разделы «Резюме», «Дополнительные источники информации»). Глава 3 начинается на стр. **115**.
- **Boundary evidence:** RAG TOC на стр. 7–8; старт `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0071:c01`; завершение `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0114:c01`; следующая глава `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0115:c01`.
- **Source format:** PDF; **PDF pages / printed pages:** 71–114; **EPUB spine:** Not applicable.
- **Addressable RAG range:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0071:c01` … `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0114:c01`, по одному chunk `c01` на страницу согласно `rag/chunk-index.jsonl`.
- **Canonical source:** `source/book.pdf`; **SHA-256:** `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **Ingestion acceptance:** `ACCEPTED`, `failed_checks: []`. **Corpus generation:** `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- **Book readiness:** accepted previous CI (workflow 38394894818) and matching RAG/metadata/templates confirmed on current main; no new RAG build.
- **No direct PDF access / no external web / no model-memory gap filling.**

## Карта главы

| Раздел | PDF | Ключевые понятия |
|---|---:|---|
| Роли узлов и компоненты кластера | 71–78 | Control Plane, worker nodes, add-ons; смешанные Linux/Windows вычислительные узлы |
| kube-apiserver и etcd | 79–85 | REST, единство API-входа, хранение желаемого состояния |
| kube-scheduler | 86–87 | Unscheduled Pod, `nodeName`, selectors, affinity, taints/tolerations |
| kube-controller-manager / cloud-controller-manager | 88–90 | Reconciliation loops и управление ресурсами облака |
| Container runtime, CRI, kubelet, kube-proxy | 90–96 | containerd, CRI-O, Unix-сокеты, приведение локальных контейнеров к спецификации и сетевые механизмы |
| kubectl / kubeconfig / YAML | 96–107 | Установка клиента, `kubectl`, контексты, imperative/declarative, `apiVersion`/`kind`/`metadata`/`spec` |
| Топологии HA / etcd | 108–113 | Один узел, один управляющий узел, несколько управляющих узлов, Raft |
| Резюме и источники | 114 | Итоги; практическая установка вынесена в главу 3 |

## Главный принцип

Kubernetes — **распределенная система с API-управлением и согласованием состояния**. Пользователь и компоненты обращаются к `kube-apiserver`; кластерное состояние сохраняется через `etcd`; scheduler назначает узел для Pod; контроллеры обеспечивают reconciliation; `kubelet` передает назначенную спецификацию локальной среде выполнения контейнеров. `kube-proxy` обслуживает сетевые механизмы, а `cloud-controller-manager` связывает кластер с облачными ресурсами в облачных установках (PDF 79–96).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — архитектура, baseline, read-only checks и безопасное управление.
- [commands.md](commands.md) — буквальные команды RAG, классы воздействия и ограничения.
- [diagram.md](diagram.md) — архитектурный путь Pod и варианты доступности.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [summary.md](summary.md) — оригинальный раздел «Резюме», стр. 114, с нормализованными переносами.
- [source-findings.md](source-findings.md) — исходные технические формулировки, требующие отдельного подтверждения.

**Review questions / exercises:** [Not applicable] — в главе между стр. 71–114 отдельного блока вопросов/упражнений нет. `review-answers.md` не нужен.

## RAG evidence

- [Component overview, p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md)
- [REST API, p0080](../../../rag/chunks/p0001-p0100/p0080-c01.md)
- [etcd и backup boundary, p0084](../../../rag/chunks/p0001-p0100/p0084-c01.md)
- [scheduler, p0086](../../../rag/chunks/p0001-p0100/p0086-c01.md)
- [reconciliation, p0088](../../../rag/chunks/p0001-p0100/p0088-c01.md)
- [CRI, p0092](../../../rag/chunks/p0001-p0100/p0092-c01.md)
- [kubelet, p0094](../../../rag/chunks/p0001-p0100/p0094-c01.md)
- [kubectl install, p0097](../../../rag/chunks/p0001-p0100/p0097-c01.md)
- [kubectl imperative, p0104](../../../rag/chunks/p0101-p0200/p0104-c01.md)
- [YAML Pod, p0106](../../../rag/chunks/p0101-p0200/p0106-c01.md)
- [HA, p0111](../../../rag/chunks/p0101-p0200/p0111-c01.md)
- [Summary, p0114](../../../rag/chunks/p0101-p0200/p0114-c01.md)

## Ограничения

Глава преимущественно теоретическая (PDF 114). Все примеры установки, изменения кластера и конфигурации зависят от окружения: **[Needs confirmation]**. Перечисленные исходником версии и частоты нельзя считать проверенными на текущем кластере. Картинки и таблицы не представлены отдельными мультимодальными RAG-объектами; используем извлеченный текст, а не интерпретацию исходных диаграмм. **Статус чтения и прогресс не меняются.**
