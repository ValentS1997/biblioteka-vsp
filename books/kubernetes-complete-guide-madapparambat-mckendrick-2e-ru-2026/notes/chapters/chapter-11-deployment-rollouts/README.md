# Глава 11. Использование объекта Deployment для управления рабочими нагрузками без сохранения состояния

**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source mode:** `rag_only`.

## Scope / provenance

- **Boundary VERIFIED:** PDF/печатные страницы **384–419** включительно; заголовок p0384, явное «Резюме» p0418–p0419 и дополнительные источники p0419; глава 12 начинается на p0420. TOC evidence: `p0014:c01`, `p0015:c01`.
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0384:c01` … `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0419:c01`, **36 адресных страниц**. PDF locator/printed: 384–419, EPUB spine: Not applicable. Файлы `rag/chunks/p0301-p0400/p0384…p0400-c01.md` и `rag/chunks/p0401-p0500/p0401…p0419-c01.md`.
- **Canonical source:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus ID `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index ID `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** ранее завершённый workflow `38394894818` PASS; `main` содержит подтверждённые acceptance и шаблон v1.7. Нового запуска readiness CLI не заявлено.
- **Evidence policy:** содержание выводится исключительно из chapter RAG, без прямого PDF, внешней проверки и дополнения модельной памятью.

## Карта главы

| Раздел | PDF | Содержание |
|---|---:|---|
| Требования, типы workload, Deployment | 384–387 | Stateless vs stateful, Job/CronJob, DaemonSet, связь Deployment → ReplicaSet |
| Создание Deployment | 388–391 | `kubectl create --dry-run=client`, `replicas`, `selector`, `template`, RollingUpdate, наблюдение rollout/RS |
| Service и доступ к Pod | 392–396 | Labels/selector, ClusterIP, `LoadBalancer`, `expose`, сетевой debug Pod `k8sutils` |
| Readiness и failure exercise | 396–402 | Непосредственное создание `/ready`, `readinessProbe`, исключение неготовых Pod из Service endpoints |
| Scale и удаление | 402–404 | `replicas: 3 → 10 → 2`, `apply`, `scale`, cascade/orphan |
| Ревизии и update strategies | 404–409 | RollingUpdate (`maxUnavailable`/`maxSurge`), Recreate, изменение nginx:1.17 → 1.18 |
| История и rollback | 409–411 | `set image`, `rollout history`, `rollout undo`, `pause/resume` |
| Canary deployments | 412–413 | Stable/canary Deployment, общий Service, мониторинг и изменение доли пользователей |
| Best practices | 414–418 | GitOps, probes, semantic tags, `apps/v1`, requests/limits, HPA, privilege/security |
| Резюме и ссылки | 418–419 | Итоги управления приложениями без состояния; следующая глава StatefulSet |

## Главный принцип

**Deployment управляет объектами ReplicaSet**, а те поддерживают Pod. Изменение `spec.template` создаёт новую ревизию и позволяет контролировать выкатывание или откат; `spec.replicas` меняет число экземпляров (p0384, p0387–p0391, p0404–p0411). Стратегия `RollingUpdate` ограничивает число недоступных и сверхплановых Pod через `maxUnavailable` и `maxSurge` (p0405–p0407). Наличие Service и **readiness** определяет, какие Pod реально получают трафик (p0392–p0402). `Running` не эквивалентен `Ready`.

Авторы рекомендуют **декларативные изменения + контроль версий** и предостерегают от `Recreate` в production и императивных rollout-команд при работе нескольких операторов (p0409, p0414–p0416). Фактический SLA и нулевой downtime от отдельных настроек не гарантирован экспериментом; см. [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — baseline, read-only, диагноз, изменение, verification и rollback.
- [commands.md](commands.md) — подтверждённые source команды/YAML с классификацией и последствиями.
- [diagram.md](diagram.md) — Mermaid flowchart по Deployment, ready endpoints и rollback.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная памятка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная памятка.
- [summary.md](summary.md) — «Резюме» из chapter RAG p0418–p0419.
- [source-findings.md](source-findings.md) — противоречия/неоднозначности исходника.

**Review questions/answers:** [Not applicable]; отдельного блока контрольных вопросов/упражнений на p0384–p0419 нет.

## Key RAG evidence

- [Типы workload, p0386](../../../rag/chunks/p0301-p0400/p0386-c01.md)
- [Обязанности Deployment, p0387](../../../rag/chunks/p0301-p0400/p0387-c01.md)
- [Deployment YAML, p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md)
- [Strategy и labels, p0389](../../../rag/chunks/p0301-p0400/p0389-c01.md)
- [Rollout status, p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md)
- [Service YAML, p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md)
- [Service доступ, p0395](../../../rag/chunks/p0301-p0400/p0395-c01.md)
- [Readiness example, p0398](../../../rag/chunks/p0301-p0400/p0398-c01.md)
- [Readiness failure, p0401](../../../rag/chunks/p0401-p0500/p0401-c01.md)
- [Scale, p0403](../../../rag/chunks/p0401-p0500/p0403-c01.md)
- [RollingUpdate vs Recreate, p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md)
- [Update, p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md)
- [Revision rollback, p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md)
- [Pause and resume, p0411](../../../rag/chunks/p0401-p0500/p0411-c01.md)
- [Canary service, p0413](../../../rag/chunks/p0401-p0500/p0413-c01.md)
- [Health best practices, p0416](../../../rag/chunks/p0401-p0500/p0416-c01.md)
- [Summary, p0418](../../../rag/chunks/p0401-p0500/p0418-c01.md)

## Safety / unknowns

`kubectl apply`, `scale`, `set image`, `rollout undo`, `pause/resume`, `delete` и `expose --type=LoadBalancer` изменяют состояние кластера или доступность приложения; `kubectl exec -- rm` разрушает файл контейнера. Выполнение не производилось. Target namespace, cluster context, RBAC, Service endpoints, драйвер облачной публикации, квоты, работающие версии и процедура безопасного rollback **[Needs confirmation]**. Не менять canonical PDF/LFS, RAG/registry, статус/даты/прогресс чтения.
