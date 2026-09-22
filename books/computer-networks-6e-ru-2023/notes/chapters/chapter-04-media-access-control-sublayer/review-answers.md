# Ответы на контрольные вопросы и задачи — глава 4

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Figure-dependent topology questions помечены `[Needs confirmation]`, если сам рисунок не представлен в текстовом RAG.

1. Средний frame service time (10,000/100,000,000=0.0001) с, то есть (mu=10,000) frames/s. Для M/M/1 (T=1/(mu-lambda)):  
   а) λ=90 → **0.1009 мс**;  
   б) 900 → **0.1099 мс**;  
   в) 9000 → **1.0 мс**.

2. Pure ALOHA maximum throughput (S_{max}=1/(2e)approx0.184) frame/frame-time. Frame time (1000/56000=0.017857) с, значит максимум ≈10.3 successful frames/s. Каждая station генерирует 0.01 frame/s → **N≈1030**.

3. 10 000×18 requests/hour =180 000/hour=50/s. Slot=125 µs. Normalized offered load **G=50×125µs=0.00625**.

4. Idle-slot probability (e^{-G}=0.1), значит **G=ln10≈2.303**. Throughput (S=Ge^{-G}approx0.2303) frame/slot. Так как slotted ALOHA максимум имеет при G=1, система **перегружена**.

5. Pure ALOHA почти не требует координации, но много collisions. Slotted ALOHA требует slot synchronization. 1-persistent CSMA уменьшает idle time, но при освобождении busy channel много stations могут collide. Nonpersistent снижает collisions случайной задержкой ценой latency. p-persistent требует slotted operation; малое p уменьшает collisions под нагрузкой, но увеличивает waiting time.

6. Contention slot ≈ round-trip propagation:  
   а) 2 км, (v=0.82c): one-way ≈8.13 µs → **16.3 µs**;  
   б) 40 км, (v=0.65c): one-way ≈205.1 µs → **410.3 µs**.

7. В bitmap protocol worst case возникает, если station становится ready сразу после своего reservation bit: ей приходится ждать оставшуюся reservation phase, transmissions текущего cycle и следующего reservation до своего bit. Точное число slots зависит от количества active stations в цикле; верхняя граница порядка **N reservation slots + до N frame slots**. Для точной формулы по обозначениям книги нужен соответствующий protocol timing fragment.

8. Binary countdown отдает приоритет старшим binary station numbers. Если stations с большими номерами постоянно готовы, они всегда побеждают arbitration, поэтому station с малым номером может **голодать (starvation)**.

9. **[Needs confirmation]** Нужна структура adaptive-tree на илл. 4.10, чтобы перечислить traversal и число дополнительных collisions.

10. При высокой постоянной нагрузке лучше **token-based deterministic access**: нет collision storm, есть fairness и ограниченное время ожидания. Nonpersistent CSMA проще, но под высокой нагрузкой увеличивает random waiting/collisions.

11. **[Needs confirmation]** Точные min/max/average slots зависят от принятого в главе traversal algorithm и положения двух active leaves; нужен RAG-фрагмент adaptive-tree derivation.

12. CSMA/CD можно применять, только если transmitter способен одновременно достаточно надёжно слушать medium и обнаружить collision, а propagation/hidden-terminal conditions позволяют это. Для обычного radio 802.11 собственный transmit signal слишком силён и hidden nodes мешают, поэтому используется CSMA/CA.

13. Да, две MACA transmissions могут идти одновременно, если обе sender/receiver pairs находятся вне взаимной interference/RTS-CTS protection области. Без конкретной геометрии A–F нельзя назвать пары, но сам protocol допускает spatial reuse.

14. Для сетки 15×7 с шагом 4 м и router в геометрическом центре сумма прямых star links ≈ **1832 м**. Если классическую shared 802.3 bus проложить «змейкой» через все 105 outlets по grid edges, потребуется (7·14·4+6·4=) **416 м**.

