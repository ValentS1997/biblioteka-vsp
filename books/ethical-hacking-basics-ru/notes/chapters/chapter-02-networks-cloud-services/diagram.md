# Diagram — глава 2

Все Mermaid-схемы основаны на PDF pp. 15–42. Это концептуальная модель, **не фактическая схема сети читателя**.

## Модели OSI и TCP/IP

```mermaid
flowchart LR
  subgraph OSI["OSI · 7 уровней"]
    O7["L7 Прикладной"]
    O6["L6 Представления"]
    O5["L5 Сеансовый"]
    O4["L4 Транспортный"]
    O3["L3 Сетевой"]
    O2["L2 Канальный"]
    O1["L1 Физический"]
  end
  subgraph TCPIP["TCP/IP · 4 уровня"]
    T4["Application"]
    T3["Transport"]
    T2["Internet"]
    T1["Link"]
  end
  O7 --> T4
  O6 --> T4
  O5 --> T4
  O4 --> T3
  O3 --> T2
  O2 --> T1
  O1 --> T1
```

RAG: `p0016:c01`–`p0019:c01`.

## Адресация и транспорт

```mermaid
flowchart TD
  D["Сообщение приложения"] --> P["L4: порт, TCP segment / UDP datagram"]
  P --> N["L3: адрес IP, маршрутизация, IP packet"]
  N --> L["L2: MAC, Ethernet frame, switch"]
  L --> F["L1: физическая передача"]
  S["ICMP: сообщения состояния/ошибок"] -.-> N
  P --> C["TCP: подтверждения, повторы, порядок"]
  P --> U["UDP: нет гарантии доставки"]
```

RAG: `p0017:c01`, `p0022:c01`, `p0024:c01`, `p0029:c01`–`p0033:c01`. О степени надёжности IP имеется [Source contradiction] между p24 и p42; см. `source-findings.md`.

## Архитектурные границы и облако

```mermaid
flowchart TD
  E["Внешняя сеть"] --> D["DMZ: внешние сервисы"]
  D --> F["Firewall / ACL boundary"]
  F --> I["Внутренние сегменты: VLAN / server / desktop"]
  I --> K["Enclave / microsegmentation: чувствительная workload"]
  R["Удалённый доступ: VPN, IPsec, TLS"] --> F
  E --> CL["Cloud: StaaS / IaaS / PaaS / SaaS"]
  CL --> SG["Клиентские access/security rules"]
  SG --> V["VM / приложения / хранилище"]
  CL --> H["IoT hub / HTTP / MQTT"]
```

Стрелки показывают **логическую группировку понятий источника**, а не фактические разрешения трафика между зонами. Нет real-world конфигурации и критериев пересылки: [Needs confirmation]. RAG: `p0033:c01`–`p0041:c01`.
