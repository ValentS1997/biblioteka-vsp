# Диаграмма: диагностика канального уровня

CPU, memory и storage сохранены как обязательные узлы schema, но глава 3 не рассматривает их как независимые bottleneck-ветви. Они отмечены как неприменимые.

```mermaid
flowchart TD
    symptom["Symptom: framing error, corruption, loss/duplicate/reorder, receiver overflow или низкая link efficiency"] --> baseline["Baseline: framing, checksum/CRC, ACK/NAK, timeout, sequence space, sender/receiver windows"]
    baseline --> resource_localization{"Resource localization: физика канала, канальный протокол или внешняя конкуренция?"}

    resource_localization --> network["Network: data-link framing, error control, flow control, sliding window"]
    resource_localization --> external_dependencies["External dependencies: свойства физического канала, peer behavior, shared-medium access"]
    resource_localization --> cpu["CPU: отдельная диагностическая ветвь главы 3 отсутствует"]
    resource_localization --> memory["Memory: отдельная ресурсная ветвь главы 3 отсутствует"]
    resource_localization --> storage["Storage: отдельная диагностическая ветвь главы 3 отсутствует"]

    network --> targeted_analysis["Targeted analysis: frame boundary → integrity → ACK/timeout/sequence → flow/window"]
    external_dependencies --> targeted_analysis

    targeted_analysis --> framing_check["Read-only: проверить byte/bit stuffing, flags и восстановление границ"]
    targeted_analysis --> error_check["Read-only: проверить checksum/CRC/FEC результат"]
    targeted_analysis --> delivery_check["Read-only: проверить ACK/NAK, timeout, duplicates и ordering"]
    targeted_analysis --> window_check["Read-only: проверить sender/receiver window и retransmission strategy"]

    framing_check --> remeasure["Remeasure/record: повторно проверить semantics протокола"]
    error_check --> remeasure
    delivery_check --> remeasure
    window_check --> remeasure

    targeted_analysis -.-> controlled_change["Controlled change: универсальная modifying action в главе отсутствует"]
    controlled_change -.-> remeasure

    remeasure --> keep_or_rollback["Keep or rollback: N/A — источник не задает эксплуатационного изменения"]
```

## Смысл диаграммы

Диагностика следует структуре главы: сначала определить корректность framing, затем целостность фрейма, после этого проверить подтверждения/таймеры/порядковые номера и только затем — flow control и эффективность sliding window. Проблемы физической среды относятся к главе 2, а конкуренция за общую среду — к главе 4.
