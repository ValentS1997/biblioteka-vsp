# Диаграммы: глава 9 — Deployment rollout

## 1. Old client-driven rolling update

~~~mermaid
flowchart LR
    K["kubectl rolling-update"] --> OLD["RC v1"]
    K --> NEW["RC v2"]
    OLD --> P1["Pods v1"]
    NEW --> P2["Pods v2"]
    K --> S["scale old down / new up"]
~~~

## 2. Deployment hierarchy

~~~mermaid
flowchart TD
    D["Deployment"] --> RS1["ReplicaSet revision 1"]
    D --> RS2["ReplicaSet revision 2"]
    RS1 --> P1["Pods v1"]
    RS2 --> P2["Pods v2"]
~~~

## 3. Declarative update

~~~mermaid
flowchart LR
    U["change Pod template"] --> D["Deployment desired state"]
    D --> RS["new ReplicaSet"]
    RS --> NP["new Pods"]
    D --> ORS["old ReplicaSet scales down"]
~~~

## 4. Revision rollback

~~~mermaid
flowchart LR
    H["Revision history"] --> R1["rev 1 / old ReplicaSet"]
    H --> R2["rev 2"]
    H --> R3["rev 3 current"]
    U["rollout undo --to-revision=1"] --> R1
    R1 --> D["Deployment converges to rev 1 template"]
~~~

## 5. RollingUpdate limits

~~~mermaid
flowchart TD
    DES["desired replicas = N"] --> MS["maxSurge"]
    DES --> MU["maxUnavailable"]
    MS --> MAX["upper temporary Pod count"]
    MU --> MIN["minimum available Pods"]
~~~

## 6. Pause/resume canary-like flow

~~~mermaid
flowchart LR
    V2["old Pods"] --> SET["set image v4"]
    SET --> P["one new Pod appears"]
    P --> PAUSE["rollout pause"]
    PAUSE --> TEST["observe limited traffic"]
    TEST --> RES["rollout resume"]
    RES --> ALL["replace remaining old Pods"]
~~~

## 7. Readiness-gated bad rollout

~~~mermaid
flowchart LR
    D["Deployment v3"] --> NEW["new Pod v3"]
    NEW --> R{"readiness passes?"}
    R -- no --> EP["excluded from Service endpoints"]
    R -- no --> BLOCK["not Available long enough"]
    BLOCK --> STOP["rollout stops progressing"]
    OLD["healthy v2 Pods"] --> SVC["Service traffic continues"]
~~~

## 8. Progress deadline and rollback

~~~mermaid
flowchart LR
    STUCK["no rollout progress"] --> PD["progressDeadlineSeconds exceeded"]
    PD --> FAIL["ProgressDeadlineExceeded"]
    FAIL --> UNDO["kubectl rollout undo"]
    UNDO --> HEALTHY["previous revision restored"]
~~~
