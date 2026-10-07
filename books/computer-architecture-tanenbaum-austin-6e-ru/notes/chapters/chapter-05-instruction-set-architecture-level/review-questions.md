# Вопросы и задания — глава 5

**Provenance:** `p0470:c01`–`p0474:c01`, PDF pages 470–474.

Нумерация источника сохранена; формулировки сокращены без добавления внешнего содержания.

1. Word value 3 is byte-copied from one byte order to the opposite order without reordering byte positions. What numeric value results?
2. With separate instruction/data address spaces, how can an OS load program code if normal stores address only data space?
3. Design a 32-bit expanding opcode for 15 commands with two 12-bit addresses + 4-bit register, 650 commands with one 12-bit address + 4-bit register, and 80 zero-address/register commands.
4. 16-bit instructions, 6-bit addresses: if there are n two-address commands, maximum number of one-address commands?
5. Can a 12-bit expanding opcode encode 4 three-register commands, 255 one-register commands and 16 zero-register commands if register number is 3 bits?
6. Accumulator machine with memory values M20=40, M30=50, M40=60, M50=70: results for immediate/direct/indirect LOAD 20 and 30.
7. For zero-, one-, two- and three-address machines, program `X=(A+B*C)/(D-E*F)` and count instruction bits; opcode=8 bits, memory address=16 bits, register=4 bits.
8. Devise a 6-bit addressing mechanism selecting any arbitrary set of 64 addresses.
9. Give another disadvantage of self-modifying code not mentioned in the chapter.
10. Convert four source infix arithmetic expressions to postfix.
11. Determine which three pairs of postfix expressions are mathematically equivalent.
12. Convert four source postfix expressions to infix.
13. Give three postfix formulas that cannot be converted to infix.
14. Convert three Boolean infix formulas to postfix.
15. Convert `(5*2+7)-(4/2+1)` to postfix and write IJVM code.
16. How many registers are supported by the formats referenced in the exercise?
17. How does hardware recognize format variant 3 when variants 1/2 are distinguished using bit 23?
18. For a hypothetical three-address interval-test command with A,B,X, how many condition bits are needed/set?
19. One advantage and one disadvantage of PC-relative addressing.
20. Why does Core i7 track carry out of bit 3?
21. Is an instruction with “two opcodes” a patent-worthy new idea?
22. Design an efficient instruction for tests like `k==0`, `a>b`, `k<5`; define fields.
23. Apply logical/arithmetic shifts and rotates by 4 to `1001 0101 1100 0011`.
24. Clear a memory word without CLR.
25. Compute `(A AND B) OR C` for the supplied 16-bit values.
26. Swap A and B without a third variable/register using XOR.
27. When are shifts+adds useful for multiplying a variable by a constant?
28. Translate `i=3`, `i=j`, `i=j-1` to Core i7 and IJVM; compare code bytes under optimistic assumptions.
29. Design an instruction for `while` loops.
30. Hanoi monks move one disk/minute. How many years for 64 disks?
31. Why does an I/O device place an interrupt identifier/vector number on the bus instead of only using a memory table?
32. DMA disk: 64×512-byte sectors/track, 16 ms/rev, 16-bit bus, 500 ns transfer, CPU uses two bus cycles/instruction. CPU slowdown?
33. Improve figure-5.20 DMA using multi-bus architecture from figure 3.33.
34. Why do interrupt handlers have priorities while ordinary procedures generally do not?
35. IA-64 has many predicate registers. Is this related to predication?
36. Why are speculative stores not analogous to speculative loads?
37. Bridge between two LANs: 250 µs interrupt+classification per 1-KiB packet, forwarding via DMA. Maximum per-network rate without packet loss?
38. If FP points to first local variable, what information must be recoverable on procedure return?
39. Write an assembly subroutine converting signed binary integer to ASCII.
40. Write an assembly subroutine converting infix formula to postfix.
41. Write an assembly recursive factorial `n!`.
42. Solve Towers of Hanoi without recursion and without simulating recursion with an explicit array stack.
