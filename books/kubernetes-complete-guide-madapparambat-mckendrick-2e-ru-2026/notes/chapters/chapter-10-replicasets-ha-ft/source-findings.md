# Source findings — Глава 10. HA/FT и ReplicaSet

**RAG-only, PDF 366–383**, `p0366:c01`–`p0383:c01`. Записи сохраняют расхождения, неопределённости и эксплуатационные риски источника. Без внешних документов, direct PDF или исправлений по памяти. Неподтверждённое — **[Needs confirmation]**.

## F-01 — [Source contradiction] — желаемые четыре реплики против «трёх» в bare-Pod опыте

- **p0372–p0374:** YAML `nginx-replicaset-example.yaml` задаёт `spec.replicas: 4`, `describe` показывает `4 current / 4 desired`.
- **p0375:** после `kubectl delete po` текст утверждает, что создание нового bare Pod приведёт к четырём соответствующим подам, после чего ReplicaSet «удалит один» для возврата «к целевому значению, равному трём».
- **p0376:** в выводе `get pods` три Pod ReplicaSet `Running` и bare Pod `Terminating`. Не представлено отдельное изменение `spec.replicas` на 3.
- **Boundary:** нельзя молча предположить невидимую команду scale или считать сценарий точно воспроизводимым. Точное состояние ReplicaSet на момент опыта **[Needs confirmation]**.

## F-02 — [Source code mismatch] — namespace в выводах kubectl get pods

- **p0372:** ReplicaSet определён в `metadata.namespace: rs-ns`; p0374 и p0375 используют `get pods -n rs-ns`.
- **p0376:** после применения bare Pod в `rs-ns` показана команда `kubectl get pods` **без** `-n rs-ns`, но вывод относится к bare Pod и ReplicaSet из `rs-ns`.
- **p0380–p0381:** отдельный ReplicaSet с liveness не задаёт namespace и `kubectl get pods` относится к текущему context.
- **Boundary:** текущий namespace пользователя источником не показан; для безопасного выполнения/наблюдения namespace и права **[Needs confirmation]**. Не менять источник на `get pods -n` без явного указания коррекции.

## F-03 — [Source wording/code mismatch] — файл для scale down

- **p0372, p0374, p0379:** создание и `apply` используют файл `nginx-replicaset-example.yaml`.
- **p0379:** при уменьшении до `replicas: 2` текст предлагает открыть **`nginx-replicaset.yaml`**, но затем выполняет `kubectl apply -f ./nginx-replicaset-example.yaml`.
- **Boundary:** имя исходного файла для редактирования не согласовано с применяемым файлом. Прежде чем проводить масштабирование, проверять, какой манифест реально меняется. **[Needs confirmation]**.

## F-04 — [Needs confirmation] — пять девяток и минуты простоя

- **p0367:** «пять девяток» названы обычно эталоном высокой доступности; приведена оценка «не более 26 секунд простоя в месяц».
- **Boundary:** условия расчётного календарного месяца и SLA окна отсутствуют, автор не задаёт SLI/SLO и не измеряет кластер из этой главы. Не объявлять 26 секунд согласованным эксплуатационным нормативом без отдельного определения периода. **[Needs confirmation]**.

## F-05 — [Needs confirmation] — контроллер ReplicaSet и гарантированная высокая доступность

- **p0367–p0369:** HA зависит от failover, SPOF, балансировки, monitoring; доступность пользователю отличается от простого числа Pod.
- **p0377–p0378:** после `cordon`, `drain` и `delete node` автор показывает четыре Pod на двух оставшихся узлах и предлагает `curl localhost:8080`.
- **Boundary:** учебный вывод подтверждает конкретный результат, но не измеряет длительность простоя, влияние на другие workloads, устойчивость control plane, сеть и сохранность данных. Совершенная FT/HA **[Needs confirmation]**.

## F-06 — [Needs confirmation] — опасный узловой эксперимент

- **p0377:** `kubectl cordon kind-worker`, `kubectl drain kind-worker --ignore-daemonsets`.
- **p0378:** `kubectl delete node kind-worker`.
- **Boundary:** source не содержит обратных действий, возврата node, проверки PodDisruptionBudget или сетевого восстановления. Это изменение инфраструктуры, не «безопасный health test». Rollback и право на вмешательство **[Needs confirmation]**.

