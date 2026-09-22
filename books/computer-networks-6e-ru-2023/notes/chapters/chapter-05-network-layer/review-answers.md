# Ответы на контрольные вопросы и задачи — глава 5

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Figure-dependent items без текстового представления рисунка помечены `[Needs confirmation]`.

1. В normal virtual-circuit service packets идут по одному path и должны сохранять порядок. Временное out-of-order возможно при **reroute/failover** или использовании нескольких параллельных paths; тогда network/transport должен либо resequence, либо явно не обещать ordering.

2. Datagram header длиннее на 12 bytes. За session экономия VC на bandwidth: (12·200·4=9600) bytes → **0.0096 cent**. VC state: 8 bytes ×4 routers=32 bytes; доля стоимости памяти за 1000 s из 2 лет по 40 h/week ≈ **0.00214 cent**. VC дешевле примерно на **0.00746 cent/session** при данных условиях.

3. Добавление next-hop information позволяет обнаружить простой routing loop: если B видит, что C достигает A через B, B не принимает этот route после потери A. Затем B объявляет A unreachable, C теряет route через B, далее информация об unreachable распространяется дальше. Для topology на илл. 5.10 точные intermediate vectors: **[Needs confirmation]** без рисунка.

4. По link-state data shortest paths от D:  
   - C: cost **3**, output C;  
   - F: **4**, output F;  
   - B: **5** через F;  
   - E: **6** через C;  
   - A: **8** через C→E;  
   - D: 0/local.

5. **[Needs confirmation]** Нужно содержимое илл. 5.7, чтобы перечислить все flooded paths A→D длиной ≤3 hops и посчитать link transmissions.

6. Найти один path, удалить/временно запретить все его edges и снова найти path. Если второй path существует, он edge-disjoint с первым; тогда отказ любой одной линии оставляет как минимум один из двух путей.

7. Векторы с добавлением local-link cost:  
   via B: (11,6,14,18,12,8); via D: (19,15,9,3,12,13); via E: (12,11,8,14,5,9).  
   Итог C: **A→B cost11; B→B 6; C local0; D→D 3; E→E 5; F→B 8**.

8. **Routing** вычисляет/поддерживает пути и таблицы. **Forwarding** принимает локальное per-packet решение по таблице и выбирает next hop. **Switching** — внутренняя передача packet/frame от input interface к нужному output внутри устройства.

9. **[Needs confirmation]** Значение ACF bits зависит от определения/рисунка 5.13; без него нельзя доказать, является ли OR=111 invariant.

10. (4800=15·16·20). Все три значения близки к (sqrt[3]{4800}approx16.9). Удобный почти оптимальный вариант: **15 routers/region, 16 regions/cluster, 20 clusters** (перестановка уровней с теми же размерами даёт ту же сумму размеров таблиц).

11. Через **proxy ARP**: home agent отвечает на ARP requests для IP mobile host своим MAC-address, поэтому Ethernet frames, предназначенные mobile host, приходят home agent, который затем туннелирует/пересылает их.

12. **[Needs confirmation]** Требуется topology илл. 5.6 для подсчёта copies при reverse-path forwarding и sink tree.

13. **[Needs confirmation]** Требуются илл. 5.15(а–в) и существующее sink tree.

14. Flow control защищает receiver, но не сеть: несколько senders могут одновременно переполнить router queues. Congestion control защищает network path, но без flow control отдельный fast sender всё равно способен выдавать данные быстрее, чем receiver application/buffer успевает принимать.

15. Backpressure stop-and-wait распространяется по всему path. При (n) последовательных router stages цикл packet+ack порядка **(2nT)**, то есть delivery rate приблизительно **(1/(2nT)) packets/s** (точное (n) зависит от того, считаются ли host-router links отдельно).

16. Пусть (q=1-p). За одну attempt ожидаемые traversed hops: **(1+q+q^2)**. Вероятность успешной delivery через оба routers: (q^2), поэтому attempts/package: **(1/q^2)**. Среднее total hops до успеха: **((1+q+q^2)/q^2)**.

17. **ECN** явно маркирует packet как испытывающий congestion, позволяя сообщить sender без потери. **RED** по growing average queue вероятностно drop/mark packets до полного заполнения queue; classic RED использует drop как ранний signal.

