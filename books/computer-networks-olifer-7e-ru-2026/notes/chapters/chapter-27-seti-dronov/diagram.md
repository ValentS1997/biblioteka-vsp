# Диаграммы — глава 27. Сети дронов

Source: `computer-networks-olifer-7e-ru-2026`, RAG p0844:c01–p0883:c01, PDF pp. 844–883; **rag_only**. Mermaid — аналитическая схема по тексту, не реконструкция рисунков 27.1–27.14. В диаграммах нет команд управления БПЛА.

## Assisted vs supported и архитектура сети

~~~mermaid
flowchart TD
  UAV["UAV in wireless networks"] --> A["UAV-assisted: временный relay / aerial base station"]
  UAV --> S["UAV-supported: БПЛА составляют сеть"]
  S --> CENTRAL["Centralized: каждый дрон через ground base station"]
  S --> FANET["FANET: Ad Hoc peer mesh + gateway drone"]
  S --> CL["Multicluster: cluster head / gateway / other clusters"]
  CENTRAL --> SP["Single point of failure / ограничение покрытия"]
  FANET --> MOV["Динамические peer links / 3D mobility"]
  CL --> HIER["Intra-cluster and inter-cluster routing"]
~~~

[p0847](../../../rag/chunks/p0801-p0900/p0847-c01.md)–[p0855](../../../rag/chunks/p0801-p0900/p0855-c01.md).

## Navigation и connectivity — двухсторонняя зависимость

~~~mermaid
flowchart TD
  M["План миссии / траектории"] --> NAV["3D координаты, speed, direction"]
  NAV --> PHY["Neighbor radio reachability"]
  PHY --> TOPO["Изменение connectivity graph"]
  TOPO --> ROUTE["Адаптация маршрутов / кластеров"]
  ROUTE --> Q{"Требования к связности выполнены?"}
  Q -->|Да| CONT["Продолжить обмен"]
  Q -->|Нет| ADAPT["Weak: сеть адаптируется; strong: mission/trajectory и connectivity совместно"]
  ADAPT -.-> M
~~~

[p0858](../../../rag/chunks/p0801-p0900/p0858-c01.md)–[p0859](../../../rag/chunks/p0801-p0900/p0859-c01.md). Это модель взаимодействия подсистем, **не** алгоритм управления реальной траекторией.

## Стек связи FANET

~~~mermaid
flowchart TD
  APP["Application: mission / telemetry, MAVLink, MQTT, CoAP, RTP"] --> TR["Transport: UDP / TCP / QUIC"]
  TR --> IP["Network: IP + routing (AODV/OLSR/GPSR/BATMAN)"]
  IP --> L2["Radio access: Wi-Fi mesh, Sidelink, mmWave, SATCOM"]
  L2 --> PHY["Drone–drone / gateway–gateway / drone–ground"]
  NAV["GNSS / navigation"] -.-> IP
  BATT["Power / energy state"] -.-> IP
~~~

[p0861](../../../rag/chunks/p0801-p0900/p0861-c01.md)–[p0873](../../../rag/chunks/p0801-p0900/p0873-c01.md). Наличие названия технологии в книге не подтверждает совместимость интерфейсов или platform configuration.

## AODV: reactive route discovery и отказ

~~~mermaid
flowchart TD
  S["Source: нет маршрута к destination"] --> RREQ["RREQ broadcast: destination, origin, B-ID, TTL"]
  RREQ --> CHECK["Neighbors: suppress duplicate / keep reverse route"]
  CHECK --> D{"Destination / fresh route найден?"}
  D -->|Нет, TTL > 0| FWD["Forward RREQ / расширить область поиска"]
  FWD --> D
  D -->|Да| RREP["RREP unicast по обратному маршруту"]
  RREP --> TABLE["Route next hop / hop count / SN"]
  TABLE --> DATA["Data over current path"]
  DATA --> BREAK{"Link failure?"}
  BREAK -->|Да| RERR["RERR: invalidate affected routes"]
  BREAK -->|Нет| DATA
~~~

[p0875](../../../rag/chunks/p0801-p0900/p0875-c01.md)–[p0880](../../../rag/chunks/p0801-p0900/p0880-c01.md). Из примера следует возможность **неоптимального** маршрута. Это не спецификация точного формата на проводе, не универсальная конфигурация TTL.

## DTN: когда непрерывного IP-пути нет

~~~mermaid
flowchart TD
  P["Network partition: destination недостижим сейчас"] --> STORE["Store: буферизовать message"]
  STORE --> CHOICE{"Способ следующей передачи"}
  CHOICE --> EP["Epidemic: copies to available peers"]
  CHOICE --> PR["PROPHET: оцениваем шанс встречи"]
  CHOICE --> FERRY["Mobile ferry: дождаться/организовать contact"]
  EP --> CONTACT["Carry + forward при доступном контакте"]
  PR --> CONTACT
  FERRY --> CONTACT
  CONTACT --> DEST["Eventual delivery, если контакт случится"]
  DEST --> LIM["Нет гарантии реального времени / buffer-cost tradeoff"]
~~~

[p0881](../../../rag/chunks/p0801-p0900/p0881-c01.md)–[p0883](../../../rag/chunks/p0801-p0900/p0883-c01.md). Доставка при задержке — не безопасный управляющий канал полёта. Материалы не описывают реальную процедуру управления дроном.

## Operational boundary

Все реальные radio settings, mission-control, frequency licenses, navigation safety, verification и rollback: **[Needs confirmation]**. Конфигурационных изменений не проводилось.
