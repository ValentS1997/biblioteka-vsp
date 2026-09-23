# Диаграмма: data-center reliability stack

~~~mermaid
flowchart TD
    A["Service reliability"] --> B["Physical infrastructure"]

    B --> C["Rack / cabling"]
    B --> D["Power"]
    B --> E["Cooling / environment"]
    B --> F["Network connectivity"]
    B --> G["Physical security"]
    B --> H["Operations / tools"]

    C --> C1["Traceable rack layout"]
    C --> C2["Accessible cable paths"]

    D --> D1["Utility power"]
    D1 --> D2["UPS"]
    D2 --> D3["Generator / alternate source"]
    D3 --> D4["Rack distribution"]
    D4 --> D5["Measured device load"]

    E --> E1["Heat-load estimate"]
    E1 --> E2["Hot / cold aisle airflow"]
    E2 --> E3["Temperature / humidity monitoring"]
    E3 --> E4["Remote environmental alert"]

    G --> G1["Site risk"]
    G1 --> G2["Perimeter"]
    G2 --> G3["Facility MFA / guards"]
    G3 --> G4["Rack / cage access"]
    G4 --> G5["Surveillance"]

    D --> I{"Backup path tested?"}
    E --> J{"Environmental monitoring works?"}
    G --> K{"Access controls verified?"}

    I -->|No| L["Do not assume redundancy"]
    J -->|No| M["Blind environmental failure risk"]
    K -->|No| N["Physical security gap"]

    I -->|Yes| O["Known power resilience"]
    J -->|Yes| O
    K -->|Yes| O

    O --> P["Operate and remeasure"]
    P --> Q["Capacity / risk review"]
    Q --> B
~~~

## Логика

Глава связывает service reliability с физическим стеком: racks, power, cooling, connectivity, physical security и operational discipline. Redundancy считается подтверждённой только после measurement/testing; environmental and access controls также должны проверяться, а не существовать только на схеме.
