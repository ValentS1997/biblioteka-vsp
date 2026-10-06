# Commands and tools — глава 5 «Установка»

## Command classification

| Command / snippet | Classification | Effect | Verification | Rollback |
|---|---|---|---|---|
| `python -V` | read-only | показывает version information / проверяет доступность команды | сам вывод команды | [Not applicable] |
| `python3 -V` | read-only | показывает version information / проверяет доступность Python 3 command | сам вывод команды | [Not applicable] |
| `cmd` | read-only / environment access | открывает Windows command prompt по source procedure | появление command prompt | [Not applicable] |
| `PATH=%PATH%;C:\Python33` | state-changing configuration | добавляет Python directory к PATH в historical AUTOEXEC.BAT procedure | `python3 -V` | [Needs confirmation] |
| `ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"` | state-changing | по source context устанавливает Homebrew, выполняя загруженный remote content | [Needs confirmation] | [Needs confirmation] |
| `brew install python3` | state-changing | устанавливает Python 3 через Homebrew | `python3 -V` | [Needs confirmation] |

## GNU/Linux / BSD package-manager references

Источник называет:

- `apt-get` для Ubuntu/Debian и Debian-based distributions;
- `yum` для Fedora;
- `pkg_add` для FreeBSD.

Но конкретные install commands/arguments в главе **не приведены**. Не добавлять
`apt-get install ...`, `yum install ...` или `pkg_add ...` из model memory.

## Compile-from-source path

Источник говорит, что Python можно скомпилировать из исходных текстов и установить,
но compile/configure/make commands в главе отсутствуют.

Status: **[Needs confirmation]** для конкретной команды.

## Windows PATH fragments

Source-confirmed fragments:

```text
;C:\Python33
```

и исторический пример:

```text
PATH=%PATH%;C:\Python33
```

Это configuration content, а не универсальные команды для современных Windows.

## Safety note for remote execution

```text
ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"
```

Классификация: **state-changing / remote-code execution pattern**.

По самой структуре команды видно, что `curl` получает удалённый контент, который
передаётся `ruby -e` на выполнение. Source не содержит отдельного шага inspect/verify
перед execution. Поэтому команда сохраняется как исторический source artifact, а не как
безусловная текущая рекомендация.

## Acceptance

После установки/настройки source verification:

```text
python3 -V
```

или, в GNU/Linux/BSD initial check:

```text
python -V
```
