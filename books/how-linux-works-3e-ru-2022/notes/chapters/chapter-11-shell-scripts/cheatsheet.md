# Шпаргалка: сценарии оболочки по главе 11

## Symptom / problem framing

Типовые проблемы:

- script не запускается;
- shell неожиданно подставляет variable/glob;
- positional parameter пустой;
- condition идёт не в ту branch;
- return code теряется;
- loop не завершается;
- temp files остаются после Ctrl+C;
- filenames с spaces/newlines ломают pipeline;
- environment change протекает наружу;
- sourced file меняет current shell;
- script стал слишком сложным для shell.

## Baseline / context

Source-derived execution model:

```text
script file
   ↓
shebang chooses interpreter
   ↓
shell parses / expands / redirects
   ↓
commands execute
   ↓
return codes drive control flow
```

Core special variables:

```text
$1 $2 ...  individual arguments
$#         argument count
$@         all arguments
$0         script name
$$         shell PID
$?         last command return code
```

## Read-only checks

### Inspect script and interpreter

```bash
ls -l <script>
head <script>
```

Source does not provide these exact diagnostic commands as a formal workflow, so only the permission/shebang concepts are canonical; use repository artifact examples as syntax reference.

### Check return code immediately

```bash
<command>
echo $?
```

Do not run unrelated commands before reading `$?`; the next command overwrites it.

### Test syntax concepts

```sh
[ -f <file> ]
[ -d <dir> ]
[ -e <path> ]
[ -s <file> ]
[ -r <file> ]
[ -w <file> ]
[ -x <file> ]
[ -z "$var" ]
[ -n "$var" ]
[ "$a" = "$b" ]
[ "$a" != "$b" ]
[ "$a" -eq "$b" ]
```

Numeric comparisons use `-eq/-ne/-lt/-gt/-le/-ge`, not string `=`.

## Interpretation

### Quoting

Single quotes:
- preserve text literally for shell parsing.

Double quotes:
- preserve grouping;
- still allow variable expansion.

Backslash:
- escapes individual shell-special characters in examples.

Defensive rule from source: quote potentially empty parameters such as `"$1"` in tests.

### Return codes

`0` usually means success.

Nonzero is command-specific. Example:
- `grep` 0 → match;
- `grep` 1 → no match;
- `grep` 2 → actual error.

### Conditions

`if` executes a command and uses its return code.

```sh
if command; then
    ...
else
    ...
fi
```

`&&` runs the second command after success.  
`||` runs it after failure.  
`!` negates a condition.

### case

Use `case` for string/pattern dispatch rather than long `elif` chains.

Each branch ends with `;;`.

### Loops

`for` is the normal shell loop over words/files.

`while` repeats while condition command returns success.

`until` reverses the termination condition.

Source warns that complex loop-heavy scripts are a sign to consider Python/awk.

### Command substitution

```sh
VAR=$(command)
```

Use `$(...)` rather than legacy backticks for readability.

Do not use `$(ls)` when glob expansion can do the job.

### Temporary files

```sh
TMP=$(mktemp /tmp/name.XXXXXX)
trap "rm -f $TMP; exit 1" INT
```

Use `mktemp` for unique names and `trap` for cleanup on interrupt.

### xargs / find

Unsafe pattern from source:

```bash
find . -name '*.gif' -print | xargs file
```

Safer source form for spaces/newlines:

```bash
find . -name '*.gif' -print0 | xargs -0 file
```

Alternative:

```bash
find . -name '*.gif' -exec file {} \;
```

### Subshell vs sourcing

Subshell:

```sh
(cd <dir>; <command>)
```

Environment changes disappear after subshell exits.

Sourcing:

```sh
. config.sh
```

Runs commands in current shell and can change current variables/definitions.

## Next action

1. Confirm interpreter/shebang and permissions.
2. Reduce quoting/expansion ambiguity.
3. Inspect return code immediately.
4. Simplify condition into one command/test.
5. For files, use file tests rather than complex parsing.
6. For temp files, add `mktemp` + cleanup handler.
7. For filename lists, use NULL-delimited `find/xargs` pattern.
8. If control flow/string/arithmetic becomes complex, move to a better-suited language.

## Modifying action

Source-confirmed modifying examples include:

```bash
chmod +rx <script>
chmod 700 <script>
rm -f <temp-files>
```

And shell/process actions:

```sh
exit 1
shift
exec <program>
. <file>
read <var>
```

Examples that write data include redirects such as `> <file>`, `>> <file>`, generated conversion output and tar extraction.

## Verification / acceptance checks

| Action/change | Verification |
|---|---|
| script permission | inspect resulting mode and execute expected script path |
| argument handling | run with known positional arguments |
| condition | check expected branch + return code |
| temp-file creation | confirm unique temp file and cleanup |
| trap cleanup | interrupt controlled test and confirm temp files are gone |
| command substitution | inspect variable/output value |
| subshell | confirm parent cwd/environment unchanged |
| sourcing | confirm intended variable/definition appears in current shell |
| exec | confirm process is replaced as intended |
| xargs/find | verify filenames with spaces/newlines are handled correctly |

## Rollback

- `chmod +rx` / `chmod 700` → restore previous mode only if baseline was captured; otherwise `[Needs confirmation]`.
- File redirects/conversions/extraction → rollback depends on previous destination contents: `[Needs confirmation]`.
- `rm -f` → deletion is not generically reversible: `[Needs confirmation]`.
- `exit` → no rollback inside terminated script.
- `exec` → no rollback inside replaced process; source calls this irreversible.
- Sourced variable/environment changes → restore previous values only if captured; otherwise `[Needs confirmation]`.
- Subshell changes normally disappear automatically when subshell exits.
