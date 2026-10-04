# Диаграммы: глава 14 — управление ресурсами

## 1. Requests and scheduling

~~~mermaid
flowchart LR
    P["Pod requests"] --> S["Scheduler"]
    N["Node allocatable"] --> S
    S --> Q{"requests fit?"}
    Q -- yes --> A["assign Pod to node"]
    Q -- no --> X["Pod remains Pending"]
~~~

## 2. CPU request fairness

~~~mermaid
flowchart LR
    A["Container A request 200m"] --> C["CPU contention"]
    B["Container B request 1000m"] --> C
    C --> R["available CPU share about 1:5"]
~~~

## 3. Limits behavior

~~~mermaid
flowchart TD
    L["Container exceeds limit"] --> T{"Resource"}
    T -- CPU --> C["throttle CPU time"]
    T -- Memory --> O["OOM kill process/container"]
    O --> R["restart policy may restart"]
    R --> B["repeated failure → CrashLoopBackOff"]
~~~

## 4. QoS derivation

~~~mermaid
flowchart TD
    P["Pod container requests/limits"] --> Q{"All absent?"}
    Q -- yes --> B["BestEffort"]
    Q -- no --> G{"Every container CPU+memory request=limit?"}
    G -- yes --> GG["Guaranteed"]
    G -- no --> BU["Burstable"]
~~~

## 5. Memory-pressure priority

~~~mermaid
flowchart LR
    B["BestEffort"] -->|"killed first"| BU["Burstable"]
    BU --> G["Guaranteed"]
    G -->|"killed last"| S["system survives"]
~~~

## 6. LimitRange vs ResourceQuota

~~~mermaid
flowchart LR
    LR["LimitRange"] --> O["individual Pod/container/PVC"]
    RQ["ResourceQuota"] --> NS["aggregate namespace budget"]
    LR --> D["defaults/min/max"]
    RQ --> H["hard aggregate limits"]
~~~

## 7. Admission with quota

~~~mermaid
flowchart LR
    M["Pod manifest"] --> LR["LimitRanger defaults/validation"]
    LR --> RQ["ResourceQuota check"]
    RQ --> Q{"within quota?"}
    Q -- yes --> API["Pod accepted"]
    Q -- no --> F["Forbidden"]
~~~

## 8. Monitoring pipeline

~~~mermaid
flowchart LR
    C["Kubelet / cAdvisor"] --> H["Heapster"]
    H --> T["kubectl top"]
    H --> I["InfluxDB"]
    I --> G["Grafana"]
    G --> R["tune requests/limits"]
~~~
