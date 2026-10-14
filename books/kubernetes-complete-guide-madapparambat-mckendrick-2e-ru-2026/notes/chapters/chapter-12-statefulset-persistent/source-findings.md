# Source findings — глава 12, StatefulSet

**Source:** только RAG p0420:c01–p0456:c01; PDF/печатные стр. 420–456. Ниже исходные противоречия и пределы доказанности, не исправления по внешним источникам. Неизвестное обозначено **[Needs confirmation]**.

## F-01 — [Source contradiction] — автоматическое provision хранилища
**p0424:** `volumeClaimTemplates` якобы полностью обеспечивает динамическое хранилище одним созданием StatefulSet. **p0426, p0430–p0431:** отдельно необходим provisioner/подготовленный backend, default StorageClass может зависеть от кластера. **Boundary:** PV и доступность storage [Needs confirmation].

## F-02 — [Source contradiction] — судьба PVC после scale-down
**p0426, p0441:** PVC после сокращения числа Pod остаются. **p0442:** `persistentVolumeClaimRetentionPolicy.whenScaled: Delete` предусматривает удаление. **Boundary:** результат зависит от actual retention policy; сохранность не универсальна [Needs confirmation].

## F-03 — [Source wording/code mismatch] — удаление PVC vs базового PV
**p0434:** PV с reclaim `Delete`. **p0443:** удаление четырёх PVC описывается как удаление связанных PV, но не проверяется физический backend. **Boundary:** возможная потеря данных, rollback [Needs confirmation].

## F-04 — [Source contradiction] — автоматическая репликация / failover
**p0423, p0427:** StatefulSet не синхронизирует данные отдельных MySQL Pod и не реализует backup. **p0455:** liveness якобы может позволить «переключение на другой исправный под с тем же состоянием». **Boundary:** ни одинаковое состояние, ни автоматический MySQL failover экспериментом не доказаны [Needs confirmation].

## F-05 — [Needs confirmation] — CNAME в DNS
**p0436:** упомянуты CNAME для индивидуальных Pod, но показанный `nslookup mysql-headless` выводит только A-записи headless Service. **Boundary:** тип DNS RR и точный FQDN каждого Pod вне показанного опыта [Needs confirmation].

## F-06 — [Needs confirmation] — всегда новый Pod IP
**p0437–p0438:** автор ожидает смену IP при удалении Pod. Вывод подтверждает то же имя и базу `ststest`, но не предъявляет пару old/new IP. **Boundary:** новый адрес для каждой попытки пересоздания [Needs confirmation]; идентичность DNS и PVC — цель примера.

## F-07 — [Source wording/code mismatch] — общий headless vs конкретный Pod
**p0435:** `mysql -h mysql-headless.mysql.svc.cluster.local` не фиксирует ordinal. **p0436–p0438:** `mysql -h mysql-stateful-0.mysql-headless` выбирает конкретную реплику. **Boundary:** вывод одной БД нельзя распространять на три Pod.

## F-08 — [Needs confirmation] — OrderedReady и блокировка при ошибках
**p0440:** остановившийся `mysql-stateful-0` должен остановить масштабирование 4→1. Негативный сценарий не исполнялся. **Boundary:** runtime исход для данной политики и версии [Needs confirmation].

## F-09 — [Needs confirmation] — смена updateStrategy
**p0445:** заявлена невозможность менять стратегию без удаления объекта. Подтверждающего CLI/результата API нет. **Boundary:** не рекомендовать деструктивное удаление без отдельной проверки [Needs confirmation].

## F-10 — [Needs confirmation] — rollback failed RollingUpdate
**p0444:** описаны ручное удаление сбойного Pod и остановка по NotReady. **p0445–p0451:** проверены только успешные сценарии. **Boundary:** safe recovery реальных данных и точный порядок rollback [Needs confirmation].

## F-11 — [Needs confirmation] — plaintext password in tutorial
**p0429–p0432:** Secret создаётся с `--from-literal` и демонстрационными паролями, альтернативный YAML упоминает Base64. **Boundary:** реальная конфиденциальность RBAC/KMS не проверена; не коммитить значения, не записывать в историю терминала.

## F-12 — [Needs confirmation] — совместимость MySQL версий
**p0429:** MySQL 8.2.0; **p0446–p0451:** 8.3.0, затем 8.4.0. **p0452–p0454:** схема БД может потребовать обратной миграции. **Boundary:** наличие тестовой `stsrolling` не доказывает совместимость всех таблиц/форматов или безопасный downgrade [Needs confirmation].

## F-13 — [Needs confirmation] — hostPath и переносимость
**p0434:** учебный `minikube-hostpath`; **p0427, p0454:** советуется удалённый backend, доступный другим узлам. **Boundary:** перенос Pod на другой node с прежними данными, backup и resilience [Needs confirmation].

## F-14 — [Needs confirmation] — OnDelete hooks
**p0444:** OnDelete требует ручного удаления Pod; названы `postStart`/`preStop` в RollingUpdate, но hooks YAML и тестов нет. **Boundary:** production lifecycle и fail path [Needs confirmation].

## F-15 — [Needs confirmation] — Parallel vs RollingUpdate
**p0440:** `podManagementPolicy: Parallel` относится к масштабированию, не к порядку RollingUpdate; **p0444–p0445:** обновление идёт с верхнего ordinal. **Boundary:** конкретный сценарий Parallel+partition в одной демонстрации не проверен.

## F-16 — [Source wording/code mismatch] — delete не равен scale-to-zero
**p0425, p0440:** упорядоченный scale down. **p0426, p0442–p0443, p0453–p0454:** удаление StatefulSet с живыми Pod порядок завершения не гарантирует. **Boundary:** для согласованного завершения сначала scale-to-zero, но полное безопасное восстановление [Needs confirmation].

## F-17 — [Needs confirmation] — локальная persistence vs backup
**p0437–p0438:** `ststest` после повторного запуска Pod с тем же PVC. **p0427:** внешних backup StatefulSet не делает. **Boundary:** этот опыт не проверяет потерю диска, полное разрушение кластера или восстановление удалённого PVC.

**Source corrections not applied.** Никаких изменений PDF/RAG, registry или статуса чтения.
