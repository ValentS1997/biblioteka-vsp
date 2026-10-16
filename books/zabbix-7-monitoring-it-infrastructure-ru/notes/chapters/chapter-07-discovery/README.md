# Глава 7. Использование службы Discovery в Zabbix

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», третье обновлённое русское издание (2025). Inventory **0020**, book ID `zabbix-7-monitoring-it-infrastructure-ru`.

## Provenance, источник и границы

- **RAG-only**: только Git-hosted книжный RAG с `rag/acceptance.yaml: ACCEPTED`. Ни исходный PDF напрямую, ни ссылки на Packt/Zabbix/Oracle, ни память модели не использовались для восполнения фактов.
- **PDF pages 291–335**, chunks `zabbix-7-monitoring-it-infrastructure-ru:p0291:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0335:c01`; [заголовок главы 7](../../../rag/chunks/p0201-p0300/p0291-c01.md), [глава 8 начинается на p0336](../../../rag/chunks/p0301-p0400/p0336-c01.md).
- Канонический source SHA-256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Значения полей UI из рисунков 7.1–7.72, отсутствующие в тексте RAG, помечены `RAG_MISS`; по общим знаниям конфигурация не достраивается.

## Структура главы

| Раздел | Страницы PDF | Что автоматизируется |
|---|---:|---|
| Настройка сетевого обнаружения Zabbix agent | 292–298 | IP-range discovery по `agent.hostname`; обнаружение Linux/Windows, Discovery actions и host group/template |
| Работа с сетевым обнаружением Zabbix SNMP | 298–303 | Проверки `SNMPv2 agent` с `sysName` и признаками ОС, Discovery action |
| Автоматизация создания узлов через авторегистрацию | 303–308 | `ServerActive`, Autoregistration actions, группы и активные agent templates; HostMetadata |
| Обнаружение счетчиков производительности Windows | 308–315 | `perfmon.exe`, `perf_instance.discovery[Processor]`, `{#INSTANCE}`, item prototypes |
| Обнаружение объектов в JMX | 315–320 | `jmx.discovery[beans,"*:type=MemoryPool,name=*"]`, `{#JMXNAME}` и атрибут `Type` |
| Низкоуровневое SNMP-обнаружение по-новому | 320–327 | `SNMP interfaces bulk`, GetBulk, dependent LLD, SNMP walk-to-JSON, `{#IFDESCR}`/`{#SNMPINDEX}` |
| Создание узлов сети с помощью LLD и пользовательского JSON | 327–335 | `zabbix_sender` → trapper raw JSON → LLD macro paths → host prototypes |

## Три разных механизма, которые нельзя путать

**Network discovery**: Zabbix server сканирует заданный диапазон адресов и выполняет проверки. Для Agent 2 книга использует `agent.hostname` и условия `lnx`/`win`, service type `Zabbix Agent` и `Discovery status = UP`; действие создаёт host, подключает host group и template. Частота сканирования влияет на нагрузку: учебные 5 минут могут быть заменены более длинным интервалом, например 1 час ([p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0298](../../../rag/chunks/p0201-p0300/p0298-c01.md)).

**SNMP network discovery**: тот же контур scan → checks → Discovery actions, но используются SNMP agent checks и OID. В тексте книги SNMPv2 check получает `sysName` с `.1.3.6.1.2.1.1.5.0`, второй OID `.1.3.6.1.2.1.25.1.4.0` даёт строку boot image как учебный признак Linux. Автор подчёркивает, что нужно подбирать тип check под SNMP version и выбирать OID согласно цели ([p0299](../../../rag/chunks/p0201-p0300/p0299-c01.md)–[p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)). Нельзя считать пример boot string универсальным детектором Linux.

**Autoregistration active Agent 2**: на агенте задаётся `ServerActive=<ZABBIX_SERVER_OR_PROXY>`; активный агент связывается с Zabbix, а отдельное `Alerts → Actions → Autoregistration actions` выполняет настройку host, группы `Linux servers`, шаблона `Linux by Zabbix agent active`. Именование или `HostMetadata` может использоваться для маршрутизации; не следует путать этот тип действия с `Discovery actions` ([p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)–[p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md)).

## LLD — механизм размножения объектов, а не сетевое сканирование

