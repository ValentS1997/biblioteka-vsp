# Cheatsheet — глава 13 «Пользовательское окружение»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0390:c01`–`p0401:c01`, PDF/печатные страницы 390–401. Только `rag_only`.

## Symptom / problem framing

Типовые проблемы главы:

1. команда запускается не из того каталога PATH;
2. environment существует в одном типе shell, но исчезает в другом;
3. login shell и terminal shell читают разные startup files;
4. prompt/alias скрывает реальное поведение команды;
5. `umask` создаёт слишком открытые или слишком закрытые файлы;
6. startup file печатает лишний stdout или ломает GUI/remote session;
7. изменение нужно раздать многим пользователям, но оно не проверено на чистом аккаунте.

Рабочая граница: **startup files — исполняемая политика среды**, а не просто персональная косметика.

## Baseline / context

| Область | Модель главы | PDF |
|---|---|---:|
| Design | Startup files должны быть короткими, простыми и комментированными | 391 |
| PATH | Порядок каталогов определяет приоритет executable | 392–393 |
| MANPATH | Не задавать без необходимости, чтобы не перебить system defaults | 393 |
| Prompt | Показывать только полезный context; избегать shell metacharacters | 393–394 |
| Aliases | Неочевидны и плохо подходят для изменения стандартных команд | 394 |
| `umask` | Default permission boundary for newly created files/dirs | 394–395 |
| Bash login | `/etc/profile` → first of `.bash_profile`, `.bash_login`, `.profile` | 396 |
| Bash non-login | `/etc/bash.bashrc` → `~/.bashrc` in source model | 396 |
| Rollout | Test with clean user across console/remote/GUI paths | 399 |
| Pitfalls | Avoid DISPLAY, terminal type, stdout, LD_LIBRARY_PATH | 400–401 |

## Read-only checks

```sh
echo "$PATH"
echo "$0"
echo "$-"
echo "$PS1"
echo "$EDITOR"
echo "$VISUAL"
echo "$PAGER"
umask
which command
```

File inspection targets from source:

```text
/etc/profile
/etc/bash.bashrc
~/.bash_profile
~/.bash_login
~/.profile
~/.bashrc
~/.tcshrc
~/.cshrc
/etc/manpath.config
```

Interpretation notes:

- In the source, `echo $0` beginning with `-` indicates a login shell.
- The source uses `$-` containing `i` to distinguish interactive shell behavior.
- PATH order matters: the first matching executable wins conceptually.
- Alias visibility does not tell you where it was defined according to the chapter.
- A startup file may interact with distribution-provided files under `/etc`; do not infer ownership from filename alone.

## Interpretation

| Observation | Meaning from chapter | Still unchecked |
|---|---|---|
| Command differs between users | PATH/startup differences are plausible | Exact executable selected and package ownership |
| `echo "$0"` starts with `-` | Source classifies shell as login shell | Whether shell-specific behavior differs on target |
| `$-` contains `i` | Source treats shell as interactive | Which startup file produced current env |
| PATH contains `.` | Current directory participates in command lookup | Immediate exploitability depends on cwd/content |
| `$HOME/bin` precedes system dirs | User executable can override system-name match | Whether this is intended policy |
| `umask` is 077 | New objects default to private permissions | App-specific overrides still possible |
| `umask` is 022 | Others may get read/traverse permission where base mode allows | Actual creator mode still matters |
| Alias changes `ls` | User may see non-default behavior invisibly | Exact alias definition/source file |
| Startup prints text | Can interfere with remote/noninteractive consumers | Which startup path invokes it |
| Environment absent over SSH but present in terminal | Different startup path likely | Exact SSH/login mode [Needs confirmation] |

## Next action

1. Identify shell executable and whether session is login/non-login and interactive/noninteractive.
2. Read only the startup files relevant to that mode.
3. Capture current PATH, key environment variables and `umask`.
4. Make one minimal, commented change.
5. Test a clean session rather than only sourcing the edited file into the current session.
6. For defaults distributed to other users, create a clean test user and exercise every supported login path.
7. If ownership/order of startup files is unclear → **[Needs confirmation]**.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| Assign/export `PATH` | Changes command lookup precedence | Wrong executable can shadow system command |
| Add `$HOME/bin` | Gives user-local programs higher priority | User-controlled replacement of common command names |
| Put `.` in PATH | Runs commands from current directory without `./` | Source strongly discourages: security + inconsistency |
| Set `PS1` | Changes prompt | Metacharacters/paste behavior can confuse shell |
| Define aliases/functions | Changes interactive command behavior | Hidden/nonportable behavior |
| `umask 077` | Restricts default access | Can break collaboration/service readability |
| `umask 022` | Allows read access for others where base mode permits | May be too permissive for sensitive files |
| `. $HOME/.bashrc` | Executes bashrc in current/login shell | Any side effects in bashrc run here too |
| Edit global/default startup files | Changes environment for many users | Error amplification across users |

## Verification / acceptance checks

| Change | Verification | Acceptance |
|---|---|---|
| PATH | new login and non-login shell; inspect PATH and command resolution | Intended directory order, no unexpected shadowing |
| Prompt | open fresh interactive shell | Prompt clear; no shell metacharacter surprise |
| Alias/function | test intended command plus unmodified alternative | Behavior explicit and reversible |
| `umask` | create test file/dir in disposable path, inspect resulting permissions | Matches intended collaboration/privacy model |
| bash startup | test console/login + terminal/non-login + remote path used by environment | Required variables available in each intended mode |
| default-user files | clean user #1, then second clean user with copied defaults | Repeatable behavior without personal-state dependency |
| no-output rule | open remote/noninteractive workflow used by environment | Startup produces no unintended stdout |

## Rollback

- Startup-file edits: save the previous file/content before change; restore it if fresh-session acceptance fails.
- PATH: rollback means restoring previous assignment/order; if the prior value was not captured, **[Needs confirmation]**.
- `umask`: restore prior startup setting; already-created object permissions are not automatically reverted.
- Alias/function: remove/revert the defining line and start a fresh shell.
- Sourced changes affect the current shell immediately; a new shell/session is the clean rollback boundary when individual variable restoration is uncertain.
- Distributed defaults: stop rollout and restore the known-good template before correcting affected users.

## Guardrails

- Do not put `.` in PATH.
- Do not set `DISPLAY` or terminal type in generic shell startup files.
- Do not set `LD_LIBRARY_PATH` there according to the source.
- Do not print to stdout from generic startup files.
- Keep global/default startup files small and commented.
- Prefer wrapper scripts/functions over aliases that silently alter standard command semantics.
- Test defaults as a clean user, not only with an existing customized home directory.
