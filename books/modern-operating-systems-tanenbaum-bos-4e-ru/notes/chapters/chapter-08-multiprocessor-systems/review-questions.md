# Review questions — source extract

Provenance: chapter-end questions/exercises, PDF pages 653–658, chunks `p0653:c01 … p0658:c01`.

Numbering follows the source. Structural cleanup only.

1. Можно ли USENET или SETI@home считать распределенной системой? Если да, к каким категориям рис. 8.1 они относятся?

2. Что произойдет, если три CPU мультипроцессора одновременно попытаются обратиться к одному слову памяти?

3. CPU выполняет 200 MIPS и при каждой инструкции делает одно обращение к памяти. Сколько CPU перегрузят шину 400 МГц при одном цикле шины на обращение? Повторите для cache hit 90%. Какой hit rate нужен 32 CPU, чтобы не перегрузить ту же шину?

4. Если оборвется провод между коммутаторами 2A и 3B в omega switching network рис. 8.5, кто от кого окажется отрезан?

5. Как обрабатывается сигнал в модели рис. 8.7?

6. При системном вызове в модели рис. 8.8 возникает проблема после trap, которой нет в рис. 8.7. В чем она и как ее решить?

7. Перепишите `enter_region` из листинга 2.3, используя обычное чтение перед TSL, чтобы уменьшить bus/cache thrashing.

8. Что перспективнее для many-core desktop: распараллеливать приложения или системные/библиотечные службы? Почему?

9. Нужны ли отдельные critical regions в SMP kernel или достаточно mutexes на структурах данных?

10. Запрашивающий CPU выполняет TSL раз в 50 bus cycles, а владелец lock изменяет cache block между попытками. Cache block = 16×32-bit words, одно слово = один bus cycle, bus = 400 MHz. Какая доля bandwidth тратится на ping-pong блока?

11. Будет ли binary exponential backoff для TSL корректно работать без максимального значения задержки?

12. Можно ли использовать атомарный `SWP`, меняющий register и memory word местами, вместо TSL для multiprocessor synchronization?

13. CPU instruction занимает 5 ns. После нее необходимые bus cycles (например для TSL) занимают по 10 ns каждый. Какую долю bus bandwidth забирает процесс, непрерывно исполняющий TSL spin loop? Instruction fetch кэшируется.

14. Affinity scheduling снижает cache misses. Снижает ли оно TLB misses? А page faults?

15. Чему равен diameter каждой topology на рис. 8.16, если host-router и router-router links считать одинаковыми?

16. Для double torus размером `k × k` найдите diameter; рассмотрите четный и нечетный `k`.

17. Чему равна bisection bandwidth сети-куба `8 × 8 × 8`, если каждая link = 1 Gbit/s?

18. В multicomputer с user-mode NIC требуется три copy operations. Передача 32-bit word через NIC в обе стороны занимает 20 ns, network = 1 Gbit/s. Найдите latency 64-byte packet без copy time, с тремя copies и с двумя дополнительными kernel copies.

19. Повторите предыдущую задачу для трех и пяти copies, но вычислите throughput.

20. Pin/unpin page system calls занимают по 1 μs. DMA = 5 bytes/ns, programmed I/O = 20 ns/byte. Какой минимальный packet size оправдывает pinning + DMA?

21. RPC переносит procedure на удаленную машину. Помимо pointers, unknown array sizes/types и globals, что произойдет, если remote procedure выполнит system call?

22. При DSM page fault требуется найти страницу. Назовите два возможных метода поиска.

23. На рис. 8.24 процесс H переносится с node 2 на node 3. Чему станет равен суммарный external traffic?

24. Для миграции уже работающего процесса между multicomputer nodes достаточно ли остановить процесс, переслать memory image и запустить его? Назовите две серьезные проблемы.

25. Почему Ethernet имеет ограничение длины кабеля?

26. На рис. 8.26 уровни middleware и application присутствуют на четырех машинах. В чем их сходство и различие между платформами?

27. Из шести network service types рис. 8.29 какая лучше подходит для:
   - а) Internet video on demand;
   - б) загрузки web page?

28. Предложите практически масштабируемую реализацию иерархической DNS database вместо одного централизованного сервера.

29. Почему при обработке URL браузер устанавливает соединение через port 80?

30. Браузер сначала получает HTML по TCP, закрывает соединение, затем открывает отдельные TCP connections для каждого image/icon. Предложите две схемы повышения производительности.

31. При session semantics изменения файла сразу видны процессу-автору и не видны remote machines до close. Должны ли изменения сразу видеть другие процессы на той же машине? Приведите аргументы за оба варианта.

32. Каковы преимущества object access перед shared-memory access, когда нескольким процессам нужны общие данные?

33. В Linda линейный поиск всего tuple space для `in` неэффективен. Предложите организацию tuple space, ускоряющую matching.

34. Напишите C-программу для измерения времени копирования буфера с `clock` или `times`; исследуйте разные размеры и отделите overhead от copy time.

35. Напишите C client/server stubs для RPC-вызова стандартного `printf` и test driver. Можно ограничить format length и число/типы/размеры параметров.

36. Реализуйте sender-initiated и receiver-initiated load-balancing algorithms. Сгенерируйте heavy и light workloads и сравните probe messages, включая min/max probes per host.

37. Напишите многопоточное publish/subscribe приложение с central broker, shared-memory producer/subscriber threads, hierarchical topics/wildcards, history delivery и динамическим созданием P/S threads; допустима также реализация через TCP.
