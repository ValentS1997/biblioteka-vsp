# Глава 7 — cheatsheet: Discovery, Autoregistration, LLD

**Источник:** только accepted RAG PDF 291–335; [полная provenance](README.md). **Диагностика не должна приводить к автоматическому созданию нежелательных объектов.**

## Symptom / problem framing

| Признак | Что выяснить прежде всего | Страницы RAG |
|---|---|---|
| Agent 2 Linux/Windows не обнаружен | Правило `Data collection → Discovery`, IP range, агент `Hostname`, агентный key `agent.hostname`, интервал и network path | [p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md) |
| IP обнаружен, но host не создан | Есть ли отдельный `Discovery action`, `UP`, service type `Zabbix Agent`, name содержит `lnx`/`win`, операции host group/template | [p0294](../../../rag/chunks/p0201-p0300/p0294-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md) |
| SNMP-host не появляется | SNMPv2 check, подходящие version/community и `sysName` OID, второй OID, диапазон сети и Discovery action | [p0299](../../../rag/chunks/p0201-p0300/p0299-c01.md)–[p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md) |
| Active agent не регистрируется | `ServerActive`, сетевой доступ Zabbix server/proxy, фильтр `Autoregistration actions` и операция присоединения active template | [p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)–[p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md) |
| Windows item prototypes пусты | `perfmon.exe` и category `Processor`, `perf_instance.discovery[Processor]`, наличие `{#INSTANCE}` и назначенного шаблона | [p0309](../../../rag/chunks/p0301-p0400/p0309-c01.md)–[p0315](../../../rag/chunks/p0301-p0400/p0315-c01.md) |
| JMX MemoryPool отсутствует | Подготовленный JMX host, gateway, `jmx.discovery[beans,"*:type=MemoryPool,name=*"]`, `{#JMXNAME}`, item prototype | [p0316](../../../rag/chunks/p0301-p0400/p0316-c01.md)–[p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md) |
| GetBulk master есть, зависимые items не появляются | Master `SNMP interfaces bulk`, LLD preprocessing walk→JSON, `{#IFDESCR}`, `{#SNMPINDEX}`, уникальный item key/index | [p0323](../../../rag/chunks/p0301-p0400/p0323-c01.md)–[p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md) |
| JSON sender доставляет значение, host prototype не создаёт hosts | Достоверность JSON, trapper host/key `lldhosts.raw`, JSONPath→`{#VM*}`, host prototype custom interface/IP/group | [p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md)–[p0334](../../../rag/chunks/p0301-p0400/p0334-c01.md) |
| После удаления discovery исчезли созданные hosts | В книге есть прямое предупреждение о cascade удаления. Без backup/recovery не выполнять дальнейшее удаление | [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md) |

## Baseline / context

Для network discovery нужны Zabbix server и новые Windows/Linux host с Agent 2, для SNMP — новое SNMP-устройство; для JMX — Java gateway/Tomcat, настроенный в главе 3. Автор использует тестовые имена `lar-book-disc-lnx`, `lar-book-disc-win`, `lar-book-disc-snmp`, `lar-book-lnx-agent-auto`, `lar-book-jmx`, `lar-book-snmp_bulk` и `lar-lldhost-creation`. IP, credentials, platform counters и имена **не универсальны** ([p0291](../../../rag/chunks/p0201-p0300/p0291-c01.md), [p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md), [p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)).

## Read-only checks и осторожные probes

- `Data collection → Discovery` — существующие rules, IP range и checks; `Monitoring → Discovery` — какие IP/service и когда появились; эти страницы **Read-only при просмотре** ([p0295](../../../rag/chunks/p0201-p0300/p0295-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md)).
- `Data collection → Hosts` и `Monitoring → Latest data` — наличие созданного host, linked template, значений item и tags; **Read-only** ([p0307](../../../rag/chunks/p0301-p0400/p0307-c01.md), [p0313](../../../rag/chunks/p0301-p0400/p0313-c01.md), [p0318](../../../rag/chunks/p0301-p0400/p0318-c01.md)).
- `perfmon.exe` → `Performance Monitor → +` — проверка реально существующей Windows-категории и экземпляров; открытие — **Read-only** (наблюдение может нагружать систему) ([p0309](../../../rag/chunks/p0301-p0400/p0309-c01.md)–[p0310](../../../rag/chunks/p0301-p0400/p0310-c01.md)).
- Прочесть `/etc/zabbix/zabbix_agent2.conf` и Windows `C:\Program Files\Zabbix Agent 2\zabbix_agent2.conf` для проверки `Hostname`/`ServerActive`, без записи. Сам `vim` из примера **State-changing при сохранении** ([p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md), [p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)).
- `snmpwalk` для идентификации OID — **Workload-generating**, создаёт SNMP-трафик и требует контроля секрета ([p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)).
- `LLD rule → Test` или Latest data после внедрения — проверка результатов: запрос/пересчёт может быть **Workload-generating**, не равен read-only для целевой сети. Конкретный `Test` в этом разделе на рисунках не подтверждён для всех типов LLD → `[Needs confirmation]`.

