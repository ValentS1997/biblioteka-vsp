# Диаграмма: logging pipeline от события до retention

~~~mermaid
flowchart TD
    A["Event source"] --> B{"Источник"}
    B -->|systemd-aware / stdout / /dev/log| J["systemd-journald"]
    B -->|Syslog API / socket / file| R["rsyslog"]
    B -->|Kernel| K["kernel ring buffer"]
    B -->|Daemon-specific file| F["local text log"]

    K --> J
    K --> D["dmesg / journalctl -k"]

    J --> Q["journalctl query/filter"]
    J --> I{"Интеграция с Syslog"}
    I -->|socket forwarding| R
    I -->|journal API| R

    R --> RF["filter: facility / severity / properties"]
    RF --> O{"Action"}
    O -->|local file| F
    O -->|remote TCP/UDP/TLS| C["central collector"]

    F --> L["logrotate / newsyslog"]
    L --> A1["archive / compression / expiry"]

    C --> S["search / indexing / analysis"]
    S --> E["ELK / Graylog / managed logging"]
    E --> A1

    A1 --> P["Retention policy"]
    P --> P1["business / security / compliance"]
    P1 --> X["Access control + audit of log access"]

    Y["Health monitoring"] --> F
    Y --> J
    Y --> C
    Y --> L

    T["Test event: logger"] --> R
    X --> Z["End-to-end verification"]
    T --> Z
~~~

## Смысл диаграммы

Глава рассматривает logging как end-to-end pipeline. Диагностика должна определить, на каком слое теряется событие: source, collector, filtering/routing, storage, central transport, rotation или retention. Изменения проверяются тестовым событием и наблюдением конечного destination.
