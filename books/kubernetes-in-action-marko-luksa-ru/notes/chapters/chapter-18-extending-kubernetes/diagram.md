# Глава 18 — diagrams

## 1. CRD и пользовательский контроллер

```mermaid
flowchart LR
    U[User] -->|creates| CR[Website custom resource]
    CR --> API[Kubernetes API server]
    C[Website controller] -->|watches| API
    C -->|creates| D[Deployment]
    C -->|creates| S[Service]
    D --> P[Pods]
    S --> P
```

## 2. Расширение API через aggregation

```mermaid
flowchart LR
    Client[kubectl / client] --> Main[Main Kubernetes API server]
    Main -->|API aggregation| Custom[Custom API server]
    Reg[APIService] --> Main
    Custom --> Store[(etcd or CRD-backed storage)]
```

## 3. Service Catalog

```mermaid
flowchart LR
    Admin[Cluster admin] --> B[ClusterServiceBroker]
    B --> C[ClusterServiceClass]
    User[User] --> I[ServiceInstance]
    C --> I
    I --> Broker[External service broker]
    User --> Bind[ServiceBinding]
    I --> Bind
    Bind --> Broker
    Broker --> Secret[Secret with connection data]
    Secret --> Pod[Client Pod]
```

## 4. OpenShift build/deploy flow

```mermaid
flowchart LR
    Git[Git repository] --> BC[BuildConfig]
    BC --> Builder[Builder Pod / Source-to-Image]
    Builder --> IS[ImageStream]
    IS --> DC[DeploymentConfig]
    DC --> RC[Replication Controller]
    RC --> Pods[Pods]
    Route[Route + Router] --> Pods
```

## 5. Helm architecture в источнике

```mermaid
flowchart LR
    Chart[Chart] --> Release[Release]
    Config[Config] --> Release
    CLI[helm CLI] --> Tiller[Tiller]
    Release --> Tiller
    Tiller --> R[Deployments / Services / Secrets / PVC / other resources]
```

## Логика главы

```mermaid
flowchart TD
    Need[Нужна более высокая abstraction] --> Q{Достаточно custom resource + controller?}
    Q -->|Да| CRD[Define CRD]
    CRD --> Obj[Create custom resource]
    Obj --> Ctrl[Controller reconciles]
    Ctrl --> Native[Create native Kubernetes resources]

    Q -->|Нет / нужен отдельный API behavior| Agg[Deploy custom API server]
    Agg --> APIService[Register APIService]
    APIService --> Unified[Expose through Kubernetes API aggregation]

    Need --> Platform{Нужен platform-level developer workflow?}
    Platform --> OpenShift[OpenShift]
    Platform --> Deis[Deis Workflow]
    Platform --> Helm[Helm package deployment]
```
