# Глава 4. Запуск контейнеров в Kubernetes

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 04.  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7; **режим:** `rag_only`.

## Scope / provenance

- **Chapter boundary VERIFIED:** PDF/печатные страницы **143–180**; глава 5 начинается на p0181. Рубежы подтверждены оглавлением p0009/p0010 и RAG p0143, p0178–p0180, p0181.
- **Addressable chapter RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0143:c01` … `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0180:c01`, 38 страниц/38 чанков, source locator `143`–`180`; EPUB spine: Not applicable.
- **Source:** `source/book.pdf`; SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`; `rag/acceptance.yaml`: `ACCEPTED`, `failed_checks: []`.
- **RAG generation:** `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- **Readiness:** current source checksum, RAG acceptance and canonical templates checked; previous book-readiness CI PASS (38394894818); no new execution of readiness script.
- Нет прямого чтения PDF, внешних источников или заполнения пробелов памятью модели.

## Карта главы

| Раздел | Страницы | Содержание |
|---|---:|---|
| Основы Pod и проектирование | 143–150 | Один или несколько контейнеров на одном узле; localhost, тома, IP/CNI, отделение состояния |
| Создание и операции с Pod | 150–159 | `run`, `apply`, `get`, `describe`, YAML/JSON, `port-forward`, `exec`, `delete` |
| Labels / annotations | 159–165 | Фильтрация, `--show-labels`, `label`, `--overwrite`, аннотации |
| Job | 165–173 | `restartPolicy`, `backoffLimit`, `completions`, `parallelism`, deadline, TTL |
| CronJob | 173–178 | Расписание, `jobTemplate`, дедлайн старта, история Job |
| Резюме и источники | 178–180 | CronJob → Job → Pod; подготовка к многоконтейнерным Pod |

**Главный принцип:** Kubernetes запускает контейнеры **в Pod**. Каждый Pod размещается на одном узле. `Job` управляет Pod для конечной задачи, а `CronJob` запускает `Job` по расписанию (p0144, p0165–p0178). Автор рекомендует пересоздаваемые Pod и внешнее долговременное состояние (p0148–p0150).

## Файлы коллекции

- [cheatsheet.md](cheatsheet.md) — baseline, проверки, интерпретация, действия и rollback.
- [commands.md](commands.md) — классифицированные команды и YAML, включая риски.
- [diagram.md](diagram.md) — концептуальные Mermaid-схемы.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная SVG-памятка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — детальная SVG-памятка.
- [summary.md](summary.md) — оригинальное «Резюме» из RAG p0178–p0179.
- [source-findings.md](source-findings.md) — спорные исходные формулировки без неявных исправлений.

Review questions/exercises: **[Not applicable]** — в главе нет отдельного блока контрольных вопросов/упражнений; `review-questions.md` и `review-answers.md` не требуются.

## Source links

- [Pod p0144](../../../rag/chunks/p0101-p0200/p0144-c01.md)
- [Pod network p0146](../../../rag/chunks/p0101-p0200/p0146-c01.md)
- [Pod design p0149](../../../rag/chunks/p0101-p0200/p0149-c01.md)
- [Imperative p0151](../../../rag/chunks/p0101-p0200/p0151-c01.md)
- [Declarative p0153](../../../rag/chunks/p0101-p0200/p0153-c01.md)
- [Forwarding p0156](../../../rag/chunks/p0101-p0200/p0156-c01.md)
- [Labels p0161](../../../rag/chunks/p0101-p0200/p0161-c01.md)
- [Job p0167](../../../rag/chunks/p0101-p0200/p0167-c01.md)
- [Parallelism p0170](../../../rag/chunks/p0101-p0200/p0170-c01.md)
- [CronJob p0177](../../../rag/chunks/p0101-p0200/p0177-c01.md)
- [Summary p0179](../../../rag/chunks/p0101-p0200/p0179-c01.md)

## Operational boundary

Примеры рассчитаны на доступный учебный Kubernetes-кластер и настроенный `kubectl` (p0144). Живой кластер не проверялся, команды не выполнялись. `kubectl delete`, `replace`, `label`, `exec`, `apply`, `port-forward` имеют эффекты и ограничения, описанные в [commands.md](commands.md); конкретный rollback **[Needs confirmation]**. Источник PDF, RAG, registry и reading status/progress не изменены.
