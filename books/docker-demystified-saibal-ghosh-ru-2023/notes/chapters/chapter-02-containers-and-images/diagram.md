# Диаграммы: контейнеры и образы

## Lifecycle container

```mermaid
stateDiagram-v2
    [*] --> Created: docker container create
    Created --> Running: run/start concept
    Running --> Paused: pause
    Paused --> Running: unpause
    Running --> Exited: process exits / stop
    Running --> Restarting: restart in progress
    Restarting --> Running
    Created --> Dead: failed partial removal
    Exited --> Dead: failed partial removal
```

Точная команда `start` в главе не демонстрируется, поэтому переход из Created к Running отмечен как concept.

## Docker runtime stack

```mermaid
flowchart TB
    U["User"] --> CLI["Docker CLI"]
    CLI --> API["Docker REST API"]
    API --> D["Docker server / dockerd"]
    D --> CTD["containerd"]
    CTD --> R["runC"]
    R --> NS["Linux namespaces"]
    R --> CG["cgroups"]
    R --> SEC["AppArmor / SELinux / filesystem access controls"]
```

## Image → container

```mermaid
flowchart TB
    L1["Immutable layer 1"] --> L2["Immutable layer 2"]
    L2 --> L3["Immutable layer 3"]
    L3 --> RW["Thin read-write layer"]
    RW --> C["Container"]
```

## Copy-On-Write

```mermaid
flowchart LR
    I["File in immutable image layer"] --> R1["Read shared file"]
    I --> W["Container wants to modify"]
    W --> COPY["Copy to read-write layer"]
    COPY --> MOD["Modify private copy"]
    I --> OTHER["Other containers keep original"]
```

## Image identity

```mermaid
flowchart TB
    C["Configuration object"] --> D1["SHA-256 digest layer A"]
    C --> D2["SHA-256 digest layer B"]
    C --> D3["SHA-256 digest layer C"]
    D1 --> FS["Filesystem assembled by Docker Engine"]
    D2 --> FS
    D3 --> FS
```

## Logging

```mermaid
flowchart LR
    APP["Process"] --> OUT["stdout / stderr"]
    OUT --> LD["Logging driver"]
    LD --> J["json-file"]
    J --> F["/var/lib/docker/containers/<id>/<id>-json.log"]
    LD --> PIPE["Central aggregator / pipeline"]
```

## Dockerfile build

```mermaid
flowchart TB
    DF["Dockerfile"] --> F1["FROM"]
    F1 --> R1["RUN / metadata instructions"]
    R1 --> CACHE["Build cache / intermediate images"]
    CACHE --> IMG["Final image"]
    IMG --> C["docker run → container"]
```

## Multi-stage build

```mermaid
flowchart LR
    S1["FROM ... stage 1"] --> ART["Build artifacts"]
    ART --> COPY["Copy required artifacts"]
    S2["FROM ... stage 2"] --> COPY
    COPY --> FINAL["Smaller final image"]
```
