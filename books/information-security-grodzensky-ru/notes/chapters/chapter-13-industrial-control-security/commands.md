# Средства и механизмы главы 13

Shell-команд в главе нет.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| Passive sniffer / traffic analyzer | Щадящий анализ АСУ ТП | read-only/observability | Анализирует traffic headers/versions без активного сканирования | Asset/version visibility | [Not applicable] |
| Data diode | Односторонняя связь | stateful/network | Блокирует обратный трафик в архитектуре источника | Directionality check | [Needs confirmation] |
| Industrial firewall | Защита PLC/network segment | state-changing | Анализирует industrial protocols и signatures | Policy/event verification | [Needs confirmation] |
| IDS/IPS | Detection/prevention | monitor/block | Выявляет/блокирует атаки | Alert/block status | [Needs confirmation] |
| Traffic monitoring / incident management | Visibility + response | observability | Inventory, unauthorized-control detection, investigation | Events/inventory | [Not applicable] |
| Network segmentation | Изоляция зон | state-changing | Разделяет corporate и ASU TP segments | Reachability/policy verification | [Needs confirmation] |
| DLP | Контроль утечек | monitor/block | Дополнительная мера из общего перечня | Events | [Needs confirmation] |
| Antivirus | Malware protection | monitor/prevent | Контроль вредоносного ПО | Protection status | [Needs confirmation] |
| Vulnerability analysis | Анализ защищённости | workload-sensitive | Оценка уязвимостей; active method может быть рискован | Findings + impact check | [Not applicable] |
| Code scanner | Анализ ПО | read-only/analysis | Ищет дефекты/уязвимости кода | Findings | [Not applicable] |
| Crypto protection | Защита каналов | stateful | Защищает communication channels | Connection/status verification | [Needs confirmation] |
| Authentication | Контроль доступа | stateful/auth | Идентифицирует и аутентифицирует субъектов | Auth result | [Needs confirmation] |
| Trusted boot | Контроль загрузки | stateful/platform | Обеспечивает доверенную загрузку | Boot-state check | [Needs confirmation] |
| Removable-media control | Контроль носителей | stateful/control | Ограничивает использование съёмных носителей | Policy result | [Needs confirmation] |

## Industrial protocols, названные в главе

- MODBUS;
- DNP3;
- CIP.

## Operational boundary

- packet crafting, exploit steps и active-scanning commands не добавлялись;
- vendor-specific rules отсутствуют;
- passive analysis показан только как source-derived подход для снижения operational risk.
