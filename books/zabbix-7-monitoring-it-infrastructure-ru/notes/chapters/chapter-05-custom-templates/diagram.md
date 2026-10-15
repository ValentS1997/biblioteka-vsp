# Глава 5 — Mermaid-диаграммы по RAG

Основание: принятый RAG PDF 197–228. Диаграммы отражают **структуру из текста книги**, а не извлечённые рисунки 5.1–5.48. Имена и примеры подтверждены страницами, отсутствующие значения — `RAG_MISS`.

## 1. Шаблон и наследование элементов ([p0205](../../../rag/chunks/p0201-p0300/p0205-c01.md)–[p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md))

```mermaid
flowchart TB
  T["Custom Linux by SNMP — template"]
  T --> ITEMS["Template Items: sysName"]
  T --> TRIG["Template Triggers: change(sysName)"]
  T --> TAGS["Template Tags: class:os, target:linux"]
  T --> MACRO["Template Macros: {$...}"]
  T --> H1["Host lar-book-templated_snmp"]
  T --> H2["Другой host с тем же template"]
  H1 --> V1["Собственное значение Latest data"]
  H2 --> V2["Собственное значение Latest data"]
```

Item создаётся на уровне template **один раз**, но каждый host получает собственные измерения. Точное выражение триггера доступно только на рисунке — здесь `change(sysName)` обозначает **смысл**, а не готовый синтаксис формулы.

## 2. Теги и макросы ([p0201](../../../rag/chunks/p0201-p0300/p0201-c01.md)–[p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md), [p0210](../../../rag/chunks/p0201-p0300/p0210-c01.md)–[p0214](../../../rag/chunks/p0201-p0300/p0214-c01.md))

```mermaid
flowchart TD
  TEMPLATE["Template Custom Linux by SNMP"]
  TEMPLATE --> TAGS["Tags class:os + target:linux"]
  TAGS --> EVENTS["Problems: фильтрация и маршрутизация"]
  TEMPLATE --> TM["User macro at template: prefix lar-"]
  TM --> INHERIT["Наследование на host"]
  INHERIT --> OVERRIDE{"Есть host-level override?"}
  OVERRIDE -- "Нет" --> LAR["Применяется lar-"]
  OVERRIDE -- "Да" --> DEV["Применяется dev-"]
  TEMPLATE --> BUILTIN["Built-in {HOST.HOST}: hostname каждого host"]
```

User macro имеет форму `{$MACRONAME}`; built-in `{HOST.HOST}` получает имя из конфигурации конкретного host. Текст источника подтверждает значения `lar-` и `dev-`, но **не** полное значение имени пользовательского макроса на рисунке 5.18.

## 3. LLD: от discovery к реальным объектам ([p0215](../../../rag/chunks/p0201-p0300/p0215-c01.md)–[p0224](../../../rag/chunks/p0201-p0300/p0224-c01.md))

```mermaid
flowchart TD
  DISC["Discovery rule: SNMP network interfaces"]
  DISC --> JSON["Discovery result: interface names + indices"]
  JSON --> LO["{#IFNAME}=lo, {#SNMPINDEX}=1"]
  JSON --> ENS["{#IFNAME}=ens192, {#SNMPINDEX}=2"]
  LO --> IP["Item prototype: Operational status"]
  ENS --> IP
  IP --> ITEMS["Items: lo status / ens192 status"]
  JSON --> TP["Trigger prototype"]
  TP --> TRIG["Triggers per interface"]
  DISC --> LOST{"Обнаруженный ресурс временно пропал?"}
  LOST -- "Immediately (учебно)" --> DELETE["Удаление resource и истории — риск"]
  LOST -- "Иная retention policy" --> CONF["Значение требует проверки для production"]
```

Числовой интерфейсный OID в одном поясняющем абзаце p222 отличается от OID приведённых значений. Для готового `net.if.discovery` / SNMP item **не восстанавливать** недостающие поля из рисунков по памяти.

## 4. Вложенные шаблоны ([p0225](../../../rag/chunks/p0201-p0300/p0225-c01.md)–[p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md))

```mermaid
flowchart TB
  HOST["Host lar-book-templated_snmp"]
  PARENT["Parent Custom Linux by SNMP"]
  CHILD["Nested Custom Linux uptime by SNMP"]
  HOST --> PARENT
  PARENT --> CHILD
  PARENT --> SNMP["Прямой item sysName"]
  CHILD --> UPTIME["Вложенный item System Uptime"]
  UPTIME --> HITEM["Host Items: System Uptime (inherited)"]
```

Источник прямо отмечает, что вложенность уменьшает дублирование, но усложняет поддерживаемую структуру.

## 5. Контроль изменения ([p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md), [p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md), [p0226](../../../rag/chunks/p0201-p0300/p0226-c01.md))

```mermaid
flowchart TD
  A["Перед изменением: определить host и шаблон"] --> B["Прочитать текущие Items/Tags/Macros"]
  B --> C["Проверить SNMP OID и значения host"]
  C --> D["Контролируемое изменение template/prototype"]
  D --> E["Проверить Latest data и Problems"]
  E --> F{"LLD item и trigger созданы правильно?"}
  F -- "Нет" --> G["Сверить Test JSON, IFNAME, SNMPINDEX и prototype"]
  G --> C
  F -- "Да" --> H["Проверить наследование nested item"]
  H --> R["Сохранить/откатить по локальному плану: Needs confirmation"]
```

**Защитные ограничения:** `Delete lost resources = Immediately` приводит к риску безвозвратной потери истории; restart snmpd и hostnamectl — изменения ОС. См. [source-findings.md](source-findings.md).
