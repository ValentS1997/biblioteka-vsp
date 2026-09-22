# Шпаргалка: сценарии и командная оболочка

Цель: превратить повторяемую административную операцию из ручной последовательности в проверяемый, воспроизводимый и version-controlled процесс.

## 1. Automation mindset

Основной вопрос главы:

~~~text
Если эта задача повторится — что я автоматизирую?
~~~

Уровни автоматизации:

~~~text
alias / function
    ↓
micro-script
    ↓
shell pipeline
    ↓
sh script
    ↓
Python / Ruby
    ↓
configuration management
~~~

Чем сложнее логика и data model, тем меньше shell подходит как основной язык.

## 2. Shell как композиционная среда

Стандартные streams:

~~~text
0 = STDIN
1 = STDOUT
2 = STDERR
~~~

Базовые конструкции:

~~~bash
command > file
command >> file
command 2> error.log
command1 | command2
command1 && command2
command1 || fallback
~~~

Практический смысл:

- полезный output и errors должны быть разделены;
- commands должны легко соединяться pipeline-ами;
- exit status управляет flow.

## 3. Разработка pipeline перед modifying action

Workflow главы:

~~~text
найти candidates
    ↓
отфильтровать
    ↓
сгенерировать будущие commands
    ↓
вывести их в STDOUT
    ↓
визуально проверить
    ↓
только потом выполнить
~~~

Примерная форма:

~~~bash
find ... | grep -v ... | while read item
do
    echo mv ...
done
~~~

До удаления `echo` или передачи generated commands в shell операция остаётся наблюдаемой, а не изменяющей state.

## 4. Shell script lifecycle

Minimal script:

~~~sh
#!/bin/sh
echo "Hello, world!"
~~~

Подготовка:

~~~bash
chmod +x script
./script
~~~

Или:

~~~bash
sh script
~~~

Выполнение в current shell:

~~~bash
source script
. script
~~~

Использовать `source` только тогда, когда нужен change текущего shell environment.

## 5. Debug и validation

Syntax-only:

~~~bash
bash -n script
~~~

Execution trace:

~~~bash
bash -x script
~~~

Важно: `-x` не делает script безопасным; modifying commands всё равно выполняются.

## 6. Input validation и exit codes

Сценарий должен:

- проверить число arguments;
- проверить expected object type;
- вывести usage при invalid input;
- errors писать в STDERR;
- завершаться с `0` при success;
- возвращать non-zero при failure.

Shell variables главы:

~~~text
$0  script name
$1  first argument
$#  argument count
$*  all arguments
$?  previous command exit status
~~~

## 7. Files with spaces

Quoting:

~~~bash
less "My spacey file"
~~~

Для `find/xargs`:

~~~bash
find ... -print0 | xargs -0 ...
~~~

Это сохраняет filenames как NUL-delimited units вместо whitespace-delimited tokens.

## 8. Core filters

| Tool | Роль |
|---|---|
| `cut` | выбрать fields/columns |
| `sort` | сортировать |
| `uniq` | collapse/count duplicate lines |
| `wc` | count lines/words/chars |
| `tee` | раздвоить STDIN в STDOUT + file |
| `head` | начало stream/file |
| `tail` | конец stream/file |
| `tail -f` | live follow |
| `grep` | regex filtering |

Смысл — не отдельные utilities, а композиция.

## 9. Environment variables

Проверка:

~~~bash
printenv
~~~

Environment inherited child processes и влияет на behavior программ.

Глава приводит `EDITOR`, `PATH`, `HOME` и другие переменные как типичные examples.

Не держать `.` в `PATH`: chapter связывает это с risk запуска чужого executable из writable directory.

## 10. Shell vs regex globbing

Не путать:

~~~text
*.log          shell glob
^foo.*bar$     regular expression
~~~

Shell globbing раскрывает filenames до запуска command.

Regex engine сопоставляет text с pattern.

## 11. Regex reference

Ключевые идеи:

- literal characters;
- `.` — любой character;
- `[...]` — character class;
- `(...)` — group/capture;
- `|` — alternation;
- `*`, `+`, `?`, `{m,n}` — quantifiers;
- `^` / `$` — anchors.

### Greedy vs lazy

