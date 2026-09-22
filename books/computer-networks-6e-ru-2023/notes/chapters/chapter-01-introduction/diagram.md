# Диаграмма: декомпозиция сетевого вопроса по главе 1

Шаблон артефактов требует узлы CPU, memory и storage. Глава 1 не использует их как отдельные диагностические ветви, поэтому они отмечены как неприменимые и не снабжены вымышленными проверками.

```mermaid
flowchart TD
    symptom["Symptom: наблюдаемое сетевое поведение или вопрос"] --> baseline["Baseline: приложение, тип сети, масштаб, метрики и требования"]
    baseline --> resource_localization{"Resource localization: локализовать тему по архитектуре главы"}

    resource_localization --> network["Network: физический → канальный → сетевой → транспортный → прикладной"]
    resource_localization --> external_dependencies["External dependencies/context: другие сети, ISP, стандарты, безопасность и приватность"]
    resource_localization --> cpu["CPU: отдельная диагностическая ветвь в главе 1 отсутствует"]
    resource_localization --> memory["Memory: отдельная диагностическая ветвь в главе 1 отсутствует"]
    resource_localization --> storage["Storage: отдельная диагностическая ветвь в главе 1 отсутствует"]

    network --> targeted_analysis["Targeted analysis: служба vs протокол; тип соединения; задержка vs пропускная способность"]
    external_dependencies --> targeted_analysis

    targeted_analysis --> ping_check["Read-only/workload check: ping для RTT"]
    targeted_analysis --> browser_check["Read-only check: Browser DevTools Network"]

    ping_check --> remeasure["Remeasure/record: сравнить полученные RTT"]
    browser_check --> remeasure["Remeasure/record: зафиксировать количество и типы запросов"]

    targeted_analysis -.-> controlled_change["Controlled change: в главе 1 не предусмотрен"]
    controlled_change -.-> remeasure

    remeasure --> keep_or_rollback["Keep or rollback: N/A — modifying action отсутствует"]
```

## Смысл диаграммы

Рабочая логика главы — классифицировать сеть и функцию по масштабу, технологии, службам и уровням, а затем переходить к соответствующему уровню архитектуры. CPU, memory, storage, controlled change и rollback не представлены в главе как части диагностической методологии; они сохранены только как обязательные узлы шаблона и явно помечены как неприменимые.
