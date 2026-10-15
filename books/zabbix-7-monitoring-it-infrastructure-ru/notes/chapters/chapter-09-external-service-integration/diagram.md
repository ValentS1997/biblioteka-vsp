# Глава 9 — Mermaid: Zabbix → внешние сервисы

Основание: **только accepted RAG PDF 371–411**. На схемах не используются непроверенные идентификаторы из рисунков; конфигурационные fields только со скриншотов = `RAG_MISS`.

## 1. Общий маршрут оповещения ([p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md)–[p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md), [p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md), [p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md))

```mermaid
flowchart TD
  PROBLEM["Zabbix PROBLEM event"] --> COND{"Trigger Action conditions + severity"}
  COND -- "No match" --> STOP["Нет отправки"]
  COND -- "Matched (например Warning+)" --> OPER["Operations: external user or script"]
  OPER --> RIGHTS["Host groups Read + User role"]
  RIGHTS --> MEDIA["User Media + Enabled Media type"]
  MEDIA --> WEBHOOK["Webhook: Slack / MS Teams / Telegram"]
  WEBHOOK --> DEST["Выбранный channel / group"]
  OPER --> SCRIPT["Opsgenie script action (server-side)"]
  SCRIPT --> OEC["OEC connector + Opsgenie API"]
  OEC --> ONCALL["Opsgenie team / on-call"]
```

Если у action нет conditions, авторы прямо указывают, что он сопоставляет все PROBLEM. User `Super admin` перекрывает назначенные группы `Read`. Это **не безопасный production default**.

## 2. Три канала и три секрета ([p0373](../../../rag/chunks/p0301-p0400/p0373-c01.md)–[p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md))

```mermaid
flowchart LR
  SLACK["Slack App + bot scopes"] --> OAUTH["OAuth bot token"]
  OAUTH --> SB["Zabbix Slack: bot_token"]
  SB --> SC["Slack #zabbix-notifications"]
  TEAMS["Teams channel + Zabbix Webhook"] --> URL["Connector webhook URL"]
  URL --> TM["Zabbix MS Teams: teams_endpoint"]
  TM --> TC["Конкретный Teams channel"]
  TELE["Telegram @BotFather /newbot"] --> TOKEN["Telegram bot Token"]
  TOKEN --> ZT["Zabbix Telegram Token + User Send to group ID"]
  ZT --> TG["Telegram New Group"]
```

Не выдавать токены/URL за обычные ссылки; это секретные параметры. Для Telegram `Send to` получает **group ID** из `/getgroupid@myidbot`, в примере он начинается с `-`.

## 3. Ограничение прав и маршрутизация ([p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md)–[p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md))

```mermaid
flowchart TD
  GROUP["External Services user group"] --> HOSTS["Host permissions: нужные groups / Read"]
  GROUP --> NOUI["No access to the frontend"]
  HOSTS --> USER["Технический Zabbix user"]
  NOUI --> USER
  USER --> ROLE{"User role"}
  ROLE -- "User/Admin по потребности" --> LIMITED["Контролируемая видимость"]
  ROLE -- "Super admin (учебно)" --> BROAD["Перекрывает Read — риск"]
  LIMITED --> MEDIA["User Media → target endpoint"]
  MEDIA --> ACTION["Trigger Action: ограниченные conditions"]
```

В книге Super admin выбран «для удобства» для Slack, Teams, Telegram и Opsgenie; там же явно сказано, что это меняет эффективные права.

## 4. Opsgenie — двусторонняя интеграция ([p0403](../../../rag/chunks/p0401-p0500/p0403-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md))

```mermaid
flowchart TD
  Z["Zabbix PROBLEM/Recovery/Update"] --> ACT["Opsgenie action"]
  ACT --> SCR["Alerts Scripts: Opsgenie connector"]
  SCR --> CMD["actionCommand.txt: RAG_MISS"]
  CMD --> CFG["OEC config.json: apiKey / command_url / user / password"]
  CFG --> REGION["baseUrl regional API endpoint"]
  REGION --> OPS["Opsgenie team / alert / on-call"]
  OPS --> RESPONSE["Acknowledgement / response"]
  RESPONSE --> Z
```

Стрелка ответа передаёт **смысл двустороннего взаимодействия**, заявленный на p410; точный HTTP/API protocol и shell code в RAG не даны.

## 5. Приёмка без массовых уведомлений

```mermaid
flowchart TD
  START["Проверить credentials без их вывода"] --> SCOPE["Host groups, role, media, action conditions"]
  SCOPE --> SMALL["Контролируемая тестовая PROBLEM"]
  SMALL --> DELIVERY{"Получена только целевым recipient?"}
  DELIVERY -- "Нет" --> TRACE["External bot / Media type / User / Action"]
  TRACE --> SCOPE
  DELIVERY -- "Да" --> RECOVERY["Если Opsgenie: проверить Recovery/Update"]
  RECOVERY --> DONE["Зафиксировать результаты, план revoke/rollback отдельно"]
```

Источник не описывает конечный тест delivery timeout, idempotency, revoke и полноценный rollback. `[Needs confirmation]`. Список проблем и `RAG_MISS`: [source-findings.md](source-findings.md).
