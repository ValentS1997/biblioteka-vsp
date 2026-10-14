# Глава 7 — подтверждённые команды и конструкции

**Provenance:** PDF 94–110, RAG `p0094:c01–p0110:c01`. Класс: read-only / workload-generating / state-changing. Команды — книжные примеры, не исполнявшиеся на ресурсах пользователя.

| Команда или выражение из RAG | Класс | Назначение и риск |
| --- | --- | --- |
| `declare -a mylist`, `local -a`, `readonly -a` | state-changing (shell) | Объявление индексированного массива; PDF 97–98. |
| `mylist[0]='foo'`, `mylist=(foo bar baz ...)` | state-changing (shell) | Присваивание элементов; PDF 97–98. |
| `mylist+=(bar)`, `mylist+=("five by five")` | state-changing (shell) | Добавление элемента; кавычки сохраняют пробелы. PDF 98. |
| `${#mylist[@]}`, `${#mylist[4]}` | read-only | Количество элементов и длина значения, PDF 98. |
| `declare -p mylist` | read-only / workload-generating | Вывод объявления массива для диагностики, PDF 99–101. |
| `printf "%q|" "${mylist[@]}"` | workload-generating | Печать экранированных аргументов с видимыми границами, PDF 99–101. |
| `function Join { local IFS="$1"; shift; echo "$*"; }` | state-changing при объявлении / workload-generating при вызове | Объединение через односивольный разделитель из `IFS`; `"$*"` применён намеренно. PDF 99, 104. |
| `String_Join '<>' "${mylist[@]}"` | workload-generating | Вызов функции объединения из примера 7.1, многоcимвольный разделитель; PDF 99. |
| `for element in "${!mylist[@]}"; do ...; done` | workload-generating | Обход индексов списка, PDF 99. |
| `"${mylist[@]:5:2}"` | read-only | Вычисление среза списка, PDF 99. |
| `mylist=("${mylist[@]:1}")` | state-changing (shell) | Создаёт новый список без первого элемента, PDF 99–100. |
| `unset -v 'mylist[-1]'`, `unset -v 'mylist[2]'` | state-changing (shell) | Удаление элемента; отрицательный индекс требует Bash 4.3+ по книге. PDF 100. |
| `unset -v mylist` | state-changing (shell) | Удаление всего массива, PDF 100. |
| `declare -A myhash`, `local -A`, `readonly -A` | state-changing (shell) | Объявление ассоциативного массива, Bash 4.0+ по книге. PDF 102–103. |
| `myhash[a]='foo'`, `myhash[f]='five by five'` | state-changing (shell) | Присваивание значения по строковому ключу, PDF 103. |
| `declare -p myhash`, `${#myhash[@]}` | read-only / workload-generating | Просмотр и количество ключей, PDF 103–104. |
| `for key in "${!myhash[@]}"; do ...; done` | workload-generating (по телу) | Перебор ключей; без гарантий порядка, PDF 104, 108. |
| `unset -v 'myhash[c]'`, `unset -v myhash` | state-changing (shell) | Удаление ключа или всего хеша, PDF 105. |
| `FORMAT='fmt --width 70 --split-only'`, `declare -p ... | $FORMAT` | workload-generating | Форматирование диагностического вывода, PDF 98–105. |
| `WORD_FILE='/tmp/words.txt'`, `> $WORD_FILE` | **state-changing (filesystem)** | В примере 7.5 файл создаётся/обнуляется по фиксированному пути; риск потери существующих данных. PDF 107. |
| `trap "rm -f $WORD_FILE" ABRT EXIT HUP INT QUIT TERM` | **state-changing (filesystem)** | Регистрирует последующее удаление временного файла; не запускать без проверки пути. PDF 107. |
| `echo "${mylist[$random_element]}" >> $WORD_FILE` | **state-changing (filesystem)** | Добавление случайного слова в файл; PDF 107. |
| `while read line; do (( myhash[$line]++ )); done < $WORD_FILE` | state-changing (shell), read-only file input | Подсчёт частот по строкам; PDF 107–108. |
| `done | sort`, `done | sort -k2,2n` | workload-generating | Сортировка уникальных значений или подсчитанных частот, PDF 108–109. |

## Безопасные границы

Примеры 7.1 и 7.3 в основном меняют переменные внутри Bash, но `unset` удаляет значения без автоматического восстановления. В примере 7.5 используется фиксированный путь `/tmp/words.txt`, а очистка через `trap` потенциально удаляет **уже существующий файл**. Реальное выполнение без предварительной проверки пути и согласия неприемлемо. [PDF 100, 105, 107–108]

В строке пояснения к примеру 7.5 RAG содержит `$$RANDOM`; она **не** заменена на предположительно правильную форму: [source-findings.md](source-findings.md). Исполнительных изменений PDF или RAG нет.

## Верификация и rollback

Перед операциями удаления подтвердить ключ и текущее содержимое через `declare -p`; перед работой с файлами подтвердить существование, владение и сохранность предыдущих данных. После изменений проверить количество элементов, их значения и вывод. Ни одна проверка в пользовательской среде не выполнялась. Проверенная процедура восстановления: **[Needs confirmation]**.