15. Manchester использует два signal intervals на bit. Для 10 Мбит/с это **20 Мбод**.

16. При Ethernet convention 0=high→low (`10`), 1=low→high (`01`):  
   0001110101 → **10 10 10 01 01 01 10 01 10 01**.  
   При противоположном обозначении уровней пары инвертируются, физические transitions те же.

17. 256-bit frame at10Mbps =25.6 µs; payload=224 bits. One-way propagation=5 µs; ACK 32 bits=3.2 µs. Cycle ≈25.6+10+3.2=38.8 µs. Effective payload rate ≈ **5.77 Мбит/с**.

18. One-way delay 1 km / (2·10^8)m/s =5 µs; round trip=10 µs. At1Gbps minimum transmitting frame must last ≥10 µs → **10 000 bits =1250 bytes**.

19. Ethernet payload minimum is 46 bytes. IP packet is 60 bytes, so **padding не требуется**.

20. Fast Ethernet сохранил 64-byte minimum, уменьшив допустимый collision-domain diameter/round-trip delay примерно пропорционально росту bitrate. В switched full-duplex collision constraint вообще исчезает.

21. Это не safety margin. Gigabit Ethernet PHY использует **8B/10B line encoding**: 1 Гбит/с payload превращается в 1.25 Gbaud coded stream для synchronization/DC-balance/control symbols.

22. Minimum Ethernet wire event включает 64-byte frame + 8-byte preamble/SFD + 12-byte interframe gap =84 bytes =672 bit times. (10^9/672≈) **1.488 млн frames/s**.

23. **Frame bursting** в Gigabit Ethernet позволяет отправить несколько коротких frames подряд в одном захваченном medium interval. Это уменьшает relative carrier-extension/contention overhead.

24. **[Needs confirmation]** Нужна илл. 4.27: близость B/C/D к A определяется конкретной geometry/radio reachability на рисунке.

25. 802.11 добавляет к RTS/CTS механизму MACA physical carrier sensing, NAV/duration reservation и ACK semantics. То есть идея та же — предупредить hidden nodes, но 802.11 связывает её с полным CSMA/CA timing.

26. **[Needs confirmation]** Для классификации hidden/exposed pairs нужны связи с илл. 4.33(б).

27. Без TXOP при equal frame opportunities slow stations занимают больше airtime; при одинаковом frame size round time пропорционален (4/6+4/18+2/54), и каждая получает примерно **1.08 Мбит/с**. При equal-airtime TXOP каждая получает около 1/10 airtime: 6-Mbit stations ≈**0.6**, 18-Mbit ≈**1.8**, 54-Mbit ≈**5.4 Мбит/с**.

28. 64-byte frame =512 bits. Frame-error probability ≈(512·10^{-7}=5.12·10^{-5}). Raw frames/s (11·10^6/512≈21484). Corrupted ≈ **1.1 frames/s**.

29. Station может намеренно помечать bulk traffic как high-priority QoS class, получая меньший AIFS/contention window и чаще выигрывая medium. Это повышает её throughput за счёт остальных и нарушает fairness.

30. При постоянном high-priority traffic low-priority queues могут испытывать **starvation/очень большую задержку**. Приоритет уменьшает latency одного класса ценой fairness и capacity другого.

31. FEC выгоднее ARQ при большом RTT/дорогой обратной связи и когда retransmission недопустима по времени (real-time), а также при broadcast/multicast.

32. На более высоких PHY rates relative cost централизованного polling/PCF overhead уменьшается, а scheduled access помогает избегать contention при traffic с QoS/real-time требованиями.

33. Profiles дают приложениям **готовый interoperable contract**: какие procedures/services/device roles должны поддерживаться для конкретного use case. Сложность core specification превращается в предсказуемость совместимости на уровне приложения.

34. Лазерная сеть wireless как 802.11, но medium сильно направленный и line-of-sight; одновременно она может напоминать point-to-point Ethernet links. MAC должен учитывать directional hidden nodes, отсутствие omnidirectional carrier sense и возможность spatial reuse независимых beams.

