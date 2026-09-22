# Диаграмма: IP routing — forwarding, control plane и safe change

~~~mermaid
flowchart TD
    A["Packet destination"] --> B["Routing-table lookup"]
    B --> C{"Connected network?"}
    C -->|Yes| D["Send directly"]
    C -->|No| E{"Specific route?"}
    E -->|Yes| F["Use route next hop/interface"]
    E -->|No| G{"Default route?"}
    G -->|Yes| H["Use default gateway"]
    G -->|No| I["Destination unreachable"]

    D --> J["Link-layer forwarding"]
    F --> J
    H --> J

    K["Control plane"] --> K1["Config files"]
    K --> K2["Kernel routing table"]
    K --> K3["Peer updates"]
    K1 --> L["Routing daemon/protocol"]
    K2 --> L
    K3 --> L

    L --> M{"Protocol model"}
    M -->|Distance-vector| N["RIP / RIPng / EIGRP family"]
    M -->|Link-state| O["OSPF"]
    M -->|Exterior| P["BGP"]

    N --> Q["Calculate preferred routes"]
    O --> Q
    P --> Q
    Q --> R["Install routes into kernel"]
    R --> S["Advertise when protocol requires"]

    T["Need routing change"] --> U["Read-only baseline"]
    U --> U1["netstat -rn / ip route"]
    U --> U2["show interfaces"]
    U --> U3["show running / show config"]
    U1 --> V["Identify route source and expected next hop"]
    U2 --> V
    U3 --> V

    V --> W{"Static or dynamic?"}
    W -->|Static| X["Change one route/config item"]
    W -->|Dynamic| Y["Change daemon/protocol config"]

    X --> Z["Verify routing table + end-to-end path"]
    Y --> Z
    Z --> AA{"Acceptance passed?"}
    AA -->|Yes| AB["Persist config / write mem / write"]
    AA -->|No| AC["Rollback from captured config"]
    AC --> U

    AD["High-risk boundary"] --> AD1["wrong router"]
    AD --> AD2["management interface change"]
    AD --> AD3["unverified config persisted"]
    AD --> AD4["dynamic protocol where static route is enough"]
    AD1 --> AC
    AD2 --> AC
    AD3 --> AC
    AD4 --> AC
~~~

## Смысл диаграммы

Глава разделяет data plane и control plane. Packet forwarding использует уже существующую route table; routing daemon/protocol вычисляет и обновляет эту table. Safe change начинается с inspection, меняет одну часть control plane, проверяет resulting route/path и только затем сохраняет configuration.
