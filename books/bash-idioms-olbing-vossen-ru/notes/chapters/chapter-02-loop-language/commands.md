# Глава 2 — подтверждённые конструкции и команды

**Provenance:** PDF 30–42, чанки `p0030:c01–p0042:c01`. Классы: read-only, workload-generating, state-changing. Книжный синтаксис сохраняется; учебные фрагменты без тела `do/done` не являются самостоятельными сценариями.

| Из источника | Класс | Назначение / риск / источник |
| --- | --- | --- |
| `for ((i=0; i<10; i++)); do printf '%d\n' "$i"; done` | workload-generating | Счётчик в стиле C, вывод десяти значений. PDF 31. |
| `for ((;;)); do printf 'forever'; done` | workload-generating | **Бесконечный вывод**, риск ресурсоёмкости; не запускать без ограничения. PDF 31. |
| `for value; do echo "$value"; done` | workload-generating | Вывод аргументов сценария/функции, значения позиционных параметров зависят от контекста. PDF 31–32. |
| `bash myloop.sh -c 17 core` | workload-generating | Книжный запуск учебного сценария, ожидаемый вывод −c, 17, core; наличие файла вне книги не подтверждено. PDF 31. |
| `for num in 1 2 3 4 5; do echo "$num"; done` | workload-generating | Явные значения. PDF 32. |
| `for i in {01..10}; do echo "$i"; done` | workload-generating | Пример brace expansion, особенности версии Bash указаны в источнике. PDF 33–34. |
| `for filename in log{01..5}.txt; do echo $filename; done` | workload-generating | Генерация имён и вывод, файл не создаёт. PDF 34. |
| `seq 2.1 0.3 3.2` | workload-generating | Печать числовой последовательности с шагом 0.3; PDF 34–35. |
| `for person in "${namelist[@]}"; do echo $person; done` | workload-generating | Сохраняет границы элементов на входе в цикл; источник для вывода использует `echo $person`, что требует внимания к аргументам вывода. PDF 37. |
| `for person in "${namelist[*]}"; do echo $person; done` | workload-generating | Одна итерация со склеенными элементами; PDF 38 (книга для вывода пишет `echo $person`). |
| `for key in "${!hash[@]}"; do echo "key $key ==> value ${hash[$key]}"; done` | workload-generating | Обход ключей и вывод значений хеша; PDF 36. |
| `declare -A hash` | state-changing | Создаёт ассоциативный массив в текущей оболочке; риски переопределения значений; rollback **[Needs confirmation]**. PDF 36. |
| `while read key value; do hash[$key]="$value"; done` | state-changing | Ввод и заполнение хеша, зависит от переданных строк; rollback **[Needs confirmation]**. PDF 36. |
| `for file in *.JPEG; do echo mv -v $file ${file/JPEG/jpg}; done` | workload-generating | **Пробный вывод** команды переименования, не само переименование; PDF 39. |
| `for file in *.JPEG; do mv -v $file ${file/JPEG/jpg}; done` | state-changing | **Изменяет имена файлов**, приведено в обсуждении на PDF 38; проверять пути и аргументы, rollback **[Needs confirmation]**. |
| `for node in web-server{00..09}; do echo ssh ...; done` | workload-generating | Только печать команд для списка узлов. Книжная конфигурация учебная; PDF 39. |
| `until ssh user@10.10.10.10; do sleep 3; done` | workload-generating | Повторные попытки SSH с задержкой, риск сетевой нагрузки/аутентификации; пользователь, IP — **заменить плейсхолдерами** при повторном использовании; см. [source-findings.md](source-findings.md). PDF 40. |
| `declare -i i` | state-changing | Объявляет целочисленную переменную для числового цикла; rollback **[Needs confirmation]**. PDF 41. |

## Дополнительные средства, прямо упомянутые авторами

`cat`, `find`, `sort -u`, `LC_ALL=C sort`, `seq` используются как поставщики значений в примерах подстановки команд (PDF 33–34); эти операции относятся к read-only / workload-generating при чтении, поиске и печати. `printf -v` упомянута как вариант конструирования имени (PDF 34), изменяет значение переменной оболочки (state-changing для shell memory). Авторы называют специализированные средства запуска команд на многих хостах: Ansible, Chef, Puppet, clusterssh, mssh, mussh, pconsole, multixterm, PAC Manager (PDF 39); их вызовы **не** приведены как команды к исполнению. Привычные дополнительные флаги и процедуры эксплуатации здесь не добавлены.

## Верификация и риски

- Перед реальным `mv` нужен подтверждённый список файлов, корректность преобразования расширения, контроль результата и отдельный rollback-план — **[Needs confirmation]**. У приведённого в книге варианта переменные не заключены в кавычки: это нельзя без проверки выдавать за безопасную массовую обработку имён с пробелами. [PDF 37–39]
- Перед реальным `ssh` нужны разрешённые хосты, безопасная аутентификация, ограничение числа попыток и критерий остановки — **[Needs confirmation]**. [PDF 39–40]
- Учебные команды-демонстрации сами по себе не подтверждают результаты выполнения в среде читателя.
