# Диаграммы: CNM и Docker bridge

## Container Network Model

```mermaid
flowchart LR
    S1["Sandbox A
network stack"] --> E1["Endpoint"]
    E1 --> N["Network"]
    N --> E2["Endpoint"]
    E2 --> S2["Sandbox B
network stack"]
```

Sandbox содержит interfaces, routes, DNS и другие network settings. Endpoint — connection point между sandbox и network.

## Driver architecture

```mermaid
flowchart TB
    D["Docker daemon"] --> L["libnetwork / CNM implementation"]
    L --> ND["Network driver"]
    L --> IPAM["IPAM driver"]
    ND --> BUILTIN["Built-in driver"]
    ND --> THIRD["Third-party driver"]
```

## veth pair between namespaces

```mermaid
flowchart LR
    NS1["Network namespace A
10.0.0.15/24"] --> V0["veth0"]
    V0 <--> V1["veth1"]
    V1 --> NS2["Network namespace B
10.0.0.16/24"]
```

## Why bridge scales better

```mermaid
flowchart TB
    NS1["Namespace A"] --> V1["veth"]
    NS2["Namespace B"] --> V2["veth"]
    NS3["Namespace C"] --> V3["veth"]
    V1 --> BR["Linux bridge
Layer 2 virtual switch"]
    V2 --> BR
    V3 --> BR
```

Вместо отдельного point-to-point link между каждой парой namespaces каждый namespace подключается к общему bridge.

## Docker default bridge

```mermaid
flowchart LR
    C1["Container A
eth0"] <--> V1["veth host end"]
    V1 <--> B["docker0
Linux bridge"]
    B <--> V2["veth host end"]
    V2 <--> C2["Container B
eth0"]
```

## Built-in driver view

```mermaid
flowchart TB
    DR["Docker network drivers"] --> BR["bridge"]
    DR --> HOST["host"]
    DR --> NONE["none"]
    DR --> OV["overlay"]
    DR --> MAC["MACVLAN"]
    OV --> VX["Linux bridge + VXLAN
per source"]
```
