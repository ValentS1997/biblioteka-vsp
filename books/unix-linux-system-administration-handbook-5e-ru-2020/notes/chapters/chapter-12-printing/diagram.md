# Диаграмма: CUPS pipeline и troubleshooting

~~~mermaid
flowchart TD
    A["User / application"] --> B["lpr / lp / GUI"]
    B --> C["cupsd"]
    C --> D["Print queue"]

    D --> E{"Queue state"}
    E -->|accept + enabled| F["MIME detection"]
    E -->|reject| E1["New jobs refused"]
    E -->|cupsdisable| E2["Jobs queue but output stops"]

    F --> G["PPD + mime.types + mime.convs"]
    G --> H["Filter chain"]
    H --> I["Backend"]
    I --> J{"Destination"}
    J -->|Local| K["USB / parallel / serial printer"]
    J -->|Network| L["IPP / LPD / socket printer/server"]

    K --> M["Physical output"]
    L --> M

    N["Read-only checks"] --> N1["lpstat -t / lpq"]
    N1 --> N2["CUPS logs"]
    N2 --> N3["lpinfo -v"]
    N3 --> N4["USB backend or TCP/631 test"]

    N4 --> O{"Failure layer found?"}
    O -->|Queue/config| P["Adjust accept/reject or enable/disable"]
    O -->|PPD/filter| Q["Correct queue model/filter path"]
    O -->|Backend/network| R["Correct URI/reachability/device path"]
    O -->|Physical| S["Repair/connect printer"]

    P --> T["Submit controlled test job"]
    Q --> T
    R --> T
    S --> T

    T --> U{"Printed correctly?"}
    U -->|Yes| V["Keep + document"]
    U -->|No| N
~~~

## Смысл диаграммы

Глава рассматривает печать как последовательный pipeline. Ошибка должна локализоваться до изменения: queue state, MIME/PPD/filter, backend, network path или physical printer. После изменения нужен controlled test job.
