# Глава 1. Основы Kubernetes

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Inventory:** `0033` · **Chapter:** `01`  
**Contract:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · **Source policy:** `rag_only`

## Chapter scope and provenance

- Название главы: **«Основы Kubernetes»**.
- Граница подтверждена по RAG-оглавлению (PDF стр. 6–7), началу главы (PDF стр. 34), завершающему разделу (стр. 70) и началу главы 2 (стр. 71).
- PDF/source locator: страницы **34–70 включительно**; printed pages: **34–70** (по колонтитулам); EPUB spine: Not applicable.
- Диапазон адресных chunk ID: `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0034:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0070:c01`.
- Canonical source: `source/book.pdf`; SHA-256: `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- RAG ingestion: `ACCEPTED`. Corpus generation: `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- Не использованы прямое чтение PDF, web и знания модели для восполнения пробелов.

## Карта главы

| Раздел | PDF-страницы | Ключевой тезис |
|---|---|---|
| Монолиты и микросервисы; DevOps, облака | 35–48 | Давление частых релизов, необходимость организационной и архитектурной гибкости |
| Контейнеры и контейнерные движки | 48–56 | Образ, запущенный контейнер, реестр, Dockerfile, Docker/Podman, Compose |
| Kubernetes и KubeVirt | 57–58 | Оркестрация кластерных рабочих нагрузок, сосуществование контейнеров и ВМ |
| История и экосистема Kubernetes | 59–62 | Идеи Borg/Omega, CNCF, платформы и альтернативы |
| Задачи Kubernetes | 62–69 | HA, обновление и откат, scaling, сети, RBAC, storage, ресурсные лимиты |
| Резюме и дополнительные источники | 69–70 | Завершение введения; переход к архитектуре Kubernetes в главе 2 |

## Основной принцип

**Контейнерный движок управляет контейнерами, а Kubernetes координирует контейнеризованные рабочие нагрузки в масштабе кластера**, включая доступность, обновления, масштабирование и политику доступа. Выбор Kubernetes зависит от масштаба и характера приложения: при отсутствии контейнеризации или очень малом количестве сервисов он может быть избыточен (стр. 52, 57–58, 62–69).

## Артефакты

- [Cheatsheet](cheatsheet.md) — контекст, ограничения, оценка применимости, безопасные действия.
- [Commands](commands.md) — только команды и инструменты, обнаруженные в RAG.
- [Conceptual diagram](diagram.md) — Mermaid-карта логики главы.
- [Compact SVG](visual-cheatsheet.svg) — краткая визуальная сводка.
- [Detailed SVG](visual-cheatsheet-detailed.svg) — расширенная визуальная сводка.
- [Original chapter-end summary](summary.md) — раздел «Резюме» со стр. 69.
- [Source findings](source-findings.md) — непроверенные технические формулировки, без молчаливого исправления источника.

**Review questions:** [Not applicable] — раздел контрольных вопросов/упражнений в RAG-главе 1 не обнаружен.

## Проверяемые RAG-точки

- [Начало главы, p0034:c01](../../../rag/chunks/p0001-p0100/p0034-c01.md)
- [Монолит и микросервисы, p0044:c01](../../../rag/chunks/p0001-p0100/p0044-c01.md)
- [Контейнерный движок, p0053:c01](../../../rag/chunks/p0001-p0100/p0053-c01.md)
- [Dockerfile, p0055:c01](../../../rag/chunks/p0001-p0100/p0055-c01.md)
- [Kubernetes production, p0057:c01](../../../rag/chunks/p0001-p0100/p0057-c01.md)
- [Обновление Deployment, p0065:c01](../../../rag/chunks/p0001-p0100/p0065-c01.md)
- [Ресурсы и резюме, p0069:c01](../../../rag/chunks/p0001-p0100/p0069-c01.md)

## Ограничения

Это обзорная глава: она не задает лабораторную среду, полный набор команд для проверки кластера, конкретные deployment manifests или воспроизводимую процедуру rollback. Эти сведения не восстанавливаются из внешних знаний: **[Needs confirmation]**. Иллюстрации PDF не являются отдельными мультимодальными RAG-объектами. Статус чтения и прогресс не изменялись.
