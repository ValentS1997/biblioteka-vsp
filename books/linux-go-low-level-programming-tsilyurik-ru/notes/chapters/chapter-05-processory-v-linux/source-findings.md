# Source findings — глава 5 «Процессоры в Linux»

## Finding 1 — inconsistent nice range

Classification: **[Source wording mismatch]**

Provenance:

- PDF page 142, chunk `p0142:c01`
- PDF page 143, chunk `p0143:c01`

Observed:

На странице 142 источник пишет диапазон nice как:

```text
-20 ... +19
```

На странице 143 в собственном описании перед help-фрагментом приводится:

```text
-19 ... +20
```

Но тут же help output команды `nice --help` снова показывает:

```text
-20 ... 19
```

Impact:

Внутри одной главы присутствуют две несовместимые границы диапазона.

Action:

- не выбирать «правильную» версию из model memory;
- в operational artifacts не закреплять спорный альтернативный диапазон как факт;
- source adjudication: **[Needs confirmation]**.

## Finding 2 — wrong function name in error text

Classification: **[Source code mismatch]**

Provenance:

- PDF page 140, chunk `p0140:c01`
- example `how-many-t.c`

Observed code:

```c
if(pthread_getaffinity_np(...) != 0)
    printf("ошибка pthread_setaffinity_np() %m\n"), exit(1);
```

Вызывается `pthread_getaffinity_np()`, но error message называет `pthread_setaffinity_np()`.

Impact:

Диагностическое сообщение может ввести в заблуждение при ошибке выполнения.

Action:

- example не исправлялся;
- mismatch зафиксирован;
- intended diagnostic name: **[Needs confirmation]** under rag-only policy.

## Finding 3 — scheduler statements are source-scoped

Classification: **[Needs confirmation]**

Provenance:

- pages 141–145

Observed:

Источник делает конкретные утверждения о Linux scheduling internals, timeslices, O(1) scheduling и default values.

Impact:

Эти утверждения зависят от версии ядра/окружения и в данном workflow не сверялись с внешней актуальной документацией.

Action:

- сохранять как source claims;
- не использовать как утверждения о текущем Linux вне контекста книги без отдельной проверки.