## Interpretation

**Network discovery:** scanner выполняет host/service check; только совпадающее `Discovery action` с `UP`, `Zabbix Agent`, `lnx`/`win` создаёт host и связывает groups/templates. Учебный интервал **5 минут**, альтернативный **1 час** снизит нагрузку; требования по размеру scan range нужно определять отдельно ([p0293](../../../rag/chunks/p0201-p0300/p0293-c01.md)–[p0298](../../../rag/chunks/p0201-p0300/p0298-c01.md)).

**SNMP discovery:** OID `.1.3.6.1.2.1.1.5.0` даёт hostname и `.1.3.6.1.2.1.25.1.4.0` даёт boot parameter string (учебный Linux detection); тип SNMPv2 agent настраивать по реальной версии устройства ([p0299](../../../rag/chunks/p0201-p0300/p0299-c01.md)–[p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)).

**Active autoreg:** запрос от agent (`ServerActive`) начинает регистрацию, сервер применяет отдельный `Autoregistration action` и добавляет host в `Linux servers` с `Linux by Zabbix agent active`. `HostMetadata`, `HostInterface`, `HostInterfaceItem` — возможности для классификации/интерфейса ([p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)–[p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md)).

**Windows/JMX:** `{#INSTANCE}` создаёт по одному item на processor instance `0`, `1`, `_Total`; JMX `{#JMXNAME}` находит MemoryPool MBean. В других системах набор instances/MBeans иной ([p0314](../../../rag/chunks/p0301-p0400/p0314-c01.md)–[p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)).

**SNMP bulk LLD:** один GetBulk master и dependent discovery/item prototypes: preprocessing walk→JSON, interface description OID `.1.3.6.1.2.1.2.2.1.2`, SNMPINDEX; значение каждого dependent item извлекается по своему индексу ([p0323](../../../rag/chunks/p0301-p0400/p0323-c01.md)–[p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md)).

**JSON hosts LLD:** `vmname`, `vmip`, `vmlocation` → `{#VMNAME}`, `{#VMIP}`, `{#VMLOCATION}` → host prototype. Код Cron p329 нарушен и **не должен исполняться**. При удалении исходного LLD rule host lifecycle может удалить созданные hosts ([p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md)–[p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md)).

## Next action / modifying action

1. Локализовать слой **rule → check/source → action → operation → template/group → output**, а для LLD **master value → transformed JSON/macros → prototype → concrete object**.
2. Создавать `Discovery rule` и `Discovery/Autoregistration action` (**State-changing**) только после ограничения scan range и проверки фильтров. Риск — массовая генерация hosts и нагрузка. Результат — `Monitoring → Discovery` и `Data collection → Hosts`.
3. Установка templates, host name change, `snmpd` restart, `ServerActive` и настройки `HostMetadata` — **State-changing**, затрагивают сеть/доступ. Rollback исходником не расписан.
4. LLD rules и item/host prototypes — **State-changing**: могут автоматически создать много items или hosts, в том числе ложноположительные. Для внешнего JSON обязательна schema-валидация до `zabbix_sender`.
5. `crontab -e` на каждую минуту и `zabbix_sender` — **State-changing + workload-generating**; риск бесконечной повторной отправки невалидного/устаревшего JSON и шумной конфигурации.
6. **Не удалять** LLD rule/родительский host ради тестирования без backup и плана сохранения автоматически созданных hosts — [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md).

## Verification / acceptance checks

- Обнаружение срабатывает только внутри согласованного IP range и нужного типа проверок; target OS попадает в нужную host group/template.
- Active agent зарегистрирован через **Autoregistration action**, а не по сканированию; конфигурация активного шаблона видна у host.
- Windows Processor discovery возвращает действительные `{#INSTANCE}` в JSON; item prototypes появились; JMX MemoryPool items появились и имеют тег `component:memory pool`.
- SNMP bulk master работает, dependent LLD строит `{#IFDESCR}`/`{#SNMPINDEX}`, значения достоверны.
- JSON host LLD содержит корректные IP/hostname, host prototypes назначают правильные интерфейсы/группы; опасный учебный cron не запускался без исправления и повторной проверки.
- Убедиться, что не удалено ни одного host/LLD объекта без отдельной операции и резервного копирования.

## Rollback

В главе нет надёжного полного плана отката установки агента, изменения hostname, SNMP/Agent конфигураций, сетевого discovery, остановки/удаления autoreregistration или cron и, особенно, **восстановления удалённых LLD host prototypes/hosts**. Для этих операций `[Needs confirmation]`; источник прямо требует backups. Результат удаления исторических данных нельзя считать обратимым.

**Источник и дефекты:** [source-findings.md](source-findings.md). Точные параметры рисунков = `RAG_MISS`. Статус чтения не изменён.
