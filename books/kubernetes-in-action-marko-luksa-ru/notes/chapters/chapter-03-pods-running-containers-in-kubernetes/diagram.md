# Диаграммы: глава 3 — Pod и организация ресурсов

## 1. Pod как logical host

~~~mermaid
flowchart TB
    P["Pod"]
    C1["Container A"]
    C2["Container B"]
    NET["Shared Network / UTS / IPC context"]
    IP["One Pod IP + one port namespace"]
    N["One worker node"]

    P --> C1
    P --> C2
    C1 --> NET
    C2 --> NET
    NET --> IP
    P --> N
~~~

Все containers одного Pod всегда co-located на одном worker node.

## 2. Flat inter-Pod network

~~~mermaid
flowchart LR
    PA["Pod A · IP A"] <--> PB["Pod B · IP B"]
    PB <--> PC["Pod C · IP C"]
    PA <--> PC
~~~

Модель главы: Pods видят реальные Pod IP друг друга без NAT на логическом уровне.

## 3. Как решать: один Pod или два

~~~mermaid
flowchart TD
    A["Two containers/processes"] --> Q1{"Must run on same host?"}
    Q1 -- "no" --> SEP["Separate Pods"]
    Q1 -- "yes" --> Q2{"Must scale together?"}
    Q2 -- "no" --> SEP
    Q2 -- "yes" --> Q3{"One tightly coupled unit?"}
    Q3 -- "yes" --> SAME["Same Pod may be appropriate"]
    Q3 -- "no" --> SEP
~~~

## 4. Labels and selectors

~~~mermaid
flowchart LR
    R1["Pod: app=pc, rel=stable"]
    R2["Pod: app=pc, rel=beta"]
    R3["Pod: app=ui, rel=beta"]
    S["Selector: app=pc,rel=beta"]
    S --> R2
~~~

Labels идентифицируют/group resources; selector выбирает matching subset.

## 5. Scheduling through node labels

~~~mermaid
flowchart LR
    P["Pod spec: nodeSelector gpu=true"] --> SCH["Scheduler"]
    N1["Node A: gpu=true"] --> SCH
    N2["Node B: gpu absent"] --> SCH
    SCH --> N1
~~~

Требование описывается property node, а не жёсткой привязкой к конкретному hostname.

## 6. Namespaces

~~~mermaid
flowchart LR
    C["One Kubernetes cluster"]
    C --> D["namespace: default"]
    C --> T["namespace: team-a"]
    C --> S["namespace: kube-system"]
    D --> P1["Pod app"]
    T --> P2["Pod app"]
~~~

Одинаковые resource names возможны в разных namespaces. Namespace — resource/name scope, не автоматическая network isolation.

## 7. Delete vs controller

~~~mermaid
flowchart LR
    RC["ReplicationController desired Pod"] --> P["Pod"]
    DEL["kubectl delete po"] --> X["Pod removed"]
    P --> X
    RC --> NEW["Replacement Pod"]
~~~

Удаление instance не отменяет desired state controller.
