# Глава 9 — команды и конструкции из RAG

**Provenance:** PDF 126–145, `p0126:c01–p0145:c01`. Классы: **read-only** (наблюдение), **workload-generating** (вычисление, вывод, сеть), **state-changing** (изменение файлов, переменных, среды или управления). Все фрагменты — подтверждённые книжные примеры; они не исполнялись здесь.

| Фрагмент из источника | Класс | Воздействие и замечания |
| --- | --- | --- |
| `grep '^nobody' /etc/passwd` | read-only / workload-generating | Читает системную базу, фильтрует запись; PDF 126–127. |
| `read -d':' user shadow uid gid gecos home shell` | state-changing (shell variables) | Записывает поля до *конца записи* по `-d`; не задаёт `IFS`, PDF 126–127. |
| `IFS=':' read user shadow uid gid gecos home shell` | state-changing (shell variables) | Разделение полей по двоеточию только для вызова `read`, PDF 127. |
| `shopt -s lastpipe` | state-changing (shell options) | Изменяет режим последнего элемента конвейера при определённых условиях; PDF 127. |
| `set +m` | state-changing (job control) | Меняет управление заданиями; авторы **не рекомендуют** это делать, PDF 127. |
| `mapfile -t nodes < /path/to/list/of/hosts` | state-changing (array) / read-only file | Загружает файл в массив без переводов строк; ограничение памяти, PDF 128. |
| `while mapfile -t -n $BATCH nodes && ((${#nodes[@]})); do ...; done < /path/to/list/of/hosts` | state-changing (array) / workload-generating | Пакетное чтение, проверка непустоты массива; PDF 128. |
| `ssh $node 'echo -e "$HOSTNAME:\t$(uptime)"'` | workload-generating (remote) | Сетевой запуск на хосте; реальные права и эффекты **[Needs confirmation]**, PDF 128. |
| `> $HOSTS_FILE`, `echo "$n" >> $HOSTS_FILE` | **state-changing (filesystem)** | Пример 9.3: перезапись и добавление в `/tmp/nodes.txt`; риск потери данных, PDF 128–129. |
| `cat $HOSTS_FILE | wc -l` | read-only / workload-generating | Считает строки; внешний вывод присваивается `node_count`, PDF 129. |
| `sleep $SLEEP_SECS_PER_NODE`, `sleep $SLEEP_SECS_PER_BATCH` | workload-generating | Замедляют обработку по авторскому примеру, PDF 129. |
| `help mapfile`, `help readarray`, `help read` | read-only | Встроенная справка, PDF 130, 133. |
| `for word in $(cat file); do echo "word: $word"; done` | workload-generating | Метод «грубой силы»; интерпретация слов зависит от разделения, PDF 131. |
| `for word in $(< file); do ...; done` | workload-generating | Книжная альтернатива без `cat`, PDF 131. |
| `IFS=$' \t\n'` | state-changing (shell state) | Форма значения по умолчанию, не рекомендуем слепо назначать глобально, PDF 131. |
| `while IFS='' read line w1 w2 w3; do ...; done < $IFS_TEST_FILE` | state-changing (local read/variables) | На один вызов `read` выключает разбиение полей, PDF 132–133. |
| `local IFS=''` внутри `Read_A_File` | state-changing (function local) | Ограничивает область изменения разделителя, PDF 132–133. |
| `cat <<'EoF' > $IFS_TEST_FILE` | **state-changing (filesystem)** | Создаёт/перезаписывает `/tmp/ifs-test.txt`, PDF 132. |
| `printf 'IFS during: %q ...' ...` | workload-generating | Печатает экранированное представление значений, PDF 132–133. |
| `cut -f1 ... | sort -u > /tmp/previous-report.log` | **state-changing (filesystem)** | Создаёт промежуточный файл, PDF 134. |
| `diff /tmp/previous-report.log /tmp/current-report.log` | read-only / workload-generating | Сравнивает файлы, PDF 134. |
| `rm /tmp/previous-report.log /tmp/current-report.log` | **state-changing (filesystem)** | Удаление промежуточных файлов, rollback **[Needs confirmation]**, PDF 134. |
| `diff <(cut -f1 ... | sort -u) <(cut -f1 ... | sort -u)` | read-only / workload-generating | Подстановка процессов вместо файлов-результатов, PDF 134–135. |
| `[ -x "$config" ] && source "$config"` | **state-changing (shell/executed code)** | Проверяет права и исполняет доверенный файл настроек, PDF 136. |
| `source /path/to/global/bash-library.lib || { ...; exit 1; }` | **state-changing / external code** | Подключение библиотеки с обработкой ошибки, PDF 137. |
| `#!/bin/bash -`, `#!/usr/bin/env bash` | выбор интерпретатора | Shebang определяет механизм запуска сценария, PDF 137–139. |
| `time for ((i=0; i<1000; i++)); do ...; done` | workload-generating | Измерение 1000 запусков; результаты конкретно книжного опыта, не этой среды, PDF 138. |
| `set -euo pipefail` | **state-changing (shell options)** | Режим обработки ошибок; требует проверки совместимости сценария, PDF 139–140. |
| `help set` | read-only | Проверка справки, PDF 140. |
| `exit n`, `return n` | state-changing (flow control) | Завершение сценария / функции со статусом, PDF 141. |
| `trap -l`, `trap -p` | read-only | Список сигналов / обработчиков, PDF 142. |
| `trap Cleanup ABRT EXIT HUP INT QUIT TERM` | **state-changing (trap handlers)** | Регистрирует вызов функции при заданных событиях, не гарантирует выполнение при `kill -9`, PDF 141–142. |
| `set -x`, `bash -x` | state-changing (trace) / workload-generating | Отладочный вывод при исполнении сценария, PDF 141. |
| `cat <<-EoH`, `cat <<'EoF'` | workload-generating / state-changing при перенаправлении | Here-document; `<<-` убирает начальные TAB, кавычки подавляют подстановки. С `> FILE` пример 9.6 пишет файл, PDF 132, 143. |
| `<<<word` | depends on consumer | Here-string; подстановка параметров и команд в выражении может выполняться, PDF 143. |
| `case "$-" in *i*) ...; esac` | read-only / workload-generating | Проверка интерактивного режима по флагам оболочки, PDF 144. |
| `[ -t 1 -a -n "$BASH_VERSION" ]` | read-only | Условие терминала и Bash, PDF 144–145. |

## Безопасность операций и проверка

Прямые команды с `>`, `>>`, `rm` изменяют данные. Их выполнение допускается только после подтверждения фактического пути, владельца, старого содержимого и способа восстановления. `source` способен исполнить любые действия подключаемого файла, которые глава не определяет. `ssh` требует сетевого доступа и отдельного контроля операций на удалённом узле. `trap` меняет реакцию сценария на события, но не гарантирует очистку во всех случаях. [PDF 127–142]

**Rollback:** для удалённых/перезаписанных файлов, параметров оболочки и произвольного импортированного кода не подтверждён исходником. **[Needs confirmation]**. Указанные пути — *буквальные пути книжных примеров*, не пути, рекомендованные для запуска у читателя.
