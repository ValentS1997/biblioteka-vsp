# Протокольные операции и формулы — глава 26

Источник: RAG p0821:c01–p0843:c01, PDF 821–843. **rag_only**.

## Исполнимые CLI

**Глава не содержит подтверждённых Linux/vendor CLI для ZigBee, Thread, Wi-SUN FAN, LoRaWAN, IPv6 или LoRa PHY.** Ниже — именованные механизмы, формулы и ограничения. Протокольные сообщения не являются безопасной инструкцией к отправке в реальную сеть.

## IEEE 802.15.4, ZigBee, Thread, Wi-SUN FAN

| Объект / механизм | Назначение по книге | Класс воздействия | RAG |
|---|---|---|---|
| FFD / RFD | координатор, маршрутизатор или маломощное оконечное устройство | роль при проектировании; смена роли state-changing | p0825–p0826 |
| EUI-64 / 16-bit short address | глобальный идентификатор и локальный адрес после join | allocation state-changing; неверное число адресов в исходнике | p0825 |
| Beacon, PAN join, coordinator | обнаружение и создание дерева соседских связей | radio workload / membership state | p0826–p0827 |
| CSMA/CA, guaranteed time slots | распределённый/централизованный доступ | MAC workload, change radio scheduling state-changing | p0827 |
| ZigBee NWK / APS / device bindings | маршруты по дереву/таблице, мультиплексирование и приложение | network/application state | p0828–p0829 |
| IPv6 / 6LoWPAN | compression и fragmentation/reassembly поверх MAC 127 bytes | data-plane adaptation | p0830 |
| RPL | маршрутизация маломощных сетей | control-plane routing changes | p0830 |
| UDP, CoAP, Matter | верхние слои в схеме Thread, CoAP у Wi-SUN FAN | application traffic / version-specific | p0830 |

## LoRaWAN

| Операция | Роль по источнику | Класс | RAG |
|---|---|---|---|
| ALOHA uplink | несогласованная передача end device | airtime / возможные коллизии | p0833 |
| Gateway → UDP/IP network server | ретрансляция и прикладывание RX quality | workload, не radio MAC coordinator | p0834 |
| Duplicate filtering | network server выбирает копию кадра от нескольких gateways | server-side data-plane | p0834 |
| Join request / MIC verification | authentication и назначение сеансового контекста | security state-changing | p0835 |
| Network/application session keys | разные домены защиты в модели главы | secret-management operation | p0835 |
| ADR | адаптивная скорость/SF при управлении сервером | state-changing radio settings | p0835 |
| Class A RX1/RX2 | окна приёма после uplink | duty-cycle design | p0835–p0836 |
| Class B / C | периодические окна либо почти постоянный RX | energy / latency tradeoff | p0836 |

## Формулы PHY из текста — только учебное применение

- Линейный chirp: `f(t) = f_min + R·t`; положительная полоса `B = f_max − f_min`; `T_sym = B/R`. **В исходном RAG p0838 порядок f_min−f_max ошибочен.**
- `M=2^SF`, `SF ∈ {7,8,9,10,11,12}` (в списке **шесть** значений); `T_sym = M/B = 2^SF/B`. [p0840]
- При `SF=9`, `B=250 kHz` из записи `Δf=B/M` получается около **488 Hz**; текст источника утверждает **1024 Hz**. Здесь значение представлено как проверка внутренней арифметики, не как восстановление испорченного примера. [p0840]
- Начальное смещение `s(n) = −B/2 + n·B/2` приведено в RAG p0839, но оно не согласуется с `M` различными частотными шагами и `n=0..M−1` на p0840. Не применять без adjudication.
- Dechirp: принятый up-chirp умножается на эталонный down-chirp, затем дискретное преобразование Фурье обнаруживает частоту с наибольшей амплитудой, соответствующую символу. [p0841–p0842]
- Заявления об ортогональности SF, −20 dB SNR и 10–15 km — примеры уровня главы, не измерения и не бесколлизионная гарантия. [p0842–p0843]

## Безопасность изменений, проверка и rollback

**Read-only:** анализ существующих topology, power budget и данных телеметрии. **Workload-generating:** join, beacon, radio uplink и диагностические отправки. **State-changing:** network membership, keys, ADR, frequency/SF, RX-window class, mesh/routes. Любые команды, назначение частот, регуляторный допуск, rollback, авторизация и post-check: **[Needs confirmation]**. Никаких изменений оборудования не проводилось.