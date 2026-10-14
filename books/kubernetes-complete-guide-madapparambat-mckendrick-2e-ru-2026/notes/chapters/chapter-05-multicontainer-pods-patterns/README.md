# Глава 5. Использование многоконтейнерных подов и паттерны проектирования

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 05.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source policy:** `rag_only`.

## Scope / provenance

- **Chapter boundary: VERIFIED.** PDF/печатные страницы **181–217**; глава 6 начинается на p0218. Основание: RAG-оглавление p0010, начало p0181, резюме p0217, следующая глава p0218.
- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0181:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0217:c01` (37 PDF-страниц, page-addressable chunks). Source locators: `181`–`217`; EPUB spine: Not applicable.
- **Canonical source:** `source/book.pdf`; SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- **Readiness:** актуальные source/RAG/template v1.7 проверены на `main`; предыдущая проверка readiness CI PASS, новый RAG не создавался. Прямой PDF, внешние сайты и модельная память для восполнения пробелов не использовались.

## Карта главы

| Раздел | PDF | Содержание |
|---|---:|---|
| Многоконтейнерный Pod | 181–188 | Связанность контейнеров, общий узел, YAML с Nginx и Debian, диагностика ImagePullBackOff |
| Жизненный цикл, exec и logs | 188–194 | Обычное и принудительное удаление, `-c`, `jsonpath`, `command` и `args` |
| Init containers | 194–198 | Последовательная подготовка содержимого, обязательность успешной инициализации, logs |
| Тома | 199–206 | `emptyDir`, `hostPath`, `volumeMounts`, связь с Pod и безопасность |
| Паттерн Ambassador | 206–209 | Посредник для исходящего обращения к внешнему сервису |
| Паттерн Sidecar | 209–212 | Логирование с Fluentd, совместный том, дополнительная функция |
| Паттерн Adapter | 212–215 | Преобразование формата журнала в отдельном контейнере |
| Нативные sidecars | 215–216 | `initContainers` с `restartPolicy: Always` по версии, описанной авторами |
| Резюме | 217 | Декларативные многоконтейнерные Pod, подготовка к namespaces |

## Главный принцип

**Pod — совместная единица размещения и управления несколькими тесно связанными контейнерами.** Контейнеры запускаются на одном узле, могут общаться через localhost и разделять тома. Init-контейнеры подготавливают окружение перед стартом основных. Паттерны Ambassador, Sidecar и Adapter разделяют вспомогательные функции, не заставляя изменять основное приложение (PDF 182–216).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — baseline, read-only диагностика, интерпретация и контролируемые изменения.
- [commands.md](commands.md) — подтверждённые RAG команды и YAML, риски, verification/rollback.
- [diagram.md](diagram.md) — Mermaid-схемы и архитектурные границы.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная сводка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная сводка.
- [summary.md](summary.md) — сохранённый раздел книги «Резюме» (p0217).
- [source-findings.md](source-findings.md) — журнал ошибок/несоответствий текста и кода.

**Review questions / exercises:** [Not applicable] — в пределах p0181–p0217 нет отдельного блока контрольных вопросов или упражнений. Поэтому `review-questions.md` и `review-answers.md` не создаются.

## Точные RAG locators

- [Сценарии, p0182](../../../rag/chunks/p0101-p0200/p0182-c01.md)
- [Манифест Pod, p0184](../../../rag/chunks/p0101-p0200/p0184-c01.md)
- [ImagePullBackOff, p0186](../../../rag/chunks/p0101-p0200/p0186-c01.md)
- [Force delete, p0189](../../../rag/chunks/p0101-p0200/p0189-c01.md)
- [kubectl exec/jsonpath, p0190](../../../rag/chunks/p0101-p0200/p0190-c01.md)
- [Init-контейнеры, p0195](../../../rag/chunks/p0101-p0200/p0195-c01.md)
- [Тома, p0199](../../../rag/chunks/p0101-p0200/p0199-c01.md)
- [emptyDir, p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md)
- [hostPath, p0204](../../../rag/chunks/p0201-p0300/p0204-c01.md)
- [Ambassador, p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md)
- [Sidecar, p0211](../../../rag/chunks/p0201-p0300/p0211-c01.md)
- [Adapter, p0214](../../../rag/chunks/p0201-p0300/p0214-c01.md)
- [Native sidecar, p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md)
- [Резюме, p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md)

## Safety / limitations

Выполнение примеров требует настроенного `kubectl` и локального или облачного Kubernetes-кластера (p0182). Никакая команда против реального кластера не исполнялась. `kubectl delete --force` может освободить имя без подтверждения фактической остановки. `emptyDir` теряет содержимое вместе с Pod. `hostPath` зависит от узла и может нарушать изоляцию. Имя манифеста Adapter и результат диагностического манифеста содержат несовпадения: см. `source-findings.md`. Статус чтения, source PDF, RAG и registry не изменяются.