Greedy quantifier пытается взять максимально возможный fragment.

Lazy forms:

~~~text
*?
+?
~~~

Chapter предупреждает:

- `.*` требует повышенного внимания;
- large whole-file matching повышает risk expensive backtracking;
- несколько ambiguous groups могут привести к catastrophic backtracking;
- smaller hierarchical matches часто лучше одного гигантского regex.

## 12. Когда shell становится тесен

В главе дана practical boundary:

- shell хорошо подходит для simple command automation;
- при росте script и need for richer structures стоит перейти на Python/Ruby.

Исторически в тексте издания Python рекомендуется как основной general-purpose scripting language для sysadmin work.

## 13. Python — модель главы

Минимальный запуск:

~~~bash
python3 script.py
~~~

Ключевые конструкции:

- indentation определяет blocks;
- `sys.argv` — arguments;
- `os.path.isdir` — example input validation;
- list/dict/file objects;
- `for ... in`;
- module `re` для regular expressions.

Python example flow:

~~~text
parse args
→ validate
→ process structured objects
→ return useful status/output
~~~

## 14. Ruby — модель главы

Ruby также рассматривается как general-purpose scripting language.

Особенности главы:

- everything-as-object style;
- hashes;
- blocks;
- method pipelines;
- built-in regex syntax;
- convenient text-filter mode.

Примеры one-liners:

~~~bash
ruby -pe '...' file
ruby -F: -ane '...' /etc/passwd
~~~

In-place edit:

~~~bash
ruby -i.bak -pe '...' file
~~~

Без backup suffix rollback в этом pattern не обеспечен.

## 15. Python/Ruby dependencies

Python:

~~~text
requirements.txt
pip install -r requirements.txt
pip freeze
virtualenv
~~~

Ruby:

~~~text
Gemfile
Gemfile.lock
Bundler
RVM
~~~

Основной reliability-паттерн:

~~~text
declare dependencies
→ lock/record versions
→ isolate environment
→ reproduce same environment elsewhere
~~~

## 16. virtualenv

Создание:

~~~bash
virtualenv myproject
~~~

Activation:

~~~bash
source myproject/bin/activate
~~~

Exit:

~~~bash
deactivate
~~~

Для cron/system startup chapter советует явно указывать binary из нужного environment, а не зависеть от interactive shell activation.

## 17. Bundler и RVM

Bundler решает recursive dependency constraints и сохраняет result в `Gemfile.lock`.

Deployment:

~~~bash
bundle install --deployment
bundle exec <command>
~~~

RVM управляет Ruby versions + gemsets:

~~~bash
rvm <ruby>@<gemset>
rvm install <version>
rvm list
~~~

Chapter отдельно подчёркивает verification source/signature перед установкой RVM bootstrap script.

## 18. Git — working tree / index / repository

Модель:

~~~text
working tree
    ↓ git add
index
    ↓ git commit
repository history
~~~

Read-only перед commit:

~~~bash
git status
git diff <file>
~~~

Change:

~~~bash
git add .
git commit -m "message"
~~~

`.gitignore` хранится в repository и описывает ignored paths/patterns.

## 19. Git limitations из главы

Git:

- хранит content history;
- отслеживает executable bit;
- не восстанавливает owner/group;
- не является полным backup permission metadata;
- не должен содержать plaintext passwords/secrets.

## 20. Minimal operational workflow

~~~text
Повторяемая задача
  ↓
Сделать вручную один раз
  ↓
Собрать read-only pipeline
  ↓
Проверить output
  ↓
Добавить validation/error handling
  ↓
Выбрать shell или Python/Ruby
  ↓
Зафиксировать dependencies
  ↓
git status / diff
  ↓
commit
  ↓
использовать как reproducible procedure
~~~

## Acceptance criteria

- destructive operation не скрыта внутри непрозрачного pipeline;
- input validation есть до state-changing action;
- STDERR и exit status используются осмысленно;
- filenames со spaces обрабатываются безопасно;
- shell script syntax проверяется отдельно от execution;
- environment dependencies зафиксированы;
- source code находится под version control;
- secrets отсутствуют в Git;
- rollback неизвестного modifying action помечен `[Needs confirmation]`.
