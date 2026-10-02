# Средства и контрольные механизмы главы 14

Shell-команд в главе нет.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| SIEM | Источник событий/инцидентов | observability | Собирает события для monitoring/reporting | Event ingestion | [Not applicable] |
| SOC | Центр мониторинга и реагирования | process | Анализирует и обрабатывает инциденты | Incident workflow | [Not applicable] |
| Specialized reporting portal | Передача сведений | process/integration | Получает данные от SIEM/SOC/ИБ и передаёт далее в модели главы | Delivery/status check | [Needs confirmation] |
| Access control | Защита значимых объектов | state-changing | Ограничивает доступ | Access verification | [Needs confirmation] |
| Identification & authentication | Контроль субъектов | state-changing | Проверяет identity | Auth result | [Needs confirmation] |
| Application restriction | Ограничение программной среды | state-changing | Ограничивает допустимое ПО | Policy check | [Needs confirmation] |
| Antivirus | Malware protection | monitor/prevent | Защищает от вредоносного ПО | Protection status | [Needs confirmation] |
| Physical access control | Организационно-техническая мера | state-changing | Ограничивает физический доступ | Access records | [Needs confirmation] |
| Controlled zone | Организационная мера | process | Формирует защищаемую физическую зону | Audit/inspection | [Needs confirmation] |

## Нормативные элементы, перечисленные в главе

- Федеральный закон №187-ФЗ;
- Постановление Правительства РФ №127;
- Приказ ФСТЭК России №235;
- Приказ ФСТЭК России №236;
- Приказ ФСТЭК России №239.

## Operational boundary

- CLI/API отсутствуют.
- Текущие forms/endpoints для передачи сведений не добавлялись.
- Правовые требования не актуализировались внешними источниками.
