# Cheatsheet — глава 26: технологии низкого энергопотребления

Source: `computer-networks-olifer-7e-ru-2026`, PDF 821–843; RAG p0821:c01–p0843:c01; **rag_only**. Учебные критерии, не данные установленной LPWAN.

## Symptom / problem framing

Сценарии: датчик часто просыпается и разряжает батарею; узел не присоединяется к PAN; 6LoWPAN/IPv6 packets не проходят по малому MTU; mesh не находит маршрут; шлюз LoRaWAN принимает сообщения, но server/application не получает; Class A не видит downlink; мала дальность на выбранном SF. Не смешивать PHY, MAC, сетевую адресацию, join/security, приложение и duty cycle.

## Baseline / context

| Слой / задача | Что зафиксировать | RAG |
|---|---|---|
| Профиль потребления | bytes/event, период, TX/RX/sleep, повторы, питание | p0821–p0823 |
| 802.15.4 | PHY band, 127-byte MAC limit, FFD/RFD, EUI-64 vs short address | p0824–p0826 |
| PAN | PAN-coordinator/children, beacon, CSMA/CA, guaranteed slots | p0826–p0827 |
| ZigBee | NWK tree assignment / table-based mesh, APS bindings и приложения | p0828–p0829 |
| Thread / Wi-SUN FAN | IPv6, 6LoWPAN compression/fragment, RPL, CoAP/Matter | p0828–p0830 |
| LoRaWAN uplink | End device → gateways → network server → application server | p0832–p0835 |
| LoRaWAN join/security | Join server, MIC, network/app session keys | p0835 |
| Power classes | A RX1/RX2, B periodic receive, C almost-continuous RX | p0835–p0836 |
| LoRa PHY | CSS bandwidth B, spreading factor SF, symbol time and demod | p0837–p0843 |

## Read-only checks

1. **Профиль сообщений.** Действительно ли сообщения редкие и короткие? Сколько airtime и ретрансляций в сутки? Нет ли постоянного RX у батарейного узла? [p0821–p0822]
2. **802.15.4.** Какие роль FFD/RFD, MAC limit 127 bytes, короткий 16-bit адрес и PAN coordinator? Есть ли недопонимание между address width и числом достижимых узлов? В RAG конфликт. [p0824–p0826]
3. **Topology.** Требуется tree forwarding ZigBee или mesh NWK table? Может ли конечный батарейный узел оказаться транзитным? [p0826–p0829]
4. **IPv6.** Если Thread/Wi-SUN FAN, настроен ли путь `IPv6 → 6LoWPAN → 802.15.4` и маршрут RPL? Не переносить схему вендора на все версии стандарта без проверки. [p0830]
5. **LoRaWAN.** Принят ли uplink одним или несколькими gateways? Приходят ли копии на network server? Как обрабатываются MIC, duplicate frames и выбор gateway для downlink? [p0833–p0835]
6. **Класс устройства.** Для Class A downlink ожидается только в окнах после uplink; Class B — дополнительные периодические окна, C — доступность RX за счёт энергии. Соответствует ли класс требованиям задержки? [p0835–p0836]
7. **LoRa SF.** Известны B, SF, ожидаемая длительность символа/кадра, чувствительность, допустимая задержка? Не подставлять ошибочный пример шага частоты из p0840. [p0838–p0842]
8. **Регуляторный режим.** Частотный план, EIRP, duty cycle, permitted channels, регион и подтверждённая версия оборудования: **[Needs confirmation]**. Примеры 868/915 MHz — не universal approval. [p0833]

## Interpretation

- Энергия определяется не только bit rate: учитываются airtime, TX power, слушание, retries, батарея, периодичность.
- PHY/MAC IEEE 802.15.4 ≠ готовое приложение ZigBee/Thread/Wi-SUN.
- `6LoWPAN` решает вопрос передачи больших IPv6 packets через короткий MAC frame; `RPL` — маршруты.
- ZigBee использует собственный NWK/APS; Thread и Wi-SUN FAN в **авторской модели** базируются на IPv6.
- LoRaWAN gateways пересылают, network server дедуплицирует; конечное устройство не прикреплено жёстко к gateway.
- Class A экономит батарею ценой доступности downlink; Class C позволяет низкую задержку при повышенном расходе.
- Более высокий SF обычно означает более длительный символ; количественные помехоустойчивость и orthogonality в RAG упрощены.
- `M=2^SF`, `T_sym=M/B` — формулы модели; сдвиги частоты и количество SF в книге содержат противоречия.

## Next action

Составить read-only inventory: роль узла, батарея/питание, тип приложения, payload bytes, event frequency, airtime, frequency plan, security domain, neighbors/routes, MAC frame/fragmentation, LoRaWAN class/SF/gateway/server. Все параметры конкретной сети до наблюдений: **[Needs confirmation]**.

## Modifying action

Менять частоту/EIRP, join credentials, короткие адреса, PAN hierarchy, 6LoWPAN/RPL routing, ZigBee binds, LoRaWAN ADR/SF, RX windows или Class A/B/C **без change-control нельзя**: это может вызвать разрыв связи, превышение лимитов эфира или потерю сроков службы батареи. Источник не даёт платформенных команд и настроек.

## Verification / acceptance checks

- Разделены источник, расчёт и действительная телеметрия.
- Профиль трафика связан с энергобюджетом, требованиями дальности/latency.
- 802.15.4 MAC, NWK, IPv6 adaptation и application layers не смешаны.
- Для LoRaWAN задокументированы gateway/network/join/application server и Class.
- Конфликты EUI-64 capacity, 0–10 dBm «мВ», SF count и численный chirp shift зарегистрированы.
- Реальная работоспособность, автономность и security не объявлены подтверждёнными.

## Rollback

Для read-only анализа: **[Not applicable]**. Для изменения радиочастот, ключей, маршрутов или классов приёма исходная конфигурация, maintenance window, измерения и план отката: **[Needs confirmation]**. Изменения не проводились.
