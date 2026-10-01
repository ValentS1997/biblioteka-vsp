# Диаграммы: контейнеризация и Docker

## Контейнер против виртуальной машины

```mermaid
flowchart LR
    subgraph VM["Virtual machine model"]
      VA["Application"] --> VO["Guest OS"]
      VO --> VH["Hypervisor"]
      VH --> HW1["Host / Hardware"]
    end

    subgraph CT["Container model"]
      CA["Application + runtime + dependencies"] --> CI["Container isolation"]
      CI --> KO["Shared host OS / kernel"]
      KO --> HW2["Hardware"]
    end
```

Глава объясняет лёгкость контейнера отсутствием отдельной гостевой ОС для каждого экземпляра и совместным использованием ядра хоста.

## Docker Engine

```mermaid
flowchart LR
    CLI["Docker CLI / client"] --> API["REST API"]
    API --> D["Docker daemon"]
    D --> C["Containers"]
    D --> I["Images"]
    D --> N["Networks"]
    D --> S["Storage / Volumes"]
```

Docker Engine представлен как клиент-серверное приложение: клиент взаимодействует с демоном, а демон управляет объектами Docker.

## Registry и CI/CD

```mermaid
flowchart LR
    VCS["Version-control change"] --> CI["CI build"]
    CI -->|successful build| IMG["New image"]
    IMG -->|push| REG["Docker Registry"]
    REG -->|notification| STAGE["Deployment to staging"]
    REG -->|pull| HOST["Consumer / host"]
```

Это схема процесса, описанного в главе: успешная сборка может отправить новый образ в registry, а уведомление от registry — запустить дальнейшее развёртывание.

## Микросервисы и контейнеры

```mermaid
flowchart TB
    APP["Application"] --> M1["Microservice A"]
    APP --> M2["Microservice B"]
    APP --> M3["Microservice C"]
    M1 --> C1["Container A"]
    M2 --> C2["Container B"]
    M3 --> C3["Container C"]
```

Граница каждого микросервиса позволяет независимо развёртывать, изменять, обновлять и масштабировать компоненты.

## Security boundaries

```mermaid
flowchart TB
    SEC["Docker security"] --> NS["Namespaces: process isolation"]
    SEC --> CG["cgroups: resource limits"]
    SEC --> NET["Container network isolation"]
    SEC --> DAEMON["Docker daemon access"]
    SEC --> CAP["Capabilities / least privilege"]
    SEC --> DCT["Docker Content Trust"]
    DAEMON --> RISK["Host-impact risk if access is abused"]
```

Глава отдельно подчёркивает, что доступ к Docker daemon и совместно используемым каталогам контейнера/хоста требует особого контроля.
