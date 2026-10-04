# Диаграммы: глава 5 — Service и discovery

## 1. Service → Endpoints → Pods

~~~mermaid
flowchart LR
    C["Client"] --> S["Service: stable IP:port"]
    S --> E["Endpoints"]
    E --> P1["Ready Pod A"]
    E --> P2["Ready Pod B"]
    SEL["Service selector"] --> E
    RDY["Readiness"] --> E
~~~

## 2. Service discovery

~~~mermaid
flowchart TB
    P["Client Pod"] --> ENV["Environment variables"]
    P --> DNS["Cluster DNS"]
    ENV --> IP["Service ClusterIP + port"]
    DNS --> FQDN["service.namespace.svc.cluster.local"]
    FQDN --> IP
~~~

## 3. External Service without selector

~~~mermaid
flowchart LR
    P["Pod client"] --> S["Service: external-service"]
    S --> E["Manual Endpoints"]
    E --> X1["External IP A"]
    E --> X2["External IP B"]
~~~

## 4. External access models

~~~mermaid
flowchart LR
    EXT["External client"] --> NP["NodePort"]
    EXT --> LB["LoadBalancer"]
    LB --> NP
    NP --> S["Service"]
    S --> P["Pods"]
~~~

## 5. Ingress

~~~mermaid
flowchart LR
    C["HTTP client"] --> I["Ingress controller"]
    I -->|host/path A| S1["Service A"]
    I -->|host/path B| S2["Service B"]
    S1 --> P1["Pods A"]
    S2 --> P2["Pods B"]
~~~

## 6. Readiness removes backend

~~~mermaid
flowchart LR
    P["Pod"] --> Q{"readinessProbe"}
    Q -- success --> E["Included in Endpoints"]
    Q -- failure --> OUT["Excluded from Endpoints"]
    E --> TRAF["Receives Service traffic"]
    OUT --> NO["No Service traffic"]
~~~

Readiness failure does not restart the container.

## 7. Headless Service

~~~mermaid
flowchart LR
    C["Client DNS query"] --> DNS["Cluster DNS"]
    DNS --> P1["Pod IP A"]
    DNS --> P2["Pod IP B"]
    DNS --> P3["Pod IP C"]
~~~

clusterIP: None makes DNS expose backend Pod IPs rather than one Service ClusterIP.

## 8. Troubleshooting decision path

~~~mermaid
flowchart TD
    A["Service unreachable"] --> B{"Testing ClusterIP from inside cluster?"}
    B -- no --> FIX1["move test inside cluster"]
    B -- yes --> C{"Ready endpoints exist?"}
    C -- no --> FIX2["check selector + readiness"]
    C -- yes --> D{"DNS only failure?"}
    D -- yes --> FIX3["test ClusterIP and DNS"]
    D -- no --> E{"Correct Service port?"}
    E -- no --> FIX4["use Service port"]
    E -- yes --> F{"Pod IP reachable?"}
    F -- no --> FIX5["check app listener / localhost binding"]
    F -- yes --> G["inspect Service path"]
~~~
