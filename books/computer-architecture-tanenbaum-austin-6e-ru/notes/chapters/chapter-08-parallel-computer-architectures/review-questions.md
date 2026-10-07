# Вопросы и задания — глава 8

**Provenance:** `p0696:c01`–`p0698:c01`, PDF pages 696–698.

Нумерация источника сохранена; формулировки сокращены.

1. Делает ли variable-length x86 instruction up to 17 bytes процессор VLIW?
2. Какие альтернативы multicore могли выбрать Intel/AMD при росте transistor budget?
3. Для диапазона 0–255: результаты saturation/clipping для 96, -9, 300, 256.
4. Совместимы ли три заданных набора TriMedia operations по slot constraints?
5. Продолжить execution diagram figure 8.5 на три cycles для fine/coarse-grained threading.
6. Если L1 miss/L2 hit требует k cycles, сколько fine-grained threads нужно для полного скрытия простоя?
7. Какой архитектуре из главы 2 подобен NVIDIA Fermi?
8. Пчёлы ищут один тип нектара независимо: SIMD или MIMD?
9. Зачем memory consistency model оформляется как software/hardware contract?
10. Shared-bus multiprocessor: два simultaneous global-memory requests.
11. То же для трёх processors.
12. Snooping cache видит address lines, но не data lines: влияет ли это на write-through protocol?
13. Shared bus, 1/4 instructions access memory and occupy bus for whole instruction: speedup of 64 processors.
14. MESI with only 3 states: which state can be removed and consequences of removing each?
15. Когда line is present locally but MESI still requires bus transaction?
16. n processors independently request bus with probability p: P(0), P(1), P(>1).
17. Главное преимущество и недостаток crossbar.
18. Сколько crossbar fabrics в full Sun Fire E25K?
19. Omega network: wire 2A→3B fails; which endpoints lose connectivity?
20. Are memory hot spots a problem in bus-based systems?
21. 4096-node omega, CPU cycle 60 ns, switch delay 5 ns: LOAD delay slots.
22. Omega with program/stack i in memory module i: small topology change improving performance and its downside.
23. NUMA local=20 ns, remote=120 ns; page P receives 1% of N accesses; copy cost C: when copy locally?
24. CC-NUMA: 512 nodes × 8 MiB, 64-byte lines: directory overhead percentage and scaling with node count.
25. Difference between NC-NUMA and CC-NUMA.
26. Diameters of figure-8.33 topologies.
27. Fault-tolerance coefficient of figure-8.33 topologies.
28. Diameter of k×k 2D torus for even/odd k.
29. Bisection bandwidth of 8×8×8 cube with 1 GB/s duplex links.
30. Amdahl maximum speedup as n→∞; value for f=0.1.
31. Figure 8.44: per-processor bandwidth for 4/16 processors, then 64, then asymptotic limits for bus vs mesh.
32. Propose a fourth send semantic similar to blocking; advantage/disadvantage.
33. On hardware-broadcast network, why does read/write ratio matter?
