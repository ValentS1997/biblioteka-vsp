# Диаграмма: от обнаружения устройства до kernel recovery

~~~mermaid
flowchart TD
    A["Hardware / kernel problem"] --> B["Observe first"]
    B --> B1["uname -r"]
    B --> B2["dmesg / journal"]
    B --> B3["sysfs / udevadm / lsusb"]
    B --> B4["lsmod / kldstat / sysctl"]

    B1 --> C{"Что меняем?"}
    B2 --> C
    B3 --> C
    B4 --> C

    C -->|Device naming/event| D["udev / devfs / devd rule"]
    C -->|Runtime behavior| E["sysctl / procfs"]
    C -->|Driver| F["loadable module"]
    C -->|Kernel feature/build| G["custom kernel"]

    D --> D1["reload rules"]
    D1 --> D2["attach/detach test"]
    D2 --> H["Verify actual device behavior"]

    E --> E1["apply one runtime value"]
    E1 --> E2["verify behavior"]
    E2 --> H

    F --> F1["load module"]
    F1 --> F2["check references/device"]
    F2 --> H

    G --> G1["configure/build/install"]
    G1 --> G2["preserve known-good fallback"]
    G2 --> G3["boot custom kernel"]
    G3 --> H

    H --> I{"Healthy?"}
    I -->|Yes| J["Keep + document persistent state"]
    I -->|No| K["Rollback to previous value/module/fallback kernel"]

    K --> L["Capture diagnostics"]
    L --> L1["dmesg / stack trace / crash dump"]
    L1 --> M["Analyze panic/oops/root cause"]
~~~

## Смысл диаграммы

Глава последовательно ведет от read-only observation к минимальному изменению. Чем ближе действие к ядру, тем важнее known-good fallback. Для failures диагностические данные нужно собрать до следующего изменения.
