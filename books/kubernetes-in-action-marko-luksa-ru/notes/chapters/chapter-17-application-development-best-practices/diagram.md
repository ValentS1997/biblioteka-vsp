# Диаграммы: глава 17 — application lifecycle

## 1. Pod recreation assumptions

~~~mermaid
flowchart LR
    P["Pod deleted/recreated"] --> I["new Pod IP"]
    P --> C["new container writable layer"]
    V["Volume / persistent storage"] --> S["state survives as designed"]
~~~

## 2. Init containers

~~~mermaid
flowchart LR
    I1["init container #1"] --> I2["init container #2"]
    I2 --> M["main containers"]
    F["failure / prerequisite missing"] --> I1
~~~

## 3. postStart lifecycle

~~~mermaid
flowchart TD
    C["main process starts"] --> H["postStart runs"]
    H --> Q{"hook success?"}
    Q -- yes --> R["container becomes Running"]
    Q -- no --> X["container terminated/restarted"]
~~~

## 4. Termination sequence

~~~mermaid
flowchart LR
    D["Pod deletionTimestamp"] --> P["preStop"]
    P --> T["SIGTERM"]
    T --> W["wait grace period"]
    W --> E{"process exited?"}
    E -- yes --> O["container stopped"]
    E -- no --> K["SIGKILL"]
~~~

## 5. Shutdown routing race

~~~mermaid
flowchart TD
    D["Pod deletion"] --> K["Kubelet shutdown path"]
    D --> E["Endpoints update path"]
    E --> P["kube-proxy / routers update"]
    K --> S["SIGTERM may arrive first"]
    S --> R["temporary risk of new/keep-alive traffic"]
~~~

## 6. Graceful request shutdown

~~~mermaid
flowchart LR
    T["SIGTERM"] --> D["short delay"]
    D --> N["stop new connections"]
    N --> K["close idle keep-alives"]
    K --> A["finish active requests"]
    A --> X["exit"]
~~~

## 7. Observability

~~~mermaid
flowchart LR
    A["Application"] --> L["stdout/stderr logs"]
    A --> T["termination message"]
    L --> F["FluentD"]
    F --> E["Elasticsearch"]
    E --> K["Kibana"]
    T --> D["kubectl describe Pod status"]
~~~

## 8. Delivery workflow

~~~mermaid
flowchart LR
    S["Source + manifests in VCS"] --> B["build binary/image"]
    B --> M["versioned manifests"]
    M --> A["kubectl apply / automation"]
    A --> C["cluster desired state"]
~~~
