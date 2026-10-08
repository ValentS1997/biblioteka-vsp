# Mermaid — глава 24. Сотовые и спутниковые сети

Источник: RAG p0721:c01–p0783:c01, PDF pp. 721–783, strict rag_only. Диаграммы **концептуальные**: не копии рисунков 24.1–24.19 и не фактическая топология оператора.

## LTE: radio access, EPC и GTP

~~~mermaid
flowchart LR
  UE["UE / C-RNTI"] <-->|"radio DL/UL"| RAN["Базовая станция LTE"]
  RAN <-->|"GTP-U user traffic"| SGW["SGW: локальный туннель"]
  SGW <-->|"GTP-U user traffic"| PGW["PGW: пакетный шлюз"]
  PGW <-->|"IP"| INT["Интернет / внешние сети"]
  MME["MME: mobility / attach control"] -. "control / tunnel coordination" .-> SGW
  MME -.-> RAN
  MME -. "authentication" .-> HSS["HSS: домашняя база абонентов"]
~~~

[p0723](../../../rag/chunks/p0701-p0800/p0723-c01.md)–[p0726](../../../rag/chunks/p0701-p0800/p0726-c01.md), [p0731](../../../rag/chunks/p0701-p0800/p0731-c01.md)–[p0739](../../../rag/chunks/p0701-p0800/p0739-c01.md). Здесь SGW — промежуточная точка tunnel chaining; GTP-C/UE-IP/TEID — не одно и то же. Обозначения S1 и S5/S8 в p0735 противоречат ориентации учебных P-S/S-B: source-findings.md.

## Attach, handover и IMS

~~~mermaid
flowchart TD
  A["UE начинает attach"] --> C["Cell search / sync / preamble"]
  C --> T["Temporary C-RNTI / radio resources"]
  T --> AUTH["MME + HSS: authentication"]
  AUTH --> IP["PGW: IP / SGW: туннельные контексты"]
  IP --> D["Data session"]
  D --> HO{"Изменение соты?"}
  HO -->|Да| H["Source/target base station: handover"]
  H --> U["Новый C-RNTI, ключи, tunnel update"]
  U --> D
  D --> IMS["IMS: SIP REGISTER / INVITE"]
  IMS --> SIP["P-/S-/I-CSCF + HSS"]
  SIP --> RTP["RTP: media после setup"]
~~~

[p0735](../../../rag/chunks/p0701-p0800/p0735-c01.md)–[p0743](../../../rag/chunks/p0701-p0800/p0743-c01.md), [p0750](../../../rag/chunks/p0701-p0800/p0750-c01.md)–[p0760](../../../rag/chunks/p0701-p0800/p0760-c01.md). Это этапы разных функций, а не гарантированная линейная транзакция всех вызовов.

## 5G network slicing и SBA

~~~mermaid
flowchart TD
  APP["Сервисы: eMBB / URLLC / MIoT / V2X"] --> SL["Network slice selection / NSSF"]
  SL --> CP["5G control plane"]
  CP --> AMF["AMF: access + mobility"]
  CP --> SMF["SMF: session control"]
  CP --> AUSF["AUSF: authentication"]
  CP --> NRF["NRF: service function registry"]
  CP --> UDM["UDM: subscriber management"]
  AMF -.-> NR["5G NR: access"]
  SMF --> UPF["UPF: user traffic"]
  NR --> UPF
  UPF --> EDGE["Edge services / data network"]
~~~

[p0763](../../../rag/chunks/p0701-p0800/p0763-c01.md)–[p0769](../../../rag/chunks/p0701-p0800/p0769-c01.md). SBA упрощён до логических связей: реальная схема стандартных интерфейсов и право вызова функций зависят от версии, не подтверждённой в контексте.

## Спутники, доступ и NTN

~~~mermaid
flowchart TD
  UE["User terminal / phone"] --> LINK["Satellite radio access"]
  LINK --> ORBIT{"Orbit / relay role"}
  ORBIT --> GEO["GEO: большой охват / высокая задержка"]
  ORBIT --> MEO["MEO: компромисс между охватом и задержкой"]
  ORBIT --> LEO["LEO: движущиеся соты / Doppler"]
  LEO --> MOD{"5G NTN mode"}
  MOD --> TR["Transparent: relay to ground base station"]
  MOD --> REG["Regenerative: satellite acts as base station"]
  REG --> ISL["Опционально: inter-satellite links / mesh"]
  TR --> GW["Gateway / terrestrial core"]
  REG --> GW
  ISL --> GW
~~~

[p0774](../../../rag/chunks/p0701-p0800/p0774-c01.md)–[p0783](../../../rag/chunks/p0701-p0800/p0783-c01.md). Описания Starlink/Iridium — исторические примеры, не подтверждение текущей сети.

## Границы использования

В материале отсутствуют platform CLI, фактический UE-state, TEID mappings, действующие радиопараметры, site topology, нормативы и rollback. Изменение GTP, IMS, 5G slice, base station либо NTN маршрута: **[Needs confirmation]**.
