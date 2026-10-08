# Cheatsheet — глава 25: Wi-Fi и Bluetooth

Источник: `computer-networks-olifer-7e-ru-2026`, PDF pp. 784–820; RAG p0784:c01–p0820:c01; mode **rag_only**. Никаких фактических наблюдений Wi-Fi/Bluetooth клиента нет.

## Symptom / problem framing

Симптомы: SSID виден, но станция не подключается; association есть, но IP/интернет недоступен; нестабилен throughput, растут retransmissions; потери при роуминге между AP; mesh не находит путь; Bluetooth pairing проходит, но профиль не работает; Bluetooth деградирует рядом с Wi-Fi 2.4 GHz. Диагностировать **по слоям**, не отождествляя RF coverage, 802.11 association, L2/DS, IP/DHCP и сервисный профиль.

## Baseline / context

| Плоскость | Минимальные сущности для проверки | RAG |
|---|---|---|
| BSS | STA / AP, SSID, BSSID, текущий канал/DS | p0785–p0789 |
| Discovery / security | beacon, probe, authentication/association, AID | p0789–p0790 |
| MAC access | CSMA/CA, DIFS/SIFS, CW/backoff, ACK, NAV | p0795–p0798 |
| Hidden terminal | RTS/CTS/Duration/NAV, RTS threshold | p0798–p0799 |
| QoS | WMM access category, TXOP | p0800–p0801 |
| Efficiency | A-MSDU, A-MPDU, Block ACK / retry | p0801–p0803 |
| OFDMA | RU, AP scheduler, BSRP/BSR, Basic Trigger, MU-BAR | p0803–p0806 |
| ESS roaming | DS/L2 bridging, neighbor AP BSSID, 802.11k/v/r | p0807–p0810 |
| Mesh | 802.11s, PLMP, HWMP P-HWMP/R-HWMP, Mesh Portal | p0810–p0814 |
| Bluetooth | Classic piconet/scatternet, SCO/ACL, pairing/profiles, FHSS/LE/AFH | p0815–p0820 |

## Read-only checks

Конкретный CLI и OEM-возможности **источником не заданы**. Это вопросы к имеющемуся survey/config/telemetry:

1. **RF и BSS.** Каковы SSID, BSSID конкретного AP, текущий диапазон, канал, зона **двусторонней** слышимости? Есть ли конкурирующие BSS и канал interference? [p0785–p0789]
2. **Присоединение.** Обнаружены beacon/probe, успешны ли authentication и association, присвоен ли AID? Появился ли адрес IP через DHCP/другой механизм? SSID, association и IP — разные контрольные точки. [p0789–p0790]
3. **MAC.** Занята ли среда? Есть ли увеличение CW и повторы по ACK timeout, скрытые станции? Какие Duration/NAV и optional RTS/CTS применяются? [p0795–p0799]
4. **QoS/aggregation.** Какая WMM категория AC_VO/VI/BE/BK и TXOP; применяется A-MSDU или A-MPDU и как подтверждаются/повторяются кадры? [p0800–p0803]
5. **OFDMA.** Управляет ли AP DL/UL RU? Доступны ли AID/RU assignment, trigger/BSR/Block ACK и совместимость старых STA? **242/252 tones** конфликтует в самом RAG. [p0804–p0806]
6. **ESS.** Несколько AP действительно образуют общий L2/ESS через DS или находятся в разных IP-подсетях? Как клиент выбирает новую BSSID, задействованы ли 802.11k/v/r? [p0807–p0810]
7. **802.11s.** Узел является Mesh STA/Portal либо обычным extender? Настроены ли Mesh ID, neighbor peer link, HWMP-контексты и маршрут к порталу/соседу? [p0810–p0814]
8. **Bluetooth.** Устройство обнаруживается, проходит pairing, есть ли нужный профиль и канал Classic SCO/ACL либо LE? Не смешивать speed/coverage цифры из разных поколений. [p0815–p0819]
9. **Coexistence.** На одном 2.4 GHz работает Wi-Fi? В тексте есть AFH exclusion занятых каналов; фактическая поддержка и нагрузка **[Needs confirmation]**. [p0820]

## Interpretation

- Сильный сигнал ≠ разрешённая ассоциация; association ≠ готовый DHCP/IP; IP ≠ доступный сервис.
- BSS data path проходит через AP, даже если станции находятся рядом; mesh 802.11s использует иную L2 forwarding topology.
- CSMA/CA снижает вероятность коллизий, но не устраняет их; RTS/CTS имеет накладные расходы.
- WMM priority не равен доказанному QoS/SLA; aggregate frames ускоряют эфир, но имеют компромиссы по retransmission.
- Fast roaming 802.11k/v/r зависит от клиентской станции, реализации AP и метода защиты, не гарантирует универсальные 50 ms.
- Bluetooth piconet/Classic и BLE имеют разные роли и PHY, а «pairing» не подтверждает пригодность приложения без профиля.
- Конфликтные числа p0791, p0804/0805, p0818/0819/0820 зарегистрированы в source-findings.md.

## Next action

Построить read-only dependency trace: STA→RF→SSID/BSSID→association/auth→MAC access→AP/DS bridge→DHCP/IP→application; для mesh — Mesh ID→peer link→HWMP path; для Bluetooth — discovery→pairing→profile→channel/AFH. Записать vendor, firmware, измерения ошибок, CCA/airtime, retransmissions, roaming event times, connection type — **[Needs confirmation]** до получения конкретных данных.

## Modifying action

Изменение SSID/BSSID, радиоканала, ширины канала, AP security, RTS threshold, WMM, mesh peering, roaming/802.11r, Bluetooth visibility/pairing/AFH — **state-changing** и может прервать связь. Примеров конфигурации или scope авторизации в главе нет. Не выполнять в production без согласованного плана.

## Verification / acceptance checks

- Изоляция PHY, MAC, association, IP и application.
- BSS, ESS и 802.11s различены по архитектуре и control/data plane.
- CSMA/CA/RTS/CTS и AP-triggered OFDMA не смешаны.
- Для Bluetooth выбран стек Classic/LE и профиль, а не только факт обнаружения.
- Исторические/ошибочные частоты, мощности, speeds и сроки стандартизации не считаются current fact.
- Реальный uptime/throughput/roaming performance: **[Needs confirmation]**.

## Rollback

Read-only диагностика: **[Not applicable]**. Для любых изменений конфигурации required backup, change window, действующий rollback и post-check — **[Needs confirmation]**; в RAG нет исполнимого runbook.
