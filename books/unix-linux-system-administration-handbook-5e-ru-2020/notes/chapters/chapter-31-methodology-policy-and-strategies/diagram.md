# Диаграмма: socio-technical operations lifecycle

~~~mermaid
flowchart TD
    A["Business / user goal"] --> B["Shared Dev + Ops ownership"]

    B --> C["CLAMS"]
    C --> C1["Culture"]
    C --> C2["Lean"]
    C --> C3["Automation"]
    C --> C4["Measurement"]
    C --> C5["Sharing"]

    B --> D["Work management"]
    D --> D1["Ticket intake"]
    D1 --> D2["Human acknowledgement"]
    D2 --> D3["One owner"]
    D3 --> D4["Prioritize / resolve"]
    D4 --> D5["Searchable history"]

    B --> E["Knowledge and change"]
    E --> E1["Documentation"]
    E --> E2["Infrastructure as code"]
    E2 --> E3["Versioned change"]
    E3 --> E4["Development"]
    E4 --> E5["Test"]
    E5 --> E6["Production"]
    E6 --> E7["Measure / monitor"]
    E7 --> E3

    B --> F["Governance"]
    F --> F1["Policy"]
    F1 --> F2["Procedure"]
    F --> F3["SLA"]
    F --> F4["Compliance / legal"]
    F4 --> F5["Current applicability check"]

    B --> G["Resilience"]
    G --> G1["Risk assessment"]
    G1 --> G2["DR plan"]
    G2 --> G3["Offline recovery data"]
    G3 --> G4["Named recovery leader"]
    G4 --> G5["Exercise / recovery"]
    G5 --> G6["Return to normal"]

    D5 --> H["Continuous learning"]
    E7 --> H
    G6 --> H
    H --> B
~~~

## Логика

Глава рассматривает системное администрирование как socio-technical discipline. Работа, изменения, документация, SLA, политика и recovery связаны общими принципами: ownership, traceability, measurable outcomes и continuous learning. Инструменты — средство реализации, а не центр методологии.
