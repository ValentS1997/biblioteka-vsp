# Source findings — Глава 13, DaemonSet

**Provenance:** RAG-only p0457:c01–p0473:c01, PDF 457–473. В журнале сохраняются исходные расхождения, ограничения опыта и непроверенные утверждения, **без исправлений по внешним источникам или памяти**. Неизвестное — **[Needs confirmation]**.

## F-01 — [Source contradiction] — Namespace DaemonSet и команды

- **p0463:** единый `fluentd-daemonset.yaml` создаёт `Namespace logging`, но DaemonSet явно содержит `metadata.namespace: kube-system`.
- **p0465:** результат `kubectl apply` сообщает `namespace/logging created`, `daemonset.apps/fluentd-elasticsearch created`; далее `kubectl describe daemonset fluentd-elasticsearch -n logging` и `kubectl get po -n logging -o wide` показывают три Pod.
- **p0468–p0469:** `rollout status`, `describe ds`, `rollout undo` и обе команды удаления снова адресуют `logging`.
- **Boundary:** без отсутствующего изменения namespace YAML не обосновывает показанные Pod и управляющие команды. Исправленную версию **не** придумывать. Этот пример нельзя выдавать за воспроизводимый end-to-end runbook; **[Needs confirmation]**.

## F-02 — [Needs confirmation] — абсолютное «один Pod на каждом узле»

- **p0457–p0458:** объект гарантирует Pod на каждом узле.
- **p0459–p0460, p0464, p0468:** оговорено соответствие nodeSelector, affinity, tolerations, labels и конкретным условиям узлов.
- **Boundary:** только подходящие узлы могут получить Pod; actual eligibility и resource constraints не проверены.

## F-03 — [Needs confirmation] — scheduler «вытесняет существующие Pod» при нехватке ресурсов

- **p0460:** стандартный scheduler описан как привязывающий Pod к выбранному узлу и «вытесняющий существующие поды при нехватке ресурсов».
- **p0466–p0467:** отдельно описаны PriorityClass и возможность вытеснения.
- **Boundary:** автоматическое вытеснение по одному факту DaemonSet не доказано; класс приоритета, политика, текущая загрузка и фактическое scheduling **[Needs confirmation]**.

## F-04 — [Needs confirmation] — абсолютная неуязвимость system-node-critical

- **p0467:** `system-node-critical` заявлен как гарантия, что Pod «не будут выселены ни при каких обстоятельствах».
- **Boundary:** source не тестирует падение узла, eviction, shutdown, конфликт ресурсов или системных условий. Не объявлять абсолютную невозможность остановки системного Pod. **[Needs confirmation]**.

## F-05 — [Source scope] — Fluentd Running ≠ доставка логов

- **p0463–p0465:** Fluentd получает `hostPath: /var/log`, env `FLUENT_ELASTICSEARCH_HOST=elasticsearch-logging`, PORT=9200; автор говорит, что настройку Elasticsearch не разбирает.
- **p0465:** подтверждены только запущенные Pod на трёх узлах и файлы внутри каталога `/var/log`.
- **Boundary:** работающий агрегатор, передача записей, парсинг/доставка, безопасность и ретенция логов **не доказаны**.

## F-06 — [Source wording/code mismatch] — внутри шаблона Namespace и подсистемные компоненты

- **p0461–p0462:** `calico-node` и `kube-proxy` показаны в `kube-system`; `calico-kube-controllers` не является одним из Pod `calico-node` DaemonSet.
- **Boundary:** фильтр `grep calico` включает **разные типы контроллеров**; нельзя принять все совпавшие строки за одинаковые Pod DaemonSet.

## F-07 — [Needs confirmation] — одинаковые права на узловой каталог

- **p0464:** Fluentd использует `hostPath` всего `/var/log` без явного `readOnly`, AppArmor/Seccomp/контекста доступа; `resource.requests.cpu: 100m`, память 200Mi.
- **Boundary:** доступ к системным логам требует threat model, минимизации привилегий и верификации реальных прав; пример не готов для production. **[Needs confirmation]**.

## F-08 — [Source wording/code mismatch] — manifest labels и service selection