18. Большой flow заполняет bottleneck queue. Малые packets вынуждены ждать behind bulk packets; растут queueing/serialization delay и jitter — классический bufferbloat/head-of-line effect.

19. Чтобы output **никогда** не превышал 20 Мбит/с, нужен **leaky bucket** с leak/output rate **20 Мбит/с**. Token bucket с rate20 допускает bursts выше20.

20. За 1 s при100 Мбит/с поступает 100 Mbit = **12.5 MB**. Такой bucket позволяет принять burst длиной1 s, после чего excess traffic начнёт отбрасываться.

21. Есть 300 MB tokens, sender идёт 15 MB/s, tokens добавляются 5 MB/s → depletion 10 MB/s. 300 MB хватает на30 s, за это время уходит450 MB. Остаток550 MB затем идёт по5 MB/s =110 s. Итого **140 s**.

22. **[Needs confirmation]** Для weighted-fair finish times нужен исходный набор packets/queues илл. 5.29.

23. Burst при peak (M=50) MB/s, token rate (r=10) MB/s, bucket (b=1) MB: (t=b/(M-r)=1/40=) **0.025 s =25 ms**.

24. **[Needs confirmation]** Для сумм reservation на A,B,C,E,H,J,K,L нужна multicast tree topology илл. 5.32.

25. M/M/1 processing: (mu=2) Mpps, (lambda=1.5) Mpps. Среднее system time/router (1/(mu-lambda)=2) µs. Для 10 routers: **≈20 µs**.

26. Не абсолютная гарантия. EF задаёт preferential treatment/low-delay behavior при корректном policing/provisioning, но overloaded EF class, link serialization или misconfiguration всё равно могут увеличить delay.

27. TCP segment: 900 data +20 TCP header =920-byte IP payload; IP header20 → total940.  
   **A–R1:** MTU (1024-14=1010), один packet: Total=940, ID=X, DF=0, MF=0, offset=0.  
   **R1–R2:** MTU (512-8=504). Fragment1 data480 → Total=500, MF=1, offset=0. Fragment2 data440 → Total=460, MF=0, offset=60.  
   **R2–B:** MTU (512-12=500): оба fragments уже помещаются; fields сохраняются. ID у обоих fragments один и тот же X.

28. 16-bit Identification даёт 65536 values. При lifetime10 s безопасно ≤6553.6 datagrams/s. Для 1024-byte datagrams: (6553.6·1024·8≈) **53.7 Мбит/с**.

29. Strict Source Route должен копироваться **во все fragments**, потому что каждый fragment маршрутизируется независимо и обязан пройти заданную sequence routers.

30. У class B первые 2 bits фиксированы `10`. Если network field увеличен с16 до20 bits, variable network bits становятся18. Число class-B networks: **(2^{18}=262,144)**.

31. C2.2F.15.82 → **194.47.21.130**.

32. Использовать **tunneling**: encapsulate IPv6 packet внутри IPv4 packet на входе в IPv4-only region и decapsulate на выходе.

33. 255.255.240.0 = /20, host bits=12. Максимум традиционно **(2^{12}-2=4094)** host addresses.

34. IP-addresses и prefixes иерархичны и отражают network topology, поэтому агрегируются в routing. Ethernet MAC addresses в основном **flat/global identifiers**, не кодируют location/network, поэтому плохо подходят для scalable routing between networks.

35. Минимальные CIDR blocks при sequential allocation:  
   - A 4000 → /20: **198.16.0.0–198.16.15.255**;  
   - B 2000 → /21: **198.16.16.0–198.16.23.255**;  
   - C 4000 → следующий aligned /20: **198.16.32.0–198.16.47.255**;  
   - D 8000 → следующий aligned /19: **198.16.64.0–198.16.95.255**.  
   Alignment оставляет gaps; reorder allocations может уменьшить fragmentation.

36. Четыре consecutive /21 blocks 57.6.96.0–57.6.127.255 образуют aligned /19. Агрегация: **57.6.96.0/19**.

37. Разбивать /17 не нужно. Оставить aggregate **29.18.0.0/17** на старую линию и добавить more-specific route **29.18.60.0/22** на новую. Longest-prefix match выберет исключение.

