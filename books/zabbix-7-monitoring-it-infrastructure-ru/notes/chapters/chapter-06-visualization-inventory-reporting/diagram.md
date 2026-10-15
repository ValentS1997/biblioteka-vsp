# Глава 6 — Mermaid-схемы визуализации, отчётности и SLA

Только [RAG PDF 229–290](README.md). Все схемы выражают связи из текста; подробности настроек из рисунков не додуманы.

## 1. От items к графикам и картам ([p0230](../../../rag/chunks/p0201-p0300/p0230-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md))

```mermaid
flowchart LR
  HOST["SNMP host"] --> ITEM["Template item / LLD item prototype"]
  ITEM --> HIST["Values + history в Zabbix DB"]
  HIST --> GRAPH["Graph / Graph prototype по {#IFNAME}"]
  HIST --> MAP["Map link label: конкретный host + item"]
  TRIGGER["Host trigger"] --> IND["Map link indicator: OK / PROBLEM"]
  IND --> MAP
  GRAPH --> MON["Monitoring → Hosts → Graphs"]
  MAP --> MAPUI["Monitoring → Maps"]
```

В книге для трафика используется `(current - previous) / time_delta * 8` для значения в бит/с, график по имени интерфейса создаётся из LLD; link на карте требует явного hostname.

## 2. Глобальные dashboard и шаблонные host dashboards ([p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md))

```mermaid
flowchart TB
  DATA["Values / Problems / Maps"]
  DATA --> GLOBAL["Global dashboard: All dashboards"]
  GLOBAL --> W["Problems / Map / Graph / Item value / Top Hosts"]
  GLOBAL --> PAGE["Overview / Host data: Gauge + Pie chart"]
  TEMPLATE["Custom Linux by SNMP"] --> HOSTD["Template dashboard: Host overview"]
  HOSTD --> HOST["Связанный host"]
  HOST --> RENDER["Monitoring → Hosts → Dashboards"]
  DATA --> RENDER
  HOSTD -. "Template сам не содержит данных" .-> EMPTY["Пусто в редакторе template — не ошибка"]
```

## 3. Связь inventory и Geomap ([p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md))

```mermaid
flowchart TD
  GLOBAL["Administration → General → Other: Automatic"] --> NEW["Новосозданные hosts"]
  OLD["Существующие hosts"] --> FIX["Отдельный host Inventory / Mass update"]
  NEW --> INV["Host inventory"]
  FIX --> INV
  ITEM["Template item: Populates host inventory"] --> INV
  INV --> COORD["Location latitude + longitude"]
  COORD --> GEO["Dashboard → Geomap widget"]
  PROVIDER["Geographical maps → Tile provider"] --> GEO
```

Глобальный default не обновляет существующие узлы. Координаты с рисунков источника помечены `RAG_MISS`.

## 4. Контур Scheduled PDF ([p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)–[p0274](../../../rag/chunks/p0201-p0300/p0274-c01.md))

```mermaid
flowchart LR
  DASH["Global view dashboard"] --> REPORT["Scheduled report: Weekly / Monday 09:00"]
  REPORT --> SERVER["Zabbix server: Report writers"]
  SERVER --> WS["Zabbix web service + Chrome"]
  WS --> FRONT["Frontend URL / TLS"]
  FRONT --> PDF["PDF snapshot"]
  PDF --> MEDIA["Email media of subscribed user"]
  MEDIA --> VERIFY["Test + проверка получателя"]
```

В учебном рецепте `IgnoreURLCertErrors=1` отключает проверку TLS-сертификата. Не считать этот обход production-ready.

## 5. Дерево бизнес-услуг и правила SLA ([p0280](../../../rag/chunks/p0201-p0300/p0280-c01.md)–[p0290](../../../rag/chunks/p0201-p0300/p0290-c01.md))

```mermaid
flowchart TD
  SETUP["Zabbix setup / SLA 99.9%"] --> S["Zabbix server"]
  SETUP --> DB["Zabbix database"]
  SETUP --> FE["Zabbix frontend"]
  FE --> ICMP["Child: ICMP"]
  FE --> AGENT["Child: Zabbix agent"]
  ICMP --> RULE{"At least 2 child services High+?"}
  AGENT --> RULE
  RULE -- "Да" --> PROBLEM["Frontend service влияет на SLA"]
  RULE -- "Нет" --> OK["Frontend остаётся OK"]
  PROBLEM --> SLA["Services → SLA report: uptime / downtime / error budget"]
  OK --> SLA
```

Базовое состояние frontend в примере `Set status to OK`; дополнительное правило High+ по **двум** child, а не по одному.

## Границы проверки

Конкретные UI-макросы/координаты, параметры SQL/MIB из рисунков отсутствуют в текстовом RAG: `RAG_MISS`. Противоречивые команды установки, расписание Weekly/Ежедневно, TLS обход и отсутствие процедур rollback сохраняются в [source-findings.md](source-findings.md).