- **p0463:** метка DaemonSet `metadata.labels.k8s-app: fluentd-logging`, selector/template `name: fluentd-elasticsearch`.
- **p0459–p0460, p0462:** рекомендуются headless/обычный Services, но полный Fluentd Service YAML в chapter RAG не показан.
- **Boundary:** нельзя подменять селектор Pod метками самого DaemonSet; подтверждённая публикация Fluentd через Service **[Needs confirmation]**.

## F-09 — [Needs confirmation] — настройка PriorityClass и безопасность приоритета

- **p0466:** `fluentd-priority` со значением 100000, `globalDefault:false`.
- **p0472:** best practice «например 10000», но в chapter нет выполнения `apply priorityclass` и наблюдений preemption.
- **Boundary:** значения иллюстративны, влияние на другие workload и возможность вытеснения не измерены. **[Needs confirmation]**.

## F-10 — [Source wording/code mismatch] — RollingUpdate как один Running Pod на узел

- **p0467:** заявлено, что в ходе RollingUpdate на любом узле не более одного Running Pod DaemonSet; описаны `maxUnavailable` default 1 и `minReadySeconds` default 0.
- **p0468:** один пример обновления v4.7→v4.7.5, но не показаны все допустимые поля стратегии или варианты конфигурации.
- **Boundary:** гарантия относится к **описанному source сценарию**, не доказывает поведение всех реализаций/параметров. **[Needs confirmation]**.

## F-11 — [Source extraction issue] — образ в императивной команде

- **p0467–p0468:** корректный image в YAML `quay.io/fluentd_elasticsearch/fluentd:v4.7.5`, но в извлечённой inline `kubectl set image` строке есть разрыв/пробел внутри имени репозитория `fluentd_ elasticsearch`.
- **Boundary:** не заявлять эту строку исполняемой без сверки; в каталоге команд сохранена точная source-compatible YAML-версия, не предполагалась проверенная CLI-коррекция.

## F-12 — [Needs confirmation] — rollback и orphan deletion

- **p0469:** `kubectl rollout undo daemonset fluentd-elasticsearch -n logging`, cascade deletion и `--cascade=orphan`.
- **Boundary:** команды не адресуют объявленный `kube-system` DaemonSet; не показаны возврат к прежней доставке логов, история ревизий и восстановление удалённых Pod в конкретном namespace. **[Needs confirmation]**.

## F-13 — [Needs confirmation] — drain узла

- **p0469:** `kubectl drain` требует флаг `--ignore-daemonsets` при наличии DaemonSet Pod, но полного безопасного сценария `drain` + обратного возврата node нет.
- **Boundary:** не применять как готовый runbook node maintenance; возможна деградация workload и сетевой инфраструктуры.

## F-14 — [Source scope] — платформенные примеры и версии

- **p0460:** minikube VirtualBox, Calico, Kubernetes v1.31.0.
- **p0470–p0471:** упоминаются AKS, Flannel, Ceph, Nginx Ingress, Fluentd, node-exporter и ссылки на внешние manifests.
- **Boundary:** текущая совместимость/поддержка API/проектов не проверялась; чужие репозитории не читались в режиме `rag_only`. Ссылки являются частью источника, но не проверенным подтверждением новых свойств.

## F-15 — [Needs confirmation] — альтернативы и best practices

- **p0471:** `preferredDuringSchedulingIgnoredDuringExecution` назван более предпочтительным, чем `requiredDuringSchedulingIgnoredDuringExecution`, ради гибкости, но source не показывает YAML для сравнения.
- **p0472:** sidecar объявлен «как правило, проще и надёжнее» DaemonSet для логов; CronJob, systemd и static Pod представлены как альтернативы.
- **Boundary:** пригодность зависит от требований per-node, overhead, security и отказоустойчивости. Глава не содержит сравнительного эксперимента. **[Needs confirmation]**.

## F-16 — [Needs confirmation] — RestartPolicy и готовность

- **p0472:** `restartPolicy: Always` предлагается как рекомендация, вместе с высоким приоритетом и `minReadySeconds`.
- **Boundary:** успех перезапуска контейнера и достижение функциональной готовности/доступности при сбоях узла не продемонстрированы; реальные liveness/readiness и SLO **[Needs confirmation]**.

**Operational boundary:** никакие live-команды не выполнялись, PDF/LFS, RAG/registry и статус чтения не изменялись.
