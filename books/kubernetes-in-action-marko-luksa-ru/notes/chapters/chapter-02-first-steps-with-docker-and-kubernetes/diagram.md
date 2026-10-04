# Диаграммы: глава 2 — Docker → Kubernetes

## 1. Сборка и публикация image

~~~mermaid
flowchart LR
    A["app.js"] --> D["Dockerfile"]
    D --> B["docker build -t kubia ."]
    B --> I["local image: kubia"]
    I --> R["docker run + curl"]
    I --> T["docker tag"]
    T --> P["docker push"]
    P --> H["Remote registry"]
~~~

## 2. Исследование container

~~~mermaid
flowchart TB
    C["kubia-container"] --> PS["docker ps / inspect"]
    C --> E["docker exec -it ... bash"]
    E --> P["ps aux"]
    E --> F["ls /"]
    P --> V["Container sees isolated PID view"]
    F --> FS["Container sees isolated filesystem"]
    HOST["Host ps aux | grep app.js"] --> SAME["Same app process, host-side PID"]
~~~

## 3. Cluster setup и client path

~~~mermaid
flowchart LR
    DEV["Developer machine"] --> K["kubectl"]
    K --> API["Kubernetes API"]
    API --> CP["Control plane"]
    CP --> N1["Worker node"]
    CP --> N2["Worker node"]
    CP --> N3["Worker node"]
    M["Minikube"] --> ONE["Local single-node cluster"]
    G["GKE"] --> CP
~~~

## 4. Первый workload

~~~mermaid
flowchart LR
    REG["Registry: image"] --> RT["Container runtime on worker"]
    RUN["kubectl run"] --> API["API server"]
    API --> RC["ReplicationController"]
    RC --> POD["Pod"]
    POD --> SCHED["Scheduled to worker"]
    SCHED --> K["Kubelet"]
    K --> RT
    RT --> CONT["Running container"]
~~~

В source-era workflow `kubectl run` создаёт ReplicationController.

## 5. Service и scaling

~~~mermaid
flowchart LR
    SCALE["kubectl scale rc ..."] --> RC["ReplicationController"]
    RC --> P1["Pod 1"]
    RC --> P2["Pod 2"]
    RC --> P3["Pod 3"]

    CLIENT["Client"] --> SVC["Service: stable access"]
    SVC --> P1
    SVC --> P2
    SVC --> P3
~~~

ReplicationController поддерживает число Pod. Service предоставляет клиентам одну точку входа и распределяет запросы между Pod.
