# Диаграмма: паттерн Sidecar

~~~mermaid
flowchart TD
    A["Application container<br/>основная логика"] --> G["Atomic group / one node"]
    S["Sidecar container<br/>дополнительная capability"] --> G

    G --> R1["Shared network namespace"]
    G --> R2["Shared PID namespace"]
    G --> R3["Shared filesystem / directory"]

    R1 --> H["Legacy HTTPS case"]
    H --> H1["External HTTPS → nginx Sidecar"]
    H1 --> H2["localhost HTTP → legacy app"]

    R3 --> C["Dynamic configuration"]
    C --> C1["Config API → manager Sidecar"]
    C1 --> C2["Update shared config file"]
    C2 --> C3["file watch / SIGHUP / restart"]

    R2 --> T["topz utility"]
    T --> T1["Inspect processes/resources"]
    T1 --> T2["Expose /topz"]

    R3 --> P["Simple PaaS"]
    P --> P1["Git-sync Sidecar"]
    P1 --> P2["shared files"]
    P2 --> P3["Node.js + nodemon restart"]

    S --> M["Reusable Sidecar quality"]
    M --> M1["Parameterization"]
    M --> M2["Stable API"]
    M --> M3["Documentation"]

    M1 --> E["Environment variables"]
    M2 --> B["Compatibility = names + semantics"]
    M3 --> D["Dockerfile: EXPOSE / ENV / LABEL"]
~~~

## Design logic

~~~text
cross-cutting capability
→ can be co-located with application?
→ choose minimum required shared resources
→ implement Sidecar
→ parameterize
→ define stable API
→ document
→ deploy beside multiple applications
→ verify observable capability
~~~

## Operational caution

Shared namespaces/filesystems are the mechanism that makes Sidecar useful, but they also create coupling. Chapter 2 does not define a generic isolation/security policy, so exact production boundaries remain `[Needs confirmation]`.