## F-07 — [Source wording/code mismatch] — принятие «голых» Pod и удаление

- **p0373:** ReplicaSet способен захватить bare Pod при совпадающих метках; в рисунке иллюстрируется adoption.
- **p0375–p0376:** после создания `nginx-pod-bare-example` с `app=nginx, environment=test` источник показывает его `Terminating` и `SuccessfulDelete`.
- **Boundary:** одна демонстрация adoption не обещает сохранение bare Pod; совпадающие labels способны привести к его удалению. Текущие ownerReferences/desired count не проверены в кластере пользователя.

## F-08 — [Needs confirmation] — рекомендация модификации шаблона ReplicaSet

- **p0380:** автор утверждает, что для изменения `spec.template` существующего ReplicaSet его «необходимо сначала удалить и создать заново».
- **p0369, p0371–p0372:** книга отдельно рекомендует управлять жизненным циклом шаблонов через Deployment и декларативные обновления.
- **Boundary:** точный режим допустимости изменения шаблона в текущем Kubernetes API непосредственно не проверен; удаление контроллера может каскадно удалить Pod. Не выполнять delete/recreate как универсальную рекомендацию. **[Needs confirmation]**.

## F-09 — [Source code mismatch] — проба без именованного Namespace против прежнего ReplicaSet

- **p0372:** начальный `nginx-replicaset-example` расположен в `rs-ns` с `app=nginx, environment=test`.
- **p0380:** `nginx-replicaset-livenessprobe-example` имеет **те же selector/template labels**, но **не** указывает `metadata.namespace`; команда p0381 не содержит `-n`.
- **Boundary:** если два ReplicaSet окажутся в одном namespace, селекторы пересекутся; если в разных — сценарий относится к двум независимым областям. Текущий namespace/ownerReferences **[Needs confirmation]**.

## F-10 — [Needs confirmation] — liveness как наблюдение HTTP 403

- **p0380:** контейнер Nginx с `httpGet.path: /`, `initialDelaySeconds: 2`, `periodSeconds: 2`; файл `/usr/share/nginx/html/index.html` предлагается удалить.
- **p0381:** `kubectl describe pod` показывает `Unhealthy: HTTP ... statuscode: 403`, затем `Killing` и повторный `Started`.
- **Boundary:** такой код является результатом конкретной конфигурации Nginx из книги; его нельзя гарантировать на всех серверах/образах. Фактический Pod name и условия удаления файла зависят от среды. Сам ReplicaSet **не** осуществляет container restart — источник прямо приписывает его kubelet.

## F-11 — [Source wording/code mismatch] — удаление ReplicaSet

- **p0382:** `kubectl delete rs/nginx-replicaset-livenessprobe-example` удаляет контроллер и его Pod; `kubectl delete ... --cascade=orphan` оставляет Pod.
- **Boundary:** эти действия взаимоисключающие альтернативы. При `orphan` оставшиеся Pod могут быть приняты иным ReplicaSet с пересекающимся selector. Не использовать их подряд как «пошаговый rollback».

## F-12 — [Needs confirmation] — ReplicaSet и распределение по worker

- **p0372:** автор использует kind с тремя worker и четырьмя репликами; примеры p0377–p0378 показывают Pod на разных узлах.
- **Boundary:** `spec.replicas: 4` вместе с label selector **не** сопровождается в YAML явным `topologySpreadConstraints`/`podAntiAffinity`. Источник не показывает гарантированный алгоритм распределения на независимые узлы; реальная конфигурация планировщика **[Needs confirmation]**. Не выдавать число реплик за гарантию failure-domain redundancy.

## F-13 — [Needs confirmation] — версия ReplicaSet / RC и production suitability

- **p0370–p0372:** ReplicationController представлен исторически, ReplicaSet — как предпочтительный наследник, но в production рекомендуются **Deployment**, а не standalone RS.
- **Boundary:** приведённые манифесты standalone ReplicaSet иллюстрируют работу контроллера; это **не готовая production-политика** выката/отката, мониторинга, защиты и масштабирования. Текущие API/совместимость версии [Needs confirmation].

**Операционная граница:** ни `delete po`, ни `drain`, ни `delete node`, ни `exec rm` не выполнялись. Сомнения не устранялись внешней документацией. PDF/RAG и статус чтения не изменены.
