# Диаграммы: глава 13 — node и network security

## 1. Default vs host namespaces

~~~mermaid
flowchart LR
    P1["Normal Pod"] --> N1["Pod network/PID/IPC namespaces"]
    P2["hostNetwork/hostPID/hostIPC Pod"] --> H["Worker-node namespaces"]
~~~

## 2. Privilege ladder

~~~mermaid
flowchart TD
    U["ordinary container"] --> C["add specific capabilities"]
    C --> P["privileged container"]
    U --> D["drop unnecessary capabilities"]
    D --> L["lower privilege"]
~~~

## 3. Read-only filesystem

~~~mermaid
flowchart LR
    A["Application"] --> R["read-only root filesystem"]
    A --> V["mounted writable volume"]
    R --> X["write denied"]
    V --> W["write allowed"]
~~~

## 4. PSP admission

~~~mermaid
flowchart LR
    U["User creates Pod"] --> RBAC["RBAC: which PSP may user use?"]
    RBAC --> PSP["PodSecurityPolicy validation/mutation"]
    PSP --> D{"Pod compliant?"}
    D -- yes --> API["Pod accepted"]
    D -- no --> F["Forbidden"]
~~~

## 5. PSP per-user access

~~~mermaid
flowchart LR
    A["Alice"] --> D["default PSP only"]
    B["Bob"] --> D
    B --> P["privileged PSP"]
    D --> NP["non-privileged Pod allowed"]
    P --> PP["privileged Pod allowed"]
~~~

## 6. NetworkPolicy target selection

~~~mermaid
flowchart LR
    NP["NetworkPolicy"] --> T["podSelector selects target Pods"]
    S1["podSelector source"] --> I["ingress rule"]
    S2["namespaceSelector source"] --> I
    S3["ipBlock source"] --> I
    I --> T
~~~

## 7. Database ingress isolation

~~~mermaid
flowchart LR
    W["Pod app=webserver"] -->|"TCP 5432"| D["Pod app=database"]
    O["other Pods"] -. denied .-> D
~~~

## 8. Egress restriction

~~~mermaid
flowchart LR
    W["Pods app=webserver"] -->|"allowed"| D["Pods app=database"]
    W -. denied .-> O["other Pods / destinations"]
~~~
