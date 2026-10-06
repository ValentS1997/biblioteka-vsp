# Commands and tools — глава 6 «Первые шаги»

## Command classification

| Command / snippet | Classification | Effect | Verification | Rollback |
|---|---|---|---|---|
| `python3` | workload-generating | запускает interactive Python interpreter | появляется `>>>` | `exit()`, Ctrl-D; Windows source variant: Ctrl-Z then Enter |
| `print('Hello World')` / source variants | workload-generating | выводит переданный текст в REPL | текст появляется сразу | [Not applicable] |
| `exit()` | state-changing (session) | завершает interactive interpreter | возврат в shell | [Not applicable] |
| `mkdir /tmp/py` | state-changing | создаёт каталог | дальнейший `cd /tmp/py` / сохранение файла | [Needs confirmation] |
| `cd /tmp/py` | state-changing (session) | меняет current working directory | subsequent command context | [Needs confirmation] |
| `python3 helloworld.py` | workload-generating | выполняет Python file | `Привет, Мир!` | [Not applicable] |
| `chmod a+x helloworld.py` | state-changing | добавляет executable mode | `./helloworld.py` | [Needs confirmation] |
| `./helloworld.py` | workload-generating | напрямую запускает executable script | `Привет, Мир!` | [Not applicable] |
| `echo $PATH` | read-only | показывает значение `PATH` | вывод списка каталогов | [Not applicable] |
| `cp helloworld.py /home/swaroop/bin/helloworld` | state-changing | копирует script в source-specific PATH directory | `helloworld` | [Needs confirmation] |
| `helloworld` | workload-generating | запускает script, найденный через `PATH` | `Привет, Мир!` | [Not applicable] |
| `PATH=$PATH:/home/swaroop/mydir` | state-changing (session/config) | дополняет `PATH` source-specific каталогом | `echo $PATH` | [Needs confirmation] |
| `help(print)` | read-only | показывает help для `print` | help text | [Not applicable] |
| `help()` | read-only | открывает help facility | help interface | [Not applicable] |
| `help('return')` | read-only | показывает help для statement name | help text | [Not applicable] |

## Interactive control keys

Source-confirmed:

- GNU/Linux/BSD or IDLE: Ctrl-D exits interpreter;
- Windows command prompt: Ctrl-Z, then Enter;
- help viewer: `q` exits help.

Это keyboard actions, не shell commands.

## Source-confirmed file content

```python
print('Привет, Мир!')
```

Executable Unix variant:

```python
#!/usr/bin/env python3
print('Привет, Мир!')
```

## Source-specific paths

- Windows example: `C:\py`
- GNU/Linux example: `/tmp/py`
- Mac OS X example: `/tmp/py`
- PATH example: `/home/swaroop/bin`
- added PATH directory example: `/home/swaroop/mydir`

Do not replace these with environment-specific values unless independently confirmed.

## Safety / operational notes

- `mkdir`, `chmod`, `cp` and `PATH=...` change state.
- Before using source-specific paths on a real system, their existence/ownership/suitability
  is **[Needs confirmation]**.
- Source provides verification for execution, but not explicit rollback procedures for
  created directories, copied files, permission changes or PATH assignment.
