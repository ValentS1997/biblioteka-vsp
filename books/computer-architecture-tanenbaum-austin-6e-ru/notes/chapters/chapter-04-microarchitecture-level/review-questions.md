# Вопросы и задания — глава 4

**Provenance:** `p0373:c01`–`p0376:c01`, PDF pages 373–376.

Нумерация сохранена; формулировки сокращены без добавления внешнего содержания.

1. Какие четыре шага используются процессорами для исполнения команд?
2. Почему B-bus source в Mic-1 кодируется 4-bit field, а C-bus destinations — bitmap?
3. Нарисовать схему блока «Старший бит» на figure 4.5.
4. Имеет ли смысл JMPC при NEXT_ADDRESS=0x1FF?
5. После source `if` добавить `k=5`. Каким будет оптимизированный IJVM assembly?
6. Дать два разных IJVM translation для `i = k + n + 5`.
7. Восстановить Java statement из IJVM: ILOAD j; ILOAD k; ISUB; BIPUSH 6; ISUB; DUP; IADD; ISTORE i.
8. Можно ли разместить L1 в 0x40, L2 в 0x140 для source conditional microbranch?
9. Почему `if_cmpeq3` нельзя свернуть в `Z=MDR-TOS; rd`?
10. Mic-1 at 2.5 GHz: execution time of Java `i=j+k`?
11. Same for Mic-2; then scale a program taking 100 ns on Mic-1.
12. Write Mic-1 microprogram for POPTWO: remove top two stack words.
13. JVM has 1-byte opcodes loading locals 0..3. What IJVM/microarchitecture changes exploit them best?
14. Add JVM ISHR 0x7A: arithmetic right shift by low 5 bits of top word; answer arithmetic equivalence for shift by 2 and microcode design.
15. Add JVM ISHL 0x78: left shift by low 5 bits; answer arithmetic equivalence for shift by 2 and microcode design.
16. Why does INVOKEVIRTUAL need parameter count?
17. Implement DLOAD for Mic-2: push local word at index and next higher word.
18. Draw tennis scoring FSM.
19. Which tennis FSM states are equivalent and can be merged?
20. Design branch-predictor FSM that changes prediction only after 3 consecutive misses.
21. Can IFU shift register be 5 bytes? 4 bytes?
22. Could a larger IFU shift register, e.g. 12 bytes, ever help?
23. Mic-2 `if_icmpeq6` branches to T, which duplicates `goto1`. Could it branch directly to `goto1` and be faster?
24. Why not remove Mic-4 decode stage and use IJVM opcode directly as micro-op ROM index?
25. Why multiple cache levels instead of one large cache?
26. L1 hit 60%, L2 hit 35%, memory 5%; latencies 5/15/60 ns sequentially. Average access?
27. Is write allocation useful if a write is followed by many reads of the same cache line?
28. Must set associativity be a power of two? Was replacing 3-way by 4-way necessary?
29. Why increase pipeline depth?
30. Five-stage pipeline: every conditional branch causes 3 idle cycles; branches are 20%. Performance loss?
31. Prefetch 20 instructions spans ~4 conditional branches, each predicted correctly with 90%. Probability prefetched instruction is on correct path?
32. In table 4.11 change instruction 6 destination from R1 to R8 after expanding register file to 16. What changes from cycle 6?
33. Can WAW dependency be optimized away?
34. Rewrite Mic-1 interpreter so LV points to first local variable instead of link pointer.
35. Write simulator for direct-mapped cache; parameterize entry count/line length and experiment.
