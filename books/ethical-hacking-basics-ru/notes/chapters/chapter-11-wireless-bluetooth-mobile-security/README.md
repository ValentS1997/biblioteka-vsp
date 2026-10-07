# Глава 11 — Wi‑Fi, Bluetooth и мобильные устройства

> Общее название главы — редакционное. Source RAG подтверждает разделы `11.1 Wi-Fi - типы, аутентификация, шифрование, BYOD, атаки` и `11.2 Bluetooth - сканирование, атаки. Мобильные устройства`. Статус: `RAG_GROUNDED`; reading state не меняется.

## Источник и границы

- Книга: «Основы этичного хакинга», А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Canonical source: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- PDF pages **298–323**, 1-indexed: **26 страниц / 39 addressable RAG chunks**.
- Первый chunk: `p0298:c01`; последний: `p0323:c01`.
- Overlap chunks: p. 298, 299, 302, 303, 304, 306, 309, 312, 317, 319, 320, 321, 322.
- PDF p. **324** начинает `12.1 Атаки на веб-приложения - OWASP, XSS, SQL injection` и исключена.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY`; RAG: `READY_WITH_KNOWN_LIMITATIONS`; chapter contract v1.7.

## Структура

| Раздел | PDF pages | Содержание |
| --- | ---: | --- |
| **11.1 Wi-Fi - типы, аутентификация, шифрование, BYOD, атаки** | 298–316 | Wi‑Fi topologies/standards, probe/auth/association, WEP/WPA/WPA2/WPA3, BYOD, monitoring/recon, deauth/evil twin/KRACK concepts |
| **11.2 Bluetooth - сканирование, атаки. Мобильные устройства** | 317–323 | pairing, scanning, bluejacking/bluesnarfing/bluebugging/bluesmack concepts, Android/iOS/mobile threats, smishing, source summary |

Boundary anchors: p.316 → p.317; p.323 → p.324.

## Главный принцип

**Wireless security depends on protocol state, authentication/encryption design and radio visibility; testing can directly disrupt connectivity.** Monitor-mode observation and passive survey are evidence-gathering tasks, while deauthentication, evil twin, Bluetooth abuse and credential-capture patterns are active/high-impact. Source itself warns not to test neighbors’ APs and notes that deauthentication can break wireless-dependent services. `p0307:c01`.

## Карта знаний

1. **Wi‑Fi topology/identity:** infrastructure/ad-hoc concepts, SSID/BSSID, probe requests/responses, authentication and association. `p0298:c01`–`p0302:c01`.
2. **Encryption/authentication:** WEP → WPA → WPA2 → WPA3; Personal/Enterprise; 802.1X/EAP and four-way handshake/SAE concepts. `p0302:c01`–`p0306:c01`.
3. **BYOD:** device trust, guest/isolated networks, NAC concepts and additional authentication/VPN boundaries. `p0306:c01`.
4. **Wireless reconnaissance:** OS network list, Kismet/WiFi Explorer/NetSpot, monitor-mode capture, channel awareness and radiotap/802.11 evidence. `p0307:c01`–`p0312:c01`.
5. **Wi‑Fi attacks:** deauthentication, evil twin and KRACK are source threat patterns; exact offensive sequences are not operationalized. `p0307:c01`, `p0311:c01`–`p0316:c01`.
6. **Bluetooth:** discovery/pairing and historic attack classes (bluejacking, bluesnarfing, bluebugging, bluesmack). `p0317:c01`–`p0320:c01`.
7. **Mobile:** third-party app stores, app data collection/leakage, public/rogue Wi‑Fi, phishing/smishing and platform fragmentation/patching concerns. `p0320:c01`–`p0323:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Практические задания

Source содержит три задания:
1. p.301 — monitor-mode observation of disconnect/reconnect authentication traffic;
2. p.307–308 — compare OS-visible WLANs with survey tools by signal level;
3. p.315–316 — deauthentication test against **your own AP**, observed in Wireshark.

Третье задание — disruptive. Оно сохраняется как source exercise с lab-only guardrails, без готовой deauthentication command line.

## Safety boundary

Deauthentication, evil-twin, key/capture attacks, rogue APs, active Bluetooth scanning/exploitation and mobile credential/data interception can disrupt or compromise third-party systems. Exact attack commands/workflows are not reproduced. Authorized radio scope, test AP/device ownership, channel plan, outage window, privacy/storage and recovery path: **[Needs confirmation]**.
