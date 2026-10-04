# Диаграммы: глава 8 — metadata и API access

## 1. Downward API via env

~~~mermaid
flowchart LR
    P["Pod metadata/spec/status"] --> F["fieldRef"]
    R["Container resources"] --> RF["resourceFieldRef + divisor"]
    F --> E["Environment variables"]
    RF --> E
    E --> A["Application process"]
~~~

## 2. Downward API via volume

~~~mermaid
flowchart LR
    M["Pod metadata"] --> D["downwardAPI volume"]
    R["Container resources"] --> D
    D --> F["Files under /etc/downward"]
    F --> A["Application"]
~~~

Labels/annotations can update through files.

## 3. Local API exploration

~~~mermaid
flowchart LR
    C["curl localhost:8001"] --> P["kubectl proxy"]
    P -->|"HTTPS + auth + verification"| API["Kubernetes API server"]
~~~

## 4. Direct in-Pod API access

~~~mermaid
flowchart LR
    APP["Application/curl"] --> TLS["CA: ca.crt"]
    APP --> AUTH["Bearer token"]
    NS["namespace file"] --> APP
    TLS --> API["https://kubernetes"]
    AUTH --> API
~~~

## 5. Namespace-scoped request

~~~mermaid
flowchart LR
    T["ServiceAccount token"] --> H["Authorization header"]
    N["namespace file"] --> URL["/api/v1/namespaces/NS/pods"]
    H --> REQ["HTTPS GET"]
    URL --> REQ
    REQ --> API["API server"]
~~~

## 6. Ambassador

~~~mermaid
flowchart LR
    MAIN["Main container"] -->|"HTTP localhost:8001"| AMB["Ambassador: kubectl proxy"]
    AMB -->|"HTTPS + bearer + CA"| API["Kubernetes API server"]
~~~

## 7. Access choice

~~~mermaid
flowchart TD
    N["Need runtime information"] --> Q{"Own Pod/container metadata only?"}
    Q -- yes --> D["Downward API"]
    Q -- no --> A["Kubernetes API"]
    A --> Q2{"Few simple calls?"}
    Q2 -- yes --> H["HTTP / ambassador"]
    Q2 -- no --> L["Client library"]
~~~

## 8. Security boundary

~~~mermaid
flowchart TD
    SA["ServiceAccount identity"] --> RBAC["RBAC authorization"]
    RBAC --> API["API actions"]
    BAD["cluster-admin for all ServiceAccounts"] --> RBAC
    BAD --> RISK["cluster-wide privilege exposure"]
~~~
