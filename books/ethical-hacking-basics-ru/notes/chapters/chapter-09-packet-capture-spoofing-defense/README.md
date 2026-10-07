# Глава 9 — перехват пакетов, spoofing и обнаружение

> Общее название главы — редакционное. Source RAG подтверждает разделы `9.1 Утилиты, Детект снифферов, Анализ` и `9.2 Спуфинг-атаки (ARP, DNS, DHCP, sslstrip) и их обнаружение`. Статус: `RAG_GROUNDED`; reading state не меняется.

## Источник и границы

- Книга: «Основы этичного хакинга», А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Canonical source: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- PDF pages **246–273**, 1-indexed: **28 страниц / 39 addressable RAG chunks**.
- Первый chunk: `p0246:c01`; последний: `p0273:c01`.
- Overlap chunks: p. 246, 247, 248, 249, 250, 253, 256, 257, 264, 271, 272.
- PDF p. **274** начинает `10.1 Принципы, Претекстинг, Физическая соц.инженерия` и исключена.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY`; RAG: `READY_WITH_KNOWN_LIMITATIONS`; chapter contract v1.7.

## Структура

| Раздел | PDF pages | Содержание |
| --- | ---: | --- |
| **9.1 Утилиты, Детект снифферов, Анализ** | 246–262 | tcpdump/tshark/Wireshark, PCAP, BPF, capture/display filters, SPAN/port mirroring, promiscuous mode detection, packet analysis |
| **9.2 Спуфинг-атаки (ARP, DNS, DHCP, sslstrip) и их обнаружение** | 263–273 | ARP/DNS/DHCP spoofing concepts, sslstrip historical example, network detection indicators, reverse-path checks, DNSSEC/TCP discussion, source summary |

Boundary anchor: p.262 → p.263. Chapter summary begins at `p0271:c02` and continues through p.273.

## Главный принцип

**Packet capture is evidence collection, but capture scope and filters determine what evidence exists.** Capture filters can permanently exclude frames from a PCAP, while display filters only change what is shown after capture. Captured traffic may contain sensitive metadata/content, so interface/scope/storage must be controlled. Section 9.2 then uses spoofing attacks to explain what defenders should detect; those attack sequences are not operationalized here.

## Карта знаний

1. **Capture tools:** tcpdump, tshark and Wireshark collect frames/packets; PCAP preserves capture data for later analysis. `p0246:c01`–`p0254:c01`.
2. **Name resolution effect:** default address-to-name resolution can generate extra DNS traffic during capture; `tcpdump -n` avoids that behavior in the source example. `p0248:c01`.
3. **BPF:** capture filters can limit by host/network/protocol/port; excluded data is not saved to the capture. `p0255:c01`–`p0256:c01`.
4. **Wireshark analysis:** protocol decoding, streams, statistics, expert information and display filters help interpret saved captures. `p0253:c01`–`p0262:c01`.
5. **Sniffer detection:** local PROMISC flags may be visible on some OSes, but source notes inconsistent behavior; indirect DNS/traffic indicators are not proof. `p0257:c01`–`p0258:c01`.
6. **Spoofing concepts:** ARP poisoning, DNS redirection, DHCP exhaustion/rogue configuration and sslstrip illustrate MITM/redirection paths. `p0263:c01`–`p0270:c01`.
7. **Defensive detection:** excessive unsolicited ARP replies, unexpected DHCP offers/discovery volume, switch MAC-table tracing, reverse-path checks and DNS protections are discussed. `p0270:c01`–`p0273:c01`.

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

Source содержит два задания:
- p.252: capture traffic with tcpdump on the local network and save it to a file;
- p.254: open that capture and filter web traffic in Wireshark.

Они оформлены с privacy/scope safeguards; capture чужого трафика без разрешения не подразумевается.

## Safety boundary

ARP/DNS/DHCP spoofing, MITM and sslstrip examples can redirect or intercept third-party traffic. The chapter artifacts preserve terminology, indicators and defensive interpretation but do **not** reproduce an executable spoofing/MITM sequence. Authorized interface, network ownership, privacy policy, storage/retention and lab scope: **[Needs confirmation]**.
