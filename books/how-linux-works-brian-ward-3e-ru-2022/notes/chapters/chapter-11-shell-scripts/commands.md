# Команды и конструкции — глава 11 «Сценарии оболочки»

**Provenance:** `p0344:c01`–`p0367:c01`, PDF/печатные страницы 344–367. Только явно поддержанные chapter RAG команды/constructs.

Классы: **RO** — observation/read-only; **WG** — workload-generating / execution; **SC** — state-changing.

## 1. Script execution / permissions

| Команда / construct | Класс | Назначение | PDF |
|---|---|---|---:|
| `#!/bin/sh` | execution metadata | Select `/bin/sh` interpreter | 344–345 |
| `#!/usr/bin/env python` | execution metadata | Find interpreter through current command path | 345 |
| `chmod +rx script` | SC | Add read/execute permission bits per source example | 345 |
| `chmod 700 script` | SC | Owner-only rwx mode example | 345 |
| `./script` | WG | Run script from current directory | 345 |

The source warns that an `env` shebang uses the first matching executable in the current command path, which may be unintended.

## 2. Quoting / literals

Source examples:

```sh
echo '$100'
grep 'r.*t' /etc/passwd
echo "There is no * in my path: $PATH"
echo I don\'t like contractions inside shell scripts.
echo "I don't like contractions inside shell scripts."
```

Semantics:
- single quotes: no variable/glob expansion inside;
- double quotes: variable expansion occurs, wildcard `*` remains literal in the demonstrated context;
- backslash can escape a quote outside single-quoted text.

## 3. Special variables / positional args

| Construct | Meaning |
|---|---|
| `$1`, `$2`, ... | Positional arguments |
| `$#` | Number of arguments |
| `$@` | All arguments |
| `$0` | Script name |
| `$$` | Shell PID |
| `$?` | Exit status of last command |
| `shift` | Drop `$1`, renumber remaining positional args |

Source example for stderr output:

```sh
echo $0: bad option $BADPARM 1>&2
```

## 4. Exit status / termination

```sh
ls / > /dev/null
echo $?
ls /asdfasdf > /dev/null
echo $?
exit 1
```

Operational rule from source: use/save `$?` immediately, because the next command overwrites it.

The chapter explicitly notes that `grep` and `diff` can use nonzero status for ordinary non-match/difference conditions and reserve another nonzero status for actual problems.

## 5. Conditional control flow

Source constructs:

```sh
if [ "$1" = hi ]; then
    ...
else
    ...
fi

elif ...

command1 && command2
command1 || command2

if [ ! "$1" = hi ]; then
    ...
fi
```

The chapter presents `[` as the `test` command interface and emphasizes spaces/argument boundaries.

### File tests

| Operator | Meaning |
|---|---|
| `-e` | Exists |
| `-s` | Exists and non-empty |
| `-f` | Regular file |
| `-d` | Directory |
| `-h` | Symbolic link |
| `-b` | Block device |
| `-c` | Character device |
| `-p` | Named pipe |
| `-S` | Socket |
| `-r` | Readable |
| `-w` | Writable |
| `-x` | Executable |
| `-u` | Setuid |
| `-g` | Setgid |
| `-k` | Sticky bit |
| `-nt` | First file newer than second |
| `-ot` | First file older than second |
| `-ef` | Same device+inode |

### String tests

- `=`, `!=`
- `-z string`: empty
- `-n string`: non-empty

### Numeric tests

- `-eq`, `-ne`, `-lt`, `-gt`, `-le`, `-ge`

## 6. `case`

Source pattern:

```sh
case $1 in
    bye)
        ...
        ;;
    hi|hello)
        ...
        ;;
    what*)
        ...
        ;;
    *)
        ...
        ;;
esac
```

The chapter emphasizes `;;` termination for each branch.

## 7. Loops

```sh
for str in one two three four; do
    echo $str
done

while command; do
    ...
done

break
```

The source also names `until`: it repeats until the tested command returns zero.

## 8. Command substitution

Preferred source syntax:

```sh
FLAGS=$(grep ^flags /proc/cpuinfo | sed 's/.*://' | head -1)
```

Traditional backticks are described as older syntax. The chapter discourages `$(ls)` for filename iteration and recommends globbing / `xargs` / `find -exec` instead.

## 9. Temporary files / signals

```sh
TMPFILE1=$(mktemp /tmp/im1.XXXXXX)
TMPFILE2=$(mktemp /tmp/im2.XXXXXX)
trap "rm -f $TMPFILE1 $TMPFILE2; exit 1" INT
rm -f $TMPFILE1 $TMPFILE2
```

`mktemp` creates unique temporary files from the template. Without a template, source says it uses a `/tmp/tmp` prefix.

The trap handler must explicitly `exit` if the script should stop after the signal.

## 10. Here-document

```sh
DATE=$(date)
cat <<EOF
Date: $DATE
...
EOF
```

The source says variables are expanded inside the shown here-document form.

## 11. basename / awk / sed

```sh
basename example.html .html
basename /usr/local/bin/example
ls -l | awk '{print $5}'
sed 's/exp/text/'
sed 's/:/%/' /etc/passwd
sed 's/:/%/g' /etc/passwd
sed 3,6d /etc/passwd
sed '/exp/d'
```

In all shown `sed` examples, output goes to stdout; no in-place editing command is supplied.

## 12. xargs / find

Source safer form for arbitrary filenames:

```sh
find . -name '*.gif' -print0 | xargs -0 file
```

Less robust source example:

```sh
find . -name '*.gif' -print | xargs file
```

Alternative:

```sh
find . -name '*.gif' -exec file {} \;
```

The chapter explicitly warns that newline-separated `xargs` can fail or become unsafe with spaces/newlines in filenames.

## 13. expr

```sh
expr 1 + 2
expr --help
```

The chapter characterizes `expr` as awkward/slow for repeated mathematics and recommends another language when arithmetic becomes common.

## 14. exec

```sh
exec cat
```

**Class: SC process state / irreversible in current shell.**

`exec` replaces the current shell process with the target program. When the target exits, that shell no longer exists.

## 15. Subshells / temporary environment

```sh
(cd uglydir; uglyprogram)
(PATH=/usr/confusing:$PATH; uglyprogram)
PATH=/usr/confusing:$PATH uglyprogram
```

Subshell changes disappear when the subshell exits. The one-command environment assignment form avoids creating a subshell for that use case.

The source also shows a `tar | (cd target; tar ...)` tree-copy example, but the extracted archive-option token contains a malformed dash; see `source-findings.md`.

## 16. Sourcing

```sh
. config.sh
```

**Class: SC current-shell environment/code execution.**

Sourcing runs commands from the file in the current shell, unlike executing a separate script.

## 17. User input

```sh
read var
```

`read` stores one line from stdin in the named variable and can support prompts/confirmation flows.

## Command discipline

- Quote expansion when argument boundaries must be preserved.
- Treat `$?` as ephemeral: read/save it immediately.
- Prefer `mktemp` + `trap` for temporary resources.
- Treat `exec` and sourcing as process/environment control boundaries.
- Do not invent modern shell options/linting commands absent from chapter RAG.
- When shell complexity grows, the source explicitly recommends switching tools/languages.
