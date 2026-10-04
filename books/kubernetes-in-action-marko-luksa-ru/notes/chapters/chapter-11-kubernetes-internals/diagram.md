# Диаграммы: глава 11 — внутреннее устройство Kubernetes

## 1. Cluster architecture

~~~mermaid
flowchart LR
    K["kubectl / clients"] --> API["API server"]
    API <--> ETCD["etcd"]
    SCH["scheduler"] --> API
    CM["controller manager"] --> API
    KL["Kubelet"] --> API
    KP["kube-proxy"] --> API
~~~

## 2. API request pipeline

~~~mermaid
flowchart LR
    R["HTTP request"] --> AU["Authentication"]
    AU --> AZ["Authorization"]
    AZ --> AC["Admission control"]
    AC --> V["Validation"]
    V --> E["etcd"]
~~~

## 3. Watch-driven control

~~~mermaid
flowchart LR
    E["etcd object changes"] --> API["API server"]
    API --> W1["watch: scheduler"]
    API --> W2["watch: controllers"]
    API --> W3["watch: Kubelet"]
    W1 --> API
    W2 --> API
    W3 --> API
~~~

## 4. Deployment to running containers

~~~mermaid
flowchart TD
    D["Deployment object"] --> DC["Deployment controller"]
    DC --> RS["ReplicaSet object"]
    RS --> RC["ReplicaSet controller"]
    RC --> P["Pod objects"]
    P --> S["scheduler"]
    S --> AP["assigned Pods"]
    AP --> K["Kubelet"]
    K --> C["containers running"]
~~~

## 5. Pod infrastructure container

~~~mermaid
flowchart TD
    P["Pod"] --> PAUSE["pause/infrastructure container"]
    PAUSE --> NS["shared Linux namespaces"]
    A["app container A"] --> NS
    B["app container B"] --> NS
~~~

## 6. Pod networking

~~~mermaid
flowchart LR
    P1["Pod A eth0"] --> V1["veth"]
    V1 --> B1["node bridge"]
    B1 --> N["node/network routing or overlay"]
    N --> B2["remote node bridge"]
    B2 --> V2["veth"]
    V2 --> P2["Pod B eth0"]
~~~

## 7. Service routing

~~~mermaid
flowchart LR
    C["client"] --> VIP["Service ClusterIP:port"]
    VIP --> IPT["iptables rules"]
    KP["kube-proxy watches Service + Endpoints"] --> IPT
    IPT --> P1["Pod endpoint A"]
    IPT --> P2["Pod endpoint B"]
~~~

## 8. HA control plane

~~~mermaid
flowchart TD
    LB["API load balancer"] --> A1["API server 1"]
    LB --> A2["API server 2"]
    LB --> A3["API server 3"]
    A1 --> E["etcd quorum"]
    A2 --> E
    A3 --> E
    S1["scheduler 1"] --> LE["leader election"]
    S2["scheduler 2"] --> LE
    C1["controller-manager 1"] --> LE2["leader election"]
    C2["controller-manager 2"] --> LE2
~~~
