# Итог главы 5

## Заключение

Глава 5 рассматривает Docker Swarm как встроенную систему orchestration и high availability для Docker Engine cluster.

Ключевая идея — desired state. Service описывает требуемое состояние приложения, а manager/scheduler размещает tasks и поддерживает их количество/состояние. При отказе worker replacement task создаётся на другом доступном node. Scaling выполняется изменением desired replica count.

Cluster делится на manager и worker nodes. Один manager является Leader. Для согласования cluster state глава описывает Raft consensus и quorum. Рекомендуется нечётное количество managers, обычно 3 или 5; source приводит формулу допустимой потери `(N-1)/2` manager nodes. При split-brain/quorum loss существующие tasks могут продолжать работу, но scheduling/reconciliation нарушается.

Service содержит image, commands, network/port/resource settings и режим исполнения. Task/replica — единичное выполнение service в container. Replicated mode создаёт указанное количество replicas. Global mode создаёт по одной task на каждом eligible node и автоматически добавляет task на новом node.

Для planned maintenance используется DRAIN: node перестаёт принимать новые Swarm tasks, а существующие service tasks пересоздаются на других ACTIVE nodes. Возврат node в ACTIVE разрешает новые tasks, но ранее перемещённые tasks автоматически назад не возвращаются.

Autolock защищает encrypted Raft logs. После включения autolock Docker генерирует unlock key; после manager restart Swarm остаётся locked, пока operator не выполнит `docker swarm unlock` и не предоставит key.

Swarm networking использует `docker_gwbridge` и default overlay `ingress`. Можно создавать custom overlay networks и привязывать к ним services. Published ports проходят через routing mesh. При использовании external load balancer source предлагает endpoint mode DNSRR для обхода routing mesh. Overlay application traffic можно дополнительно шифровать с помощью `--opt encrypted`, учитывая performance overhead.

Troubleshooting direction в конце главы — сначала смотреть service logs, используя follow/tail, если logging driver поддерживает соответствующие operations.

## Основные тезисы источника

- Swarm — native Docker orchestration/HA mechanism.
- Desired state автоматически reconciled managers.
- Managers orchestrate; workers execute tasks.
- Service — desired state; task/replica — единица исполнения.
- Cluster state decisions требуют consensus/quorum.
- Replicas легко scale up/down.
- Global service размещает task на каждом eligible node.
- DRAIN evacuates Swarm service tasks from node.
- Autolock protects manager state after restart.
- Swarm creates default bridge/overlay networking objects.
- Routing mesh distributes published service traffic.
- Overlay application traffic can be encrypted.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| Docker Swarm | Built-in cluster orchestration mode |
| Manager | Node, управляющий cluster state/orchestration |
| Worker | Node, исполняющий assigned tasks |
| Leader | Active manager receiving/processing cluster changes |
| Service | Description of desired application state |
| Task | One scheduled execution of a service |
| Replica | Task instance в replicated/global discussion |
| Desired state | Требуемое состояние, поддерживаемое scheduler |
| Raft consensus | Consensus algorithm named by source |
| Quorum | Majority required for cluster decisions |
| DRAIN | Node availability mode that evacuates Swarm tasks |
| ACTIVE | Node may receive and execute tasks |
| Autolock | Manager lock after restart requiring unlock key |
| ingress | Default Swarm overlay network |
| docker_gwbridge | Bridge used for cluster containers to external connectivity |
| Routing mesh | Built-in request distribution path for published services |
| DNSRR | Endpoint mode used with external load balancing |
| Published port | Exposed service port |
| Overlay encryption | Additional encrypted data plane option |

## Source-specific caveat

Source states both that cluster metadata is stored in distributed `etcd` on managers and that Swarm consensus/log protection uses Raft. This artifact does not silently reconcile those statements with external knowledge.

## Provenance

- Chapter RAG: `p0088:c01`–`p0113:c01` + `p0096:c02`
- PDF pages: 88–113
- Printed pages: 93–118
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
