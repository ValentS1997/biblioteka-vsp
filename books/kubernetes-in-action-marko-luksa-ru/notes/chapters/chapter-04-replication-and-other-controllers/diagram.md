# Диаграммы: глава 4 — managed Pods

## 1. Liveness self-healing

~~~mermaid
flowchart LR
    P["livenessProbe"] --> Q{"healthy?"}
    Q -- yes --> R["keep running"]
    Q -- repeated failure --> K["Kubelet kills container"]
    K --> N["new container instance"]
    N --> P
~~~

## 2. ReplicationController reconciliation

~~~mermaid
flowchart TD
    S["selector: app=kubia"] --> C["count matching Pods"]
    D["desired replicas = N"] --> CMP{"actual vs desired"}
    C --> CMP
    CMP -- "actual < N" --> ADD["create Pods from template"]
    CMP -- "actual > N" --> DEL["delete excess Pods"]
    CMP -- "actual = N" --> OK["no change"]
    ADD --> C
    DEL --> C
~~~

## 3. Node failure

~~~mermaid
flowchart LR
    N1["Node with managed Pod"] --> F["Node becomes unavailable"]
    F --> U["old Pod becomes Unknown"]
    RC["ReplicationController"] --> NEW["new replacement Pod"]
    NEW --> N2["available Node"]
~~~

Pod не переносится; controller создаёт новый Pod.

## 4. Selector scope

~~~mermaid
flowchart LR
    P["Pod: app=kubia"] --> RC["RC selector app=kubia"]
    L["change label to app=foo"] --> OUT["Pod outside RC scope"]
    OUT --> R["RC sees too few matching Pods"]
    R --> NEW["replacement app=kubia Pod"]
~~~

## 5. ReplicaSet selector

~~~mermaid
flowchart LR
    RS["ReplicaSet"] --> ML["matchLabels"]
    RS --> ME["matchExpressions"]
    ME --> IN["In / NotIn"]
    ME --> EX["Exists / DoesNotExist"]
~~~

## 6. DaemonSet

~~~mermaid
flowchart LR
    DS["DaemonSet nodeSelector disk=ssd"]
    N1["Node A disk=ssd"]
    N2["Node B disk=hdd"]
    N3["Node C disk=ssd"]
    DS --> P1["daemon Pod"]
    P1 --> N1
    DS --> P3["daemon Pod"]
    P3 --> N3
~~~

Desired state определяется набором matching nodes, а не числом replicas.

## 7. Job

~~~mermaid
flowchart LR
    J["Job"] --> C["completions"]
    J --> P["parallelism"]
    J --> POD["finite Pod"]
    POD --> Q{"success?"}
    Q -- no --> RET["retry/replacement according to policy"]
    Q -- yes --> DONE["successful completion counted"]
    DONE --> C
~~~

## 8. CronJob

~~~mermaid
flowchart LR
    CR["CronJob schedule"] --> J1["Job at scheduled time"]
    J1 --> P1["Pod(s)"]
    D["startingDeadlineSeconds"] --> J1
~~~

Source reliability model: scheduled Jobs can be duplicated or missed; workload should be idempotent.
