# Вопросы и задания — глава 7

**Provenance:** `p0587:c01`–`p0589:c01`, PDF pages 587–589.

1. Сравнить три стратегии: весь код на C; весь на assembler; C + переписать hotspot 2% на assembler. Дано: 100 person-months for C, assembler 10× harder, 4× faster, hotspot = 50% runtime.
2. Применимы ли правила two-pass assembler к compiler, если compiler emits object modules vs assembly text?
3. Какие проблемы возникают, если x86 assembler меняет традиционный порядок operands destination/source?
4. Можно ли за два прохода обработать цепочку `P EQU Q; Q EQU R; R EQU S; S EQU 4`?
5. 40-bit word, symbol names only letters excluding Q: maximum symbol length and encoding.
6. Чем instruction отличается от assembler directive?
7. Чем Instruction Location Counter отличается от processor Program Counter?
8. Построить symbol table для заданных x86 statements beginning at address 1000.
9. Может ли label совпадать с opcode name?
10. Выполнить binary search для Berkeley в заданном отсортированном списке, choosing upper middle for even size.
11. Работает ли binary search для таблицы с prime number of elements?
12. Вычислить hash codes for `els, jan, jelle, maaike` with letter sums mod 19 and resolve collision.
13. При table occupancy R сколько probes в среднем нужно open-addressing insertion?
14. Как реализовать associative memory с тысячами identical processors, small local memory and 3 shared registers?
15. Как directive `SEG N` влияет на Instruction Location Counter?
16. Было бы эффективнее поместить все procedures в один giant DLL?
17. Можно ли map same DLL into two processes at different virtual addresses; what problems/solutions?
18. Работает ли one-pass static-library scan when newly extracted procedures introduce further external references?
19. Может ли actual macro parameter быть register? constant?
20. Что меняется, если macro definitions may appear after macro calls?
21. Как ввести macro assembler в infinite loop?
22. Five modules of 200, 800, 600, 500, 700 words: relocation constants in load order.
23. Написать `enter/lookup` symbol table using hashing.
24. То же, но sort after insertion and use binary search.
25. Написать simple assembler for Mic-1; support symbolic constants and assembling a constant into a machine word.
26. Добавить macro support к assembler из задания 25.
