# Глава 15 — Протоколы транспортного уровня TCP и UDP

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0442:c01` … `p0471:c01`.
- PDF pages: **442–471**, включительно; **30** адресуемых RAG chunks.
- Печатные страницы книги: **441–470**.
- На `p0442:c01` явно начинается «Глава 15. Протоколы транспортного уровня TCP и UDP».
- На `p0472:c01` явно начинается «Глава 16. Протоколы маршрутизации и технология SDN»; `p0472:c01` в scope главы 15 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Ports / sockets / multiplexing | 442–445 | `p0442:c01`–`p0445:c01` | transport demultiplexing, well-known/dynamic ports, socket = IP+port |
| UDP | 445–446 | `p0445:c01`–`p0446:c01` | datagram service, 8-byte header, checksum, message boundaries |
| TCP segment and connection | 446–452 | `p0446:c01`–`p0452:c01` | byte stream, header/flags, SYN/ACK/FIN, connection identity, per-connection demultiplexing |
| ARQ / sliding-window methods | 452–460 | `p0452:c01`–`p0460:c01` | Stop-and-Wait, Go-Back-N, Selective Repeat, cumulative vs selective ACK |
| TCP sliding window / flow control | 461–466 | `p0461:c01`–`p0466:c01` | byte numbering, ACK number, receiver window, buffers, retransmission timer, adaptive RTT |
| Congestion control | 466–470 | `p0466:c01`–`p0470:c01` | flow vs congestion control, congestion window, slow start, duplicate ACK, ECN |
| TCP evolution | 470–471 | `p0470:c01`–`p0471:c01` | SACK, CUBIC, BBR, HyStart++, ECN/L4S-like text, Westwood+, MPTCP source snapshot |

Boundary anchors: [p0442:c01](../../../rag/chunks/p0401-p0500/p0442-c01.md) → [p0471:c01](../../../rag/chunks/p0401-p0500/p0471-c01.md) → [p0472:c01](../../../rag/chunks/p0401-p0500/p0472-c01.md).

## Главный принцип

**Transport protocols turn host-to-host IP delivery into application-to-application communication.** UDP preserves message boundaries with minimal service; TCP builds a reliable duplex byte stream by combining connection state, sequence numbers, acknowledgements, windows, timers, retransmission and congestion control.

## Что важно вынести

1. **Transport multiplexing/demultiplexing maps network traffic to applications.** Ports identify application endpoints; the source distinguishes assigned/well-known and locally allocated dynamic port numbers. `p0442:c01`–`p0444:c01`.
2. **A socket is presented as the pair `(IP address, port number)`.** UDP and TCP sockets use their respective transport-port namespaces. `p0444:c01`.
3. **UDP is message-oriented and best effort.** One application message becomes one UDP datagram; UDP adds an 8-byte header and does not guarantee delivery. `p0445:c01`–`p0446:c01`.
4. **UDP detects corruption but does not repair it.** If its checksum indicates an error, the datagram is discarded. `p0446:c01`.
5. **TCP is stream-oriented.** It treats application data as an unstructured byte stream and divides it into segments independently of application message boundaries. `p0446:c01`–`p0447:c01`.
6. **TCP header state reflects reliability functions.** Sequence/acknowledgement numbers, window, checksum and flags such as SYN/ACK/FIN/RST/PSH/URG support connection management and data transfer. `p0447:c01`–`p0448:c01`.
7. **TCP connection setup is source-described as a three-message SYN → SYN+ACK → ACK exchange.** Connection close is shown schematically with FIN/ACK exchange and a timeout before final closure. `p0449:c01`–`p0450:c01`.
8. **A TCP connection is identified by a pair of sockets.** One listening/server-side socket can participate in several different connections because the remote socket differs. `p0450:c01`–`p0452:c01`.
9. **Reliability is built from ARQ principles.** Send data, receive acknowledgements, use timers, retransmit when necessary and detect duplicates/order. `p0452:c01`–`p0454:c01`.
10. **Stop-and-Wait is simple but inefficient.** The sender waits for an ACK before sending the next unit, wasting capacity on higher-delay links. `p0453:c01`–`p0454:c01`.
11. **Sliding windows permit multiple outstanding units.** Window boundaries define what may be transmitted before new ACKs arrive. `p0454:c01`–`p0456:c01`.
12. **Go-Back-N uses cumulative ACKs and a receiver window of one in the source model.** A loss/timeout can cause retransmission of the base packet and all later unacknowledged packets. `p0456:c01`–`p0458:c01`.
13. **Selective Repeat trades complexity for lower retransmission overhead.** The receiver buffers out-of-order valid packets, ACKs them individually and the sender retransmits only the missing/expired unit. `p0458:c01`–`p0460:c01`.
14. **TCP applies the window to bytes, not packet numbers.** Sequence number identifies the first data byte in a segment; ACK number represents the next byte expected for the contiguous stream. `p0461:c01`–`p0464:c01`.
15. **TCP ACKs are cumulative in the basic model.** An out-of-order segment beyond a gap does not advance the cumulative ACK; the receiver repeats the ACK for the first missing byte boundary. `p0463:c01`–`p0464:c01`.
16. **SACK is presented as an extension that allows selective acknowledgement of out-of-order data.** It reduces unnecessary retransmission relative to purely cumulative recovery. `p0464:c01`.
17. **Receiver window is flow control.** The receiving side advertises how much additional data its buffer can accept; zero window tells the sender to stop ordinary transmission until capacity returns. `p0462:c01`–`p0465:c01`.
18. **Retransmission timeout must adapt to RTT.** Too short causes spurious retransmissions; too long causes unnecessary stalls. The source describes an adaptive RTT-based estimate. `p0465:c01`–`p0466:c01`.
19. **Flow control and congestion control solve different problems.** Receiver window protects the endpoint buffer; congestion window limits pressure on the network. `p0466:c01`–`p0467:c01`.
20. **The effective sending window is source-described as the minimum of receiver and congestion windows.** `min(rwnd, cwnd)` captures endpoint and network constraints simultaneously. `p0467:c01`.
21. **Slow Start increases congestion window cautiously, then reacts strongly to inferred loss.** The chapter uses a classical example beginning at one segment and transitioning to slower linear growth after a threshold. `p0468:c01`–`p0469:c01`.
22. **Duplicate ACKs can signal a specific loss before timeout.** The source describes three duplicate ACKs as a reason to retransmit without waiting for the retransmission timer. `p0469:c01`.
23. **ECN provides explicit congestion signalling through IP/TCP rather than inferring everything from loss.** `p0469:c01`–`p0470:c01`.
24. **TCP continues to evolve.** The final source table names SACK, CUBIC, BBR, HyStart++, ECN-related mechanisms, Westwood+ and MPTCP; these entries are edition/source snapshots rather than externally verified current defaults. `p0470:c01`–`p0471:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed transport mechanisms/fields; executable OS/network commands are absent.
- [diagram.md](diagram.md) — Mermaid map of ports/sockets → UDP vs TCP → reliability/flow/congestion control.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance and historical/source-snapshot caveats.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 442–471 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions or exercises inside the verified boundary **не обнаружены** → `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG contains footer contamination, OCR/glyph substitutions and degraded timing/window diagrams. Port-number ranges, urgent-data behavior, retransmission formulas, congestion-control defaults and the final TCP-extension table are treated as source/edition context and are not silently modernized.
