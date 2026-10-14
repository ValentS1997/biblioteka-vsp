# Глава 12. Объект StatefulSet: развертывание приложений с сохранением состояния

**Inventory:** 0033 · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Mode:** `rag_only`.

## Provenance / boundary

- **VERIFIED:** PDF/печатные страницы **420–456** включительно. Заголовок p0420, явное «Резюме» p0455–p0456, дополнительные источники p0456; следующая глава 13 начинается на **457**. Оглавление RAG p0015:c01–p0016:c01.
- **Source RAG locators:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0420:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0456:c01`; **37 PDF страниц**, `rag/chunks/p0401-p0500/p####-c01.md`. EPUB spine: not applicable.
- **Canonical source PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`. Full RAG acceptance `ACCEPTED`, `failed_checks: []`, corpus ID `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index ID `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** prior book readiness CI `38394894818` PASS; canonical template v1.7 and acceptance inspected at main. New readiness CLI execution is **not claimed**.
- **Source discipline:** no direct PDF, no external sources, no supplementation from model memory, no live Kubernetes tests. Unknown outcomes **[Needs confirmation]**.

## Карта главы

| Раздел | PDF | Ключевые сведения |
|---|---:|---|
| Состояние в контейнере и Pod | 420–423 | изменяемые данные, тома, PV/PVC/StorageClass, различие компонентов stateful/stateless |
| StatefulSet vs Deployment | 424–426 | имена `mysql-stateful-0`, порядок Pod, `volumeClaimTemplates`, headless service |
| Ограничения и репликация данных | 426–428 | storage provisioner, PVC retention, backup и репликация приложения отдельно от StatefulSet |
| Создание MySQL StatefulSet | 428–435 | `mysql-secret`, namespace `mysql`, `mysql-headless`, 3 Pod, отдельные PVC 1Gi RWO |
| DNS и сохранность при пересоздании | 435–439 | FQDN `mysql-stateful-0.mysql-headless`, база `ststest`, delete/recreate Pod |
| Масштабирование | 439–442 | `OrderedReady` vs `Parallel`, scale 3→4→2, PVC после scale-down остаются |
| Удаление и retention | 442–443 | cascading/orphan; `persistentVolumeClaimRetentionPolicy`; опасное удаление PVC |
| RollingUpdate, OnDelete, partition | 443–451 | обратный порядок 2→1→0; mysql 8.2.0→8.3.0→8.4.0; staged canary 3→2→0 |
| Откат, best practices | 452–455 | Git rollback, обратная миграция данных, scale-to-zero before delete, network storage, probes |
| Резюме и ссылки | 455–456 | итог StatefulSet, переход к DaemonSet |

## Главная идея

**StatefulSet гарантирует стабильную идентичность реплики, а не репликацию её данных.** Имена Pod `<statefulset>-<ordinal>` стабильны при пересоздании; поды `mysql-stateful-0`, `-1`, `-2` получают **разные PVC**, созданные по `volumeClaimTemplates`: `mysql-data-mysql-stateful-0`, `-1`, `-2`. Через `spec.serviceName: mysql-headless` и `clusterIP: None` обеспечивается предсказуемое DNS-обращение к каждой реплике (p0424–p0436).

Сохранение одной тестовой БД `ststest` в **одной** реплике при удалении и пересоздании Pod показано на p0437–p0438. Наличие трёх отдельных томов не означает MySQL replication, data consistency или HA: source p0423, p0427 прямо выносит синхронизацию данных, удалённое storage и external backup за пределы StatefulSet.

`OrderedReady` задаёт последовательность создания/удаления Pod; `RollingUpdate` обновляет в обратном порядке, ожидая Ready. `partition` сохраняет менее старшие реплики на прежней версии и позволяет поэтапно обновлять (p0440–p0451). **Нельзя откатывать MySQL образ без проверки совместимости формата данных** (p0452–p0454).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — workflow с baseline, диагностикой, интерпретацией, изменением и восстановлением.
- [commands.md](commands.md) — YAML/CLI из главы, эффект, риск, проверка, откат.
- [diagram.md](diagram.md) — Mermaid: идентичность PVC, ordered scale, rollout и retention.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактный визуальный конспект.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробный визуальный конспект.
- [summary.md](summary.md) — оригинальный раздел «Резюме», p0455–p0456.
- [source-findings.md](source-findings.md) — source contradictions, code mismatches, caveats.

**Review questions/answers:** [Not applicable] — нет отдельного контрольного блока на страницах 420–456.

## Evidence index

- [Что такое состояние, p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md)
- [StatefulSet vs Deployment, p0424](../../../rag/chunks/p0401-p0500/p0424-c01.md)
- [Упорядоченные реплики, p0425](../../../rag/chunks/p0401-p0500/p0425-c01.md)
- [Ограничения и storage, p0426](../../../rag/chunks/p0401-p0500/p0426-c01.md)
- [Данные и внешняя репликация, p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)
- [MySQL StatefulSet, p0429](../../../rag/chunks/p0401-p0500/p0429-c01.md)
- [volumeClaimTemplates, p0430](../../../rag/chunks/p0401-p0500/p0430-c01.md)
- [Headless + Secret, p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md)
- [PVC и Pod, p0433](../../../rag/chunks/p0401-p0500/p0433-c01.md)
- [DNS, p0436](../../../rag/chunks/p0401-p0500/p0436-c01.md)
- [Сохранение ststest, p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)
- [Scale и OrderedReady, p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md)
- [Retain vs whenScaled Delete, p0442](../../../rag/chunks/p0401-p0500/p0442-c01.md)
- [Удаление PVC и риски, p0443](../../../rag/chunks/p0401-p0500/p0443-c01.md)
- [Rollout и OnDelete, p0444](../../../rag/chunks/p0401-p0500/p0444-c01.md)
- [Partition, p0445](../../../rag/chunks/p0401-p0500/p0445-c01.md)
- [Canary, p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md)
- [Rollback и миграция схемы, p0452](../../../rag/chunks/p0401-p0500/p0452-c01.md)
- [Резюме, p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)

## Safety

Ни один кластер не изменялся. Демонстрационные пароли MySQL в книге являются plaintext и не переносятся в runbook; `kubectl create secret --from-literal` может раскрывать значения в shell history. `kubectl delete pvc` при `Delete` reclaim может уничтожить базовый том и данные; `kubectl delete po`/ `scale`/ `apply`/ `patch` и `rollout undo` меняют приложение. Откаты форматов БД без обратной миграции опасны. StorageClass, провиженер, RBAC, backup и реальная репликация [Needs confirmation]. Не изменять source, RAG, registry, reading status/progress/dates.
