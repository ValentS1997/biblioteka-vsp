# Диаграмма: сеть и ее конфигурация по главе 9

## Сетевые уровни

~~~mermaid
flowchart TB
    APP["Application / name resolution"] --> TRANSPORT["Transport: TCP / UDP"]
    TRANSPORT --> IP["Network layer: IPv4 / IPv6"]
    IP --> LINK["Link / physical: Ethernet / Wi-Fi"]
    LINK --> HW["Network interface / hardware"]
~~~

## Troubleshooting flow

~~~mermaid
flowchart TD
    S["Network symptom"] --> I["Interface exists and is UP?"]
    I -->|No| L["Link / interface layer"]
    I -->|Yes| A["Expected address + prefix present?"]
    A -->|No| CFG["DHCP / NetworkManager / manual address config"]
    A -->|Yes| R["Route/default gateway present?"]
    R -->|No| RT["Routing configuration"]
    R -->|Yes| N["Neighbor resolution works?"]
    N -->|No| ARP["ARP / NDP / local-link issue"]
    N -->|Yes| D["Name resolution needed?"]
    D -->|Yes| DNS["nsswitch → hosts → resolver/DNS"]
    D -->|No| T["TCP/UDP endpoint"]
    DNS --> T
    T --> P["Application/service layer"]
~~~

## Route decision

~~~mermaid
flowchart TD
    PKT["Destination IP"] --> MATCH["Find matching routes"]
    MATCH --> SPEC["Choose matching network/prefix"]
    SPEC --> Q{"Specific route exists?"}
    Q -->|Yes| SR["Use specific next hop/interface"]
    Q -->|No| DR["Use default route"]
    DR --> GW["Default gateway"]
~~~

## Name resolution

~~~mermaid
flowchart LR
    APP["Application resolver call"] --> NSS["/etc/nsswitch.conf"]
    NSS --> HOSTS["/etc/hosts"]
    NSS --> DNS["DNS resolver path"]
    DNS --> RESOLVED["systemd-resolved / cache when used"]
    RESOLVED --> NS["Configured name server"]
~~~

## TCP listener model

~~~mermaid
flowchart LR
    CLIENT["Client<br/>ephemeral local port"] --> CONN["TCP connection"]
    CONN --> SERVER["Server<br/>listening port"]
    VIEW["netstat -nt / -ntl"] --> CLIENT
    VIEW --> SERVER
~~~

## Linux router + NAT

~~~mermaid
flowchart LR
    LAN["Private LAN"] --> IN["Internal interface"]
    IN --> FW["FORWARD policy/rules"]
    FW --> FWD["IP forwarding"]
    FWD --> NAT["POSTROUTING MASQUERADE"]
    NAT --> OUT["External interface"]
    OUT --> NET["External network"]
~~~

## Firewall first-match semantics

~~~mermaid
flowchart TD
    P["Incoming packet"] --> R1["Rule 1"]
    R1 -->|match| A1["Apply target and stop"]
    R1 -->|no match| R2["Rule 2"]
    R2 -->|match| A2["Apply target and stop"]
    R2 -->|no match| RN["..."]
    RN --> DEF["Default chain policy"]
~~~

## ARP / NDP local-link role

~~~mermaid
flowchart LR
    IP4["IPv4 destination on local link"] --> ARP["ARP"]
    ARP --> MAC4["MAC address"]
    IP6["IPv6 neighbor on local link"] --> NDP["NDP"]
    NDP --> MAC6["Link-layer neighbor information"]
    REMOTE["Remote destination"] --> GW["Resolve next-hop router on local link"]
~~~

## Wi-Fi configuration layers

~~~mermaid
flowchart TB
    SCAN["iw scan"] --> ASSOC["Wireless association"]
    ASSOC --> AUTH["wpa_supplicant for WPA2/WPA3"]
    AUTH --> IP["IP address / routes"]
    IP --> DNS["Name resolution"]
    NM["NetworkManager"] --> ASSOC
    NM --> IP
    NM --> DNS
~~~
