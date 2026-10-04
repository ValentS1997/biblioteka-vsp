# Диаграммы: глава 12 — API security и RBAC

## 1. Authentication to authorization

~~~mermaid
flowchart LR
    R["API request"] --> A["Authentication plugins"]
    A --> I["Identity + groups"]
    I --> Z["Authorization plugin / RBAC"]
    Z --> D{"Allowed?"}
    D -- yes --> API["API operation"]
    D -- no --> F["Forbidden"]
~~~

## 2. Pod identity

~~~mermaid
flowchart LR
    P["Pod"] --> SA["ServiceAccount"]
    SA --> T["token"]
    T --> API["API server authentication"]
    API --> U["system:serviceaccount:namespace:name"]
~~~

## 3. RBAC object model

~~~mermaid
flowchart TD
    R["Role"] --> RB["RoleBinding"]
    CR["ClusterRole"] --> RB
    CR --> CRB["ClusterRoleBinding"]
    RB --> S["User / Group / ServiceAccount"]
    CRB --> S
~~~

## 4. Namespaced Role

~~~mermaid
flowchart LR
    SA["foo:default"] --> B["RoleBinding in foo"]
    B --> R["Role service-reader in foo"]
    R --> RES["Services in foo"]
~~~

## 5. Reusable ClusterRole with RoleBinding

~~~mermaid
flowchart LR
    SA["foo:default"] --> B["RoleBinding in foo"]
    B --> CR["ClusterRole view"]
    CR --> RES["namespaced resources in foo only"]
~~~

## 6. Cluster-wide ClusterRoleBinding

~~~mermaid
flowchart LR
    SA["foo:default"] --> B["ClusterRoleBinding"]
    B --> CR["ClusterRole view / pv-reader"]
    CR --> ALL["all namespaces or cluster-scoped resources"]
~~~

## 7. Privilege escalation boundary

~~~mermaid
flowchart TD
    S["Secret read"] --> T["obtain higher-privilege token"]
    T --> E["impersonate higher-privilege identity"]
    E --> P["privilege escalation"]
    C["cluster-admin binding"] --> P
~~~

## 8. Least privilege

~~~mermaid
flowchart LR
    A["workload A"] --> SA1["ServiceAccount A"]
    SA1 --> R1["minimal read Role"]
    B["workload B"] --> SA2["ServiceAccount B"]
    SA2 --> R2["minimal write Role"]
~~~
