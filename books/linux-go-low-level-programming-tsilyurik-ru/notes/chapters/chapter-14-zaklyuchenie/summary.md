# Summary — «Заключение»

Книга завершается возвращением к исходной идее: предметом является не столько синтаксис Go, сколько эффективное использование многопроцессорного hardware.

Источник подчёркивает:

- в Go остаётся много возможностей, не охваченных книгой;
- ключевая тема — программное использование множества processors одновременно;
- исторический рост производительности за счёт одной только clock frequency, по мнению автора, исчерпал себя;
- дальнейший рост производительности связывается с увеличением числа processors;
- эффективное использование этой архитектурной реальности остаётся отдельной инженерной задачей.

В контексте предыдущих глав operational conclusion книги:

```text
more CPU
≠ automatic speedup

useful parallel decomposition
+ race-free shared-state handling
+ controlled synchronization cost
+ measurement
= potentially useful multicore scaling
```

Это итоговый source-derived summary. Page 281 `Об авторе` в него не входит.
