# Diagram — глава 20

RAG: computer-networks-olifer-7e-ru-2026, PDF 608–638, p0608:c01–p0638:c01. Mermaid — **концептуальный** пересказ текстовых фрагментов, не восстановленный оригинал рисунков.

## MPLS forwarding

~~~mermaid
flowchart LR
  IP["IP-пакеты внешней сети"] --> LE["Ingress LER"]
  LE --> F{"Классификация FEC"}
  F --> FTN["FTN: FEC → LSP"]
  FTN --> PUSH["Push ingress label"]
  PUSH --> L1["LSR1 / LFIB: Swap"]
  L1 --> L2["LSR2 / LFIB: Swap или Pop"]
  L2 --> E["Egress LER"]
  E --> OUT["IP-forwarding / другая сеть"]
  C["IGP + signalling / control plane"] -. "создают и поддерживают" .-> FTN
  C -.-> L1
  C -.-> L2
~~~

[p0613](../../../rag/chunks/p0601-p0700/p0613-c01.md)–[p0619](../../../rag/chunks/p0601-p0700/p0619-c01.md). LSP однонаправлен; для встречного потока нужен отдельный путь. PHP в примере означает Pop на предпоследнем hop.

## Создание путей: LDP или TE

~~~mermaid
flowchart TD
  G["Топология / IGP маршруты"] --> DEC{"Тип forwarding path"}
  DEC -->|LDP| L["Следование next-hop IGP"]
  L --> H["LDP Hello / session TCP 646"]
  H --> MAP["Downstream label mapping"]
  MAP --> LFIB["FTN/LFIB: установленный LSP"]
  DEC -->|TE| TED["OSPF-TE / IS-IS-TE: TED"]
  TED --> CSPF["CSPF: фильтр ограничений и маршрут"]
  CSPF --> METHOD{"Метод установки"}
  METHOD -->|RSVP-TE| R["Signalling + bandwidth reservation"]
  METHOD -->|SR-MPLS| S["Node-SID / Adj-SID в SR-Policy"]
  R --> TE["TE LSP / policy"]
  S --> TE
  PCE["LER или PCE/controller"] -. "вычисляет / задаёт TE-path" .-> CSPF
~~~

[p0623](../../../rag/chunks/p0601-p0700/p0623-c01.md)–[p0635](../../../rag/chunks/p0601-p0700/p0635-c01.md). Не отождествлять LDP shortest-IGP LSP с путём RSVP-TE либо SR Policy.

## Иерархия меток и защита

~~~mermaid
flowchart TD
  N["Основной LSP: рабочий канал"] --> X{"Отказ линии или узла?"}
  X -->|Нет| F["Forwarding по LFIB основной метки"]
  X -->|Да| D{"Есть заранее проложенный detour?"}
  D -->|Да| STACK["Push обходной метки над внутренней меткой основного LSP"]
  STACK --> B["Временный bypass LSP"]
  B --> POP["Pop верхней обходной метки"]
  POP --> REJOIN["Возврат в основной LSP с ожидаемой меткой"]
  D -->|Нет| REC["Нужно построить новый путь"]
  REJOIN --> REC
  REC --> VERIFY["Сверить восстановленный основной путь"]
~~~

[p0619](../../../rag/chunks/p0601-p0700/p0619-c01.md), [p0635](../../../rag/chunks/p0601-p0700/p0635-c01.md)–[p0638](../../../rag/chunks/p0601-p0700/p0638-c01.md).

**Safety:** эти схемы не являются конкретной процедурой изменения конфигурации; в RAG нет команд precheck, state change, rollback или live verification. Реальный failover и его время — [Needs confirmation].
