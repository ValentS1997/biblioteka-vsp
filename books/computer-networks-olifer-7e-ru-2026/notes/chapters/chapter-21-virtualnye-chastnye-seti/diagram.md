# Mermaid — Глава 21. VPN

Канонический RAG: p0639:c01–p0654:c01, PDF pp. 639–654. Схемы являются логической интерпретацией текста, не реконструкцией исходных рисунков 21.1–21.9.

## Разделение свойств VPN

~~~mermaid
flowchart TD
  S["VPN через общую пакетную сеть"] --> O{"Кто поддерживает услугу?"}
  O --> A["Client-managed"]
  O --> B["Provider-managed"]
  S --> P{"Как достигаются свойства?"}
  P --> T["Транспортные туннели: разграничение трафика"]
  P --> C["Защищённые каналы: шифрование IPsec / TLS"]
  T --> D["L2/L3 service, адресное разделение, возможный TE/QoS в сети провайдера"]
  C --> E["Конфиденциальность и целостность поверх обычного доступа"]
  E --> W["Нет автоматической гарантии полосы и QoS в интернете"]
  D --> X["Изоляция не доказывает криптографическую защиту"]
~~~

Основа: [p0641](../../../rag/chunks/p0601-p0700/p0641-c01.md)–[p0645](../../../rag/chunks/p0601-p0700/p0645-c01.md).

## Сервисы Ethernet по MEF

~~~mermaid
flowchart TD
  U["UNI / EVC"] --> M{"Топология соединения"}
  M --> L["E-LINE: point-to-point"]
  M --> A["E-LAN: multipoint / all-to-all"]
  M --> T["E-TREE: roots / leaves"]
  L --> P["Private: целый UNI → EPL"]
  L --> V["Virtual private: по VLAN C-VID → EVPL"]
  A --> LP["Private: EPLAN"]
  A --> LV["Virtual private: EVPLAN"]
~~~

Основа: [p0645](../../../rag/chunks/p0601-p0700/p0645-c01.md)–[p0647](../../../rag/chunks/p0601-p0700/p0647-c01.md). E-TREE leaves не соединяются друг с другом по модели главы.

## MPLS L2VPN / VPWS

~~~mermaid
flowchart LR
  CE1["Сайт A / CE"] --> AC1["UNI / AC"]
  AC1 --> B1["PE1: Bridge B → NSP → VS"]
  B1 --> EN["PW inner label: service ID"]
  EN --> OUT["Outer MPLS label: transport LSP"]
  OUT --> P["Provider MPLS core: P routers"]
  P --> PE2["PE2: outer label removal / PW demux"]
  PE2 --> AC2["Remote AC / UNI"]
  AC2 --> CE2["Сайт B / CE"]
  BACK["Обратное направление"] -.-> BIDIR["Отдельный направленный LSP/PW label binding"]
~~~

Основа: [p0648](../../../rag/chunks/p0601-p0700/p0648-c01.md)–[p0652](../../../rag/chunks/p0601-p0700/p0652-c01.md). Реальный PW в тексте описан как двунаправленный сервис, составленный из двух однонаправленных направлений MPLS. Псевдоканал и transport tunnel сигнализируются независимо.

## VPLS: L2-эмуляция

~~~mermaid
flowchart TD
  I["VPLS instance клиента"] --> PE1["PE1: virtual switch + MAC table"]
  I --> PE2["PE2: virtual switch + MAC table"]
  I --> PE3["PE3: virtual switch + MAC table"]
  PE1 <-->|"PW full mesh"| PE2
  PE2 <-->|"PW full mesh"| PE3
  PE1 <-->|"PW full mesh"| PE3
  PE1 --> F["Known MAC: forwarding по таблице"]
  PE1 --> U["Unknown / broadcast: flooding в данном VPLS"]
  PE1 --> S["Split horizon: кадр из PW не пересылать в другой PW"]
~~~

Основа: [p0653](../../../rag/chunks/p0601-p0700/p0653-c01.md)–[p0654](../../../rag/chunks/p0601-p0700/p0654-c01.md). Исходный текст имеет неоднозначную метку PW при flooding между двумя сервисами. Диаграмма не воспроизводит эти конкретные имена: см. source-findings.md.

## Operational safety

Нет исполнимого CLI и пошаговой проверки реальной сети. Применение VLAN/AC/PW/LSP-binding требует отдельного change-control, верификации и rollback: [Needs confirmation].
