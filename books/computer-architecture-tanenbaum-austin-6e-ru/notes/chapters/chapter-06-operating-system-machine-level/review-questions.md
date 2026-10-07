# Вопросы и задания — глава 6

**Provenance:** `p0548:c01`–`p0554:c01`, PDF pages 548–554.

Нумерация источника сохранена; формулировки сокращены.

1. Почему ОС интерпретирует только часть команд уровня ОС, тогда как микропрограмма интерпретирует весь ISA?
2. Сколько страниц в 32-битном byte-addressed virtual space при page size 4 KiB?
3. Обязан ли page size быть степенью двойки; возможна ли страница 4000 байт?
4. Для заданной таблицы 8 virtual pages / 4 frames / 1024 words: какие адреса fault и каковы physical addresses?
5. Для reference string `0,7,2,7,5,8,9,2,4` и 4 frames: faults при LRU и FIFO.
6. Улучшить описанный FIFO accounting так, чтобы не обновлять счетчики всех resident pages.
7. Что произойдёт, если page-fault handler сам окажется paged out?
8. Как отслеживать dirty pages без аппаратного dirty bit, имея protection bits?
9. Для segmented+paged memory из таблиц 6.11/6.12 вычислить physical addresses или тип faults.
10. Какие проблемы создаёт direct I/O в user-space buffer при compaction?
11. Почему memory-mapped file должен начинаться на page boundary?
12. Зачем Core i7 кэширует descriptor во внутренней части segment register?
13. Core i7: segment 10, offset 8000, BASE=10000 — directory/page entry и offset.
14. Возможные алгоритмы удаления segments в pure segmented memory.
15. Сравнить internal и external fragmentation и способы уменьшения.
16. LRU или FIFO для вытеснения товара с полки супермаркета?
17. Применимы ли arguments page-size trade-off к cache-line size?
18. Почему file должен явно открываться перед чтением?
19. Bitmap vs free-list: при каком числе holes список станет больше bitmap на заданном диске?
20. Преимущества allocation from the largest remaining free hole.
21. Назвать ещё одну цель `open`, не указанную явно в основном объяснении.
22. При run-length distribution `P(i)=2^-i` для data и holes: expected number of holes on N-sector disk.
23. Будут ли неизвестно растущие files храниться contiguously?
24. Что статистика file-size distribution говорит о block size?
25. Работает ли semaphore atomicity через disabling interrupts на one-CPU и two-CPU shared-memory systems?
26. Чем очередь blocked waiters лучше случайного пробуждения?
27. Решает ли операция `peek` проблему блокировки перед `down`?
28. Составить timeline P1/P2/P3 для заданных up/down events от 0 до 1000 ms.
29. Защитить ticket file binary semaphore-ом.
30. Написать `lock`/`unlock` с atomic `TSL X`.
31. Вычислить `in/out` ring buffer length 65 после восьми заданных операций.
32. UNIX-like inode: block=2 KiB, 512 addresses per indirect block — maximum file size.
33. Что делает `unlink("/usr/ast/bin/game3")` в показанном directory/link scenario?
34. Можно ли обойтись без `pipe`; что станет с pipelines?
35. Почему идея никогда не переиспользовать уже выдававшийся file descriptor плоха?
36. Windows ACL: запретить Светлане всё, остальным дать полный доступ.
37. Два producer/consumer варианта Windows с shared buffer + semaphores.
38. Спроектировать simulator LRU/FIFO для 64 virtual pages ×1 KiB и исследовать locality parameter x.
39. Экспериментально подобрать delay/computation, чтобы race из listing 6.1 зависал примерно раз в час.
40. UNIX/Windows program: вывести raw directory order, sizes и unused directory slots.
