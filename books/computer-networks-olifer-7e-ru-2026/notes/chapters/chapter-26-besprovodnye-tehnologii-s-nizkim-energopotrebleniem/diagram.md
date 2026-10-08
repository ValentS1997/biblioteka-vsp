# Mermaid — глава 26: беспроводные технологии НЭ

book_id computer-networks-olifer-7e-ru-2026, PDF pp. 821–843, RAG p0821:c01–p0843:c01. **rag_only**. Схемы логические, не прямое извлечение рисунков 26.1–26.12.

## Энергетический компромисс

~~~mermaid
flowchart TD
  APP["Условия приложения: объём, частота, задержка"] --> Q{"Соответствует LP-профилю?"}
  Q -->|Редкие короткие события| LP["Минимизировать airtime и активный RX"]
  Q -->|Постоянные данные / real-time| NOT["НЭ может не удовлетворять требованиям"]
  LP --> RADIO["Radio TX → краткое RX → Sleep"]
  RADIO --> TRADE["Компромисс: bitrate, дальность, задержка, батарея"]
~~~

[p0821](../../../rag/chunks/p0801-p0900/p0821-c01.md)–[p0823](../../../rag/chunks/p0801-p0900/p0823-c01.md).

## Общее основание IEEE 802.15.4

~~~mermaid
flowchart TD
  PHY["802.15.4: PHY + MAC, max 127-byte frame"] --> R["Роли FFD/RFD и PAN coordinator"]
  PHY --> A["EUI-64 / 16-bit short address"]
  PHY --> M["CSMA/CA или beacon-superframe"]
  R --> TREE["Tree: родители / потомки"]
  R --> MESH["Mesh: соседние координаторы"]
  PHY --> Z["ZigBee: NWK + APS + applications"]
  PHY --> T["Thread: 6LoWPAN → IPv6 / RPL → CoAP/Matter (модель главы)"]
  PHY --> W["Wi-SUN FAN: 6LoWPAN → IPv6 / RPL (модель главы)"]
~~~

[p0824](../../../rag/chunks/p0801-p0900/p0824-c01.md)–[p0830](../../../rag/chunks/p0801-p0900/p0830-c01.md). Число EUI-64 адресов p0825 конфликтно; конкретная PHY скорость Wi-SUN зависит от режима.

## LoRaWAN: путь кадров и join

~~~mermaid
flowchart LR
  ED["End device: uplink / ALOHA"] --> GW1["Gateway 1"]
  ED --> GW2["Gateway 2"]
  GW1 --> NS["Network server: dedup + ADR"]
  GW2 --> NS
  NS --> AS["Application server: payload"]
  JS["Join server: MIC + session keys"] -.-> NS
  JS -.-> AS
  JS -.-> ED
~~~

[p0832](../../../rag/chunks/p0801-p0900/p0832-c01.md)–[p0835](../../../rag/chunks/p0801-p0900/p0835-c01.md). Шлюз ретранслирует, а не назначает эксклюзивный доступ устройству; параметры и архитектура зависят от реализации.

## Классы RX LoRaWAN

~~~mermaid
flowchart TD
  E["LoRaWAN конечное устройство"] --> A["Class A"]
  E --> B["Class B"]
  E --> C["Class C"]
  A --> RX["TX uplink → RX1 / RX2 → sleep"]
  B --> P["Периодические receive windows"]
  C --> CONT["Длительный / почти непрерывный RX"]
  RX --> ENERGY["Минимизация батарейного расхода / задержка downlink"]
  CONT --> POWER["Быстрее downlink, выше энергозатраты"]
~~~

[p0835](../../../rag/chunks/p0801-p0900/p0835-c01.md)–[p0836](../../../rag/chunks/p0801-p0900/p0836-c01.md).

## LoRa Chirp Spread Spectrum

~~~mermaid
flowchart TD
  DATA["SF bits → выбор символа n"] --> SHIFT["Циклический начальный сдвиг up-chirp"]
  SHIFT --> IQ["Модулятор: цифровой I/Q → DAC → RF"]
  IQ --> AIR["Канал: LoRa chirp signal"]
  AIR --> DOWN["Приёмник: синхронизация + эталонный down-chirp"]
  DOWN --> DE["Dechirping / комплексное перемножение"]
  DE --> DFT["DFT: поиск частотного пика"]
  DFT --> RESTORE["Восстановленное значение символа"]
~~~

[p0837](../../../rag/chunks/p0801-p0900/p0837-c01.md)–[p0843](../../../rag/chunks/p0801-p0900/p0843-c01.md). В тексте **несовместимы** формула `s(n)`, `B/M`, SF=9 frequency step и число поддержанных SF. Не использовать рисунок как подтверждение численной реализации.

## Operational boundary

Ни одна диаграмма не содержит исполнимых platform CLI, ключей, частотных настроек, измерений покрытия или rollback. Настройки, country radio permissions, исправление исходных формул: **[Needs confirmation]**.
