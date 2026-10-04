# Диаграммы: глава 15 — autoscaling

## 1. HPA metric flow

~~~mermaid
flowchart LR
    P["Pods"] --> C["cAdvisor / Kubelet"]
    C --> H["Heapster"]
    H --> A["HorizontalPodAutoscaler"]
    A --> S["Scale subresource"]
    S --> D["Deployment / RS / RC / StatefulSet"]
~~~

## 2. HPA decision loop

~~~mermaid
flowchart TD
    M["collect metrics"] --> C["calculate desired replicas"]
    C --> B{"within min/max?"}
    B --> U["update Scale subresource"]
    U --> W["workload controller reconciles Pods"]
    W --> M
~~~

## 3. Multiple metrics

~~~mermaid
flowchart LR
    CPU["CPU metric → needs 4 replicas"] --> MAX["choose maximum"]
    QPS["QPS metric → needs 3 replicas"] --> MAX
    MAX --> R["desired replicas = 4"]
~~~

## 4. CPU utilization

~~~mermaid
flowchart LR
    U["actual CPU usage"] --> D["divide by CPU request"]
    R["CPU request"] --> D
    D --> P["HPA utilization %"]
~~~

## 5. Custom metric types

~~~mermaid
flowchart TD
    H["HPA metrics"] --> R["Resource"]
    H --> P["Pods"]
    H --> O["Object"]
    R --> CPU["CPU utilization"]
    P --> Q["per-Pod QPS"]
    O --> I["Ingress latency"]
~~~

## 6. Cluster scale-up

~~~mermaid
flowchart LR
    P["Unschedulable Pod"] --> CA["Cluster Autoscaler"]
    CA --> G["find fitting node group"]
    G --> N["add cloud node"]
    N --> K["Kubelet registers Node"]
    K --> S["Scheduler places Pod"]
~~~

## 7. Cluster scale-down

~~~mermaid
flowchart TD
    N["underutilized node"] --> C{"safe to remove?"}
    C -- no --> K["keep node"]
    C -- yes --> U["mark unschedulable"]
    U --> E["evict managed movable Pods"]
    E --> R["controllers recreate elsewhere"]
    R --> D["delete/return node"]
~~~

## 8. PDB during voluntary disruption

~~~mermaid
flowchart LR
    D["drain / Cluster Autoscaler"] --> E["request eviction"]
    P["PodDisruptionBudget minAvailable=3"] --> E
    E --> Q{"would availability fall below 3?"}
    Q -- yes --> B["block eviction"]
    Q -- no --> A["allow eviction"]
~~~
