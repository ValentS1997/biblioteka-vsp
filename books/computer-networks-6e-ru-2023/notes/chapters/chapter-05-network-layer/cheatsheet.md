# Шпаргалка: сетевой уровень

## Goal / symptom

Использовать главу 5, когда вопрос относится к доставке пакета через несколько маршрутизаторов или к управлению сетевым уровнем:

- какой путь выбран до адресата;
- почему маршруты меняются;
- как routing protocol масштабируется;
- где возникает congestion;
- как обеспечиваются QoS/QoE;
- как соединяются неоднородные сети;
- как работает IP addressing/CIDR/subnetting;
- какую роль играют ICMP, ARP, DHCP, MPLS, OSPF или BGP;
- как SDN отделяет control logic от packet forwarding;
- как политика влияет на interdomain routing.

Конкретный сценарий: [Needs confirmation].

## Baseline / context

| Параметр | Значение |
|---|---|
| Source / destination | [Needs confirmation] |
| Datagram или virtual-circuit model | [Needs confirmation] |
| Routing scope: intra-network / interdomain | [Needs confirmation] |
| Routing protocol / algorithm | [Needs confirmation] |
| Address family: IPv4 / IPv6 | [Needs confirmation] |
| Prefix / subnet / mask | [Needs confirmation] |
| Path MTU | [Needs confirmation] |
| Observed delay / queueing / loss | [Needs confirmation] |
| QoS requirement | [Needs confirmation] |
| Administrative domains / AS | [Needs confirmation] |

## Read-only checks

### 1. Разделить forwarding и routing

Forwarding — локальное решение маршрутизатора о том, куда отправить конкретный пакет.

Routing — механизм построения/обновления путей и таблиц, на основании которых происходит forwarding.

Не смешивать эти задачи при диагностике.

### 2. Определить service model

Для datagram network:

- путь может выбираться независимо для каждого пакета;
- маршрутизаторы не обязаны хранить состояние отдельного соединения.

Для virtual circuit:

- маршрут выбирается при установлении соединения;
- маршрутизаторы хранят состояние канала;
- последующие пакеты используют идентификатор виртуального канала.

### 3. Классифицировать routing algorithm

Глава рассматривает:

- shortest path;
- flooding;
- distance vector;
- link state;
- hierarchical routing;
- routing for mobile hosts;
- broadcast;
- multicast;
- anycast.

### 4. Проверить путь с traceroute / tracert

Подтвержденные source commands:

```text
traceroute <destination>
tracert <destination>
```

Сопоставить последовательность hops с ожидаемой межсетевой структурой. Не делать выводов о внутренней причине выбора каждого hop, если RAG/наблюдение этого не подтверждают.

### 5. При задержке и потерях проверить congestion model

Глава связывает congestion с ростом нагрузки, очередей, задержки и loss.

Механизмы управления включают:

- traffic-aware routing;
- admission control;
- feedback;
- throttling;
- load shedding.

Не подменять congestion flow control: это разные проблемы.

### 6. Для QoS/QoE

Проверить, какие свойства важны приложению:

- throughput;
- delay;
- jitter;
- loss.

Глава рассматривает shaping, scheduling, reservation, admission control, integrated/differentiated service.

### 7. Для internetworking

Проверить:

- различается ли MTU;
- нужен ли Path MTU;
- возникает ли fragmentation;
- используется ли tunneling для прохождения через отличающуюся сеть.

### 8. Для SDN

Разделить:

- control plane / controller logic;
- forwarding/data plane;
- southbound mechanism (в главе обсуждаются OpenFlow, NETCONF и YANG);
- programmable forwarding pipeline;
- telemetry.

### 9. Для IP

Проверить:

- IPv4 или IPv6;
- network prefix и CIDR;
- subnetting;
- longest-prefix style routing context;
- роль ICMP, ARP и DHCP;
- intra-domain routing (OSPF);
- interdomain routing (BGP);
- требуется ли MPLS или multicast context.

## Interpretation

- Datagram и virtual-circuit networks делают разные trade-offs между setup, state, failure behavior и QoS.
- Distance-vector и link-state — основные семейства адаптивной внутрисетевой маршрутизации, выделенные в резюме главы.
- Hierarchical routing уменьшает объем информации в крупных сетях ценой менее детального знания удаленной топологии.
- Congestion control защищает сеть от чрезмерной нагрузки; flow control защищает получателя от слишком быстрого отправителя.
- QoS требует не только выбора маршрута, но и управления очередями, admission/resources и обработкой разных классов трафика.
- Fragmentation и Path MTU относятся к различиям в допустимом размере пакетов между сетями.
- BGP route choice определяется не только технической длиной пути, но и политикой автономной системы.
- SDN делает network control более программируемым, но не отменяет базовые задачи forwarding/routing.

## Next action

- L2 framing, retransmission, bridge/VLAN и MAC access → главы 3–4.
- End-to-end process transport, TCP/UDP и transport reliability → глава 6.
- Application protocols → глава 7.
- Если проблема остается на L3, уточнить routing scope, protocol, prefix/path и observed behavior.

## Modifying action

[Not applicable]

Глава не задает универсальной operational-команды для изменения route, OSPF/BGP, QoS или SDN state.

## Verification / acceptance checks

Анализ согласован с главой, когда:

- forwarding и routing различены;
- service model определена;
- routing scope и algorithm/protocol установлены;
- при congestion не смешиваются network congestion и receiver flow control;
- IP prefix/subnet/MTU факты основаны на реальных параметрах;
- traceroute/tracert рассматривается как наблюдение пути, а не доказательство внутренней политики каждого маршрутизатора;
- BGP policy и intra-domain routing не смешиваются;
- при SDN различены control plane и forwarding plane.

## Rollback

[Not applicable]

Подтвержденных modifying actions в canonical operational форме глава не задает.
