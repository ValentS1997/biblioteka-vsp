# Вопросы и задания — глава 3

**Provenance:** `p0264:c01`–`p0269:c01`, PDF pages 264–269.

Нумерация источника сохранена; формулировки сокращены без добавления внешнего содержания.

1. Защищены ли цифровые схемы от шума? Обосновать.
2. Разобрать логическое выражение «гамбургер ИЛИ хот-дог И картофель фри» при XOR для ИЛИ и неопределенном приоритете И/ИЛИ.
3. Две банды: одна всегда говорит правду, другая всегда лжет. Как одним вопросом определить дорогу в Диснейленд?
4. Таблицей истинности доказать `X = (X AND Y) OR (X AND NOT Y)`.
5. Сколько Boolean functions существует от 3 и от n переменных?
6. Сколько Boolean functions существует от 4 переменных?
7. Реализовать AND двумя NAND gates.
8. 8:1 mux с тремя select variables: реализовать odd parity function.
9. Показать, как 8:1 mux реализует произвольную функцию четырех Boolean variables; затем реализовать source word-length parity example.
10. Нарисовать 4-to-2 encoder при one-hot input.
11. Нарисовать 1-to-4 demultiplexer с двумя control lines.
12. Определить функцию схемы, показанной в source figure.
13. Сколько pins требуется 4-bit adder, если четыре таких блока должны образовать 16-bit adder?
14. Ускорить ripple-carry adder, генерируя carries параллельно.
15. При gate delay 1 ns определить minimum valid-output time для source ALU figure.
16. Может ли source 8-bit ALU выполнять subtraction? Объяснить/модифицировать.
17. 16-bit ALU из 16 one-bit stages: 10 ns per stage + 1 ns inter-stage propagation. Worst-case result time?
18. Получить constant −1 на source 8-bit ALU двумя способами и задать шесть control signals.
19. Idle inputs S/R для NAND-based SR latch?
20. Преобразовать rising-edge flip-flop в falling-edge version.
21. Расширить source 4×3 memory (22 AND, 3 OR) до 256×8: сколько AND/OR?
22. Оценить chip с четырьмя D flip-flops, common clock, Q and NOT-Q outputs, no preset/clear.
23. Адресовать 2^n memory words с меньшим количеством address pins, чем n.
24. 32-bit data bus + 1M×1 DRAM chips: minimum memory size?
25. Source synchronous bus: clock period 20 ns instead of 10 ns; timing constraints unchanged. Worst-case memory time after MREQ?
26. 100-MHz clock, TAD=4 ns: можно ли использовать 10-ns memory?
27. Может ли TML быть отрицательным, то есть MREQ появляться до полного установления адреса?
28. Long block transfer versus separate transfers; effect of changing bus width from 8 to 32 bits.
29. Выписать inequalities/cause-order for source asynchronous full handshake.
30. Advantages of multicore chip versus several PCs over Ethernet.
31. Почему появились multicore processors; роль technology and Moore's law.
32. Отличие memory bus от PCI bus.
33. На 32-bit bus как однозначно разместить 16-bit read/write?
34. Зачем специальный interrupt-acknowledge bus cycle?
35. 32-bit bus, 200 MHz, 4 cycles per 32-bit read: fraction of theoretical bus bandwidth used?
36. 64-bit bus, 200 MHz, 4 cycles per 64-bit read: same question.
37. 32-bit aligned machine: valid byte/halfword/word read combinations and required pins; give two encodings.
38. Зачем L1/L2/L3 cache hierarchy?
39. L1=1 ns, L2=2 ns, memory=10 ns; 20% L1 hits, 60% L2 hits: average access time?
40. Bus bandwidth for 1280×960, 30 fps, color, data crosses bus twice.
41. Which signals in source PCIe figure are not strictly required for the protocol?
42. PCIe x16: conductors/raw/useful bandwidth using numeric premise from exercise.
43. DMA disk transfer: 2048×512-byte sectors/track, 5-ms access, 32-bit DMA operation takes one 10-ns bus cycle. CPU needs two bus cycles/instruction. Slowdown?
44. USB isochronous device: max payload 1023 bytes and one data packet/frame. Max throughput?
45. Add address line A13 to NAND selecting PIO in partial-decode source figure. What changes?
46. Write simulator for m×n array of 2-input NAND gates with j inputs/k outputs and wiring table; print all 2^j outputs.
47. Write program that parses two Boolean expressions and determines equivalence by truth tables.
