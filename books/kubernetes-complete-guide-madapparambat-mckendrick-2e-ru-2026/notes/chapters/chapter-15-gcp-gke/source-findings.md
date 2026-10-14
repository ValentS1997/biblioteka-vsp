# Source findings — Глава 15, Google Cloud / GKE

**Strict evidence:** `p0515:c01`–`p0536:c01`, PDF/printed pp515–536. Классы замечаний: [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation]. Без прямого PDF, внешних исследований и исправлений по памяти. Все реальные облачные действия не проводились.

## F-01 — [Needs confirmation] — trial credits and actual pricing

- **p0518:** автор описывает пробные **$300 на 90 дней** на момент подготовки книги, с требованием указать платёжный способ.
- **p0515, p0535:** расходы реальны, исторические ориентиры около **$55 в месяц** за 2 узла и **$347 в месяц** за 8 узлов.
- **Boundary:** право на trial, включённые операции и актуальная стоимость сегодня не проверены. Эти суммы **не являются текущей ценовой офертой**, и нет калькуляции балансировщика/дисков/трафика. [Needs confirmation].

## F-02 — [Needs confirmation] — опасный установщик Windows без checksum

- **p0521:** `choco install --ignore-checksum gcloudsdk`.
- **p0521:** выше предлагается установить Chocolatey через PowerShell, загружающий и исполняющий внешний скрипт.
- **Boundary:** ни пакет, ни подпись/проверка целостности в chapter RAG не проверены. Не объявлять это безопасной общесистемной инструкцией. [Needs confirmation].

## F-03 — [Needs confirmation] — удалённый shell installer Linux

- **p0521:** `curl https://sdk.cloud.google.com | bash` загружает код и сразу исполняет.
- **Boundary:** source не предоставляет pinned checksum, threat model, верификацию содержимого либо откат. Ни одна команда не выполнялась. [Needs confirmation].

## F-04 — [Source wording/code mismatch] — Cloud Shell и версии CLI

- **p0522:** сказано, что gcloud в Cloud Shell уже инициализирован, но также что версии «соответствуют» локально установленным.
- **p0520–p0521:** разные OS используют различные способы установки, но actual `gcloud version` для каждой среды не приводится текстом целиком.
- **Boundary:** равенство версий/профилей CLI разных сред не доказано; выбранный project/context надо проверять отдельно. [Needs confirmation].

## F-05 — [Needs confirmation] — kubeconfig side effect and target cluster

- **p0524–p0525:** `gcloud container clusters create` сообщает о создании kubeconfig entry.
- **p0526–p0527:** для другого локального kubectl `get-credentials` изменяет kubeconfig, `use-context` переключает текущую цель.
- **Boundary:** источник не фиксирует предыдущий context, не даёт rollback kubeconfig и не доказывает, что последующие `kubectl apply` адресуют нужный проект без проверки. [Needs confirmation].

## F-06 — [Needs confirmation] — применение изменяемых удалённых YAML

- **p0527:** шесть манифестов Guestbook применяются прямо из URL `raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/...`.
- **Boundary:** URL привязаны к ветке `main`, а не к неизменному commit SHA; полные тексты манифестов отсутствуют в RAG главы. Версия, labels, контейнеры, security и актуальная работоспособность **[Needs confirmation]**. Не представлять их как аудированные.

## F-07 — [Source scope] — публичный frontend без HTTPS

- **p0528:** автор прямо предписывает открыть `http://EXTERNAL-IP`, не HTTPS, поскольку frontend слушает 80, а не 443.
- **p0530–p0531:** Service frontend имеет публичный LoadBalancer, Redis — ClusterIP.
- **Boundary:** пример годится только для тестовых данных; TLS/Ingress/Certificate/Identity protection для production не приводятся. Данные Guestbook не объявлять защищёнными на публичном HTTP. [Needs confirmation].

## F-08 — [Needs confirmation] — данные Redis/Guestbook и SLO

