# Диаграмма: IP routing — forwarding, control plane и source-supported operations

~~~mermaid
flowchart TD
    A["Packet destination"] --> B["Routing-table lookup"]
    B --> C{"Directly connected network?"}
    C -->|Yes| D["Send directly"]
    C -->|No| E{"Specific route?"}
    E -->|Yes| F["Use route gateway/interface"]
    E -->|No| G{"Default route?"}
    G -->|Yes| H["Use default gateway"]
    G -->|No| I["No matching route"]

    D --> J["Link-layer forwarding"]
    F --> J
    H --> J

    K["Routing/control plane"] --> K1["Configuration files"]
    K --> K2["Existing routing table"]
    K --> K3["Peer daemons"]
    K1 --> L["Routing daemon"]
    K2 --> L
    K3 --> L
    L --> M{"Protocol family"}
    M -->|Distance-vector| N["RIP / RIPng / EIGRP"]
    M -->|Link-state| O["OSPF"]
    M -->|Exterior| P["BGP"]
    N --> Q["Compute routes"]
    O --> Q
    P --> Q
    Q --> R["Write routes to kernel table"]
    R --> S["Advertise when required"]

    T["Route/config inspection"] --> T1["netstat -rn / ip route"]
    T --> T2["show interfaces"]
    T --> T3["show running / show config"]

    U["Quagga"] --> U1["vtysh / quaggaadm"]
    U1 --> U2["enable"]
    U2 --> U3["config term"]
    U3 --> U4["configuration commands"]
    U4 --> U5["write"]

    V["Cisco IOS example"] --> V1["ssh router"]
    V1 --> V2["show ..."]
    V2 --> V3["enable"]
    V3 --> V4["config term"]
    V4 --> V5["interface / ip address"]
    V5 --> V6["Ctrl+Z"]
    V6 --> V7{"Change succeeded?"}
    V7 -->|Yes| V8["write mem"]
    V7 -->|No| V9["Exact rollback: [Needs confirmation]"]

    W["Configuration protection"] --> W1["hostname reduces wrong-router mistakes"]
    W --> W2["backup with scp / tftp"]
    W --> W3["SSH instead of Telnet"]
    W --> W4["RANCID: retrieve → compare → version control"]
~~~

## Смысл диаграммы

Глава разделяет перенаправление пакетов и вычисление/поддержание маршрутов. Forwarding использует существующую таблицу; routing daemons строят и обновляют ее. Для Cisco источник показывает inspection-команды, переход в режим конфигурации и сохранение через `write mem` только после успешного изменения. Полный acceptance-test и rollback procedure в доступном RAG не заданы: `[Needs confirmation]`.
