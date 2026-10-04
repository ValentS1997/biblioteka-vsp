# Диаграммы: глава 16 — advanced scheduling

## 1. Taint and toleration

~~~mermaid
flowchart LR
    N["Node taint"] --> Q{"Pod tolerates?"}
    Q -- no --> X["scheduler rejects node"]
    Q -- yes --> A["node remains eligible"]
~~~

## 2. Taint effects

~~~mermaid
flowchart TD
    T["Taint"] --> N["NoSchedule"]
    T --> P["PreferNoSchedule"]
    T --> E["NoExecute"]
    N --> N1["block new Pods without toleration"]
    P --> P1["prefer other nodes"]
    E --> E1["block new + evict existing unsupported Pods"]
~~~

## 3. Required node affinity

~~~mermaid
flowchart LR
    P["Pod nodeAffinity"] --> L["required node labels"]
    L --> N1["matching node"]
    L -. rejects .-> N2["non-matching node"]
~~~

## 4. Preferred node affinity

~~~mermaid
flowchart LR
    R1["zone1 weight 80"] --> S["scheduler score"]
    R2["dedicated weight 20"] --> S
    O["other priority functions"] --> S
    S --> N["selected node"]
~~~

## 5. Required pod affinity

~~~mermaid
flowchart LR
    B["backend Pod app=backend"] --> T["topology domain: hostname"]
    F["frontend podAffinity"] --> T
    T --> N["same node placement"]
~~~

## 6. topologyKey

~~~mermaid
flowchart TD
    K["topologyKey"] --> H["hostname → node"]
    K --> Z["zone → availability zone"]
    K --> R["region → region"]
    K --> C["custom rack → rack"]
~~~

## 7. Required pod anti-affinity

~~~mermaid
flowchart LR
    P1["frontend replica 1"] --> N1["node1"]
    P2["frontend replica 2"] --> N2["node2"]
    P3["frontend replica 3"] -. no valid hostname domain .-> X["Pending"]
~~~

## 8. Hard vs preferred rule

~~~mermaid
flowchart TD
    R["Placement rule"] --> H{"Must violation be impossible?"}
    H -- yes --> REQ["requiredDuringScheduling..."]
    H -- no --> PREF["preferredDuringScheduling..."]
    REQ --> P["may leave Pod Pending"]
    PREF --> F["scheduler can fall back"]
~~~
