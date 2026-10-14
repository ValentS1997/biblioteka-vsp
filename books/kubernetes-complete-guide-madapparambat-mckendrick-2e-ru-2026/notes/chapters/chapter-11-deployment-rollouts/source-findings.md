# Source findings — Глава 11: Deployment

**Strict source policy:** RAG-only p0384:c01–p0419:c01, PDF 384–419. Сохранены несовпадения, неопределённости и операционные риски *исходника*. Они не разрешаются по памяти модели или внешним источникам. Где из главы нельзя получить подтверждение, ставится **[Needs confirmation]**.

## F-01 — [Source contradiction] — безусловный zero downtime

- **p0389:** RollingUpdate «гарантирует отсутствие простоя».
- **p0405–p0407:** допускается `maxUnavailable: 1` при трех репликах; исходник демонстрирует readiness conditions и медленные обновления, но не измеряет доступность с точки зрения пользователя.
- **p0414:** Recreate приводит к downtime. **Boundary:** опыт не доказывает нулевой downtime RollingUpdate во всякой среде. Нужны readiness, запас capacity, traffic metrics, SLA **[Needs confirmation]**.

## F-02 — [Source code mismatch] — nginx:1.25.4 против nginx:1.17 в rollingupdate

- **p0398–p0399:** `nginx-deployment-readinessprobe.yaml` явно содержит `image: nginx:1.25.4`, пользовательскую shell-команду, создающую `/ready`.
- **p0406:** автор просит *скопировать тот же файл*, при этом утверждает, что он использует `image: nginx:1.17` и `RollingUpdate`. Далее приводит **частичный** `nginx-deployment-rollingupdate.yaml` с nginx:1.17, затем nginx:1.18 (p0407).
- **Boundary:** без подтверждённого промежуточного редактирования исходное копирование не воспроизводит указанную версию образа. **[Needs confirmation]**.

## F-03 — [Source extraction issue] — YAML/Shell command с переносами

- **p0398:** shell `echo "You have been served by Pod with IP address: $(hostname -i)" > /usr/share/nginx/html/index.html` в извлечённом фрагменте перенесён внутри кавычек.
- **p0399:** текст объясняет команду как создание одной строки, содержащей IP Pod.
- **Boundary:** нельзя слепо применять извлечённый PDF-перенос как исходный shell; нормализованная демонстрация в `commands.md` отмечена, фактическая исполняемость на версии образа **[Needs confirmation]**.

## F-04 — [Source wording/code mismatch] — `kubectl delete deployment` перед созданием и последствия Service

- **p0397:** предлагается `kubectl delete deployment nginx-deployment-example` перед созданием `nginx-deployment-readiness`.
- **p0395–p0400:** Service остаётся с selector `app=nginx,environment=test`; после удаления старого Deployment доступ зависит от появления/готовности новых Pod, но окно недоступности не измерено.
- **Boundary:** source exercise intentionally disruptive; не объявлять эту миграцию downtime-free. **[Needs confirmation]**.

## F-05 — [Source code mismatch] — orphan deletion не того Deployment

- **p0404:** `kubectl delete deploy nginx-deployment-readiness --cascade=orphan` — удаляет Deployment readiness и оставляет его Pod.
- **p0404:** следующий текст говорит, что остаются Pod, ранее принадлежавшие `nginx-deployment-example` (другое имя).
- **Boundary:** не отождествлять разные объекты; нужное текущее состояние и владельцы Pod **[Needs confirmation]**.

## F-06 — [Source contradiction] — rollback to revision и новая ревизия

- **p0410:** история `1,2,3` с nginx `1.17→1.18→1.19`.
- **p0411:** `rollout undo` откатывает к предыдущей, и история становится `1,3,4`, ревизия 2 отсутствует; в source отдельно показывается `--to-revision=2` как альтернатива.
- **Boundary:** исходник не доказывает выполнение обеих rollback-команд последовательно. Нельзя приравнивать номер ревизии версии образа или создавать фиксированную неизменную цепочку. **[Needs confirmation]**.

## F-07 — [Source wording/code mismatch] — pause/resume относятся к другому имени

- **p0410–p0411:** rollout/undo осуществляется для `nginx-deployment-rollingupdate`.
- **p0411:** пример `kubectl rollout pause deployment nginx-deployment-example` и `resume deployment nginx-deployment-example` ссылается на **другое** имя.
- **Boundary:** не применять эти команды как часть единого скрипта rollback без проверки фактического deployment; **[Needs confirmation]**.

