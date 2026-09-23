# Диаграмма: DNS resolution, authoritative data и BIND changes

~~~mermaid
flowchart TD
    A["Application needs a name"] --> B["Resolver policy: nsswitch.conf"]
    B --> C["Recursive server: resolv.conf"]
    C --> D{"Cached answer?"}
    D -->|Yes| E["Return cached RR until TTL expires"]
    D -->|No| F["Query hierarchy"]
    F --> G["Root"]
    G --> H["TLD"]
    H --> I["Delegated authoritative server"]
    I --> J["Answer / referral / error"]
    J --> K["Cache result"]
    K --> A

    L["Authoritative DNS data"] --> L1["named.conf: role/policy/access/views"]
    L --> L2["Zone files: SOA NS A AAAA PTR MX CNAME SRV TXT"]
    L2 --> L3["SOA serial"]
    L1 --> M["named daemon"]
    L2 --> M
    M --> N["Authoritative answers / zone transfers"]

    O["Read-only checks"] --> O1["dig / drill / host / nslookup / delv"]
    O1 --> O2["Check server directly with @server"]
    O1 --> O3["Trace delegation with +trace / -T"]
    O1 --> O4["Check logs and rndc status"]

    P["Static master-zone change"] --> P1["Edit zone data"]
    P1 --> P2["Increment SOA serial"]
    P2 --> P3["rndc reload"]
    P3 --> P4["Verify master/slave answers with dig"]

    Q["Dynamic-zone manual edit"] --> Q1["rndc freeze zone"]
    Q1 --> Q2["Edit zone file"]
    Q2 --> Q3["rndc thaw zone"]
    Q3 --> Q4["Verify with dig"]

    R["Security policy"] --> R1["Restrict recursion"]
    R --> R2["Restrict zone transfer"]
    R --> R3["Authenticate dynamic updates with TSIG"]
    R --> R4["DNSSEC: keygen → signzone → trust chain"]

    S["Split DNS"] --> S1["Restricted internal view first"]
    S --> S2["External view: public data / no recursion"]

    T["Rollback"] --> T1["freeze → thaw pair is source-supported"]
    T --> T2["Other universal rollback: [Needs confirmation]"]
~~~

## Смысл диаграммы

Глава разделяет client resolution, authoritative zone data и управление BIND. Проверка выполняется query tools и logging; изменение static master zone требует обновления SOA serial и reload; dynamic zone перед ручным редактированием должна быть frozen и затем thawed. Security policy ограничивает recursion/transfers/updates и добавляет TSIG/DNSSEC там, где это требуется.