- **Windows**: `perfmon.exe` показывает доступные категории и счётчики, `perf_instance.discovery[Processor]` возвращает значения `{#INSTANCE}` для `0`, `1`, `_Total`. `Windows performance by Zabbix agent` с item prototype создаёт три элемента наблюдения, в рецепте используется счётчик `% C1 time`; значения относятся к конкретной Windows-машине ([p0309](../../../rag/chunks/p0301-p0400/p0309-c01.md)–[p0315](../../../rag/chunks/p0301-p0400/p0315-c01.md)).
- **JMX**: шаблон `App Apache Tomcat JMX discovery`, правило `Discover JMX object MemoryPool`, ключ `jmx.discovery[beans,"*:type=MemoryPool,name=*"]`; `name=*` → `{#JMXNAME}`, далее item prototype читает JMX-атрибут `Type` для каждого MemoryPool. Требуется подготовленный JMX host из главы 3 ([p0316](../../../rag/chunks/p0301-p0400/p0316-c01.md)–[p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)).
- **SNMP GetBulk**: собранный ранее item `SNMP interfaces bulk` опрашивает дерево `.1.3.6.1.2.1.2.2.1`. Зависимое LLD через preprocessing преобразует SNMP walk в JSON; `{#IFDESCR}` берётся из `.1.3.6.1.2.1.2.2.1.2`, `{#SNMPINDEX}` адресует отдельный интерфейс. Другие dependent items извлекают значения из **одного** SNMP bulk result. Не следует делать независимый SNMP запрос на каждый item ([p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)–[p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md)).
- **Host prototypes из JSON**: sender отправляет массив объектов, например `vmname`, `vmip`, `vmlocation`; JSONPath/LLD macros преобразуют их в `{#VMNAME}`, `{#VMIP}`, `{#VMLOCATION}`; host prototype назначает hostname, custom interface/IP, группу и template ([p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md)–[p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md)). **Пример cron на p329 повреждён**; это не готовая команда для копирования.

## Практический порядок

1. Проверить, какое обнаружение нужно: scanner по IP range, autoregistration активного агента, LLD метрик на уже известном host либо LLD host prototypes.
2. Для network discovery указать **согласованный ограниченный IP range** и правило проверки; учесть частоту и нагрузку; разделить Actions Linux/Windows/SNMP, проверить host name/template/group.
3. Для autoregistration проверить `ServerActive` и существование `Autoregistration action`; для типизации использовать hostname и/или HostMetadata.
4. Для Windows/JMX ознакомиться с исходным доступным counter/MBean, затем создать template discovery rule и item prototype; проверить `Latest data` по хосту и тегам.
5. Для SNMP bulk LLD убедиться, что master SNMP walk уже получает данные, затем dependent discovery преобразует walk в JSON и dependent item prototype берёт нужный индекс.
6. Для JSON-host LLD проверить корректность массива JSON **до отправки**, создать trapper source host/key, host LLD и host prototype, затем проверить новые hosts, их names/IP/groups.
7. До удаления любого LLD rule проверить зависимости от host prototypes и сделать backup: в источнике **прямо указано**, что удаление LLD rule/родителя может удалить созданные хосты ([p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md)).

## Материалы и ограничения

[Cheatsheet](cheatsheet.md) · [Команды и операции](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Регистр проблем источника](source-findings.md).

Особенности RAG: URL внешнего файла написан как `lldhosts.json` и `lldHosts.json` (разный регистр); у cron строки испорчены кавычки/число; про `HostMetadata` в тексте встречается название `Discovery action`, хотя рецепт создаёт `Autoregistration actions`. Эти версии не исправляются молча; [source-findings.md](source-findings.md).

**Критические границы:** network scan и SNMP probing создают нагрузку; `hostnamectl`/agent config изменения влияют на ОС; `zabbix_sender` вносит данные, cron повторяет отправку; удаление LLD rule может удалить созданные hosts. Проверенные production rollback, резервное восстановление истории и сценарии безопасного удаления **не даны**: `[Needs confirmation]`.

В [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md) нет отдельного итогового summary и review questions/answers; [p0336](../../../rag/chunks/p0301-p0400/p0336-c01.md) начинает главу 8. Условные chapter-end артефакты не создаются. **Статус чтения не изменяется.**

Контракты: `process-compliance-router v1.2`, `session-recovery v1.0`, `chapter-analysis-request v1.4`, `chapter-artifact-collection v1.8`, `chapter-publication v1.0`.
