# Ответы на контрольные вопросы и задачи — глава 6

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Для задач, зависящих от рисунка/точной simulation convention, используется `[Needs confirmation]`.

1. Нет. `LISTEN` может быть неблокирующим: socket переводится в nonblocking mode, а готовность принимать connection отслеживается через event loop/`select`/`poll`-подобный механизм. Преимущество — один thread/process может обслуживать много sockets и выполнять другую работу, не зависая в одном вызове.

2. TCP — **byte stream**, а не message protocol. Один `receive()` может вернуть половину сообщения, несколько сообщений сразу или произвольную границу между ними. Нужен framing: length prefix, delimiter или другой application protocol.

3. Если network layer гарантирует отсутствие потерь, можно убрать loss-recovery transitions, связанные с timeout/retransmission отдельных packets. Но connection setup/teardown, ordering/flow control и state management могут остаться нужны; «не теряет» не означает автоматически «не переупорядочивает» и не решает process crashes.

4. Client должен обращаться к тому port number, на котором server делает `LISTEN`. Если значения различаются, transport demultiplexing доставит SYN/connection request не тому service endpoint либо никому.

5. 15-bit timer с tick 100 ms оборачивается за (2^{15}·0.1=3276.8) s ≈54.6 min. **[Needs confirmation]** Для точных периодов ресинхронизации в пунктах (а)/(б) нужна конкретная forbidden-region construction из соответствующего рисунка главы; одной частоты timer и расхода sequence numbers недостаточно, чтобы однозначно воспроизвести принятую в тексте формулу.

6. Старое ACK тоже может пережить connection и после reuse connection identifiers/sequence space быть принято за подтверждение нового packet. Поэтому перед повторным использованием sequence space должны исчезнуть **и data packets, и их ACKs**.

7. **[Needs confirmation]** Нужен точный forbidden-region model из раздела о clock-based initial sequence numbers. 10-bit clock wraps каждые (1024·0.125=128) s, MSL=64 s, sender расходует4 seq/s, но момент входа в forbidden region зависит от определения границ в модели.

8. На link layer RTT обычно мал и стабилен, topology fixed, поэтому timeout можно выбирать почти постоянным. На transport layer RTT включает variable queueing/routing/congestion и может меняться на порядки, поэтому RTO должен **адаптироваться к измеренному RTT/variance**.

9. На receiver стороне безопаснее **записать/зафиксировать данные до отправки ACK**; после crash sender retransmits unacknowledged data. На sender стороне безопаснее сохранять состояние outstanding operation до send и удалять/commit его только после надёжного ACK. Так минимизируются loss и duplicate effects, хотя полностью exactly-once semantics при crash без stable transaction state не гарантируется.

10. **[Needs confirmation]** Для max-min allocation нового flow E нужна topology/capacities илл. 6.20.

11. **[Needs confirmation]** Нужны capacities/link mapping илл. 6.20, чтобы вычислить bottleneck sharing для A–D.

12. Credit scheme явно сообщает sender объём доступного receiver buffer и хорошо работает с variable-size data. Плюсы: точнее flow control, не обязательно связывать credit с sequence-space window. Минусы: дополнительное state/control traffic, stale/lost credits и сложнее recovery/synchronization.

13. **AIAD:** additive increase/decrease обычно не уменьшает разницу между flows → fairness не гарантируется. **MIAD:** multiplicative increase раздувает различия, additive decrease их не устраняет → плохая стабильность/fairness. **MIMD:** ratio flows почти сохраняется, поэтому если старт несправедливый, к fairness не сходится. Именно **AIMD** сочетает convergence к efficiency line и fairness.

14. Да, такая decrease function сильнее уменьшает большой flow, чем малый: преобразование (x	osqrt{x}) сжимает разницу rates, а additive increase затем её не увеличивает. Поэтому AISRD должен двигать allocation к fairness при повторяющихся congestion events.

15. UDP host A генерирует (100·8/0.001=800) кбит/с и не снижает rate из-за congestion. TCP host B пытается 600 кбит/с, но congestion control отступит. На 1-Мбит/с bottleneck A может занять около **800 кбит/с**, B — остаток порядка **200 кбит/с**; A получает больше.

16. UDP даёт ports/process demultiplexing, checksum и стандартный transport API. Raw IP не предоставляет удобного process-level addressing, требует приложениям самим формировать IP protocol semantics и обычно требует privileged/raw access.

17. После crash client/server теряют stop-and-wait state: sequence/request IDs, информацию о последнем acknowledged block и о том, выполнен ли request. Возможны duplicates, повторная выдача/перезапись результата, ambiguity «request обработан, но ACK потерян». Нужны stable transaction IDs/state или idempotent operations.

