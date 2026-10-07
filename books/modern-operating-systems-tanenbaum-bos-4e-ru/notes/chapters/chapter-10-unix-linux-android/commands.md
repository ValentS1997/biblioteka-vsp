# Source-confirmed operations, commands and APIs

Scope: chapter 10 RAG only, PDF pages 784–930.

| Item | Class | Source-grounded role | Safety / verification |
|---|---|---|---|
| `wc -l <a >b &` | workload-generating | Shell example: count lines in `a`, redirect to `b`, run in background | Verify `b` is the intended output target. |
| `sort <x | head &` | workload-generating | Background pipeline example | Input/output redirection and `&` are shell semantics. |
| `cat`, `grep`, `head`, `tail`, `sort` | read-only / workload-generating | POSIX-style text/file utilities | Read-only when only reading inputs and stdout is not redirected to a destructive target. |
| `cp` | state-changing | Copy file data; chapter also shows copying to a special device file | Destination is modified/created; verify destination before use. |
| `rm`, `rmdir` | state-changing | Remove files/directories | Destructive; source does not provide a generic rollback. |
| `chmod` | state-changing | Change file protection mode | Record previous mode; new mode affects later access checks, not already-open descriptors. |
| `fork()` | state-changing | Create a child process | Child initially observes fork semantics; Linux implements pages with COW. |
| `waitpid()` | read-only / synchronizing | Wait for child termination and receive status | Does not itself mutate persistent data. |
| `execve()` | state-changing | Replace current process image | Current address-space image is replaced on success. |
| `exit()` | state-changing | Terminate process and return status | Parent may retain zombie metadata until status is collected. |
| `kill(pid, sig)` | state-changing | Send a signal | Signal semantics vary; an unhandled terminating signal may kill the receiver. |
| `alarm()` | state-changing | Schedule `SIGALRM` | A later `alarm` replaces the previous pending alarm in the chapter description. |
| `clone(..., sharing_flags, ...)` | state-changing | Create task with configurable sharing | Verify `CLONE_VM`, `CLONE_FS`, `CLONE_FILES`, `CLONE_SIGHAND`, `CLONE_PARENT` intent. |
| `nice(value)` | state-changing | Change normal-task scheduling preference | Negative values improve service and are restricted to administrator in the chapter. |
| `brk(addr)` | state-changing | Change data-segment size | Incorrect boundaries can invalidate process assumptions. |
| `mmap(addr,len,prot,flags,fd,offset)` | state-changing | Map file into address space | Address/length/file offset are page-aligned as required by the source description. |
| `unmap(addr,len)` | state-changing | Remove all/part of mapping | Verify which remainder stays mapped. |
| `read` / `write` | read-only / state-changing | Common file/device/socket I/O interface | `write` changes file/device/socket state. |
| `socket`, `listen`, `connect`, `close` | state-changing | Network endpoint lifecycle | Network behavior depends on peer and protocol; no deployment recipe is added. |
| `sync`, `fsync`, `fdatasync` | state-changing | Flush dirty data toward persistent storage | Verify intended file/device and completion semantics. |
| `creat`, `link`, `unlink` | state-changing | Create directory entry/file, add hard link, remove link | `unlink` of last link removes file when no open-reference semantics keep it alive. |
| `chdir` | state-changing | Change process working directory | Changes interpretation of subsequent relative paths. |
| `opendir`, `readdir`, `closedir`, `rewinddir` | read-only | Directory traversal | No direct directory writes through this interface. |
| `chmod(path,mode)` | state-changing | Change protection bits | Owner/root only in the source model; capture previous mode for rollback. |
| `access(path,mode)` | read-only | Check access using real UID/GID | Used to avoid privilege confusion in SETUID programs. |
| `getuid/geteuid/getgid/getegid` | read-only | Inspect process identities | Distinguish real and effective identity. |
| `chown`, `setuid`, `setgid` | state-changing | Change owner/group or process identity | Privileged in the source model; exact modern constraints are `[Needs confirmation]`. |
| `/proc/<pid>/...` | read-only or state-changing depending file | Virtual process/system information | Most information is readable; some `/proc` files are writable and can change kernel parameters. |
| Binder `transact()` / `onTransact()` | workload-generating | Android cross-process RPC transaction | Kernel attaches caller identity and resolves object references. |
| Android `ContentResolver.query()` | read-only in shown use | Query a content provider through Binder-backed interface | Data access remains subject to provider/security policy. |

## Important source semantics

### Permission check is not continuous

The chapter states that the effective UID/GID is checked when a process opens a file. Later `read` and `write` operations do not repeat that permission check. Consequently, changing mode after a file was opened does not revoke access already represented by that descriptor.

### `clone` sharing flags

| Flag set | Meaning in source |
|---|---|
| `CLONE_VM` | share virtual memory / create a thread-like task |
| `CLONE_FS` | share working/root directories and umask |
| `CLONE_FILES` | share file descriptors |
| `CLONE_SIGHAND` | share signal-handler table |
| `CLONE_PARENT` | use caller's parent |

## Extraction note

The terminal-control table on PDF page 844 contains a malformed extracted token for the input-speed getter (`cfgtetispeed` in the text layer). It is not silently normalized here. See `source-findings.md`.

## Rollback rule

For state-changing operations, capture the pre-change object first. Where the chapter does not define a reversible procedure, rollback remains `[Needs confirmation]` rather than importing a modern platform command from outside RAG.
