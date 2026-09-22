# Диаграмма: логика главы 5

```mermaid
flowchart TD
    start["Пакет должен пройти от source к destination через сеть"] --> service{"Service model?"}

    service --> datagram["Datagram: каждый пакет маршрутизируется независимо"]
    service --> vc["Virtual circuit: путь и state создаются при установлении"]

    datagram --> routing["Routing: построить путь/таблицу"]
    vc --> routing

    routing --> intra{"Scope маршрутизации"}
    intra -->|Внутри сети| algorithms["Shortest path / flooding / distance vector / link state / hierarchy"]
    intra -->|Между AS| interdomain["Interdomain policy / BGP"]

    algorithms --> forwarding["Forwarding: выбрать next hop для конкретного пакета"]
    interdomain --> forwarding

    forwarding --> traffic{"Есть congestion / QoS requirements?"}
    traffic -->|Congestion| congestion["Traffic-aware routing / admission / feedback / throttling / load shedding"]
    traffic -->|QoS| qos["Shaping / scheduling / reservation / differentiated treatment"]
    traffic -->|Нет| internetwork["Internetworking"]

    congestion --> internetwork
    qos --> internetwork

    internetwork --> hetero{"Различаются сети/MTU?"}
    hetero -->|Да| adaptation["Path MTU / fragmentation / tunneling"]
    hetero -->|Нет| internet["Internet network layer"]

    adaptation --> internet
    internet --> ip["IPv4/IPv6 + prefixes/CIDR"]
    internet --> control["ICMP / ARP / DHCP / MPLS"]
    internet --> protocols["OSPF / BGP / multicast"]

    start --> sdn["SDN: controller/control plane ↔ programmable forwarding plane"]
    sdn --> forwarding

    start --> observe["Read-only/workload observation: traceroute / tracert"]
```

Диаграмма разделяет service model, route computation, packet forwarding, traffic management, internetworking и конкретные интернет-протоколы, как это делает сама глава.
