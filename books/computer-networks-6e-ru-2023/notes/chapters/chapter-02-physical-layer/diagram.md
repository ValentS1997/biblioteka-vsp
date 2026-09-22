# Диаграмма: локализация физического ограничения

Обязательные узлы CPU, memory и storage сохранены по шаблону, но глава 2 не использует их как ветви диагностики физического уровня. Они явно помечены как неприменимые.

```mermaid
flowchart TD
    symptom["Symptom: низкая скорость, высокая задержка, ошибки или нестабильность физического канала"] --> baseline["Baseline: среда, расстояние, bandwidth, data rate, SNR, duplex и способ доступа"]
    baseline --> resource_localization{"Resource localization: физический канал или внешнее ограничение?"}

    resource_localization --> network["Network: проводная / беспроводная / сотовая / кабельная / спутниковая среда"]
    resource_localization --> external_dependencies["External dependencies: общий сегмент, частотный спектр, регуляторные ограничения, инфраструктура доступа"]
    resource_localization --> cpu["CPU: отдельная диагностическая ветвь главы 2 отсутствует"]
    resource_localization --> memory["Memory: отдельная диагностическая ветвь главы 2 отсутствует"]
    resource_localization --> storage["Storage: отдельная диагностическая ветвь главы 2 отсутствует"]

    network --> targeted_analysis["Targeted analysis: bandwidth/SNR/distance/interference + modulation/multiplexing + access technology"]
    external_dependencies --> targeted_analysis

    targeted_analysis --> capacity_check["Read-only analysis: пределы Найквиста/Шеннона при известных параметрах"]
    targeted_analysis --> medium_check["Read-only analysis: свойства среды и shared/dedicated access"]

    capacity_check --> remeasure["Remeasure/record: сравнить наблюдаемые параметры с физическими ограничениями"]
    medium_check --> remeasure

    targeted_analysis -.-> controlled_change["Controlled change: глава 2 не задает универсальных modifying actions"]
    controlled_change -.-> remeasure

    remeasure --> keep_or_rollback["Keep or rollback: N/A — изменение конфигурации источником не предписано"]
```

## Смысл диаграммы

Логика главы начинается с самой физической среды. Сначала фиксируются свойства канала, затем проверяются фундаментальные ограничения, способ модуляции/мультиплексирования и архитектура доступа. Переход к изменению конфигурации глава не задает; поэтому controlled change и rollback не превращаются в выдуманный tuning.
