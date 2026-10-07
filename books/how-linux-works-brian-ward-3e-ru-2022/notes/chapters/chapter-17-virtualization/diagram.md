# Mermaid — глава 17 «Виртуализация»

Источник: **RAG `p0458:c01`–`p0477:c01`**, PDF/печатные страницы 458–477. Диаграммы синтезированы только из связей, подтвержденных главой.

## 1. Isolation boundary

```mermaid
flowchart TD
  NEED["Need isolation"] --> B{"What must be isolated?"}
  B -->|Full machine + guest kernel| VM["System virtual machine"]
  B -->|Process set on shared Linux kernel| CT["Container"]
  B -->|Application/runtime dependencies| RT["Runtime virtual environment"]
```

## 2. Hypervisor model

```mermaid
flowchart LR
  HW["Physical hardware"] --> T1["Type 1 hypervisor"]
  T1 --> G1["Guest OS / VM"]
  HW --> HOSTOS["Host operating system"]
  HOSTOS --> T2["Type 2 hypervisor"]
  T2 --> G2["Guest OS / VM"]
```

## 3. Virtual hardware path

```mermaid
flowchart TD
  GUEST["Guest OS"] --> DEV["Virtual device interface"]
  DEV --> HYP["Hypervisor"]
  HYP --> HOST["Host resource"]
  DEV --> PARA["Paravirtualized path when provided"]
  PARA --> HOST
```

## 4. Container construction model

```mermaid
flowchart TD
  K["One host Linux kernel"] --> CG["Control groups"]
  K --> PID["PID namespace"]
  K --> FS["Filesystem/device isolation"]
  K --> NET["Network namespace/interfaces"]
  CG --> C["Container process set"]
  PID --> C
  FS --> C
  NET --> C
```

## 5. Docker image build

```mermaid
flowchart LR
  DF["Dockerfile"] --> FROM["FROM base image"]
  FROM --> RUN["RUN build-time command"]
  RUN --> LAYER["New image layer"]
  LAYER --> CMD["CMD runtime command"]
  CMD --> IMG["Tagged image"]
```

## 6. Image versus container lifecycle

```mermaid
flowchart TD
  IMG["Image"] --> RUN["docker run"]
  RUN --> PROC["Container with running process"]
  PROC --> PS["docker ps"]
  PROC --> EXIT["Process exits"]
  EXIT --> ALL["docker ps -a"]
  ALL --> RM["docker rm cleanup"]
  IMG --> IMAGES["docker images"]
  IMAGES --> RMI["docker rmi cleanup"]
```

The source contains a contradiction about persistence of filesystem changes after process exit; this diagram therefore separates **exit** from explicit **container removal** and does not assert automatic filesystem deletion. See `source-findings.md`.

## 7. Docker network model

```mermaid
flowchart LR
  EXT["External network"] --> NAT["Host NAT"]
  NAT --> BR["Docker bridge / private subnet"]
  BR --> VETH["Virtual interface pair"]
  VETH --> NS["Container network namespace"]
  NS --> ETH["Container interface"]
  NS --> LO["Private loopback"]
```

## 8. Overlay filesystem model

```mermaid
flowchart TD
  BASE["Lower layers / image content"] --> MERGE["Overlay view"]
  UPPER["Upper layer / changes"] --> MERGE
  WORK["Work directory"] --> MERGE
  MERGE --> ROOT["Container root filesystem"]
```

## 9. Container management levels

```mermaid
flowchart TD
  KERNEL["Kernel isolation primitives"] --> DOCKER["Docker / Podman"]
  KERNEL --> LXC["LXC"]
  LXC --> LXD["LXD management"]
  DOCKER --> K8S["Kubernetes orchestration"]
  K8S --> MANY["Run / monitor / restart / network / update many containers"]
```

## 10. Container risk map

```mermaid
flowchart TD
  APP["Containerized application"] --> STORAGE["Storage growth"]
  APP --> CPU["Finite host resources"]
  APP --> DATA["Persistent data + logs"]
  APP --> VERSION["Image/version management"]
  APP --> TRUST["Base-image/repository trust"]
  APP --> CONFIG["Misconfiguration"]
  STORAGE --> REVIEW["Operational review"]
  CPU --> REVIEW
  DATA --> REVIEW
  VERSION --> REVIEW
  TRUST --> REVIEW
  CONFIG --> REVIEW
```

## 11. Python runtime virtualization

```mermaid
flowchart LR
  SYS["System Python + packages"] --> CREATE["python3 -m venv test-venv"]
  CREATE --> ENV["Separate environment tree"]
  ENV --> ACT["Activate shell environment"]
  ACT --> PKG["Environment-specific package library"]
  PKG --> DEACT["deactivate"]
```

The literal activation path in the source uses `test-env` instead of the created `test-venv`; the diagram avoids silently choosing a corrected command and records the mismatch in `source-findings.md`.