35. Master задаёт piconet clock/hopping sequence и schedule. Один radio не может одновременно вести две независимые master time/frequency schedules без time-sharing, поэтому устройство не может быть master обеих piconets одновременно в обычной модели.

36. Для base-rate 3-slot ACL packet типа DH3 maximum user payload — **183 bytes** (без payload FEC); multi-slot packet экономит repeated access/header overhead.

37. **SCO** — synchronous connection-oriented, прежде всего для постоянного-rate voice/audio. **ACL** — asynchronous connectionless packet data для bursty/general data traffic.

38. **[Needs confirmation]** Нужны точные payload/header/FEC размеры one-slot и five-slot packet из таблицы главы; по одной исходной эффективности 13% однозначно вычислить five-slot value нельзя.

39. Да, Bluetooth также требует tight clock/frequency-hop synchronization. Beacon/control information должен позволять участникам согласовать timing; конкретное поле «delay» отличается от 802.11 FH implementation.

40. Если system board ограничена 10 Гбит/с и считать minimum 64-byte frames без wire preamble/IFG внутри backplane, максимум (10^{10}/512≈) **19.53 млн frames/s**.

41. **[Needs confirmation]** Нужна топология/port numbering илл. 4.33(б) для построения learning table B2.

42. **[Needs confirmation]** Нужна илл. 4.33(б), потому что flooding зависит от learned ports после предыдущих transmissions.

43. **[Needs confirmation]** Нужна илл. 4.33(б) и port mapping обоих bridges.

44. **[Needs confirmation]** Нужна исходная topology илл. 4.36 для нового spanning tree с B0.

45. **[Needs confirmation]** Нужны labels/topology илл. 4.39 и значение «станет белой» в легенде рисунка.

46. При default STP root=bridge0: links **0–1, 0–2**, а bridges3–6 при равной cost выберут lower-ID upstream bridge1, то есть **1–3,1–4,1–5,1–6**. Для traffic, в основном идущего к bridge2, лучше настроить priorities так, чтобы branches3–6 шли через **2**, например tree 2–0, 2–3…6, 0–1.

47. Hub образует один shared collision domain, поэтому даже при duplex pair cabling collisions возможны и нужен CSMA/CD. Switch с **half-duplex** links создаёт отдельный collision domain на каждом port, но station и switch всё ещё могут collide — CSMA/CD нужен. При full-duplex switched links он не нужен.

48. Store-and-forward switch принимает весь frame и проверяет FCS до forwarding, поэтому corrupted frame можно отбросить. Cut-through начинает forwarding до получения trailer/FCS и способен распространить damaged frame дальше.

49. Если для всех ports данного bridge STP находит более дешёвые/приоритетные пути через другие bridges, его ports могут стать blocked; bridge не входит в active spanning tree и остаётся резервным.

50. Hub — layer-1 repeater: он не читает VLAN tags/MAC addresses и не принимает forwarding decisions, поэтому configuration table ему не нужна. Но он также **не может обеспечить VLAN isolation** — все bits повторяются всем участникам segment.

51. Да, ordinary switch допустим внутри одного access VLAN, если VLAN-aware upstream device назначает VLAN по port и на обычный switch приходят/уходят untagged frames. Один такой switch не должен смешивать несколько VLAN, которые требуется различать tags.

52. **[Needs confirmation]** Это лабораторное задание: нужен реальный capture пользователя и результаты симулятора. В RAG есть постановка, но не измеренный результат.

53. Simulator: maintain per-station attempt count/backoff; каждый slot stations с backoff=0 transmit; 1 transmitter → success event; >1 → collision, jam-slot и binary exponential random backoff (0..2^k-1) с cap; после success удалить station/frame и вывести timestamp/station ID.

54. **[Needs confirmation]** Задание требует внешней загрузки Wireshark и tutorial/экспериментов; в RAG-only режиме конкретный результат не существует.
