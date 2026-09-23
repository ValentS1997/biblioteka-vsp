# Диаграмма: container lifecycle and security boundaries

~~~mermaid
flowchart TD
    A["Application + dependencies"] --> B["Dockerfile / image"]
    B --> C["Read-only image layers"]
    C --> D["docker run"]
    D --> E["Writable container layer"]
    D --> F["Namespaces / cgroups / capabilities / seccomp"]
    D --> G["Network mode"]
    D --> H["Volumes / bind mounts"]

    F --> I["Running process tree"]
    I --> J["PID 1 lifecycle"]
    J --> K["STDOUT / STDERR"]
    K --> L["Docker logging driver"]
    L --> M["docker logs"]

    G --> G1["bridge"]
    G --> G2["host"]
    G --> G3["none"]

    H --> H1["Disposable container layer"]
    H --> H2["Persistent external data"]

    N["Security boundary"] --> N1["Protect dockerd"]
    N --> N2["TLS for remote API"]
    N --> N3["Unprivileged USER"]
    N --> N4["Drop capabilities"]
    N --> N5["Trusted images"]
    N --> N6["Avoid privileged mode"]

    O["Troubleshooting"] --> O1["docker ps / inspect / logs"]
    O1 --> O2["docker exec only when needed"]
    O2 --> O3["Fix image, then replace container"]

    P["Scale-out"] --> P1["Scheduler / orchestrator"]
    P1 --> P2["Kubernetes"]
    P1 --> P3["Mesos / Marathon"]
    P1 --> P4["Docker Swarm"]
    P1 --> P5["AWS ECS"]

    B --> Q["Registry"]
    Q --> Q1["TLS / authentication / content trust"]
~~~

## Смысл диаграммы

Контейнерный runtime не отменяет системное администрирование: lifecycle, network, persistent data, image supply chain и privileged daemon образуют отдельные security/operational boundaries. Оркестрация добавляется только поверх уже воспроизводимого single-host container workflow.
