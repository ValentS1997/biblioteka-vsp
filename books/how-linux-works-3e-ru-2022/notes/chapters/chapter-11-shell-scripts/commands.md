# Команды и интерфейсы главы 11

Только команды, constructs и utilities, явно подтверждённые RAG главы 11.

| Команда / конструкция | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `#!/bin/sh` | Select Bourne/POSIX-style shell interpreter | execution metadata | Kernel starts interpreter for script | Wrong interpreter changes semantics | Run script with known input | Edit script back from known-good content |
| `#!/usr/bin/env python` | Find interpreter through current PATH | execution metadata | `env` selects first matching executable in PATH | Source warns first match may be unintended | `[Needs confirmation]` | Restore previous shebang |
| `chmod +rx <script>` | Add read/execute permissions | state-changing | Changes file mode, including access for other users | May make script readable/executable more broadly than intended | Check resulting mode + execute | Restore previous mode if baseline known; otherwise `[Needs confirmation]` |
| `chmod 700 <script>` | Owner-only rwx mode example | state-changing | Restricts mode to owner rwx | Changes prior permissions | Check resulting mode | Restore previous mode if known |
| `./<script> ...` | Execute script in current directory | workload-generating | Starts interpreter/process | Script effects depend on contents | Return code/output | Script-specific |
| `shift` | Drop `$1` and shift remaining args | shell-state-changing | Rewrites positional parameter view | Original positional ordering is lost inside current script | Inspect following `$1/$#` | `[Needs confirmation]` |
| `echo $?` | Read previous command return code | read-only | Prints current `$?` but then updates it to echo's status | Must be read immediately | Observe value | N/A |
| `exit 1` | Terminate script with nonzero status | state-changing/process-control | Ends current script | Remaining cleanup/work is skipped unless already handled | Parent sees exit status | No rollback inside terminated script |
| `[ "$1" = hi ]` / `test ...` | Condition command | read-only | Returns status based on test | Unquoted empty args may break syntax | Check exit status/branch | N/A |
| `&&` / `||` / `!` | Return-code-based logical control | control-flow | Selects later command execution | Misread command-specific status semantics | Verify branch/outcome | N/A |
| `case ... esac` | Pattern-based string dispatch | control-flow | Selects matching branch | Missing `;;` may cause syntax error | Run representative inputs | N/A |
| `for ... do ... done` | Iterate over values | control-flow | Repeats body for values | Expansion/quoting affects values | Test representative list | N/A |
| `while ... do ... done` | Loop while condition command succeeds | control-flow | Repeats body based on return code | Can loop unexpectedly | Controlled test + termination condition | N/A |
| `break` | Exit loop | control-flow | Stops current loop | May skip remaining body work | Observe post-loop flow | N/A |
| `$(command)` | Command substitution | workload-generating | Captures stdout into shell expression | Overuse can mishandle filename lists/large output | Inspect expanded value | N/A |
| `mktemp /tmp/name.XXXXXX` | Create unique temp file | state-changing | Creates empty temporary file with unique suffix | Temp files remain if cleanup is missed | Check returned path/file | `rm -f <temp>` |
| `rm -f <temp...>` | Remove temp files | state-changing/destructive | Deletes target files | Wrong variable/path deletes unintended files | Confirm intended files absent | Not generically reversible |
| `trap "rm -f ...; exit 1" INT` | Cleanup handler for interrupt | shell-state-changing | Installs signal handler in shell | Bad variable expansion/handler may remove wrong files | Controlled interrupt test | Handler state rollback `[Needs confirmation]` |
| Here-doc `<<EOF ... EOF` | Feed block text to stdin | redirection/control | Supplies multi-line stdin; variables expand in shown form | Unexpected expansion can alter content | Inspect consumer output | N/A |
| `basename <path> [suffix]` | Strip directory/suffix | read-only | Prints transformed name | None | Compare output | N/A |
| `awk '{print $5}'` | Select field from input | read-only/workload-generating | Parses input and prints field | Field positions depend on input format | Inspect output | N/A |
| `sed 's/exp/text/'` | Stream substitution | read-only/workload-generating | Reads input, writes transformed stdout | Without redirect it does not modify source file in chapter examples | Compare stdout/source | N/A |
| `sed 's/:/%/g' /etc/passwd` | Global substitution to stdout | read-only/workload-generating | Does not edit source in shown example | Sensitive file is read; output transformed | Verify source unchanged | N/A |
| `find ... -print | xargs file` | Feed filenames to command | workload-generating | Runs `file` in batches | Source warns spaces/newlines cause errors/security problems | Compare with safe form | N/A |
| `find ... -print0 | xargs -0 file` | NULL-delimited filename processing | workload-generating | Handles spaces/newlines safely in shown pattern | Some target commands may need `--` for leading dashes | Verify representative filenames | N/A |
| `find ... -exec file {} \;` | Run command per found file | workload-generating | Invokes target command per match | Command-specific effects if target command changes state | Verify per-file result | Command-specific |
| `expr 1 + 2` | Arithmetic example | read-only/workload-generating | Prints arithmetic result | Source calls it awkward/slow for substantial math | Check result | N/A |
| `exec <program>` | Replace current shell process | state-changing/process-control | Current shell/script disappears and becomes program | Source explicitly calls it irreversible | Observe replacement process behavior | No rollback inside replaced process |
| `(cd <dir>; <program>)` | Run commands in subshell | workload-generating | Environment/cwd changes isolated in child shell | Target command effects still persist externally if it writes data | Parent cwd unchanged | Subshell environment reverts on exit |
| `PATH=... <program>` | One-command environment override | shell invocation | Applies variable only to command invocation | Wrong PATH may choose unintended executable | Observe command selected/behavior | Automatic after command exits |
| `. config.sh` | Source file into current shell | state-changing/shell-context | Executes file in current shell; variables/definitions persist | Untrusted or incorrect file can modify current environment/state | Check intended definitions | Restore captured prior state; otherwise `[Needs confirmation]` |
| `read <var>` | Read line from stdin into variable | shell-state-changing | Changes shell variable | User input may drive later unsafe actions if not validated | Inspect controlled input/result | Reassign/unset only if prior state known |

## Special variables from source

| Variable | Meaning |
|---|---|
| `$1`, `$2`, ... | Individual positional arguments |
| `$#` | Number of arguments |
| `$@` | All arguments |
| `$0` | Script name |
| `$$` | Shell process PID |
| `$?` | Return code of last command |

## test operators highlighted by source

File:
- `-e` exists;
- `-s` nonempty;
- `-f` regular file;
- `-d` directory;
- `-h` symlink;
- `-b` block device;
- `-c` character device;
- `-p` named pipe;
- `-S` socket;
- `-r/-w/-x` access permissions;
- `-u/-g/-k` setuid/setgid/sticky;
- `-nt/-ot/-ef` two-file comparisons.

String:
- `=`, `!=`, `-z`, `-n`.

Numeric:
- `-eq`, `-ne`, `-lt`, `-gt`, `-le`, `-ge`.

## Safety notes

1. Quote possibly empty positional parameters in tests.
2. Read `$?` immediately if it matters.
3. Do not assume every nonzero return code means a fatal error.
4. Prefer `mktemp` for temporary files; clean them with a signal handler when needed.
5. Prefer `find -print0 | xargs -0` for arbitrary filenames.
6. `exec` is irreversible for the current shell process.
7. Sourcing executes another file in the current shell context.
8. Source repeatedly recommends switching to Python/Perl/awk when shell logic becomes complex.