18. При 100 км fiber one-way propagation ≈0.5 ms, RTT≈1 ms. 128 bytes at1Gbps передаются за1.024 µs. Если request и reply одинакового размера, line busy около2.048 µs за ~1.002 ms RPC cycle: efficiency порядка **0.2%**.

19. При симметричных 128-byte request/reply:  
   - 1 Гбит/с: (1	ext{ ms}+2·1.024	ext{ µs}approx) **1.002 ms**;  
   - 1 Мбит/с: (1	ext{ ms}+2·1.024	ext{ ms}approx) **3.048 ms**.  
   Вывод: для tiny RPC propagation latency может доминировать, и 1000× bandwidth increase далеко не даёт 1000× response improvement.

20. Process IDs локальны хосту/ОС, могут быстро переиспользоваться и не являются стабильным network namespace. Ports — компактные protocol-defined endpoint identifiers, позволяющие demultiplex services независимо от конкретного PID и давать well-known service names.

21. RTP обычно поверх UDP, потому что real-time media предпочитает своевременность retransmission/order blocking; RTP сам даёт timestamps/sequence metadata. RTP over TCP допустим, если UDP блокируется или latency не критична (например, non-live media/tunnel), и head-of-line/retransmission delays приемлемы.

22. N1 имеет bounded jitter: finite playback buffer около worst-case delay позволяет гарантировать отсутствие late packets ценой большой latency. В N2 tail unbounded — никакой finite buffer не даёт гарантии; выбирают playout deadline и поздние packets discard. RTP timestamps/sequence numbers помогают измерять jitter, но не устраняют arbitrarily delayed packets.

23. Для IPv4 traditional minimum reassembly datagram 576 bytes: 20-byte IP +20-byte TCP оставляют MSS536. Итого minimum TCP/IP MTU context — **576 bytes** без link overhead.

24. Да, TCP всё равно должен re-sequence **segments**, потому что разные IP datagrams могут прийти в другом порядке по разным paths/queues. IP reassembly скрывает только fragmentation одного datagram.

25. Stereo CD rate: 44 100 sample pairs/s. Если один RTP packet несёт одну pair 2×16 bit, требуется **44 100 packets/s**. На практике packet агрегирует много samples, поэтому real pps значительно меньше.

26. Для одних и тех же two host addresses и ports TCP 4-tuple одинаков, поэтому одновременно может существовать **одно** такое connection. Несколько connections требуют отличаться хотя бы одним address/port.

27. ACK bit сообщает, что Acknowledgement Number действительно валиден. Без него при SYN/некоторых control states содержимое 32-bit field нельзя было бы однозначно интерпретировать.

28. Нет. TCP sequence numbers нумеруют **байты**, а не segments. При той же byte rate увеличение MSS не уменьшает скорость расходования sequence space.

29. SYN-RCVD достигается:  
   - passive opener в LISTEN получает SYN и посылает SYN+ACK;  
   - при simultaneous open активная сторона после собственного SYN получает peer SYN и также переходит в SYN-RCVD.

30. Nagle задерживает small writes, пока outstanding data не подтверждены. При high RTT/congestion ACK приходит поздно, поэтому interactive data может искусственно собираться в bursts и получать заметную дополнительную задержку.

31. Да: **Nagle algorithm** вместе с delayed ACK может превратить frequent tiny actions в burst/slideshow. Другая network-причина — queueing/bufferbloat, congestion loss/retransmission или очень variable RTT.

32. MSS=2 KB, receive window=24 KB=12 MSS. Slow start с cwnd1: rounds дают 1→2→4→8→≥12. При RTT10 ms полное 12-MSS window становится доступно примерно через **40 ms** от старта.

33. Timeout: ssthresh=18/2=9 KB, cwnd reset≈1 KB. После успешных rounds slow start: 1→2→4→8, затем до threshold ≈**9 KB**; после этого начинается congestion avoidance. Точная величина после каждого ACK зависит от реализации, но round-model главы даёт около 9 KB после четвёртого успешного шага.

34. Round0=1 KB. Slow start до threshold64: 2,4,8,16,32,64 на rounds1–6. Затем additive +1 KB/round: round7=65, round8=**66 KB**.

35. (RTT_{new}=0.9·RTT_{old}+0.1·sample):  
   30→29.6→29.84→**29.256 ms**.

36. Window65535 B, RTT20 ms → max (65535/0.02=) **3.27675 MB/s ≈26.2 Мбит/с**. На 1 Гбит/с line efficiency ≈**2.62%**.

