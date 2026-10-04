# Диаграммы: глава 10 — StatefulSet

## 1. Stable ordinal identity

~~~mermaid
flowchart LR
    S["StatefulSet kubia"] --> P0["kubia-0"]
    S --> P1["kubia-1"]
    S --> P2["kubia-2"]
~~~

## 2. Stable per-Pod storage

~~~mermaid
flowchart LR
    T["volumeClaimTemplates: data"] --> C0["PVC data-kubia-0"]
    T --> C1["PVC data-kubia-1"]
    C0 --> V0["PV / storage 0"]
    C1 --> V1["PV / storage 1"]
    P0["kubia-0"] --> C0
    P1["kubia-1"] --> C1
~~~

## 3. Pod replacement

~~~mermaid
flowchart LR
    O["old kubia-0 on Node A"] --> X["graceful deletion"]
    X --> N["new kubia-0 on Node B"]
    PVC["PVC data-kubia-0"] --> O
    PVC --> N
~~~

Identity and storage persist across rescheduling.

## 4. Ordered lifecycle

~~~mermaid
flowchart TD
    C0["create kubia-0"] --> R0{"Ready?"}
    R0 -- yes --> C1["create kubia-1"]
    C1 --> R1{"Ready?"}
    R1 -- yes --> C2["create kubia-2"]
~~~

Scale-down reverses ordinal order.

## 5. Headless Service and DNS

~~~mermaid
flowchart LR
    P["Pod"] --> Q["DNS SRV query"]
    Q --> H["headless Service kubia"]
    H --> P0["kubia-0.kubia..."]
    H --> P1["kubia-1.kubia..."]
    H --> P2["kubia-2.kubia..."]
~~~

## 6. Client vs peer path

~~~mermaid
flowchart LR
    C["Client"] --> SVC["kubia-public ClusterIP Service"]
    SVC --> P1["one StatefulSet Pod"]
    P1 --> DNS["SRV discovery"]
    DNS --> P0["peer kubia-0"]
    DNS --> P2["peer kubia-2"]
~~~

## 7. Node failure safety

~~~mermaid
flowchart TD
    N["Node network lost"] --> NR["Node NotReady"]
    NR --> U["Pod status Unknown/Terminating"]
    U --> Q{"Old Pod definitely stopped?"}
    Q -- no/unknown --> WAIT["Do not create replacement"]
    Q -- yes --> DEL["Admin removes old API object/node"]
    DEL --> NEW["StatefulSet may create replacement"]
~~~

## 8. Force-delete hazard

~~~mermaid
flowchart LR
    OLD["old kubia-0 may still run"] --> F["force delete API object"]
    F --> NEW["new kubia-0 created"]
    OLD --> RISK["duplicate identity/storage"]
    NEW --> RISK
~~~
