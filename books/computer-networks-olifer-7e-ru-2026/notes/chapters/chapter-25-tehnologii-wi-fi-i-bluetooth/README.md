# Глава 25 — Технологии Wi-Fi и Bluetooth

**Artifact state:** RAG_GROUNDED; CI / review / merge: **[Needs confirmation]**. Наличие анализа не подтверждает прочтение главы.

## Provenance / границы

- В. Олифер, Н. Олифер. «Компьютерные сети. Принципы, технологии, протоколы», **7-е изд., 2026**, часть VI.
- Book ID: `computer-networks-olifer-7e-ru-2026`.
- Source: `source/book.pdf`; SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d` (RAG acceptance и `source/SHA256` совпадают).
- **Source policy:** `rag_only`. Канонический PDF напрямую не читался; model memory и external web не использовались для исправления либо восполнения содержания.
- **PDF pages: 784–820**; **printed pages: 783–819**. Объём **37 PDF-страниц**, RAG endpoints `p0784:c01`–`p0820:c01`. Это 37 адресуемых страниц; наличие дополнительных `c02+` чанков отдельно не проверялось.
- Начало: [p0784:c01](../../../rag/chunks/p0701-p0800/p0784-c01.md) — заголовок «ГЛАВА 25».
- Конец: [p0820:c01](../../../rag/chunks/p0801-p0900/p0820-c01.md) — «Сосуществование Bluetooth и Wi-Fi».
- Следующая глава: [p0821:c01](../../../rag/chunks/p0801-p0900/p0821-c01.md) — «ГЛАВА 26. Беспроводные технологии с низким энергопотреблением».
- **Boundary VERIFIED**; RAG manifest `READY_WITH_KNOWN_LIMITATIONS`, ingestion acceptance `ACCEPTED`.
- Contract: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG anchors | Содержание |
|---|---:|---|---|
| Wi-Fi и BSS | 784–788 | p0784–p0788 | IEEE 802.11, STA/AP, DS, физическая и логическая звезда |
| Присоединение станции | 789–790 | p0789–p0790 | SSID/BSSID, beacon, probe, association, authentication, AID, DHCP |
| Физический и MAC-уровни | 790–795 | p0790–p0795 | PHY table, 2.4/5/6 GHz, PPDU, 802.11 frame/3–4 addresses, power save |
| CSMA/CA и скрытая станция | 795–799 | p0795–p0799 | DCF, DIFS/SIFS, random backoff, NAV, RTS/CTS, ACK |
| QoS и aggregation | 800–803 | p0800–p0803 | WMM/EDCF AC, TXOP, A-MSDU, A-MPDU, Block ACK |
| OFDMA в Wi-Fi 6/7 | 803–806 | p0803–p0806 | AP scheduling, RU, DL MU-BAR/Block ACK, UL BSRP/BSR/Trigger |
| ESS и роуминг | 807–810 | p0807–p0810 | Ethernet DS, один L2-домен, BSSID, 802.11k/v/r |
| 802.11s mesh | 810–814 | p0810–p0814 | Mesh STA/AP/Portal, PLMP, HWMP proactive/reactive |
| Bluetooth: PAN, piconet | 814–817 | p0814–p0817 | Master/subordinate в модели книги, scatternet, SCO/ACL, profiles/pairing |
| Bluetooth PHY, BLE, coexistence | 817–820 | p0817–p0820 | FHSS/TDM, Bluetooth LE, каналы, AFH coexistence |

## Центральный тезис

**Wi-Fi и Bluetooth используют общую радиосреду, но проектируют взаимодействие узлов по-разному.** В инфраструктурном Wi-Fi AP задаёт логическую звезду, MAC-уровень координирует доступ через CSMA/CA и, в новых поколениях, OFDMA. ESS расширяет BSS общей распределительной системой, а 802.11s строит multi-hop mesh. В классической модели Bluetooth пикосеть использует главное устройство, временное разделение и частотные переходы FHSS; BLE вводит отдельные энергосберегающие механизмы.

## Проверенные положения

1. **BSS:** AP — центр логической звезды; две ассоциированные станции обмениваются кадрами **через AP**, даже если физически могут слышать друг друга. DS связывает AP с внешней L2/корпоративной сетью; DS не обязателен для самого BSS. [p0785](../../../rag/chunks/p0701-p0800/p0785-c01.md)–[p0787](../../../rag/chunks/p0701-p0800/p0787-c01.md).
2. **Идентификаторы и присоединение:** SSID — символьное имя сети, BSSID — идентификатор BSS (в модели главы MAC AP). Beacon = passive discovery, probe = active discovery; затем authentication/association, AID и возможное назначение IP через DHCP. Идентичность SSID **не** доказывает доверенный AP. [p0789](../../../rag/chunks/p0701-p0800/p0789-c01.md)–[p0790](../../../rag/chunks/p0701-p0800/p0790-c01.md).
3. **PHY/802.11 frame:** глава сравнивает поколения, диапазоны 2.4/5/6 GHz, OFDM/OFDMA и PPDU. MAC-кадр содержит Frame Control, Duration, 3–4 MAC-addresses (в зависимости от To/From AP), Sequence Control, payload, CRC; физический PPDU и MAC frame не тождественны. Таблица PHY/частот включает ошибки/датированные регуляторные обобщения: source-findings.md. [p0790](../../../rag/chunks/p0701-p0800/p0790-c01.md)–[p0794](../../../rag/chunks/p0701-p0800/p0794-c01.md).
4. **CSMA/CA:** станция слушает среду, ждёт DIFS и случайное окно CW, при занятости замораживает остаток backoff; получение ACK после SIFS подтверждает принятие кадра. Поле Duration/NAV резервирует среду виртуальным carrier-sense. Отсутствие ACK не доказывает исключительно коллизию; объяснение в книге упрощённое. [p0795](../../../rag/chunks/p0701-p0800/p0795-c01.md)–[p0798](../../../rag/chunks/p0701-p0800/p0798-c01.md).
5. **Hidden station:** RTS → CTS → DATA → ACK, с интервалами SIFS и NAV, позволяет скрытым друг от друга станциям узнать о занятости AP; механизм может быть пороговым и несёт overhead. [p0798](../../../rag/chunks/p0701-p0800/p0798-c01.md)–[p0799](../../../rag/chunks/p0701-p0800/p0799-c01.md).
6. **WMM/EDCF:** четыре категории `AC_VO`, `AC_VI`, `AC_BE`, `AC_BK` с различными параметрами доступа и TXOP. Приоритет — преимущество в конкуренции, **не автоматически гарантированная задержка**. [p0800](../../../rag/chunks/p0701-p0800/p0800-c01.md)–[p0801](../../../rag/chunks/p0801-p0900/p0801-c01.md).
7. **Агрегирование:** A-MSDU объединяет данные нескольких пакетов в одну MAC-единицу; A-MPDU агрегирует кадры со своими заголовками/контрольными суммами, использует Block ACK и выборочный повтор. Утверждение книги о разных конечных получателях A-MPDU — **[Needs confirmation]** для строгого сопоставления стандарту, см. findings. [p0801](../../../rag/chunks/p0801-p0900/p0801-c01.md)–[p0803](../../../rag/chunks/p0801-p0900/p0803-c01.md).
8. **Wi-Fi 6/7 OFDMA:** AP распределяет RU в период полученного TXOP. В DL используются назначения RU и MU-BAR / Block ACK; в UL — BSRP → BSR → Basic Trigger → передача → Multi-STA Block ACK в модели главы. Значения **242 / 252 tones** противоречат друг другу, точное значение не исправляется без проверки. [p0803](../../../rag/chunks/p0801-p0900/p0803-c01.md)–[p0806](../../../rag/chunks/p0801-p0900/p0806-c01.md).
9. **ESS и roaming:** несколько BSS соединены L2 DS, один SSID, разные BSSID; в описанной модели одна IP-подсеть, при переходе точка AP меняется, IP может остаться тем же. Клиент инициирует roaming; 802.11k/v/r ускоряют поиск AP/выбор/защищённое переприсоединение, но не гарантируют одинаковое время у всех устройств. [p0807](../../../rag/chunks/p0801-p0900/p0807-c01.md)–[p0810](../../../rag/chunks/p0801-p0900/p0810-c01.md).
10. **Mesh 802.11s:** Mesh STA, Mesh AP, Mesh Portal; PLMP создаёт соседские связи. Маршрутизация по MAC/канальному уровню через HWMP: proactive к порталу и reactive по запросу между mesh-узлами. **Mesh extender не равен 802.11s mesh-node.** [p0810](../../../rag/chunks/p0801-p0900/p0810-c01.md)–[p0814](../../../rag/chunks/p0801-p0900/p0814-c01.md).
11. **Bluetooth Classic:** piconet с главным узлом, подчинёнными, scatternet через узел-мост; SCO для времени-чувствительного трафика, ACL для данных; pairing и профили реализуют сервисы поверх собственного стека. [p0815](../../../rag/chunks/p0801-p0900/p0815-c01.md)–[p0817](../../../rag/chunks/p0801-p0900/p0817-c01.md).
12. **Bluetooth PHY/LE:** источник описывает FHSS, 79 каналов по 1 MHz и 625 μs time-slot для Classic; Bluetooth LE — отдельную модель с 40 каналами по 2 MHz и режимами энергосбережения. Завершающий раздел рассматривает адаптивное исключение занятых Wi-Fi частот (AFH). Числа скоростей и единиц LE в RAG конфликтны. [p0818](../../../rag/chunks/p0801-p0900/p0818-c01.md)–[p0820](../../../rag/chunks/p0801-p0900/p0820-c01.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — учебный read-only troubleshooting и критерии.
- [commands.md](commands.md) — подтверждённые протокольные кадры/операции, без выдуманных конфигурационных CLI.
- [diagram.md](diagram.md) — Mermaid BSS/association, CSMA/CA, OFDMA, ESS/mesh, Bluetooth.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная сводка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная сводка.
- [source-findings.md](source-findings.md) — численные/терминологические конфликты RAG и ограничения.

## Условные артефакты и ограничения

На [p0820:c01](../../../rag/chunks/p0801-p0900/p0820-c01.md) завершается Bluetooth coexistence, [p0821:c01](../../../rag/chunks/p0801-p0900/p0821-c01.md) начинает главу 26. Самостоятельных chapter-end summary и review questions/answers **в указанных границах не выявлено**; `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

Текстовый RAG не содержит машиночитаемой геометрии рисунков 25.1–25.14. Диаграммы и SVG — **аналитические схемы по тексту**, не копии оригинальных изображений. Числа на страницах 791, 805, 818–820 нельзя подставлять в производственные расчёты или современный radio-domain policy без верификации.
