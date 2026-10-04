# Диаграммы: глава 7 — configuration flow

## 1. Configuration hierarchy

~~~mermaid
flowchart LR
    I["Container image"] --> C["command / args"]
    C --> E["env variables"]
    E --> CM["ConfigMap"]
    CM --> S["Secret"]
~~~

## 2. ConfigMap consumption

~~~mermaid
flowchart LR
    CM["ConfigMap"] --> K["configMapKeyRef"]
    CM --> EF["envFrom"]
    CM --> V["configMap volume"]
    K --> ENV1["single env var"]
    EF --> ENV2["many env vars"]
    V --> F["files"]
~~~

## 3. ConfigMap update

~~~mermaid
flowchart LR
    EDIT["kubectl edit configmap"] --> CM["ConfigMap new data"]
    CM --> DIR["new data directory"]
    DIR --> LINK["atomic ..data symlink switch"]
    LINK --> FILES["mounted files"]
    FILES --> APP["application"]
    APP --> RELOAD["application-specific reload"]
~~~

## 4. Secret consumption

~~~mermaid
flowchart LR
    S["Secret"] --> V["secret volume"]
    S --> ENV["secretKeyRef"]
    V --> F["decoded file"]
    ENV --> EV["env variable"]
    F --> APP["application"]
    EV --> APP
~~~

Source recommends volume for sensitive values.

## 5. HTTPS example

~~~mermaid
flowchart LR
    CM["ConfigMap: nginx config"] --> CV["config volume"]
    SEC["Secret: cert + private key"] --> SV["secret volume"]
    CV --> N["Nginx container"]
    SV --> N
    N --> HTTPS["HTTPS listener"]
~~~

## 6. Private registry

~~~mermaid
flowchart LR
    CRED["Registry credentials"] --> S["docker-registry Secret"]
    S --> IPS["Pod imagePullSecrets"]
    IPS --> K["Kubernetes image pull"]
    K --> R["Private registry"]
~~~

## 7. Security decision

~~~mermaid
flowchart TD
    D["Configuration data"] --> Q{"Sensitive?"}
    Q -- no --> CM["ConfigMap"]
    Q -- yes --> SEC["Secret"]
    SEC --> Q2{"Delivery method?"}
    Q2 -- file --> V["Secret volume — preferred by source"]
    Q2 -- env --> E["Environment variable — leak risk"]
~~~
