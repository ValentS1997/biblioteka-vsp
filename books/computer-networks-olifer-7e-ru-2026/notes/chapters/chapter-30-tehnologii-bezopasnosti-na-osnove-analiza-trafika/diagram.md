# Диаграммы — глава 30: traffic analysis security

Источник: RAG p0955:c01–p0990:c01, p0978:c02; PDF pp. 955–990, **rag_only**. Схемы концептуальные, не извлечение геометрии оригинальных рисунков 30.1–30.13. Они не являются схемами развёртывания или командными последовательностями.

## 1. Decision path filtering / stateful / application firewall

~~~mermaid
flowchart TD
  PKT["Ingress packet / flow"] --> PATH["Выбор интерфейса и зоны безопасности"]
  PATH --> ACL["ACL: src/dst IP, protocol, ports, first match"]
  ACL --> DENY{"Пакет разрешён?"}
  DENY -->|Нет| DROP["Drop / optional log"]
  DENY -->|Да| STATE["Stateful: таблица сеанса и его история, если применяется"]
  STATE --> APP["App inspection: HTTP/SMTP/FTP content, если поддерживается"]
  APP --> FWD["Proxy/NAT/route → protected service"]
  FWD --> AUDIT["Counters / IDS / audit"]
~~~

[p0955](../../../rag/chunks/p0901-p1000/p0955-c01.md)–[p0965](../../../rag/chunks/p0901-p1000/p0965-c01.md). Порядок компонентов зависит от конкретной реализации — это логическая учебная модель, не vendor packet pipeline.

## 2. Proxy и NAPT — разная роль посредника

~~~mermaid
flowchart LR
  CLI["Client 10.0.x.x"] --> PROXY["Application proxy"]
  PROXY --> EXT["External service"]
  CLI --> NAT["NAPT: IP:port mapping"]
  NAT --> INET["Internet peer"]
  INET --> NAT
  NAT --> CLI
  PROXY --> CACHE["Cache / content/user policy"]
~~~

[p0967](../../../rag/chunks/p0901-p1000/p0967-c01.md)–[p0970](../../../rag/chunks/p0901-p1000/p0970-c01.md); [p0971](../../../rag/chunks/p0901-p1000/p0971-c01.md)–[p0976](../../../rag/chunks/p0901-p1000/p0976-c01.md). Ни NAT, ни прокси сами по себе не подтверждают полноту security control.

## 3. Packet/flow monitoring, IDS/IPS и audit

~~~mermaid
flowchart TD
  NET["Коммутатор / маршрутизатор / host"] --> MIRROR["SPAN mirror + approved capture"]
  MIRROR --> PCAP["Packet analyzer: Wireshark / PCAP"]
  NET --> EXP["Flow exporter: aggregation/sampling"]
  EXP --> COL["NetFlow collector"]
  COL --> ANA["Flow analyzer + baseline"]
  PCAP --> IDS["IDS sensors / rules / correlation"]
  ANA --> IDS
  IDS --> ALERT["Security event → manager/operator + audit"]
  ALERT --> CHOICE{"IPS response authorised?"}
  CHOICE -->|Нет| REVIEW["Investigation"]
  CHOICE -->|Да| BLOCK["Change firewall / block traffic"]
~~~

[p0977](../../../rag/chunks/p0901-p1000/p0977-c01.md)–[p0985](../../../rag/chunks/p0901-p1000/p0985-c01.md), Wireshark continuation [p0978:c02](../../../rag/chunks/p0901-p1000/p0978-c02.md). PCAP содержит пакеты, NetFlow — метаданные; IDS ≠ IPS.

## 4. Audit and accountability

~~~mermaid
flowchart TD
  LOGS["Firewall / host / IDS event logs"] --> CLOCK["Align time and object identities"]
  CLOCK --> KEEP["Protected storage / retention / integrity"]
  KEEP --> CORR["Correlation + timeline reconstruction"]
  CORR --> RESPONSE["Analyst: investigate and improve policy"]
  RESPONSE --> UPDATE["Controlled change → verification"]
~~~

[p0984](../../../rag/chunks/p0901-p1000/p0984-c01.md)–[p0986](../../../rag/chunks/p0901-p1000/p0986-c01.md). Сбор/доступ к журналам должен быть авторизован.

## 5. DMZ и внутренние зоны

~~~mermaid
flowchart TD
  INTERNET["Internet / external providers"] --> EDGE["Outer perimeter firewall"]
  EDGE --> DMZ["Zone 1: public DNS / web / mail (DMZ)"]
  DMZ --> INNER["Inner firewall / interzone policy"]
  INNER --> PORTAL["Zone 2: corporate applications/data"]
  INNER --> EXTRA["Zone 3: extranet partners"]
  INNER --> USERS["Zone 4: internal workstations"]
  VPN["Zone 5: remote users via VPN"] --> INNER
  INNER --> ADMIN["Zone 6: security administration"]
  ADMIN --> IDS["IDS and firewall policy management"]
~~~

[p0986](../../../rag/chunks/p0901-p1000/p0986-c01.md)–[p0990](../../../rag/chunks/p0901-p1000/p0990-c01.md). Стрелки отражают контролируемые связи, а не безусловно разрешённое направление traffic: для каждого interzone flow нужна отдельная политика.

## Operational limits

Модели не содержат конкретной конфигурации устройства, pass/fail тестов и маршрутов работающей сети. Все дополнительные значения и rollback **[Needs confirmation]**. Ничего не настраивалось и не захватывалось.
