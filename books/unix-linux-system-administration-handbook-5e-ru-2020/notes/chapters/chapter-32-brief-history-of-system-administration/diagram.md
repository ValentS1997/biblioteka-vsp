# Диаграмма: evolution of system administration

~~~mermaid
flowchart LR
    A["1952–1960<br/>System operators"] --> B["1961–1969<br/>Time-sharing"]
    B --> C["1969–1973<br/>UNIX birth"]
    C --> D["1974–1990<br/>UNIX / BSD spread"]
    D --> E["1980s<br/>System administrator profession"]
    E --> F["Documentation / training / communities"]
    F --> G["1991–1995<br/>Linux emergence"]
    G --> H["1996–1999<br/>Windows growth"]
    H --> I["2000–2009<br/>Mixed platforms"]
    I --> J["2010–publication era<br/>Virtualization / cloud"]
    J --> K["IoT / distributed systems"]

    C --> C1["Small tools"]
    C1 --> C2["Text streams"]
    C2 --> C3["Composition / pipes"]

    D --> D1["Universities"]
    D1 --> D2["BSD"]
    D2 --> D3["TCP/IP sockets"]

    E --> E1["Troubleshooting"]
    E --> E2["Users"]
    E --> E3["Backups / storage"]
    E --> E4["Local tools / standards"]

    J --> J1["API-driven infrastructure"]
    J --> J2["Automation"]
    J --> J3["Fleet-scale monitoring"]

    K --> L["Enduring role"]
    L --> L1["Reliability"]
    L --> L2["Security"]
    L --> L3["Knowledge sharing"]
    L --> L4["Adaptation"]
~~~

## Логика

Раздел показывает не замену профессии новыми технологиями, а расширение масштаба: от оператора одной специализированной машины к администратору общей UNIX-среды, затем к multi-platform, cloud и distributed infrastructure. Через все этапы сохраняются reliability, troubleshooting, users и knowledge sharing.
