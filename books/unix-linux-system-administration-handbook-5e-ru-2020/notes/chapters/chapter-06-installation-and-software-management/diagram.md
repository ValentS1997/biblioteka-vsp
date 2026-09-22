# Диаграмма: от provisioning до controlled rollout

~~~mermaid
flowchart TD
    A["Нужно установить или обновить ПО"] --> B{"Новая система или существующая?"}

    B -->|Новая система| P["Provisioning"]
    P --> P1["PXE: DHCP → TFTP → image server"]
    P1 --> P2{"Installer family"}
    P2 -->|Red Hat/CentOS| P3["Kickstart / ks.cfg"]
    P2 -->|Debian/Ubuntu| P4["preseed / debconf"]
    P2 -->|FreeBSD| P5["custom image / bsdinstall"]
    P3 --> L
    P4 --> L
    P5 --> L

    B -->|Существующая система| S["Package management"]

    S --> S1{"Platform"}
    S1 -->|RPM Linux| R["rpm → APT/yum high-level layer"]
    S1 -->|Debian/Ubuntu| D["dpkg → APT"]
    S1 -->|FreeBSD| F["base + pkg + ports"]

    R --> Q
    D --> Q
    F --> Q

    L["Localization / local config"] --> Q["Change control"]

    Q --> T["Test limited scope"]
    T --> U{"Результат приемлем?"}
    U -->|Нет| X["Rollback / fix / [Needs confirmation]"]
    X --> T
    U -->|Да| G["Staged rollout by groups"]
    G --> C["Critical systems last"]
    C --> V["Verify + document + user feedback"]

    S --> M["Repository / mirror / dependencies"]
    M --> T
~~~

## Смысл диаграммы

Глава объединяет installation и package management в один управляемый pipeline. Инструменты различаются по платформам, но control plane один: источник → dependency model → reproducible configuration → testing → staged rollout → verification.
