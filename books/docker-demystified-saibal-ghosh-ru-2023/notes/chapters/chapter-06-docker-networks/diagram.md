# Диаграммы: Docker networks

## Default bridge

```mermaid
flowchart LR
    C["Container
eth0 172.17.0.x"] <-->|veth| V["Host veth"]
    V <--> B["docker0
Linux bridge"]
    B <--> H["Host NIC"]
    H <--> E["External network"]
```

## User-defined bridge

```mermaid
flowchart TB
    C1["mybox3"] --> B["mybridge"]
    C2["mybox4"] --> B
    B --> DNS["Name-based discovery
shown by source"]
```

## Host / None

```mermaid
flowchart LR
    HC["Host-network container"] --> H["Host network namespace"]
    NC["None-network container"] --> LO["Isolated stack / loopback"]
```

## Port mapping / NAT

```mermaid
flowchart LR
    EXT["External client"] --> HP["Host :8080"]
    HP --> NAT["netfilter / NAT"]
    NAT --> CP["Container :80"]
    C["Container outbound"] --> MASQ["POSTROUTING MASQUERADE"]
    MASQ --> H["Host external IP"]
```

## MACVLAN

```mermaid
flowchart TB
    NIC["Host parent eth0"] --> M1["MACVLAN endpoint A"]
    NIC --> M2["MACVLAN endpoint B"]
    M1 --> P["Physical network"]
    M2 --> P
```

## MACVLAN trunk

```mermaid
flowchart LR
    NIC["eth1"] --> SUB["eth1.50
802.1Q subinterface"]
    SUB --> MV["MACVLAN network"]
    MV --> C["Container"]
```

## Overlay container interfaces

```mermaid
flowchart TB
    C["Container"] --> E0["eth0
overlay IP"]
    C --> E1["eth1
gwbridge IP"]
    E0 --> ONS["Overlay netns
br0"]
    ONS --> VX["vxlan0 / VTEP"]
    VX --> U["UDP 4789 underlay"]
    E1 --> GW["docker_gwbridge"]
    GW --> EXT["External network"]
```

## Cross-host VXLAN

```mermaid
flowchart LR
    C1["Container A L2"] --> B1["br0"]
    B1 --> V1["VTEP"]
    V1 --> U["Outer MAC/IP/UDP 4789/VXLAN
physical L3"]
    U --> V2["Remote VTEP"]
    V2 --> B2["br0"]
    B2 --> C2["Container B L2"]
```

## VXLAN encapsulation

```mermaid
flowchart LR
    F["Original L2 frame"] --> VX["VXLAN header"]
    VX --> UDP["Outer UDP"]
    UDP --> IP["Outer IP"]
    IP --> MAC["Outer MAC"]
```
