# Итог главы 4

## Заключение

Глава 4 объясняет сетевую архитектуру Docker через Container Network Model и базовые Linux networking primitives.

CNM состоит из sandbox, endpoint и network. Sandbox содержит полный сетевой стек container. Endpoint связывает sandbox с network. Network обеспечивает среду связи между endpoints.

Libnetwork описывается как реализация CNM и библиотека для создания и управления network stacks. Network drivers предоставляют конкретную реализацию сети; IPAM drivers назначают subnets/IP addresses. Источник различает built-in и third-party drivers.

Встроенные drivers главы: bridge, host, none, overlay и MACVLAN. Bridge основан на Linux bridge. Host использует network host. None оставляет container без внешнего connectivity. Overlay предназначен для multi-host networking и в изложении главы использует Linux bridge + VXLAN. MACVLAN использует Linux MACVLAN bridge.

Практический блок строится на Linux network namespaces. Namespace — isolated network stack. veth pair соединяет два namespaces как full-duplex virtual Ethernet channel. Глава создаёт два namespaces, помещает по одному концу veth в каждый, назначает IP addresses, поднимает interfaces и подтверждает reachability через ping.

Point-to-point veth architecture плохо масштабируется при большом количестве namespaces. Linux bridge выступает как L2 virtual switch: каждый namespace подключается к bridge через собственную veth pair.

Docker использует эту модель в default bridge. На host автоматически появляется `docker0`. Container-side interface называется `eth0`; host-side end veth подключён к `docker0`. IP address container назначает встроенный Docker IPAM.

## Основные тезисы источника

- Docker networking architecture базируется на CNM.
- Libnetwork — реализация CNM.
- Network drivers обеспечивают работу Docker networks.
- Network namespaces изолируют container networks.
- Linux bridge — Layer-2 virtual switching mechanism.
- veth pair соединяет namespaces либо namespace/container с bridge.
- Default Docker bridge `docker0` базируется на Linux bridge.
- Containers, подключённые к `docker0`, могут взаимодействовать через bridge.
- IPAM driver отвечает за address allocation.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| CNM | Абстрактная Docker network architecture |
| Sandbox | Изолированный network stack container |
| Endpoint | Connection point sandbox ↔ network |
| Network | Среда связи endpoints |
| Libnetwork | Реализация CNM / network stack management library |
| Network driver | Конкретная network implementation |
| IPAM | IP address/subnet management |
| Network namespace | Изолированный экземпляр Linux network stack |
| veth | Virtual Ethernet pair |
| Linux bridge | Layer-2 virtual switch in kernel |
| docker0 | Default Docker bridge on host |
| bridge driver | Docker driver based on Linux bridge |
| overlay driver | Multi-host network driver по описанию источника |
| MACVLAN | Driver based on Linux MACVLAN |

## Provenance

- Chapter RAG: `p0076:c01`–`p0087:c01`
- PDF pages: 76–87
- Printed pages: 81–92
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