37. 32-bit byte sequence space при MSL120 s позволяет payload rate (2^{32}/120≈35.79) MB/s. При 1500 user bytes/segment это ≈23 861 segments/s. С TCP20+IP20+Ethernet18 bytes line bytes ≈1558/segment → line rate ≈**297 Мбит/с** (без preamble/IFG).

38. TCP extensions можно negotiation-добавлять через options, сохраняя базовый header/API и совместимость endpoints. IPv6 меняет адреса и fixed IP header, затрагивая hosts, routers, forwarding tables и всю internetwork infrastructure, поэтому deployment значительно тяжелее.

39. 8-bit segment sequence numbers →256 values. За MSL30 s максимум (256/30≈8.53) segments/s. При128 bytes/segment: **≈1092 B/s ≈8.74 кбит/с**.

40. Без timestamps 32-bit byte sequence space не должен обернуться за128 s: (2^{32}/128=) **33 554 432 B/s ≈268.4 Мбит/с** payload rate.

41. **[Needs confirmation]** Для всех запрошенных метрик требуется воспроизвести точную round-by-round Reno simulation convention главы (fast recovery, отправка new data во время recovery и модель bottleneck queue). Из данных точно следует, что bottleneck BDP при RTT500 ms и64 кбит/с =32 кбит=4 MSS; queue начинает расти при cwnd>4. Для canonical numeric answer нужно отдельное пошаговое моделирование по правилам раздела.

42. Timer resolution 1 ms грубее измеряемого event. Если processing time почти постоянен и start phase относительно tick равномерна, доля measurements=1 ms примерно равна реальной длительности в ms: оценка **~0.73 ms**. Но индивидуальные 0/1 readings не означают реально нулевую/1-ms работу.

43. 64-bit word=8 B, 10 instructions/copy; 4 copies →40 instructions/8B =5 instr/B. 1 Гбит/с=125 MB/s →625 MIPS. CPU=1000 MIPS, значит **да**, теоретически справится, загрузка ~62.5%.

44. 75 Тбит/с =9.375·10^12 B/s. (2^{64}/9.375·10^{12}approx1.97·10^6) s ≈ **22.8 суток**. MSL должен быть меньше этого, чтобы byte sequence space не обернулся.

45. 128 B: instructions (50+10·16=210); **4.76 млн packets/s**, useful throughput ≈**609.5 MB/s**.  
   1024 B: (50+10·128=1330); **0.752 млн packets/s**, useful throughput ≈**769.9 MB/s**.

46. 20 km one-way при propagation≈2·10^8 m/s → RTT≈0.2 ms. Для 1 KiB packet (8192/R=0.0002) → **R≈40.96 Мбит/с**.

47. BDP при RTT0.1 s:  
   - T1 1.5M → **150 kbit =18.75 KB**;  
   - Ethernet10M → **1 Mbit =125 KB**;  
   - T3 45M → **4.5 Mbit =562.5 KB**;  
   - STS-3 155M → **15.5 Mbit =1.94 MB**.  
   16-bit TCP window max65535 B, значит без scaling только T1 pipe помещается полностью; на остальных throughput ограничен примерно **5.24 Мбит/с** при RTT100 ms.

48. Для GEO take RTT≈540 ms. BDP (50	ext{ Mbit/s}·0.54=) **27 Mbit =3.375 MB**. При1500-byte packets нужно окно примерно **2250 packets**.

49. Client speed test может упираться не в access link, а в test server/path, Wi‑Fi/LAN, TCP window+RTT, congestion, CPU, concurrent household traffic, protocol overhead, ISP shaping/boosting или transient cache/CDN placement.

50. Экономия 4 bits не уменьшит standard header, если всё равно требуется alignment/целые words; зато последующие fields станут misaligned, что усложнит hardware/software parsing и может **ухудшить performance**.

51. а) Добавить client args `offset,length`; request protocol должен передавать range, server делает seek/read только этого участка.  
   б) `-w`: добавить operation type WRITE, server принимает pathname/range/data, проверяет authorization/errors и подтверждает result. Protocol framing должен различать READ/WRITE и длины.

52. Zero-copy design: message — список/ref-counted immutable buffer segments (`iovec`/rope). Add/remove header меняет segment list/offsets; split создаёт две views; concatenate соединяет lists; copy увеличивает refcount. Реальные payload bytes не копируются до необходимости materialization.

53. Coordinator: well-known UDP socket, registry sessions→server endpoint, CREATE/JOIN/LEAVE control. На CREATE запускается/назначается TCP chat server и возвращается endpoint/token. Chat server принимает TCP clients, multiplexes messages group members, handles disconnects. Client через UDP coordinator находит/создаёт session, затем поддерживает TCP connection с выбранным server.
