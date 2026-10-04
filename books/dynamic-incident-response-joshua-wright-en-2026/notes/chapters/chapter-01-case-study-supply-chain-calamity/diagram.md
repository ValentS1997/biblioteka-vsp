# Диаграмма: почему локальный cleanup не равен incident closure

```mermaid
flowchart TD
    A["Gilded Freight SDK supply-chain compromise"] --> B["Jordan installs/updates SDK"]
    B --> C["ms: 127.0.0.1:8080"]
    B --> D["ssupd/Tor: 0.0.0.0:9150"]
    D --> E["Filesystem access + SOCKS pivot"]

    E --> F["SSH private key + known_hosts"]
    E --> G["Database credential"]
    E --> H["AWS credentials"]

    F --> I["Internal dev servers"]
    I --> J["Additional credentials / CI/CD access"]

    H --> K["AWS enumeration"]
    K --> L["S3 customer data + algorithm assets"]
    K --> M["Attacker-controlled EC2"]
    L --> N["Staging / exfiltration"]
    M --> N

    C --> O["Jordan detects port conflict"]
    D --> O
    O --> P["killall processes"]
    P --> Q["rm -fr /opt/gilded"]
    Q --> R["Local activity disappears"]

    R --> S["Six days later: Sam investigates workstation"]
    S --> T["Processes/listeners absent"]
    S --> U["Historical logs reviewed"]
    S --> V["Persistence checks clean"]
    S --> W["Malware scan clean"]

    T --> X["Ticket closed"]
    U --> X
    V --> X
    W --> X

    X -. misses .-> Y["Other SDK installations"]
    X -. misses .-> Z["SSH key use on internal hosts"]
    X -. misses .-> AA["AWS/CloudTrail activity"]
    X -. misses .-> AB["Running EC2 resource"]
    X -. misses .-> AC["Active stolen DB credentials"]

    N --> AD["Actual breach persists beyond workstation"]

    style X stroke-width:3px
    style AD stroke-width:3px
```

## Interpretation

Глава строит две параллельные линии:

1. **что видно defender'у локально**;
2. **что attacker уже успел сделать за пределами initial host**.

Локальная cleanup действительно прекращает работу обнаруженного implant на workstation. Ошибка возникает позже, когда это локальное состояние принимают за границу всего incident.

Ключевой переход:

```text
initial indicator
      ↓
attacker capability
      ↓
credentials / trust paths
      ↓
downstream systems
      ↓
cloud / data / persistence
```

Если investigation останавливается после первого блока, реальный scope остаётся неизвестным.
