# Диаграммы: Docker Enterprise security

## Enterprise components

```mermaid
flowchart TB
    DE["Docker Enterprise"] --> EE["Docker Engine Enterprise"]
    DE --> UCP["Universal Control Plane"]
    DE --> DTR["Docker Trusted Registry"]
    UCP --> ORCH["Swarm / Kubernetes
per source"]
    DTR --> IMG["Enterprise image registry"]
```

## Source lab topology

```mermaid
flowchart LR
    N1["Node 1
Docker EE"] --> UCP["UCP
Swarm manager"]
    N2["Node 2
Docker EE"] --> W["Swarm worker"]
    N2 --> DTR["DTR"]
    UCP --> W
    UCP --> DTR
```

## Client Bundle

```mermaid
flowchart LR
    USER["Authorized user"] --> B["Client Bundle
cert/key + scripts"]
    B --> ENV["DOCKER_HOST
DOCKER_CERT_PATH
DOCKER_TLS_VERIFY"]
    ENV --> CLI["Docker CLI / Kubectl"]
    CLI --> TLS["TLS-authenticated request"]
    TLS --> UCP["UCP"]
```

## Vulnerability scanning

```mermaid
flowchart LR
    IMG["Image"] --> PUSH["Push to DTR"]
    PUSH --> SCAN["Vulnerability scan"]
    CVE["CVE database
online/offline update"] --> SCAN
    SCAN --> FIND["Findings by layer/component"]
    PUSH --> AUTO["Optional scan on push"]
    AUTO --> SCAN
```

## RBAC model

```mermaid
flowchart LR
    S["Subject
user/org/team"] --> G["Grant"]
    R["Role
permissions"] --> G
    C["Collection
resource set"] --> G
    G --> ACCESS["Effective access"]
```

## Custom grant workflow

```mermaid
flowchart TB
    C["Create My_collection"] --> R["Create My_role"]
    R --> S["Choose subject"]
    S --> RS["Choose resource set"]
    RS --> RR["Choose role"]
    RR --> G["Create grant"]
```

## Built-in role spectrum

```mermaid
flowchart LR
    V["View Only"] --> RC["Restricted Control"]
    RC --> SCH["Scheduler"]
    SCH --> FC["Full Control"]
```

Это conceptual ordering для запоминания names; конкретные permission sets source описывает отдельно и не сводит их к строгой линейной superset hierarchy.
