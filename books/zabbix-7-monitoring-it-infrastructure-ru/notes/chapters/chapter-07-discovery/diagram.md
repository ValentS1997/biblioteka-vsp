# Глава 7 — Mermaid: маршруты обнаружения и создание объектов

Источник: accepted RAG PDF 291–335. Схемы — **структура из извлечённого текста**, не реконструкция значений UI из скриншотов.

## 1. Network Discovery по диапазону ([p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md))

```mermaid
flowchart LR
  RANGE["Разрешённый IP range"] --> SCAN["Zabbix server: Discovery rule"]
  SCAN --> AGENT["Check Zabbix agent: agent.hostname"]
  SCAN --> SNMP["Check SNMPv2: sysName + дополнительный OID"]
  AGENT --> CONDITION["Discovery actions: status UP, service, lnx/win"]
  SNMP --> CONDITION
  CONDITION --> CREATE["Create host + group + template"]
  CREATE --> VERIFY["Monitoring → Discovery; Data collection → Hosts"]
```

Сетевой scan выполняется сервером. Для Agent hostname (`lnx` или `win`) и service `Zabbix Agent`; SNMP OID нельзя выбирать вне реальной структуры устройства. Чем меньше интервал и шире range, тем выше нагрузка.

## 2. Active Agent autoregistration — другой старт ([p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)–[p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md))

```mermaid
flowchart TD
  AGENT["Новый Agent 2: ServerActive + Hostname/Metadata"] --> SERVER["Zabbix server / proxy: запрос конфигурации"]
  SERVER --> ACTION["Autoregistration action (не Discovery action)"]
  ACTION --> FILTER["Фильтр имени/HostMetadata"]
  FILTER --> GROUP["Group: Linux servers"]
  FILTER --> TEMPLATE["Template: Linux by Zabbix agent active"]
  GROUP --> HOST["Автоматически созданный host"]
  TEMPLATE --> HOST
```

`HostMetadata` уместен для среды, где hostname не отражает ОС. Существование active agent не является доказательством настройки самого action.

## 3. LLD объектов: Windows и JMX ([p0309](../../../rag/chunks/p0301-p0400/p0309-c01.md)–[p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md))

```mermaid
flowchart TD
  WIN["Windows: perfmon.exe → Processor"]
  WIN --> PKEY["perf_instance.discovery[Processor]"]
  PKEY --> INSTANCE["{#INSTANCE}: 0, 1, _Total"]
  INSTANCE --> ITEMS["Windows item prototypes → counters"]
  JMX["JMX host + gateway"] --> DISC["jmx.discovery[beans, wildcard MemoryPool]"]
  DISC --> NAME["{#JMXNAME}: MBean name"]
  NAME --> JITEM["JMX item prototypes → Type"]
  ITEMS --> VERIFY["Monitoring → Latest data"]
  JITEM --> VERIFY
```

JMX ключ дан полностью в [p0319](../../../rag/chunks/p0301-p0400/p0319-c01.md), здесь короткое описание из-за разбиения блоков. Число instances зависит от целевой Windows среды.

## 4. SNMP GetBulk — один master, много dependent ([p0321](../../../rag/chunks/p0301-p0400/p0321-c01.md)–[p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md))

```mermaid
flowchart TB
  DEVICE["SNMP device"] --> BULK["Один GetBulk: SNMP interfaces bulk"]
  BULK --> RAW["Master SNMP walk item"]
  RAW --> DEP["Dependent LLD: SNMP walk → JSON"]
  DEP --> DESCR["{#IFDESCR}: OID .1.3.6.1.2.1.2.2.1.2"]
  DEP --> INDEX["{#SNMPINDEX}: unique interface"]
  INDEX --> PROTO["Dependent item prototypes"]
  DESCR --> PROTO
  RAW --> PROTO
  PROTO --> DATA["Latest data: per-interface value"]
```

Детали preprocessing, показанные только на рисунках 7.54 и 7.57, остаются `RAG_MISS`.

## 5. JSON-driven host prototypes и жизненный цикл ([p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md)–[p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md))

```mermaid
flowchart TD
  SOURCE["Валидный JSON: vmname/vmip/vmlocation"] --> SENDER["zabbix_sender; учебная cron строка неисполнима"]
  SENDER --> TRAPPER["lar-lldhost-creation: trapper lldhosts.raw"]
  TRAPPER --> RULE["LLD rule + JSONPath macros"]
  RULE --> MACROS["{#VMNAME}, {#VMIP}, {#VMLOCATION}"]
  MACROS --> PROTO["Host prototype: name, IP, host group, template"]
  PROTO --> HOSTS["Автоматически созданные hosts"]
  RULE --> DELETE{"Удалён LLD rule / host?"}
  DELETE -- "Да" --> RISK["Риск каскадного удаления созданных hosts"]
  DELETE -- "Нет" --> HOSTS
```

Важно: текст p335 прямо предупреждает, что удаление discovery parent может удалить созданные hosts. Не производить тестовое удаление без backup и проверенного recovery.

## 6. Диагностика по границам

```mermaid
flowchart TD
  START["Ожидаемый объект отсутствует"] --> TYPE{"Тип механизма?"}
  TYPE -- "Network scan" --> N["IP range → check → Discovery action"]
  TYPE -- "Active autoreg" --> A["ServerActive → Autoregistration action"]
  TYPE -- "LLD items" --> I["Master/Discovery value → macros → item prototype"]
  TYPE -- "LLD hosts" --> H["JSON source → trapper → LLD macros → host prototype"]
  N --> VERIFY["Проверить Monitoring Discovery / Hosts / Latest data"]
  A --> VERIFY
  I --> VERIFY
  H --> VERIFY
```

**Необратимые изменения и источник:** `hostnamectl`, `snmpd`, конфигурация Agent, cron, широкое scan и удаление LLD objects требуют локальной проверки. [source-findings.md](source-findings.md).
