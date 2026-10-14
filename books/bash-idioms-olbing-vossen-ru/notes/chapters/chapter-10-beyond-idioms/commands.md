# Глава 10 — подтверждённые команды, эффекты и риски

**Источник:** PDF 146–174, RAG `p0146:c01–p0174:c01`. Классы: **read-only** — получение сведений; **workload-generating** — запускает вычисления, внешние команды либо вывод; **state-changing** — изменяет окружение, файлы, историю, журнал или поведение оболочки. Класс контекстный; ниже не приводятся новые исполняемые рецепты.

| Форма из RAG | Класс | Эффект и осторожность |
| --- | --- | --- |
| `PS0='Start: ...'` | state-changing (shell) | Изменяет приглашение перед исполнением команды, Bash 4.4+, PDF 148. |
| `export PS1=...`, `export PS4=...`, `export TZ=UTC` | state-changing (shell) | Меняет приглашение, трассировку, часовой пояс для последующих программ, PDF 149–150. |
| `export PROMPT_COMMAND='logger ...'` | **state-changing (logging)** | Автоматический вызов логирования перед приглашением; возможно попадание командной истории и данных в системный журнал, PDF 150. |
| `history -d 5275` | state-changing (history) | Удаляет указанную запись из истории Bash; не гарантирует удаления других копий, PDF 149. |
| `help read`, `help select`, `help history` | read-only / workload-generating | Просмотр справки, PDF 149–151. |
| `read -ei 'default value' -p 'Enter something: '` | state-changing (shell variable) | Запрашивает редактируемый ввод в `REPLY`, PDF 152. |
| `read -sp 'Enter the secret password: '` | state-changing (shell variable) | Скрывает отображение ввода; **не исключает утечки при дальнейшей печати**, как в источнике, PDF 152. |
| `read -n1 -p 'Press any key to continue...'` | state-changing (REPLY/input) | Пауза до символа, PDF 153. |
| `read -t 4 -p 'Are you there?'` | state-changing (REPLY/input) | Ввод с ограничением времени; при тайм-ауте ненулевой статус, PDF 153. |
| `select ssh_target in ...; do case $REPLY ...; done` | state-changing (REPLY) / workload-generating | Меню; книжный пример анализирует конфигурацию SSH и **печатает**, но не исполняет команду `ssh`, PDF 153–154. |
| `alias`, `\unalias`, `case "$HOSTNAME" in ... alias ...` | state-changing (shell namespace) | Определяет или убирает псевдонимы; обратный слеш предотвращает подстановку псевдонима, PDF 154–156. |
| `alias pc='xsel -bi'`, `alias gc='xsel -b'` | state-changing при объявлении; затем clipboard-changing/read-only | Демонстрационные псевдонимы, требуют внешних программ; PDF 155–156. |
| `function mcd` с `\mkdir -p` и `\cd` | **state-changing (filesystem, CWD)** | Создать каталог и перейти в него; исходное экранирование параметра требует сверки в source-findings, PDF 156–157. |
| `IFS=':' read ...` | state-changing (REPLY/fields; temporary env) | Однокомандное присваивание разделителя, PDF 157. |
| `bind` c `history-search-backward`, `menu-complete` | state-changing (Readline) | Меняет привязки клавиш и поведение автодополнения, PDF 158. |
| `export HISTCONTROL=...`, `export HISTIGNORE=...` | state-changing (shell history policy) | Меняет правила сохранения истории; извлечённая строка HISTCONTROL содержит `+` после кавычки — [Needs confirmation], PDF 158–159. |
| `logger --tag "${0##*/}[$$]" <msg>` | **state-changing (system log)** | Пишет сообщение в журнал; `<msg>` — издательский placeholder, **не** готовая shell-команда, PDF 159. |
| `jq '.title' atlas.json`, `jq -r '.title' atlas.json` | workload-generating (read-only input) | Извлечение значения JSON; доступность `jq` может отсутствовать, PDF 160. |
| `jq '.formats | keys' atlas.json`, `jq '.formats.pdf.syntaxhighlighting' atlas.json` | workload-generating (read-only input) | Извлечение ключей и вложенного поля, PDF 160–161. |
| `ps auwx | grep '[p]roggy'`, `pgrep -fl`, `pidof` | read-only / workload-generating | Поиск процессов; рекомендуемое авторами выражение исключает собственный процесс grep, PDF 162. |
| `find /path/to/files ... -ls`, `find ... -print` | read-only / workload-generating | Просмотр кандидатов на ротацию; **перед** удалением, PDF 163. |
| `find /path/to/files \( -type f -a -name 'some-pattern' -a -mtime 5 \) -delete` | **state-changing (filesystem)** | Рекурсивное удаление совпавших файлов. Нужна проверка глубины и имён, rollback [Needs confirmation], PDF 163–164. |
| `find ... -print0 | xargs -0 rm -f` | **state-changing (filesystem)** | Альтернативная идиома удаления, обрабатывающая пробелы в именах; PDF 162–163. |
| `pandoc README.md > /tmp/README.html && firefox file:///tmp/README.html` | state-changing / workload-generating | Перезаписывает файл HTML и открывает браузер, PDF 164. |
| `: << 'DOCS'` | read-only в показанном контексте | Here-doc как встроенная документация, не выполняемая Bash; текст можно извлекать отдельно, PDF 165–170. |
| `perl -ne` из примера `--emit-docs` | workload-generating | Извлекает блоки документации по маркерам; сложная regex в источнике, PDF 165, 169. |
| `bash -n /path/to/script` | **read-only** | Синтаксическая проверка без выполнения команд, PDF 171. |
| `bash -v /path/to/script`, `set -v` | workload-generating / state-changing | Печать читаемых строк; `set -v` меняет режим текущей оболочки, PDF 171. |
| `bash -x /path/to/script`, `set -x`, `set +x` | **workload-generating / state-changing** | Выполняет и трассирует команды; возможны утечки аргументов, токенов, переменных; выключение `set +x` не стирает старый вывод, PDF 171–172. |
| `env`, `printenv`, `set` для просмотра окружения | read-only / workload-generating, **sensitive output** | Могут раскрыть секретные значения; исходник упоминает Perl-фильтрацию, но это не гарантия защиты, PDF 172. |
| `bash --debugger` | workload-generating | Отладчик может отсутствовать или быть несовместим, PDF 173. |

## Проверка и обратимость

- Перед удалением: запускать **только source-confirmed** `find` с `-ls`/`-print` вместо `-delete`, сверять критерии `-mtime`, `-type f`, `-name` и глубину `-maxdepth`. Подтверждённого общего rollback для удалённого файла нет. [PDF 163–164]
- Перед `PROMPT_COMMAND`/`logger`, трассировкой и выдачей окружения: определить, какие сведения попадут в логи, и кто будет иметь к ним доступ. **Нельзя демонстрировать реальные секреты**. [PDF 150, 152, 171–172]
- Для обновления истории, Readline и псевдонимов сохранить исходную конфигурацию и отдельно проверить эффект. Источник не предоставляет универсальных команд восстановления: **[Needs confirmation]**.
- Никаких реальных каталогов, удалений, SSH-сессий, системных журналов и других state-changing операций при подготовке анализа не выполнялось.
