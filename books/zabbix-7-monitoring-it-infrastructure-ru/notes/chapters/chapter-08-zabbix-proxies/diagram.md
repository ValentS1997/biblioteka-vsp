# Глава 8 — Mermaid: Zabbix proxy, режимы, безопасность и HA

**Основание:** accepted RAG PDF 336–370. Это авторское представление **только текстовых отношений** главы, а не реконструкция рисунков 8.1–8.42.

## 1. Кто инициирует соединение? ([p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md)–[p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md))

```mermaid
flowchart TB
  SERVER["Zabbix server: config, values"]
  PASSIVE["Passive proxy: ProxyMode=1"]
  ACTIVE["Active proxy: ProxyMode=0"]
  HOSTP["Локальные SNMP / passive Agent hosts"]
  HOSTA["Локальные active Agent hosts"]
  SERVER -->|"TCP/10051: server инициирует"| PASSIVE
  ACTIVE -->|"TCP/10051: proxy инициирует"| SERVER
  HOSTP --> PASSIVE
  HOSTA --> ACTIVE
```

`ProxyMode` — это режим соединения **proxy↔server**. Он не эквивалентен автоматически passive/active режиму **агента**: хост может использовать разные комбинации проверок, если маршруты корректны.

## 2. Куда уходят значения и где возможна потеря? ([p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md)–[p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md), [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md))

```mermaid
flowchart TD
  ITEM["Сбор значения на proxy"] --> BUFFER{"ProxyBufferMode"}
  BUFFER -- "Hybrid" --> RAM["Memory buffer"]
  RAM -->|"Заполнение"| SQLITE["Disk/SQLite buffer"]
  BUFFER -- "Memory" --> MEMORY["Хранение в памяти"]
  BUFFER -- "Disk" --> SQLITE
  RAM --> SEND["Передача в Zabbix server"]
  SQLITE --> SEND
  MEMORY --> SEND
  SQLITE --> REMOVE["Удаление DB-файла: потеря неотправленных values"]
  MEMORY --> RESTART["Restart с memory only: риск потери values"]
  SEND --> HISTORY["Центральная история"]
```

`ProxyOfflineBuffer` определяет срок сохранения при сбое связи (источник: default 1 час), но **не гарантирует** хранение вне заданной конфигурации.

## 3. PSK требует согласования обеих сторон ([p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md)–[p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md))

```mermaid
flowchart LR
  CONFIG["Proxy TLSConnect/TLSAccept = psk"]
  CONFIG --> FILE["TLSPSKFile: защищённый файл"]
  FILE --> ID["TLSPSKIdentity: уникальная пара"]
  ID --> SERVER["Administration → Proxies → Encryption"]
  SERVER --> CHECK["Проверка совпадения PSK и Last seen"]
  CHECK --> OK["Данные по зашифрованному соединению"]
```

Исходная `cat`-проверка может раскрыть секрет, а `chmod 400/etc/...` и `Systemctl` на p354 — сломанные команды; см. [source-findings.md](source-findings.md).

## 4. Proxy group и failover ([p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md)–[p0360](../../../rag/chunks/p0301-p0400/p0360-c01.md))

```mermaid
flowchart TD
  GROUP["Administration → Proxy groups"]
  GROUP --> MEMBERS["Active и passive proxies"]
  MEMBERS --> ADDR["Address for active agents"]
  GROUP --> SETTINGS["Minimum number of proxies / Failover period"]
  HOST["Host: Monitored by Proxy group"] --> GROUP
  AGENT["Active Agent ServerActive: адреса proxies"] --> ADDR
  MEMBERS --> FAIL{"Proxy недоступен?"}
  FAIL -- "Да" --> CAP["Проверка количества и мощности оставшихся"]
  CAP --> REDIRECT["Переназначение мониторинга при допустимых условиях"]
  FAIL -- "Нет" --> NORMAL["Штатное распределение"]
```

Источник отдельно предупреждает, что SNMP traps могут потребовать дополнительного способа доставки на несколько экземпляров группы.

## 5. Discovery через proxy и два вида health checks ([p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md)–[p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md))

```mermaid
flowchart TB
  DISC["Network discovery rule: Discovery by = Proxy"] --> P["Zabbix proxy"]
  AUTOREG["Active agent: ServerActive → Proxy"] --> P
  P --> HOSTS["Новые hosts через Discovery/Autoregistration"]
  P --> LOCAL["Local Agent2 + proxy health monitored by proxy"]
  SERVER["Zabbix server"] --> REMOTE["Remote Zabbix proxy health; StatsAllowedIP"]
  REMOTE --> P
  P --> QUEUE["Administration → Queue: overview by proxy"]
  HOSTS --> DANGER["Удаление старых hosts из рецепта — destructive"]
```

Local monitoring может зависеть от состояния proxy. Remote monitoring обеспечивает альтернативный наблюдающий контур. **Никакой восстановительной процедуры удалённых хостов или истории в главе нет**.

## Контроль результата

Проверки: `Last seen(age)`, `Latest data`, proxy log, queue by proxy; проверить конкретную связь host→proxy, режим/TLS/PSK, сохранившиеся значения и фактическое failover, не только наличие объектов в UI. Конкретные настройки только на рисунках обозначены `RAG_MISS`.