## F-08 — [Source wording/code mismatch] — canary как точный процент трафика

- **p0412:** 10% traffic на canary описаны при участии Ingress-контроллеров или аннотаций, но конкретной конфигурации нет.
- **p0412–p0413:** stable — 3 реплики, canary — 1, один Service с selector только `app=myapp,tier=frontend`; заявлено, что изменением числа реплик можно регулировать «процент пользователей».
- **Boundary:** source не измеряет traffic share, session affinity, веса или 10%-маршрутизацию. Доля реплик сама по себе не доказывает строгую долю запросов. **[Needs confirmation]**.

## F-09 — [Source scope] — canary manifests неполные

- **p0412–p0413:** stable и canary представлены **фрагментами с многоточиями**, отсутствуют полноценные `apiVersion`, `kind`, `spec`, selector/template, порты контейнера. Только Service даётся целиком.
- **Boundary:** не дополнять недостающие поля из памяти как будто их предоставила книга. Исполнимость двух Deployment YAML [Needs confirmation].

## F-10 — [Needs confirmation] — LoadBalancer и отсутствие провайдера

- **p0394–p0395:** Service `type: LoadBalancer`, затем локальная совместимость оговаривается как зависящая от платформы.
- **p0396:** `kubectl expose deployment --type=LoadBalancer` создаёт **другой** Service, имя равно имени Deployment.
- **Boundary:** внешнего IP, cloud charges, namespace и отдельной политики доступа на target environment source не подтверждает. Применение двух методов может создать два ресурса. **[Needs confirmation]**.

## F-11 — [Needs confirmation] — degraded readiness и время восстановления

- **p0398–p0400:** `failureThreshold: 2`, `periodSeconds: 2`; `rm ready` выключает один endpoint.
- **p0401–p0402:** при отсутствии всех готовых Pod показан `curl` connection failure, затем `touch ready`, текст сообщает «примерно через 2 секунды» доступ к приложению.
- **Boundary:** интервалы и задержки примерные, источник не измеряет гарантированного времени изменения Endpoints/traffic или восстановления для иных probes/caches. **[Needs confirmation]**.

## F-12 — [Needs confirmation] — labels и управление чужими Pod

- **p0389:** source сообщает о `pod-template-hash` как средстве предотвращения конфликта дочерних ReplicaSet и accidental adoption.
- **p0389, p0415:** тут же отмечены overlapping selectors и риск непредсказуемого поведения; предупреждение не создавать bare Pod с совпадающими метками.
- **Boundary:** hash не является универсальной гарантией защиты от любого overlap. Реальные ownerReferences и selectors **[Needs confirmation]**.

## F-13 — [Source wording/code mismatch] — security data, ConfigMap vs Secret

- **p0418:** совет хранить «чувствительную информацию, такую как пароли или конфигурационные данные» в объектах `Secret` и `ConfigMap` вместо встраивания в Deployment.
- **p0386, p0397–p0418:** эта глава не даёт готового secure secret management / RBAC / encryption workflow, отсылает к главе 18.
- **Boundary:** тип `ConfigMap` не объявлен в этой главе криптографически защищённым хранилищем, secure implementation **[Needs confirmation]**.

## F-14 — [Needs confirmation] — outdated/version-dependent commands

- **p0390/p0410:** `--record` прямо объявлен deprecated; change-cause рекомендуется задавать аннотацией.
- **p0417:** `extensions/v1beta1` с Deployment удалён, рекомендуют `apps/v1`.
- **Boundary:** учебные API-версии, `kubectl` и образы Nginx привязаны к источнику; целевой кластер/совместимость и security не проверялись.

## F-15 — [Needs confirmation] — liveness/readiness и external dependencies

- **p0397:** слишком строгие liveness проверки могут порождать лишние перезапуски.
- **p0415–p0416:** readiness рекомендуют для приложений с инициализацией, но дорогое cache warmup не выполнять при каждой проверке; liveness лучше делать простой, не зависящей от внешней БД.
- **Boundary:** вывод является best-practice исходника, но для неизвестного приложения endpoints/thresholds/SLO [Needs confirmation]. Не универсализировать без измерений.

**Operational register:** `delete`, `rm`, `set image`, `scale`, `undo`, `pause/resume`, `apply` могут менять доступность; production-test в книге не доказан. Источник и статусы чтения не менялись.
