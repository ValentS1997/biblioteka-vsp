# Диаграмма: настройка системы по главе 7

## Logging flow

~~~mermaid
flowchart LR
    APP["service / daemon / kernel"] --> J["journald"]
    APP --> S["syslog interface"]
    J --> JC["journalctl filters"]
    S --> RS["rsyslog/syslogd"]
    RS --> LF["/var/log files"]
    LF --> LR["logrotate"]
~~~

## Scheduled jobs

~~~mermaid
flowchart TB
    TASK["Task"] --> C{"Recurring or one-time?"}
    C -->|Recurring| CR["cron / crontab"]
    C -->|Recurring| ST["systemd timer"]
    C -->|One-time| AT["at"]
    C -->|One-time| SR["systemd-run transient timer"]

    ST --> TU["timer unit"]
    TU --> SU["service unit"]
    SU --> PROC["process in cgroup"]
~~~

## User identity and privilege

~~~mermaid
flowchart LR
    NAME["login name"] --> DB["user database"]
    DB --> UID["UID / GID"]
    UID --> R["RUID: original identity"]
    R --> P["process"]
    SET["setuid executable / setuid()"] --> E["EUID: effective identity"]
    E --> P
    P --> AUTHZ["kernel permission checks"]
~~~

## Authentication concepts

~~~mermaid
flowchart LR
    ID["Identification<br/>Who are you?"] --> AUTH["Authentication<br/>Prove it"]
    AUTH --> AZ["Authorization<br/>May you do this?"]
    AZ --> APP["Application action"]
~~~

## PAM flow

~~~mermaid
flowchart TB
    APP["Application: login/chsh/etc."] --> FUNC["PAM function<br/>auth/account/session/password"]
    FUNC --> R1["configured rule 1"]
    R1 --> R2["configured rule 2"]
    R2 --> RN["..."]
    RN --> RESULT["success / failure"]

    R1 -.-> M1["PAM module"]
    R2 -.-> M2["PAM module"]
~~~

Control arguments determine whether evaluation stops or continues.

## Getty login flow

~~~mermaid
flowchart LR
    G["getty / agetty"] --> L["login"]
    L --> PAM["PAM authentication"]
    PAM --> SH["exec user shell"]
~~~
