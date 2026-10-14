# Глава 3 — подтверждённые команды и конструкции

Источник: PDF 43–57, RAG `p0043:c01–p0057:c01`. Классификация зависит от результата выполнения тела ветви.

| Команда/конструкция в книге | Класс | Назначение и риск |
| --- | --- | --- |
| `case "$var" in … esac` | зависит от тела ветви | Выбор действий по шаблону, PDF 43. |
| `yes) echo "glad you agreed" ;;` | workload-generating | Вывод сообщения, PDF 43. |
| `no) … exit ;;` | state-changing | Завершение сценария, PDF 43. |
| `[Nn][Oo]*`, `[Yy]??`, `[Ss]ure`, `[Oo][Kk]*` | read-only при одном сопоставлении | Варианты шаблонов, PDF 44–45. |
| `ls -1 "$@"`, `ls -N --color=tty -T 0 "$@"` | read-only / workload-generating | Просмотр файлов; переносимость опций не подтверждена, PDF 47. |
| `sort -n`, `tail -1` | workload-generating | Сортировка и отбор результатов, PDF 47. |
| `printf '%3d %s\n' ${#fn} ${fn}` | workload-generating | Форматирование длины и имени файла, PDF 47. |
| `(( $# < 1 )) && Usage_Exit` | state-changing при вызове `exit` | Выход при недостатке аргументов, PDF 47. |
| `sub=$1`, `shift` | state-changing (состояние оболочки) | Назначить подкоманду и сместить параметры, PDF 47. |
| `[ -n "$BOOK_ASC" ]`, `[ -x /usr/bin/xsel -a $# -lt 1 ]` | read-only | Проверки условий в обёртке, PDF 49. |
| `\cd "$BOOK_ASC"` | state-changing | Изменение текущего каталога, PDF 49. |
| `xsel -b` / `xsel -bi` | read-only / state-changing | Чтение или изменение буфера обмена, PDF 49. |
| `echo -en "$*"` | workload-generating | Вывод через функцию `Output`, PDF 49. |
| `tr` и конвейер преобразования ID | workload-generating | Обработка текста, PDF 51. |
| `egrep`, `grep`, `more` | read-only / workload-generating | Генерация справки из строк сценария, PDF 52–55. |
| действие `index` в `wrapper.sh` | state-changing | Запись `index.txt`, rollback **[Needs confirmation]**, PDF 51. |
| действие `rerun` в `wrapper.sh` | state-changing | Повторный запуск сценариев с перезаписью `*.out`, rollback **[Needs confirmation]**, PDF 51. |
| действие `cleanup` в `wrapper.sh` | state-changing | Удаление совпавших файлов, rollback **[Needs confirmation]**, PDF 52. |
| `;;`, `;&`, `;;&` | поток управления | Завершить `case`; перейти к следующему телу; продолжить поиск совпадений, PDF 55–57. |

## Операционные границы

1. Только чтение: проверка условий, исходных шаблонов, выводов `ls` и справки. Фактический результат зависит от окружения.
2. Изменения: `index`, `rerun`, `cleanup` и команды с `exit` требуют понимания эффекта. Нельзя запускать их как универсальные инструкции.
3. Проверка: подтвердить аргументы и контекст, конкретные целевые файлы и возможность восстановления. Источник не даёт универсальных команд отката: **[Needs confirmation]**.
4. В примере на PDF 44 есть `continue` без показанного окружающего цикла; контекст применения **[Needs confirmation]** (см. [source-findings.md](source-findings.md)).
