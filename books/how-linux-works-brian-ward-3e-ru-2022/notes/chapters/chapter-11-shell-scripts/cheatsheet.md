# Cheatsheet — глава 11 «Сценарии оболочки»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0344:c01`–`p0367:c01`, PDF/печатные страницы 344–367. Только `rag_only`.

## Symptom / problem framing

Глава помогает разбирать короткие automation scripts, где ошибка обычно возникает в одной из областей:

1. интерпретатор/shebang и execute/read permissions;
2. quoting/expansion и неожиданные аргументы;
3. positional parameters и специальные переменные;
4. неправильная интерпретация exit status;
5. условные конструкции/циклы;
6. временные файлы и cleanup;
7. pipeline/text-processing complexity;
8. неожиданное изменение текущей shell environment через sourcing/exec.

Основной вопрос главы: **остаётся ли задача простой композицией команд, или shell уже стал неподходящим инструментом?**

## Baseline / context

| Объект | Модель главы | PDF |
|---|---|---:|
| Shebang | Первая строка выбирает interpreter, например `#!/bin/sh` | 344–345 |
| Permissions | Script должен быть читаем interpreter-ом и executable для direct launch | 345 |
| Expansion | Shell обрабатывает variables/globs/substitution до запуска команды | 346–348 |
| Positional args | `$1`, `$2`, `$#`, `$@`, `$0` | 349–350 |
| Process/status | `$$` = shell PID; `$?` = last command status | 351 |
| Tests | `[`/`test` возвращает status для `if`/`while` | 352–357 |
| Loops | `for`, `while`, `until`, `break` | 358–359 |
| Command substitution | `$(...)` injects stdout into shell parsing context | 359–360 |
| Temp files | `mktemp` + `trap` | 360–361 |
| Text helpers | basename, awk, sed, xargs, expr | 362–365 |
| Process context | `exec`, subshell `(...)`, sourcing `.` | 365–367 |
| Input | `read var` | 367 |

## Read-only checks

Source-grounded checks that inspect behavior without intentionally changing persistent system state:

```sh
echo "$?"
echo "$#"
echo "$0"
echo "$$"
test -f file
[ -e file ]
[ -s file ]
[ -r file ]
[ -w file ]
[ -x file ]
basename /usr/local/bin/example
ls -l | awk '{print $5}'
sed 's/:/%/' /etc/passwd
sed 's/:/%/g' /etc/passwd
sed 3,6d /etc/passwd
find . -name '*.gif' -print
```

Interpretation caveats:

- `$?` must be read/saved immediately after the command being tested; the next command overwrites it.
- `grep`/ `diff` may use nonzero status for normal conditions; consult their documented EXIT VALUE/DIAGNOSTICS semantics.
- Shell expansion happens before the target command receives arguments.
- `[` is treated as a command interface in the chapter; spaces/argument boundaries matter.

## Interpretation

| Observation | Meaning in chapter | Still unchecked |
|---|---|---|
| Script runs via `./script` | Shebang/permissions/path are sufficient for that invocation | Portability to other systems/interpreters |
| `echo '$100'` prints literal text | Single quotes suppress shell expansion | Embedded single quotes need separate handling |
| `echo "$PATH"` expands variable | Double quotes allow variable expansion | Other shell-specific expansion behavior |
| `$# = 0` | No positional args remain | Whether missing args should be error/default |
| `$? = 0` | Previous command reported success/true | Program-specific meaning must be known |
| `$? != 0` after grep | Could mean “no match”, not necessarily execution failure | Exact grep status semantics |
| `[ -f file ]` succeeds | Target resolves as regular file | Whether symlink itself vs target matters |
| Major script complexity grows | Shell may be wrong implementation language | Migration target/design [Needs confirmation] |
| Temp files remain after Ctrl+C | Script lacks or failed cleanup path | Exact interrupted code path |
| Sourced file changes variables | Commands ran in current shell | Whether source file is trusted |
| `exec` returns no shell | Current shell process was replaced | Recovery is via parent/session, not same shell |

## Next action

1. Confirm interpreter and invocation path.
2. Reproduce the exact expansion/quoting boundary.
3. Capture positional args and expected status semantics.
4. For conditionals, reduce the condition to the command that produces the status.
5. For temporary files, verify creation **and** interrupt cleanup.
6. For filename pipelines, use a representation that survives spaces/newlines when source provides one.
7. If the script needs repeated complex parsing/arithmetic/control flow, stop expanding shell complexity and consider Python/awk/etc.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| `chmod +rx script` | Adds read/execute permissions according to current mode rules | May broaden who can read/run script |
| `chmod 700 script` | Restricts source example to owner rwx | Changes access mode |
| `shift` | Drops first positional arg and renumbers remaining args | Irreversible within current argument list |
| `exit 1` | Terminates script with nonzero status | Stops remaining commands |
| `mktemp ...` | Creates unique temporary file | Cleanup still required |
| `trap "...; exit 1" INT` | Installs signal cleanup handler | Handler content itself becomes control path |
| `rm -f $TMPFILE1 $TMPFILE2` | Removes temporary files | Wrong expansion/value can delete wrong target |
| `exec command` | Replaces current shell process | **Irreversible in that process** |
| `. config.sh` | Executes file in current shell | Imported code can alter current environment/state |
| `read var` | Reads interactive/stdin input into variable | Input validation still required |

## Verification / acceptance checks

| Change | Verification from source model | Acceptance |
|---|---|---|
| Script permission | direct invocation succeeds as intended | Correct user can run; unintended exposure reviewed |
| Quoting fix | command receives intended literal/expanded arguments | No wildcard/word-splitting surprise |
| Conditional | force both true/false test cases | Correct branch chosen from status |
| Exit handling | inspect parent-visible `$?` immediately | Intended zero/nonzero status |
| Temp-file handling | normal run + interrupted run | No stale temp files after cleanup path |
| xargs/find path handling | test filenames with spaces/newlines conceptually supported by `-print0 | xargs -0` | File boundaries remain intact |
| Sourcing | inspect expected variables/environment afterward | Only intended current-shell changes remain |
| exec | run only in disposable shell/process context | Replacement behavior is intended |

## Rollback

- Permission changes: previous mode must be captured before modification; exact inverse depends on that prior mode → **[Needs confirmation]** if not recorded.
- `shift`: original positional list is not restored automatically; preserve inputs before destructive argument manipulation if needed.
- Temp files: cleanup is explicit `rm`; if path variables are wrong, there is no generic rollback.
- `exec`: no rollback inside the replaced shell process; use a new/parent shell.
- Sourcing: no automatic rollback of variables/functions/current directory; use a subshell when isolation is required.
- File transformations shown with `sed` write to stdout in the source examples; persistent file-edit rollback is therefore outside this chapter's concrete commands.

## Guardrails

- Prefer single quotes for full literals when no expansion is needed.
- Treat every unquoted expansion as a possible argument-boundary/globbing change.
- Do not assume nonzero exit status always means “error”.
- Use `mktemp` rather than predictable `/tmp` names.
- Use `trap` for interrupted cleanup where temp resources matter.
- Prefer `find ... -print0 | xargs -0 ...` over newline-separated filenames when source examples require arbitrary filenames.
- If a shell script becomes long or parsing-heavy, the chapter explicitly recommends changing tools rather than adding more shell complexity.
