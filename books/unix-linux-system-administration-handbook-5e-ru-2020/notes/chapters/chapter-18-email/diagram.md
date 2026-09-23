# Диаграмма: путь сообщения, SMTP и MTA operations

~~~mermaid
flowchart TD
    A["User composes mail in MUA"] --> B["MSA :587"]
    B --> B1["SMTP AUTH + encrypted submission"]
    B1 --> C["Local MTA"]
    C --> D{"Local recipient?"}
    D -->|Yes| E["DA/LDA"]
    E --> F["Message store"]
    F --> G["IMAPS / POP3S"]
    G --> H["Recipient MUA"]

    D -->|No| I["DNS / mail routing"]
    I --> J["Remote MTA :25"]
    J --> K["Remote DA/LDA"]
    K --> L["Remote message store"]

    M["SMTP dialogue"] --> M1["EHLO/HELO"]
    M1 --> M2["MAIL FROM"]
    M2 --> M3["RCPT TO"]
    M3 --> M4["DATA"]
    M4 --> M5["QUIT"]
    M5 --> M6{"Response class"}
    M6 -->|2xx| M7["Success"]
    M6 -->|4xx| M8["Temporary failure / retry"]
    M6 -->|5xx| M9["Permanent failure"]

    N["Read-only diagnosis"] --> N1["Headers / Received"]
    N --> N2["Queue ID / mailq"]
    N --> N3["Logs"]
    N --> N4["DNS MX + firewall"]
    N --> N5["Aliases / lookup tables"]

    O["sendmail"] --> O1["mailq / -bv / version check"]
    O --> O2["sendmail -q / -q -v"]
    O2 --> O3["Queue delivery workload"]

    P["Exim"] --> P1["exim -bv / -bp / -bt"]
    P --> P2["exim -q"]
    P2 --> P3["Queue runner workload"]

    Q["Postfix"] --> Q1["postconf / mailq / qshape"]
    Q --> Q2["postmap / postalias / postsuper"]
    Q2 --> Q3["State-changing table/queue operations"]

    R["Security"] --> R1["Avoid open relay"]
    R --> R2["SPF / DKIM"]
    R --> R3["TLS / STARTTLS"]
    R --> R4["IMAPS / POP3S"]
    R --> R5["File/program aliases are sensitive"]

    S["Test safety"] --> S1["Postfix soft_bounce=yes"]
    S1 --> S2["Disable after testing"]
    S --> S3["Universal config rollback: [Needs confirmation]"]
~~~

## Смысл диаграммы

Глава разделяет транспорт почты на submission, межсерверный SMTP, локальную доставку и доступ к message store. Диагностика должна следовать реальному пути сообщения: заголовки/queue ID → SMTP code → queue/logs → DNS/firewall → routing/aliases → local delivery. Команды sendmail, Exim и Postfix сгруппированы отдельно, потому что их operational syntax различается.
