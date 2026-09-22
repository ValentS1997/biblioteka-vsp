# Диаграмма: проектирование и отладка сетевой инфраструктуры

~~~mermaid
flowchart TD
    A["Requirements / expected traffic"] --> B["Choose medium"]
    B --> B1["UTP"]
    B --> B2["Fiber"]
    B --> B3["Wireless"]

    B1 --> C["Physical topology"]
    B2 --> C
    B3 --> C

    C --> D["Switching / WAP access"]
    D --> E["Logical segmentation"]
    E --> E1["Broadcast domains"]
    E --> E2["VLAN / SSID mapping"]
    E1 --> F["Routing boundary"]
    E2 --> F

    F --> G["Operational constraints"]
    G --> G1["Autonegotiation consistency"]
    G --> G2["MTU consistency"]
    G --> G3["PoE budget"]
    G --> G4["Wireless channel / coverage"]
    G --> G5["Filtering / security"]

    G1 --> H["Install / configure"]
    G2 --> H
    G3 --> H
    G4 --> H
    G5 --> H

    H --> I["Test physical segment"]
    I --> J{"Physical fault?"}
    J -->|Yes| K["Cable/termination/power repair"]
    K --> I
    J -->|No| L["Inspect packet behavior"]

    L --> M{"Logical fault?"}
    M -->|Yes| N["Change one logical variable"]
    N --> O["Verify same segment"]
    O --> L
    M -->|No| P["End-to-end verification"]

    P --> Q{"Acceptance passed?"}
    Q -->|No| R["Rollback / [Needs confirmation]"]
    R --> I
    Q -->|Yes| S["Document topology, labels, ownership"]
    S --> T["Operate / monitor / plan growth"]

    U["High-risk anti-patterns"] --> U1["uncontrolled switch loop"]
    U --> U2["VLAN treated as security boundary"]
    U --> U3["one-sided speed/duplex setting"]
    U --> U4["partial jumbo-frame rollout"]
    U --> U5["weak wireless security"]
    U1 --> R
    U2 --> R
    U3 --> R
    U4 --> R
    U5 --> R
~~~

## Смысл диаграммы

Глава 14 строит сеть как совокупность физических и логических слоев. Кабельный тестер отвечает на вопросы physical layer, packet analyzer — на вопросы frame/protocol layer. Любое изменение должно быть локализовано по segment/fault domain, проверено на месте, затем end-to-end и только после этого закреплено в документации.
