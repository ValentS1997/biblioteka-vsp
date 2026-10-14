# Глава 7. Настройка подов с помощью объектов ConfigMap и Secret

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** 0033. **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026`. **Chapter:** 07.  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · `rag_only`.

## Scope / provenance

- **Границы VERIFIED:** PDF/печатные страницы **248–280** включительно; глава 8 начинается p0281. RAG-оглавление p0011–p0012; p0248 начало, p0279 «Резюме», p0280 источники.
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0248:c01` … `…:p0280:c01`; 33 source-page chunks. EPUB spine: Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`. Full-book RAG `ACCEPTED`, `failed_checks: []`; corpus ID `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- Current main, acceptance and canonical template v1.7 checked; prior readiness run 38394894818 PASS. No direct PDF, web or memory-derived sources; no new readiness CLI execution claimed.

## Карта главы

| Раздел | PDF | Содержание |
|---|---:|---|
| Отделение кода от конфигурации | 248–253 | ConfigMap, Secret; применение env и volumes |
| Создание ConfigMap | 254–260 | `get cm`, `create`, `apply`, literals, file, env-file |
| ConfigMap внутри Pod | 261–266 | `configMapKeyRef`, `envFrom`, конфигурационный том |
| Изменение и удаление | 266–268 | `delete cm`, `FailedMount`, `edit`, immutable |
| Конфиденциальные данные | 268–274 | Base64, RBAC, KMS, императивное/декларативное создание Secret |
| Secret внутри Pod | 275–279 | `secretKeyRef`, `envFrom.secretRef`, том Secret, удаление и обновление |
| Резюме | 279–280 | Конфигурация отдельно от контейнерного образа; далее Service |

**Главный вывод:** отделить конфигурацию от образа контейнера, создать ConfigMap/Secret и связать с Pod через переменные окружения или том. Base64 — **кодирование, не шифрование**. Для защиты Secret в книге рекомендованы RBAC, KMS, внешние хранилища и аудит (p0268–p0275).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [source-findings.md](source-findings.md)

Review questions and answers: **[Not applicable]**, отдельного раздела контрольных вопросов или упражнений в p0248–p0280 нет.

## Source links

- [ConfigMap/Secret, p0251](../../../rag/chunks/p0201-p0300/p0251-c01.md)
- [Способы внедрения, p0252](../../../rag/chunks/p0201-p0300/p0252-c01.md)
- [ConfigMap literals, p0256](../../../rag/chunks/p0201-p0300/p0256-c01.md)
- [Flask env, p0262](../../../rag/chunks/p0201-p0300/p0262-c01.md)
- [Flask volume, p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md)
- [FailedMount, p0267](../../../rag/chunks/p0201-p0300/p0267-c01.md)
- [Secret security, p0269](../../../rag/chunks/p0201-p0300/p0269-c01.md)
- [stringData, p0272](../../../rag/chunks/p0201-p0300/p0272-c01.md)
- [Secret env, p0275](../../../rag/chunks/p0201-p0300/p0275-c01.md)
- [Secret volume, p0278](../../../rag/chunks/p0201-p0300/p0278-c01.md)
- [Summary, p0279](../../../rag/chunks/p0201-p0300/p0279-c01.md)

## Operational boundary

Никаких команд на рабочем кластере не исполнялось. Реальные токены, пароли, Base64-значения и закрытые настройки в артефакты не включать; демонстрационные секретные значения книги приводятся только как концептуальные примеры с placeholders. `kubectl get secret`, `exec -- env`, просмотр файлов могут раскрыть значения в журналах. `delete` может нарушить запуск Pod; указывается rollback [Needs confirmation]. Статус чтения и прогресс книги, RAG и PDF не меняются.
