# Диаграммы — глава 25: Wi-Fi и Bluetooth

Источник: PDF pp. 784–820, RAG p0784:c01–p0820:c01, **rag_only**. Все схемы — аналитические абстракции по текстовым параграфам; не копии повреждённых рисунков 25.x.

## 1. BSS, ассоциация и IP

~~~mermaid
flowchart TD
  STA["Wi-Fi STA"] --> FIND["Passive Beacon / Active Probe"]
  FIND --> CHOOSE["SSID + BSSID: выбор AP"]
  CHOOSE --> AUTH["Authentication / association"]
  AUTH --> AID["AID, параметры MAC/PHY"]
  AID --> DHCP["DS / DHCP / IP"]
  DHCP --> APP["Приложение / внешняя сеть"]
  STA --> DATA["Кадр STA → AP"]
  DATA --> AP["AP: forwarding в другую STA или DS"]
  AP --> OTHER["STA-получатель / Ethernet DS"]
~~~

[p0785](../../../rag/chunks/p0701-p0800/p0785-c01.md)–[p0790](../../../rag/chunks/p0701-p0800/p0790-c01.md). Между STA внутри инфраструктурной BSS нет прямого логического пути мимо AP.

## 2. CSMA/CA и скрытые станции

~~~mermaid
flowchart TD
  Q["Есть кадр к отправке"] --> S{"Medium idle?"}
  S -->|Нет| W["Ждать, сохранить backoff"]
  W --> S
  S -->|Да| D["DIFS + random slots из CW"]
  D --> R{"RTS threshold используется?"}
  R -->|Нет| DATA["Передать DATA"]
  R -->|Да| RTS["RTS → CTS (AP)"]
  RTS --> NAV["Duration / NAV и SIFS"]
  NAV --> DATA
  DATA --> ACK{"ACK после SIFS?"}
  ACK -->|Да| DONE["Успех"]
  ACK -->|Нет| CW["Повтор / увеличить contention window"]
  CW --> S
~~~

[p0795](../../../rag/chunks/p0701-p0800/p0795-c01.md)–[p0799](../../../rag/chunks/p0701-p0800/p0799-c01.md). Отсутствие ACK не доказывает причину отказа; RTS/CTS не исключает все помехи.

## 3. QoS, aggregation и OFDMA

~~~mermaid
flowchart TD
  AP["AP / 802.11 MAC"] --> AC["WMM: VO / VI / BE / BK"]
  AC --> TXOP["TXOP в разделяемой среде"]
  TXOP --> AGG["A-MSDU или A-MPDU / Block ACK"]
  TXOP --> OFDMA["Wi-Fi 6/7: OFDMA scheduler"]
  OFDMA --> DL["DL: AID/RU → PPDU → MU-BAR / Block ACK"]
  OFDMA --> UL["UL: BSRP → BSR → Trigger → PPDU → Multi-STA ACK"]
  LEG["Старые STA"] --> CONTEND["CSMA/CA совместимость"]
  CONTEND --> TXOP
~~~

[p0800](../../../rag/chunks/p0701-p0800/p0800-c01.md)–[p0806](../../../rag/chunks/p0801-p0900/p0806-c01.md). Количество tones в последней RU: p0804 = 242, p0805 = 252, **[Needs confirmation]**.

## 4. ESS и mesh

~~~mermaid
flowchart TD
  ESS["ESS: несколько BSS / общий SSID"] --> B1["AP1, BSSID1"]
  ESS --> B2["AP2, BSSID2"]
  B1 <-->|"Ethernet DS / bridge"| B2
  STA["STA roaming"] --> MOVE["Client decision: BSSID1 → BSSID2"]
  MOVE --> KVR["802.11k/v/r помогают соседями/нагрузкой/переходом"]
  M["802.11s mesh"] --> PEER["Mesh STA / AP / Portal"]
  PEER --> PL["PLMP: peer link establishment"]
  PL --> HW["HWMP: L2 MAC paths"]
  HW --> P["Proactive: к portal"]
  HW --> R["Reactive: ad hoc по запросу"]
~~~

[p0807](../../../rag/chunks/p0801-p0900/p0807-c01.md)–[p0814](../../../rag/chunks/p0801-p0900/p0814-c01.md). ESS L2 roaming и маршрутизация 802.11s не одна архитектура. Extender также не равен 802.11s mesh.

## 5. Bluetooth Classic/LE и coexistence

~~~mermaid
flowchart TD
  BT["Bluetooth radio 2.4 GHz"] --> CL["Classic piconet"]
  CL --> MASTER["Главное устройство / планирование TDM + FHSS"]
  MASTER --> SUB["Подчинённые / SCO или ACL"]
  CL --> SC["Scatternet через multi-piconet node"]
  BT --> LE["Bluetooth Low Energy"]
  LE --> BLE["Отдельный PHY/stack: 40 × 2 MHz по главе"]
  BT --> DISC["Discovery → Pairing → Profile"]
  BT --> AFH["Adaptive Frequency Hopping"]
  WIFI["Wi-Fi 2.4 GHz occupies channels"] --> AFH
  AFH --> FREE["Исключить занятые части hopping set"]
~~~

[p0815](../../../rag/chunks/p0801-p0900/p0815-c01.md)–[p0820](../../../rag/chunks/p0801-p0900/p0820-c01.md). Источник использует историческую терминологию Classic/pairing и содержит некорректные BLE speeds/единицы мощности: source-findings.md.

## Безопасность операций

Схемы не содержат исполнимого vendor CLI. Живые каналы, параметры сети, credentials, результаты измерений и rollback: **[Needs confirmation]**. Никаких конфигурационных изменений не выполнено.
