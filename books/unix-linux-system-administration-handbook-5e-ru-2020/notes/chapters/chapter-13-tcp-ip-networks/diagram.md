# Диаграмма: TCP/IP troubleshooting и controlled change

~~~mermaid
flowchart TD
    A["Need connectivity / network change"] --> B["Read-only baseline"]

    B --> B1["Link/interface<br/>ip link / ifconfig / ethtool"]
    B1 --> B2["Address/prefix<br/>ip address / ipcalc"]
    B2 --> B3["Neighbor resolution<br/>ip neigh / ARP / ND"]
    B3 --> B4["Routing<br/>ip route / netstat -rn"]
    B4 --> B5["Policy<br/>sysctl / firewall / NAT"]
    B5 --> B6["End-to-end probes<br/>ping / traceroute"]
    B6 --> B7["Packet evidence<br/>tcpdump / Wireshark"]
    B7 --> B8["Application-specific check"]

    B8 --> C{"Change required?"}
    C -->|No| D["Document verified state"]
    C -->|Yes| E{"Which layer?"}

    E -->|Link| F["speed/duplex/MTU"]
    E -->|Address| G["IP/prefix/interface config"]
    E -->|Route| H["specific/default route"]
    E -->|Kernel policy| I["sysctl"]
    E -->|Firewall/NAT| J["ordered rule change"]
    E -->|Cloud network| K["VPC/subnet/route/policy via IaC"]

    F --> L["Apply one controlled change"]
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L

    L --> M["Re-check same layer"]
    M --> N["Re-run end-to-end checks"]
    N --> O{"Acceptance passed?"}

    O -->|Yes| P["Persist / version-control / reboot or reload verify"]
    O -->|No| Q["Rollback to captured state / recovery path"]
    Q --> R["Collect packet/state evidence"]
    R --> B

    S["High-risk boundaries"] --> S1["route flush"]
    S --> S2["ifdown / network restart"]
    S --> S3["default-deny firewall"]
    S --> S4["remote interface change"]
    S --> S5["terraform destroy"]
    S1 --> Q
    S2 --> Q
    S3 --> Q
    S4 --> Q
    S5 --> Q
~~~

## Смысл диаграммы

Глава 13 дает послойную operational model: link → address → neighbor → route → policy → probe → packet evidence → application. Изменение допустимо только после локализации слоя. Для remote/high-risk actions recovery path должен существовать до выполнения команды.
