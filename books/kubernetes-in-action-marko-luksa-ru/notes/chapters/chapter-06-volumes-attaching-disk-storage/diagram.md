# Диаграммы: глава 6 — Kubernetes storage

## 1. emptyDir shared volume

~~~mermaid
flowchart LR
    G["html-generator"] -->|write /var/htdocs| V["emptyDir volume"]
    V -->|read-only mount| N["Nginx web-server"]
    N --> C["HTTP client"]
~~~

## 2. gitRepo initialization

~~~mermaid
flowchart LR
    R["Git repository"] -->|clone at Pod creation| V["gitRepo volume"]
    V --> W["web container"]
    R -. later commits not synced .-> V
~~~

## 3. Sidecar synchronization concept

~~~mermaid
flowchart LR
    R["Git repository"] --> S["git-sync sidecar"]
    S --> V["shared volume"]
    V --> A["main application container"]
~~~

Specific sidecar image/configuration not defined inside chapter.

## 4. hostPath coupling

~~~mermaid
flowchart LR
    N1["Node A filesystem"] --> V1["hostPath"]
    V1 --> P1["Pod on Node A"]
    N2["Node B filesystem"] --> V2["same path, different data"]
    V2 --> P2["Pod rescheduled on Node B"]
~~~

## 5. Direct persistent storage

~~~mermaid
flowchart LR
    P["Pod"] --> V["gcePersistentDisk volume"]
    V --> D["GCE Persistent Disk"]
    X["Pod deleted/recreated"] --> V
~~~

## 6. PV/PVC abstraction

~~~mermaid
flowchart LR
    A["Cluster admin"] --> PV["PersistentVolume"]
    U["User"] --> PVC["PersistentVolumeClaim"]
    PVC -->|binding| PV
    P["Pod"] -->|claimName| PVC
    PV --> S["Actual storage"]
~~~

## 7. Reclaim lifecycle

~~~mermaid
flowchart TD
    A["PV Available"] --> B["PVC binds"]
    B --> C["PV Bound"]
    C --> D["PVC deleted"]
    D --> E{"Reclaim policy"}
    E -- Retain --> R["PV Released + data retained"]
    E -- Recycle --> C2["contents erased → Available"]
    E -- Delete --> X["underlying storage deleted"]
~~~

## 8. Dynamic provisioning

~~~mermaid
flowchart LR
    PVC["PVC"] --> SC["StorageClass"]
    SC --> PR["Provisioner"]
    PR --> PV["new PV"]
    PR --> S["actual storage"]
    PV -->|Bound| PVC
~~~

Default StorageClass may be selected when storageClassName is omitted.