- **p0527–p0528:** три Deployment, три Service и демонстрационные записи Guestbook.
- **p0530–p0532:** Console показывает метрики и расположение ресурсов, Backup for GKE упомянут как отдельная функция.
- **Boundary:** data persistence, репликация Redis между зонами, backup restore, encrypted secrets, SLA или disaster recovery не тестируются. [Needs confirmation].

## F-09 — [Source wording/code mismatch] — `--num-nodes=2` zonal vs regional

- **p0524–p0526:** `--num-nodes=2 --zone=us-central1-a` даёт **2 узла всего**.
- **p0534:** `--num-nodes=2 --region=us-central1` даёт **2 узла в каждой из трёх зон = 6** в данном опыте.
- **Boundary:** один и тот же параметр используется для разных scope; нельзя называть региональный кластер «двухузловым». Default zones текущей версии GKE **[Needs confirmation]**.

## F-10 — [Source wording/code mismatch] — regional update `--min-nodes` vs create `--num-nodes`

- **p0534:** региональный `create` использует `--num-nodes=2` и четыре `--node-locations`.
- **p0535:** `update` существующего кластера использует **`--min-nodes=2`**, также четыре зоны.
- **Boundary:** точная семантика `min-nodes` против явной численности `num-nodes` не объяснена, но результат описан как 8 узлов. Нельзя без проверки считать `--min-nodes` эквивалентом команды create или гарантией итоговых 8 узлов. [Needs confirmation].

## F-11 — [Needs confirmation] — повторное имя кластера в разных примерах

- **p0524:** создание zonal `myfirstgkecluster`.
- **p0533:** команда удаления zonal кластера.
- **p0534–p0535:** создание нового regional `myfirstgkecluster`, затем update.
- **Boundary:** примеры различаются location и предполагают правильный lifecycle; book не приводит проверку идентификатора каждого существующего кластера или затрат до повторного create. Не объединять их в один слепой shell script.

## F-12 — [Source contradiction] — абсолютная зональная отказоустойчивость

- **p0533:** утверждается, что при отказе одной зоны и распределённой workload «ее работа не будет нарушена».
- **p0534–p0536:** много-зонный кластер назван полностью избыточным и высокодоступным, но проведена только проверка `kubectl get nodes`.
- **Boundary:** отсутствие измеренной пользовательской доступности, anti-affinity, readiness, data replica/zone failover и failed-zone drill означает, что нулевой downtime и полноценная DR **не доказаны**. [Needs confirmation].

## F-13 — [Needs confirmation] — `kubectl delete service` и биллинг

- **p0533:** `kubectl delete service frontend`, затем удаление zonal GKE кластера.
- **p0533:** автор предупреждает об осиротевших Google Cloud ресурсах/сервисах, которые следует проверить в консоли.
- **Boundary:** teardown **не гарантирует** нулевой баланс расходов, отсутствие оставшихся дисков, IP или других объектов. Нужно проверить console/billing после удаления; откат данных не показан. [Needs confirmation].

## F-14 — [Source scope] — Backup for GKE и app backup

- **p0532:** `Backup for GKE` назван отдельным сервисом, который не входит в базовую GKE, и описана авторская стратегия вынесения stateful данных в управляемые облачные БД.
- **Boundary:** ни Backup for GKE, ни database-as-a-service в лаборатории фактически не настроены, а восстановление нигде не тестируется. [Needs confirmation].

## F-15 — [Needs confirmation] — naming, regions, quotas, available machine types

- **p0533:** автор напоминает, что не все типы машин доступны в любой зоне; p0534–p0535 используют четыре названные зоны `a,b,c,f`.
- **Boundary:** наличие зон, квоты, текущие региональные defaults, доступные типы узлов и цены при реальном развёртывании не проверены. [Needs confirmation].

**No external adjudication.** Источник/статус чтения не изменены, никаких аккаунтов/ресурсов GCP не создавалось.
