# Commands and code — глава 13 «Решение задач»

## Execution commands

| Command / operation | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python3 backup_ver1.py` | state-changing / workload | creates first backup ZIP | success message + archive path | [Needs confirmation] |
| generated `zip -qr <target> <sources>` | state-changing external command | recursively writes ZIP archive | command exit status / target archive | [Needs confirmation] |
| `os.system(zip_command)` | state-changing / shell execution | invokes generated external command | source checks result against 0 | [Needs confirmation] |
| `python3 backup_ver2.py` | state-changing / workload | date directory + ZIP | shown directory/archive output | [Needs confirmation] |
| `os.path.exists(today)` | read-only filesystem check | tests date directory | Boolean result | [Not applicable] |
| `os.mkdir(today)` | state-changing filesystem | creates date directory | directory exists | [Needs confirmation] |
| `python3 backup_ver3.py` | negative test | intentionally hits syntax error before backup execution | `SyntaxError: invalid syntax` | [Not applicable] |
| `python3 backup_ver4.py` | state-changing / interactive | fixed backup + optional comment | success path + target archive | [Needs confirmation] |
| `print(zip_command)` | read-only diagnostic | exposes generated shell command | command text printed | [Not applicable] |

## Version 1 — generated command

```python
zip_command = "zip -qr {0} {1}".format(target, ' '.join(source))
```

Source explains:

- `-q` — quiet mode;
- `-r` — recursive mode;
- target archive follows options;
- source files/directories follow target.

The exact expanded command is runtime-dependent; do not invent one without actual
`source` and `target` values.

## Debugging path

Source procedure:

```python
print(zip_command)
```

Then copy the printed command into the shell and test it independently.

This independent command is still state-changing because it can create an archive.

## Version 2

```python
today = target_dir + os.sep + time.strftime('%Y%m%d')
now = time.strftime('%H%M%S')

if not os.path.exists(today):
    os.mkdir(today)

target = today + os.sep + now + '.zip'
```

## Version 3 — intentional failure

Source broken line:

```python
target = today + os.sep + now + '_' +
    comment.replace(' ', '_') + '.zip'
```

Expected source result:

```text
SyntaxError: invalid syntax
```

This is a deliberate negative example, not a candidate working implementation.

## Version 4 — corrected continuation

```python
target = today + os.sep + now + '_' + \
    comment.replace(' ', '_') + '.zip'
```

## Suggested version 5 direction

Source proposes replacing:

```python
os.system(zip_command)
```

with standard-library `zipfile` or `tarfile`.

No version-5 implementation is provided in the chapter. Do not synthesize one into the
canonical chapter artifacts.

## Source-specific paths / dependencies

- `C:\My Documents`
- `C:\Code`
- `E:\Backup`
- `C:\Program Files\GnuWin32\bin`
- external command `zip`

All require **[Needs confirmation]** before real-system use.

## Rollback

The source gives no commands for deleting generated archives/directories or reverting
PATH/dependency installation: **[Needs confirmation]**.
