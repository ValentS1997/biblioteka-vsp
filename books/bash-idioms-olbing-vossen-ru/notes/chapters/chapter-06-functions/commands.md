# Глава 6 — команды и конструкции, подтверждённые RAG

**Provenance:** PDF 83–93, чанки `p0083:c01–p0093:c01`. Классы: read-only (наблюдение), workload-generating (вычисление/вывод), state-changing (изменяет переменные, состояние или внешние данные). Ниже приведены учебные фрагменты, не подготовленные к запуску без контекста.

| Форма в источнике | Класс | Назначение / риск / PDF |
| --- | --- | --- |
| `Do_Something`, `Find_File 25 $MPATH $ECODE`, `Show_All $*` | зависит от тела функции | Вызовы не определённых здесь функций; действие неизвестно. PDF 83. |
| `function Helper ()`, `function Helper`, `Helper ()` | state-changing (namespace shell) | Объявление функции; тело в примере определений опущено. PDF 84. |
| `function Say_So { echo 'Here we are in the function named Say_So'; }` | state-changing при объявлении, workload-generating при вызове | Имя функции и вывод; PDF 84. |
| `function See2it` с `echo "First arg: $1"`, `echo "Second arg: $2"` | workload-generating при вызове | Демонстрация позиционных аргументов; PDF 85. |
| `Tell_All 47 tree /tmp` | workload-generating | Вызов функции, печатающей `$FUNCNAME`, `$#`, `"$@"`; PDF 86. |
| `for arg in "$@"; do echo "$arg"; done` | workload-generating | Сохраняет границы аргументов при перечислении, PDF 86. |
| `$?` | read-only | Статус последней команды/функции, PDF 86. |
| `$(...)` при вызове функции | workload-generating или state-changing по телу | Захват её вывода через подоболочку; не равен статусу функции. PDF 86. |
| `local i`, `local -i i`, `declare -i i` | state-changing (shell scope) | Локальная переменная и целочисленный атрибут; динамическая область видимости. PDF 87–88. |
| `SUM=0`, `let SUM+=i` | state-changing (shell scope) | Модификация результата через глобальную переменную в `Summer`; контекст фигурных скобок цикла требует проверки. PDF 87. |
| `function Usage_Message { … } 1>&2` | state-changing при объявлении; workload-generating при вызове | Одно перенаправление всего вывода функции в STDERR. PDF 88–89. |
| `type -a printf` | read-only | Определение встроенного и внешнего `printf`, PDF 89. |
| `help printf`, `printf --help`, `man 1 printf` | read-only / workload-generating | Документация встроенной или внешней реализации, PDF 90. |
| `/usr/bin/printf --help`, `env printf --help` | read-only / workload-generating | Справка о внешнем бинарнике, если доступен. PDF 89–90. |
| `printf '%s\n'`, `printf '%b\n'` | workload-generating | Демонстрация явной управляющей последовательности перевода строки; PDF 90. |
| `printf -v today '%(%F)T' '-1'` | state-changing (shell variable) | Сохранение отформатированной текущей даты в `today`; требует поддерживаемой версии Bash. PDF 91. |
| `printf '%(%F %T %z)T: %s\n' '-1' 'Your log message here'` | workload-generating | Форматированная строка журнала с датой. PDF 91. |
| `printf '%q' "This example is from $today\n"` | workload-generating | Экранирующий вывод для повторного использования/отладки, PDF 92. |
| `date -d '2 months ago' '+%B'` | workload-generating | Пример GNU date для арифметики с датами, PDF 91–92; переносимость не установлена. |

## Контроль эффектов

`$?` — получение статуса, но **не** возврат строкового значения; `printf -v` — изменение переменной, а `printf` без `-v` — вывод. `local` защищает от порчи глобальных переменных, но не закрывает доступ дочерним функциям. [PDF 86–93]

Для действий, изменяющих глобальное состояние, нужно заранее определить имена переменных, ожидаемый результат, проверку и rollback. В RAG универсального отката нет: **[Needs confirmation]**.

`Summer` на PDF 87 представлен с арифметическим циклом и фигурными скобками; это зафиксировано без исправления в [source-findings.md](source-findings.md). Никаких неподтверждённых команд в исполняемый рецепт не добавлено.
