# Ответы на контрольные вопросы и задачи — глава 3

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Для вопросов, зависящих от поврежденного OCR/рисунка или отсутствующих параметров, используется `[Needs confirmation]`.

1. Ничего особенного: при byte-count/framing receiver уже знает, что находится внутри текущего frame, и не воспринимает случайно встретившуюся preamble как начало нового кадра.

2. При byte stuffing специальные байты экранируются:  
   **A B ESC ESC C ESC ESC ESC FLAG ESC FLAG D**.

3. Если каждый data byte требует escaping, поток удваивается. Максимальный overhead — **100% относительно исходных данных**.

4. **[Needs confirmation]** OCR исходной bit sequence поврежден; для точного удаления stuffed bits нужен однозначный исходный поток.

5. Да, при конечной checksum возможна комбинация framing/data corruption, которая случайно даст корректную checksum. Большая checksum уменьшает вероятность недетектированной ошибки, но не делает её нулевой.

6. Вероятность успешной передачи всех 10 frames за попытку: (0.8^{10}). Среднее число полных попыток: (1/0.8^{10}approx) **9.31**.

7. FEC без обратной связи предпочтителен, когда feedback дорог/невозможен: simplex link, очень большой RTT, broadcast/multicast или real-time traffic, где retransmission приходит слишком поздно.

8. Минимальное Hamming distance такой схемы — **2**: две ошибки внутри одной parity-группы могут сохранить parity.

9. При двойной передаче code rate = **1/2**, а минимальное расстояние удваивается и для исходного minimum distance 1 становится **2**. Обычный parity bit тоже даёт distance 2, но с намного меньшим overhead.

10. Для duplicated m-bit message две ошибки останутся незамеченными, только если попадут в соответствующие позиции обеих копий: вероятность **(1/(2m-1))** при равновероятном выборе двух разных bit positions. Для simple parity любые ровно две bit flips сохраняют parity, то есть остаются незамеченными.

11. Для Hamming(12,8) с even parity, если data bits 10101111 размещать в positions 3,5,6,7,9,10,11,12, получается codeword **011001001111**.

12. Для byte 10011010 с odd parity при том же размещении получается **101100101010**.

13. Для received 0xB4D = 1011 0100 1101, even-parity Hamming syndrome указывает одиночную ошибку; после correction и извлечения data positions получается **[Needs confirmation]** — требуется сверка принятого в книге порядка bit numbering/MSB placement, иначе возможны разные hex results.

14. При distance 3 можно гарантированно либо исправлять 1 error, либо обнаруживать 2; одновременное SEC+DED требует большего distance. В общем случае при distance (d): correction до **(lfloor(d-1)/2floor)** ошибок; detection до **(d-1)** ошибок.

15. Для 128 data bits и 8 redundancy bits: (2^8=256ge128+8+1=137). Значит **да**, 8 parity bits достаточно для single-error-correcting Hamming code.

16. 2D parity обнаруживает все single-, double- и triple-bit errors. Некоторые four-bit errors не обнаруживаются: например, четыре инверсии в углах прямоугольника — каждая затронутая row/column получает по две ошибки.

17. Такая схема гарантированно **исправляет 1 ошибку** и **обнаруживает до 3 ошибок**; некоторые 4-bit patterns остаются незамеченными.

18. Для correction всех single и double errors нужен уникальный syndrome для no-error, каждого single-bit и каждой пары:  
   **(2^r ge 1+(m+r)+inom{m+r}{2})**.

19. Для multiple-error correction детерминированное Hamming-style увеличение distance быстро требует много redundancy. Convolutional/LDPC codes позволяют получать более выгодный coding gain и приближаться к channel capacity при умеренной redundancy.

20. Hamming SEC для 1000 data bits требует 10 check bits. ARQ с 1 parity bit выгоднее по average transmitted bits при ((1-p)^{1001}>1001/1010), то есть примерно при **(p<8.94cdot10^{-6})**.

21. Если четыре flipped bits выбираются из (n	imes k) positions, undetected rectangle patterns: (inom n2inom k2). Вероятность:  
   **(rac{inom n2inom k2}{inom{nk}{4}})**.

22. 4-bit Internet checksum для nibbles 9, C, A, 3: one's-complement sum = 4, complement = **B (1011)**.

23. **[Needs confirmation]** OCR степеней полиномов поврежден; без точного dividend/generator remainder вычислять нельзя.

24. **[Needs confirmation]** Степень generator polynomial повреждена OCR; нужен точный RAG token.

25. **[Needs confirmation]** Для уверенного расчёта нужно подтвердить generator polynomial из исходного RAG.

26. CRC помещают в trailer, потому что remainder зависит от **всего предшествующего frame**; его естественно вычислить после формирования header+data.

27. Да. Даже без потерь ACK может задержаться дольше timeout, sender retransmits frame, и receiver получает duplicate. Поэтому sequence numbers всё равно нужны.

28. Stop-and-wait utilization (U=T_f/(T_f+2T_p)). Для (Uge0.5) нужно (T_fge40) мс. При 4 кбит/с размер frame ≥ **160 бит**.

