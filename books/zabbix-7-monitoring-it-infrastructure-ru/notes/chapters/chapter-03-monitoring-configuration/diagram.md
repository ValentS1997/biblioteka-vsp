# Глава 3 — Mermaid-схемы по RAG

**Основа:** [README](README.md), PDF 93–160. Диаграммы отражают **только текстово подтверждённые связи**, не копируют и не интерпретируют невидимые изображения учебника.

## 1. Где начинается передача метрик ([p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md)–[p0101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [p0115](../../../rag/chunks/p0101-p0200/p0115-c01.md)–[p0123](../../../rag/chunks/p0101-p0200/p0123-c01.md))

```mermaid
flowchart LR
  S["Zabbix server / proxy"]
  A["Zabbix Agent 2"]
  SN["SNMP host"]
  P["Host: zabbix_sender"]
  DB[("История значений Zabbix")]
  S -->|"passive polling"| A
  A -->|"active checks → send"| S
  S -->|"OID / walk[] / GetBulk"| SN
  SN -->|"SNMP-ответ"| S
  P -->|"trapper: key + value"| S
  S --> DB
  S -->|"simple check: TCP availability"| TCP["Служба / порт"]
```

У простого TCP-check смысл результата **только с точки зрения server/proxy**, поскольку firewall по пути может помешать запросу ([p0122](../../../rag/chunks/p0101-p0200/p0122-c01.md)).

## 2. Мастер, preprocessing и зависимые элементы ([p0111](../../../rag/chunks/p0101-p0200/p0111-c01.md)–[p0115](../../../rag/chunks/p0101-p0200/p0115-c01.md), [p0125](../../../rag/chunks/p0101-p0200/p0125-c01.md)–[p0130](../../../rag/chunks/p0101-p0200/p0130-c01.md))

```mermaid
flowchart TB
  POLL["Один сбор: SNMP walk[] либо составная проверка DB/browser"]
  RAW["Master item: исходные данные"]
  POLL --> RAW
  RAW --> PP1["Preprocessing: выбор OID / индекса / поля"]
  RAW --> PP2["Preprocessing: извлечение другого поля"]
  PP1 --> ITEM1["Dependent item A: конкретное значение"]
  PP2 --> ITEM2["Dependent item B: конкретное значение"]
  RAW -. "опция, если сырая история не нужна" .-> NOSTORE["Do not keep history"]
  ITEM1 --> VIEW["Monitoring → Latest data"]
  ITEM2 --> VIEW
```

Dependent item не выполняет отдельный сбор по своему interval. Вычисляемый item — другая модель: расчёт агрегата из существующих значений (пример 15-минутной средней памяти).

## 3. Маршруты получения значений ([p0130](../../../rag/chunks/p0101-p0200/p0130-c01.md)–[p0153](../../../rag/chunks/p0101-p0200/p0153-c01.md))

```mermaid
flowchart TB
  Z["Zabbix server"]
  Z -->|"External check"| EX["Исполняемый сценарий → stdout"]
  Z -->|"JavaGateway / Java pollers"| JG["Zabbix Java gateway"]
  JG --> JMX["Tomcat / JMX"]
  Z -->|"ODBC item"| DRV["ODBC DSN / driver"]
  DRV --> SQL["MariaDB: SQL query"]
  Z -->|"HTTP agent"| HTTP["HTTP/JSON endpoint"]
  HTTP --> JSON["JSONPath → latest_release"]
  Z -->|"browser item"| WD["Selenium WebDriver"]
  WD --> WEB["Веб-страница / действия пользователя"]
  WEB --> PERF["JS performance/result JSON"]
  PERF --> DEP["Dependent item: нужная метрика"]
```

Ветви не взаимозаменяемы: JMX требует Java gateway, ODBC требует connector/DSN, browser зависит от Selenium/JS (и несёт отличающиеся риски).

## 4. Диагностический алгоритм ([p0097](../../../rag/chunks/p0001-p0100/p0097-c01.md), [p0113](../../../rag/chunks/p0101-p0200/p0113-c01.md), [p0155](../../../rag/chunks/p0101-p0200/p0155-c01.md)–[p0160](../../../rag/chunks/p0101-p0200/p0160-c01.md))

```mermaid
flowchart TD
  A["Нужного значения нет в Latest data"] --> B{"Соответствуют host/interface/template и режим?"}
  B -- "Нет" --> B1["Проверить Agent Hostname/ServerActive или SNMP интерфейс"]
  B -- "Да" --> C{"Пришли исходные данные?"}
  C -- "Нет" --> C1["Проверить сеть, OID, sender key, ODBC, JavaGateway"]
  C -- "Да" --> D{"Preprocessing извлекает искомое?"}
  D -- "Нет" --> D1["Проверить master value, индекс, JSONPath/Regexp"]
  D -- "Да" --> E["Проверить единицы, history и итоговую метрику"]
  B1 --> F["Изменение конфигурации — только после оценки рисков"]
  C1 --> F
  D1 --> F
  F --> G["Повторно проверить Latest data / History"]
```

## 5. Осознанные ограничения

- Browser-пример со строкой `systemctl restart zabbbix-server` и `dnf` для Ubuntu содержит исходниковые несоответствия; **не нормализовать молча** ([p0144](../../../rag/chunks/p0101-p0200/p0144-c01.md)).
- `AllowKey=system.run[*]` и отключённая JMX-аутентификация/SSL — высокорисковые настройки из учебного примера, не образец производственной эксплуатации ([p0133](../../../rag/chunks/p0101-p0200/p0133-c01.md), [p0155](../../../rag/chunks/p0101-p0200/p0155-c01.md)).
- Для неизвестных regexp/параметров скриншотов оставить `RAG_MISS`: подробности [source-findings.md](source-findings.md).
