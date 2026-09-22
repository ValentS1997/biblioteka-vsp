# Команды главы 7

Только команды и формы команд, подтверждённые RAG главы 7.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `set -o vi` | Переключить shell line editing в vi mode | editing mode изменился | state-changing |
| `set -o emacs` | Вернуть emacs-style shell editing | editing mode изменился | state-changing |
| `printenv` | Показать environment variables | PATH, EDITOR, HOME и др. | read-only |
| `grep bash /etc/passwd > /tmp/bash-users` | Пример STDOUT redirection в файл | файл создан с ожидаемыми строками | state-changing / output-generating |
| `sort < /tmp/bash-users` | Прочитать STDIN из файла и отсортировать | sorted output | read-only |
| `find / -name core 2> /dev/null` | Отделить STDERR от полезного STDOUT | permission errors suppressed, matches visible | read-only |
| `find / -name core > /tmp/corefiles 2> /dev/null` | Разделить useful output и errors | result file contains matches | output-generating |
| `find / -name core 2> /dev/null \| less` | Передать stdout поиска в pager | pipeline result | read-only |
| `ps -ef \| grep httpd` | Фильтровать process list | matching process lines | read-only |
| `cut -d: -f7 < /etc/passwd \| sort -u` | Получить unique shells из passwd | unique sorted field list | read-only |
| `mkdir foo && cd foo` | Выполнить вторую команду только после успешной первой | directory created, cd executed only on success | state-changing |
| `cd foo \|\| echo "No such directory"` | Выполнить fallback только после failure | failure handling | state-changing/read-only mix |
| `mkdir foo; cd foo; touch afile` | Выполнить последовательность независимо от previous status | все команды выполняются по порядку | state-changing |
| `source <file>` / `. <file>` | Выполнить shell file в текущем shell | environment/current-shell state изменён ожидаемо | state-changing |
| `sh <script>` | Выполнить sh-script в новом shell process | exit status/output | state-changing depending on script |
| `chmod +x <script>` | Сделать script executable | execute bit set | state-changing |
| `./<script>` | Выполнить executable script из current directory | expected output/exit status | state-changing depending on script |
| `bash -x <script>` / `sh -x <script>` | Показать commands перед выполнением | trace output соответствует control flow | workload-generating / may change state |
| `bash -n <script>` | Проверить shell syntax без выполнения | zero/nonzero syntax result | read-only |
| `find . -type f -name '*.log'` | Найти regular files по pattern | selected paths | read-only |
| `find ... \| grep -v <pattern>` | Исключить нежелательные paths из pipeline | final candidate set | read-only |
| `find ... -print0 \| xargs -0 ...` | NUL-safe processing filenames со spaces | filenames не split по whitespace | depends on final command |
| `echo` | Простой shell output | produced text | read-only |
| `printf` | Форматированный output | formatting/newlines/tabs | read-only |
| `read <var>` | Получить input в shell variable | variable value | state-changing in shell state |
| `cut` | Выделить fields/columns | selected fields | read-only |
| `sort -t: -k3,3 -n /etc/group` | Numeric sort по третьему field | numeric ordering | read-only |
| `du -sh /usr/* \| sort -h` | Human-readable size sort | sizes ordered correctly | workload-generating / read-only |
| `cut -d: -f7 /etc/passwd \| sort \| uniq -c` | Count duplicated shell values | counts per unique line | read-only |
| `wc /etc/passwd` | Count lines/words/chars | counts | read-only |
| `tee <file>` | Копировать STDIN одновременно в STDOUT и file | both outputs receive data | output-generating |
| `head <file>` | Показать начало file | first lines | read-only |
| `tail <file>` | Показать конец file | last lines | read-only |
| `tail -f <file>` | Follow appended lines | live additions | read-only / long-running |
| `grep -c <pattern> <file>` | Count matching lines | match count | read-only |
| `grep -i <pattern> <file>` | Case-insensitive matching | expected matches | read-only |
| `grep -v <pattern> <file>` | Invert matching | nonmatching lines | read-only |
| `grep -l <pattern> <files...>` | Показать names файлов с match | matching filenames | read-only |
| `tail -f <log> \| grep --line-buffered <pattern>` | Live filtered log stream | matches appear without grep buffering delay | read-only / long-running |
| `sudo pkg install bash` | FreeBSD: установить bash | package installed | state-changing |
| `chsh` | Изменить login shell | shell field changed as intended | state-changing |
| `python3 <script> [args]` | Выполнить Python 3 script | output/exit status | state-changing depending on script |
| `ruby -pe '<expr>' <file>` | Использовать Ruby как line filter с auto-print | transformed output | read-only |
| `ruby -F: -ane '<expr>' /etc/passwd` | Split input fields and process as filter | selected transformed fields | read-only |
| `ruby -i.bak -pe '<expr>' <file>` | In-place Ruby edit с backup suffix | original backup + modified file | state-changing |
| `gem search <term>` | Искать Ruby gem | matching packages | read-only / network |
| `gem install <package>` | Установить Ruby gem | gem/dependencies installed | state-changing / network |
| `gem install <package> --user-install` | Установить gem в user scope | package installed outside system gem set | state-changing / network |
| `pip search <term>` | Искать Python package, как описано в главе | matching packages | read-only / network |
| `pip install <package>` | Установить Python package и basic dependencies | package installed | state-changing / network |
| `pip install --user <package>` | User-scope Python package install | package installed in user environment | state-changing / network |
| `pip install -r requirements.txt` | Установить dependency set из file | requested versions installed | state-changing / network |
| `pip freeze` | Вывести current Python packages в requirements format | exact package/version list | read-only |
| `gem install bundler` | Установить Bundler | bundler available | state-changing / network |
| `bundle` / `bundle install` | Разрешить и установить Ruby dependencies | Gemfile.lock/environment state | state-changing / network |
| `bundle install --deployment` | Установить deployment dependencies локально для project | isolated deployment package set | state-changing / network |
| `bundle exec <command>` | Запустить command в Bundler-managed environment | expected dependency context | state-changing depending on command |
| `virtualenv <path>` | Создать isolated Python environment | environment directory/bin created | state-changing |
| `source <venv>/bin/activate` | Активировать virtualenv в current shell | PATH points to venv tools | state-changing in shell state |
| `deactivate` | Выйти из active virtualenv | shell PATH restored | state-changing in shell state |
| `rvm <ruby>@<gemset>` | Активировать Ruby version + gemset | ruby/gem resolve to requested context | state-changing in shell state |
| `rvm install <ruby-version>` | Установить Ruby version через RVM | requested version available | workload-generating / state-changing |
| `rvm list` | Показать installed/available RVM Rubies | version inventory | read-only |
| `git init` | Создать repository metadata | `.git` created | state-changing |
| `git add .` | Скопировать working-tree state в index, кроме ignored paths | staged set | state-changing |
| `git commit -m "<message>"` | Зафиксировать index в repository | new commit created | state-changing |
| `git commit <file> -m "<message>"` | Commit selected tracked file changes directly | only intended file included | state-changing |
| `git commit -a` | Auto-stage modified tracked files and commit | new files are not included | state-changing |
| `git status` | Показать tracked/untracked/staged state | intended change set | read-only |
| `git diff <file>` | Показать unstaged changes | exact diff | read-only |
| `echo tmpfile >> .gitignore` | Добавить path/pattern в ignore rules | file now ignored after rule is committed/applied | state-changing |

## Shell scripting safety rules из главы

- Проверять input и output до destructive operations.
- Usage errors отправлять в STDERR.
- Возвращать exit code `0` при успехе и ненулевой при failure.
- До реального batch change сначала выводить generated commands и визуально проверять.
- Не использовать setuid для administrative scripts; privilege control строить через `sudo`.
- Не помещать current directory `.` в PATH: chapter предупреждает о command-trap risk.
- Для filenames с spaces использовать quoting или NUL-safe `find -print0 | xargs -0`.
- `bash -n` — syntax check; `-x` выполняет script и поэтому не является read-only.
- `ruby -i` изменяет файл на месте; backup suffix нужен, если требуется сохранить исходник.
- Не включать plaintext passwords/secrets в Git repository.
- Git отслеживает executable bit, но не является backup-механизмом ownership и обычных permission bits.

## Rollback

- Для generated shell batch operations rollback зависит от самой операции: `[Needs confirmation]`.
- In-place Ruby edit с `-i.bak` оставляет backup в показанном chapter workflow.
- Git хранит историю content и позволяет возвращаться к known-good versions концептуально, но конкретные rollback-команды в этой части главы не приведены: `[Needs confirmation]`.