29. Если window=20 как раз почти заполняет pipe, stop-and-wait window=1 даст примерно **1/20 ≈5%** utilization.

30. (0.25=T/(T+0.1)Rightarrow T=0.0333) с. (R=900/0.0333approx) **27 кбит/с**.

31. Frame transmission time (300/50000=6) мс. (0.6=6/(6+2d)) → **d=2 мс** one-way.

32. (T_f=800/1.2cdot10^6=0.667) мс. (U=0.667/(0.667+16)approx) **4.0%**.

33. Если window 3 давал ~100% при старой bandwidth, удвоение bandwidth удваивает bandwidth-delay product. Старый window покрывает половину pipe → примерно **50%**.

34. Для stop-and-wait/one-outstanding-frame protocol новый data timer не должен запускаться поверх уже работающего для того же outstanding frame; следующий start выполняется после ACK/timeout.

35. T1: 1.544 Мбит/с; 512-bit frame → 0.332 мс transmission. One-way propagation 3000×6 µs =18 мс. Для полной загрузки нужно около (1+36/0.332approx110) frames. Go-Back-N requires (2^k-1ge110), поэтому **7 bits** sequence number.

36. **[Needs confirmation]** Нужен точный вариант обозначений четырёх границ окна из текста протокола; общий invariant: receive window должен оставаться однозначно отделим от old/outstanding sequence space и не перекрываться неоднозначно после wraparound.

37. Удаление `else` приводит к запуску auxiliary ACK timer даже после немедленной отправки NAK. Это обычно создаёт лишний ACK/traffic, но **не нарушает корректность**.

38. Удаление цикла, который последовательно выгружает уже buffered in-order frames, может нарушить progress: несколько готовых frames останутся в buffer до будущего event. Это уже не просто performance issue; возможна задержка/зависание delivery.

39. **[Needs confirmation]** Вопрос ссылается на параметры предыдущей задачи, которые в OCR-выгрузке не сохранились однозначно.

40. Без обработки checksum_error receiver не посылает ранний NAK; recovery произойдёт по sender timeout. **Корректность сохраняется, производительность ухудшается**.

41. Условие нужно, чтобы не отправлять повторные NAK для одного и того же пропуска/не реагировать на frame, который не требует нового NAK. Иначе возможны NAK storms и лишние retransmissions.

42. Если ACK можно piggyback только с редкими outgoing frames (~1 раз/с), а timeout 10 мс, sender будет повторять frame порядка **100 раз** до появления ACK. Это иллюстрирует необходимость ACK timer.

43. Да, sequence space не обязан быть (2^n), если modulo arithmetic и window constraints реализованы корректно. При `MAX_SEQ=4` нужно убедиться, что window sizes не создают ambiguity после wraparound.

44. Frame time =1 мс, one-way propagation=270 мс, (1+2a=541).  
   - stop-and-wait W=1: **0.185%**;  
   - Protocol 5 / Go-Back-N, 3-bit seq → W=7: **1.29%**;  
   - Protocol 6 / selective repeat → W=4: **0.739%**.

45. Только NAK может работать для **непрерывного, нумерованного потока**, где receiver знает, что очередной frame должен появиться. Для конечной передачи silence не отличает «всё закончено» от «последний frame потерян», поэтому нужны ACK/timeout/дополнительное соглашение.

46. Frame 512 B =4096 bit, transmission time 64 мс; RTT propagation=540 мс; pipe factor ≈9.44 frames. Throughput:  
   - W=1: **≈6.78 кбит/с**;  
   - W=7: **≈47.5 кбит/с**;  
   - W=15: **64 кбит/с**;  
   - W=127: **64 кбит/с**.

47. Propagation 100 км при (2cdot10^8) м/с =0.5 мс. Bits in flight =1.544 Мбит/с×0.0005 = **772 бита**.

48. PPP часто работает поверх byte-oriented links/interfaces; byte stuffing проще реализовать на octet boundary и не требует bit-level insertion/removal machinery.

49. При standard PPP с 2-byte FCS фиксированный minimum overhead порядка **8 bytes/frame** (flags, address, control, protocol, FCS; соседние flags могут совместно использоваться). Maximum зависит от escaping: в худшем случае каждый data/control byte может потребовать дополнительный ESC, то есть byte-stuffing почти удваивает соответствующую часть frame.

50. ESC=01111101, FLAG=01111110. При PPP escaping с XOR 0x20:  
   ESC → **01111101 01011101**;  
   FLAG → **01111101 01011110**.  
   Для ESC FLAG FLAG ESC:  
   **7D 5D 7D 5E 7D 5E 7D 5D**.

51. AAL5: 100-byte IP packet + 8-byte trailer =108 bytes; pad до кратности 48 →144 bytes = **3 ATM cells**. Последняя cell содержит остаток data + padding + AAL5 trailer.

52. Generator: прочитать data bits и generator polynomial, дописать (k-1) zeros, выполнить modulo-2 division, заменить zeros на remainder и вывести codeword+polynomial. Verifier: прочитать codeword и polynomial, выполнить то же XOR-division; **zero remainder = frame accepted**, nonzero = error detected.
