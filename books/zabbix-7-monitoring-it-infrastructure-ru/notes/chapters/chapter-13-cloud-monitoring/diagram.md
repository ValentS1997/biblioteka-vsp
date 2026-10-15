# Глава 13 — Mermaid-диаграммы облачного мониторинга

Схемы основаны только на **accepted RAG PDF 490–510**; отсутствующие на рисунках IAM JSON / JavaScript / preprocessing fields помечены `RAG_MISS`, без добавления внешнего кода.

## 1. AWS → Zabbix Script → обнаруженные hosts ([p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md))

```mermaid
flowchart TD
  AWS["AWS EC2, RDS, S3 в выбранных регионах"]
  IAM["Dedicated IAM user + inline policy, access key"]
  HOST["Zabbix host: AWS by HTTP"]
  REGION["Host macros: AWS region, credentials"]
  SCRIPT["Script item: JavaScript → AWS API"]
  JSON["API response → JSON"]
  LLD["3 discovery rules: EC2, RDS, S3"]
  PROTO["Host prototypes"]
  METRICS["AWS resource hosts + AWS EC2 by HTTP / другие templates"]
  AWS --> SCRIPT
  IAM --> REGION
  REGION --> HOST
  HOST --> SCRIPT
  SCRIPT --> JSON
  JSON --> LLD
  LLD --> PROTO
  PROTO --> METRICS
```

Скрипт и policy JSON **показаны только на рисунках**, поэтому нельзя считать диаграмму готовым deployment workflow. CloudWatch может быть платным.

## 2. Azure: identity, Reader, LLD ([p0499](../../../rag/chunks/p0401-p0500/p0499-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md))

```mermaid
flowchart TD
  APP["Enterprise application и App registration"]
  SECRET["Client secret Value"]
  READER["Subscription IAM → Reader role"]
  TENANT["Tenant ID / Subscription ID / Application ID"]
  MACROS["Azure Zabbix macros: APP.ID, PASSWORD, SUBSCRIPTION.ID, TENANT.ID"]
  HOST["Host: Azure by HTTP"]
  SCRIPT["JavaScript Script items → Azure API → JSON"]
  DISC["6 LLD rules: VM и DB"]
  PROTO["Host prototypes → resource-specific templates"]
  APP --> SECRET
  APP --> READER
  SECRET --> MACROS
  TENANT --> MACROS
  READER --> SCRIPT
  MACROS --> HOST
  HOST --> SCRIPT
  SCRIPT --> DISC
  DISC --> PROTO
```

Связь двух объектов Azure portal (Enterprise application vs App registration) текстом описана не полностью: `[Needs confirmation]`. Права Reader нужно проверять на нужной Subscription.

## 3. Docker: agent master → dependent items ([p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md))

```mermaid
flowchart TD
  ENGINE["Docker host: daemon и контейнеры"]
  AGENT["Zabbix Agent 2, доступ к Docker"]
  HOST["Zabbix host: Docker by Zabbix agent 2"]
  INFO["Master: Docker Get info, key docker.info"]
  DEPS["Dependent items + preprocessing"]
  DISC["LLD: images + containers"]
  NAMES["docker.containers.discovery → {#NAME}"]
  CINFO["Master: docker.container_info"]
  CDEPS["Dependent prototypes по контейнеру"]
  ENGINE --> AGENT
  AGENT --> INFO
  HOST --> INFO
  INFO --> DEPS
  HOST --> DISC
  DISC --> NAMES
  NAMES --> CINFO
  CINFO --> CDEPS
```

Команда `gpasswd -a zabbix docker` из источника выдаёт права группе Docker и **не является безопасным универсальным default**.

## 4. Сравнение: облачный host discovery vs локальный Docker LLD

```mermaid
flowchart TD
  START["Задан ресурс для мониторинга"]
  TYPE{"Где источник метрик?"}
  START --> TYPE
  TYPE -- "AWS / Azure" --> AUTH["IAM principal, API credentials, billing/scope"]
  AUTH --> HTTP["Zabbix Script JavaScript и cloud API"]
  HTTP --> HOSTLLD["JSON → LLD host prototypes → host"]
  TYPE -- "Docker on Linux host" --> LOCAL["Agent 2 с разрешённым Docker-доступом"]
  LOCAL --> MASTER["docker.info / docker.container_info"]
  MASTER --> ITEMLLD["Dependent items и item prototypes по {#NAME}"]
  HOSTLLD --> VERIFY["Latest data и обнаруженные объекты"]
  ITEMLLD --> VERIFY
```

## 5. Приёмка перед небезопасным изменением

```mermaid
flowchart TD
  S["Read-only: scope, region/subscription, container list"] --> A["Проверить auth, IAM Reader и секреты без их раскрытия"]
  A --> M["Проверить cloud Script item или docker.info master"]
  M --> J["JSON, LLD правила, индексы, prototypes"]
  J --> V{"Ожидаемые hosts/items видны?"}
  V -- "Нет" --> GAP["Зафиксировать RAG_MISS / Needs confirmation и диагностировать предыдущий слой"]
  V -- "Да" --> END["Документировать Latest data, quota/cost, privileges и сроки ключей"]
```

Исходник не даёт полного rollback и не гарантирует стоимость CloudWatch, безопасность membership `docker`, отсутствие лишних IAM разрешений или работоспособность старых облачных UI. См. [source-findings.md](source-findings.md).