38. Чрезмерная aggregation объявит C диапазоны, которых A/B реально не обслуживают, что создаст blackholes/misrouting. Решение: не агрегировать через holes либо дополнительно публиковать more-specific routes/exceptions так, чтобы longest-prefix match корректировал aggregate.

39. Простое резервирование NAT-router недостаточно: NAT хранит per-flow translation state. При failover новый router без state не знает старые mappings и existing sessions рвутся. Нужны state synchronization/shared mapping/public address или иной deterministic HA design.

40. Friend's NAT получает unsolicited inbound packet на public address/port без mapping и обычно **drop** его. Решения: static port forwarding, NAT traversal/hole punching, UPnP/NAT-PMP/PCP или relay server.

41. Да. На разных hosts одинаковый local port допустим, потому что flows различаются IP-addresses. За NAT оба могут выйти через один public IP: NAT назначит **разные external source ports** и сохранит отдельные mappings.

42. ARP — boundary mechanism: он разрешает network-layer IP в link-layer MAC и сам передаётся непосредственно в link layer. Поэтому утверждение «служит IP → автоматически часть link layer» слишком упрощённо; это interface protocol между L3 addressing и L2 delivery.

43. Скорее всего source DHCP OFFER — LAN IP домашнего router/DHCP server, например **192.168.0.1**. Точное значение зависит от конфигурации modem/router.

44. Reassembly key: source, destination, protocol, Identification. Receiver размещает fragment data по **Fragment Offset**, отслеживает gaps, MF=0 определяет final length; когда покрыт весь диапазон, header восстанавливается и datagram передаётся выше. Нужен timeout.

45. После expiry старый reassembly context уничтожен. Поздний isolated fragment следует **discard** (или начать новый context только при уверенной идентификации новой datagram); смешивать его со старыми fragments нельзя.

46. Router изменяет IPv4 header (например TTL), поэтому header checksum приходится пересчитывать на каждом hop. Payload обычно защищён transport/application checksum; исключение data уменьшает per-router processing.

47. Да, если laptop должен оставаться доступным по **home address** при нахождении в другой IP-network. То, что access wireless, не отменяет Mobile-IP home/foreign-agent problem; если приложения просто используют новый DHCP address, mobility protocol может не требоваться.

48. (2^{128}approx3.40·10^{38}) addresses. При (10^6) addresses/ps = (10^{18})/s хватит примерно на (3.40·10^{20}) s ≈ **1.08·10^{13} лет**.

49. Постоянный globally stable IPv6 address ухудшает privacy/tracking и мешает topology-based aggregation/mobility/provider renumbering. IPv6 позволяет стабильные internal identities, но на внешнем уровне часто полезны hierarchical и temporary/privacy addresses.

50. В IPv6 его функцию выполняет **Next Header**: он указывает либо следующий extension header, либо upper-layer protocol (TCP/UDP/ICMPv6). Отдельное IPv4-style Protocol field не нужно.

51. Conceptually address resolution всё ещё требуется, но IPv6 не использует ARP: его заменяет **Neighbor Discovery** на ICMPv6 с multicast. Значит изменение не косметическое, а protocol-level/technical.

52. Simulator: каждый packet хранит TTL/hop counter; в каждом discrete step link передаёт максимум один packet. Реализовать: flood all outgoing; flood all except incoming; flood k statically best. Сравнивать deterministic k=1 по average delay, successful delivery и total link transmissions; flooding обычно снижает chance/path delay ценой резкого bandwidth growth.

53. Discrete-event model: finite router queues, one head packet/link/step, drop on full buffer, end-to-end ACK+timeout retransmission at source. Для набора error rates sweep timeout; измерять goodput, retransmissions, queue occupancy и delay. Слишком малый timeout создаёт spurious retransmissions/congestion, слишком большой — медленное recovery.

54. Для destination IP пройти все table triples, проверить ((dst & mask)==network), выбрать matching entry с **самой длинной prefix mask**, вернуть outgoing line; если ни одного — default route/error.

55. **[Needs confirmation]** Это measurement task. Нужны реальные результаты `traceroute`/`tracert`; transoceanic links нельзя достоверно вывести без фактического path output.
