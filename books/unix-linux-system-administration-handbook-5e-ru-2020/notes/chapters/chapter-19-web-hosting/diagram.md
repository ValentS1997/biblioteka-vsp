# Диаграмма: HTTP request path и web-hosting control points

~~~mermaid
flowchart TD
    A["Client request"] --> B["DNS"]
    B --> C{"HTTPS?"}
    C -->|Yes| D["TLS + SNI"]
    C -->|No| E["HTTP"]
    D --> F["Load balancer / reverse proxy"]
    E --> F

    F --> G{"Cached response?"}
    G -->|Yes| H["Return cached response"]
    G -->|No| I["Web server"]
    I --> J{"Static resource?"}
    J -->|Yes| K["Serve file"]
    J -->|No| L["Application server"]
    L --> M["Database / backend"]
    M --> N["Build response"]
    K --> N
    N --> O["Cache / proxy layers"]
    O --> A

    P["Read-only checks"] --> P1["curl verbose / custom Host"]
    P --> P2["origin vs cache comparison"]
    P --> P3["httpd -t / apachectl status"]
    P --> P4["nginx -t"]
    P --> P5["logs / health status"]

    Q["Apache change"] --> Q1["Syntax check"]
    Q1 --> Q2["Edit config"]
    Q2 --> Q3["apachectl graceful"]
    Q3 --> Q4["Verify HTTP and logs"]

    R["NGINX"] --> R1["server / location / proxy_pass"]
    R --> R2["upstream pool + health checks"]

    S["HAProxy"] --> S1["frontend"]
    S1 --> S2["backend"]
    S2 --> S3["health checks"]
    S3 --> S4["remove/re-add backend"]
    S --> S5["TLS termination / sticky cookie"]

    T["Security boundaries"] --> T1["No Basic Auth without HTTPS"]
    T --> T2["Protect private keys"]
    T --> T3["Disable obsolete SSL"]
    T --> T4["Logs and caches need resource controls"]

    U["Rollback"] --> U1["Narrow inverse actions only where supported"]
    U --> U2["Universal config rollback: [Needs confirmation]"]
~~~

## Смысл диаграммы

Глава рассматривает web hosting как цепочку независимых control/failure domains. Диагностика начинается с фактического HTTP response и движется внутрь: DNS/TLS → load balancer/cache → web server → application/backend. Изменения Apache/NGINX/HAProxy не следует смешивать; сначала выполняются source-supported read-only checks.
