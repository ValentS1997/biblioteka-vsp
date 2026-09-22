# Диаграмма: диагностика загрузки и системных демонов

```mermaid
flowchart TD
    symptom["Symptom: boot failure или service failure"] --> baseline["Baseline: last known good, recent change, previous kernel, snapshot, journal"]
    baseline --> resource_localization{"Resource localization: на каком этапе ломается цепочка?"}

    resource_localization --> firmware["Firmware / UEFI"]
    resource_localization --> bootloader["Bootloader: GRUB / FreeBSD loader"]
    resource_localization --> kernel["Kernel / root filesystem"]
    resource_localization --> pid1["PID 1: systemd / init / FreeBSD rc"]
    resource_localization --> network["Network/service dependency"]
    resource_localization --> storage["Storage: ESP / boot disk / root filesystem"]
    resource_localization --> external_dependencies["External dependencies: cloud console / recovery instance / attached volume"]

    resource_localization -.-> cpu["CPU: отдельная диагностическая ветвь в главе 2 не задана"]
    resource_localization -.-> memory["Memory: отдельная диагностическая ветвь в главе 2 не задана"]

    firmware --> targeted_analysis["Targeted analysis"]
    bootloader --> targeted_analysis
    kernel --> targeted_analysis
    pid1 --> targeted_analysis
    network --> targeted_analysis
    storage --> targeted_analysis
    external_dependencies --> targeted_analysis

    targeted_analysis --> read_only["Read-only: efibootmgr -v / systemctl status / journalctl / disk discovery"]
    read_only --> decision{"Причина подтверждена?"}

    decision -->|Нет| recovery["Recovery path: previous kernel / rescue / emergency / recovery image"]
    decision -->|Да| controlled_change["Controlled change: BootOrder / GRUB / unit override / target / filesystem repair"]

    recovery --> remeasure["Remeasure: boot, status, journal"]
    controlled_change --> remeasure

    remeasure --> verify{"Система загружается и нужные services active?"}
    verify -->|Да| keep_or_rollback["Keep: документировать known-good state"]
    verify -->|Нет| rollback["Rollback: previous kernel / previous target / snapshot или [Needs confirmation]"]
    rollback --> resource_localization
```

## Смысл диаграммы

Глава предлагает мыслить по слоям загрузки. Неисправность firmware, bootloader, kernel, root filesystem и PID 1 требует разных проверок. Сначала собираются наблюдаемые данные, затем выполняется локальное изменение только в подтверждённом слое, после чего состояние проверяется повторной загрузкой, status/journal или recovery boot.

Узлы CPU и memory сохранены из общего artifact template, но явно помечены как неиспользуемые отдельные ветви: глава 2 не задаёт CPU/memory troubleshooting как часть boot workflow.
