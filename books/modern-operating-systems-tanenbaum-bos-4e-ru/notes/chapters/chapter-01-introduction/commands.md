# Source-confirmed commands, system calls and tools

Scope: chapter 1 RAG only, PDF pages 22–110.

## UNIX/POSIX process interfaces

| Item | Class | Source-grounded effect | Risk / verification / rollback |
|---|---|---|---|
| `fork()` | workload-generating / state-changing | Creates a child process as a copy of the caller | Resource growth; verify returned PID/branch of execution. Rollback: process termination; exact recovery `[Needs confirmation]`. |
| `waitpid(...)` | read-only / synchronization | Waits for child completion and returns termination status | Can block caller; verify returned status. |
| `execve(...)` | state-changing | Replaces current process image with another program | Current image is replaced. Rollback `[Needs confirmation]`. |
| `exit(status)` | state-changing | Terminates the current process and returns status to parent | Process ends; rollback not applicable. |
| `brk(...)` | state-changing | Changes end of data segment | Chapter notes POSIX does not standardize it and recommends `malloc` for programmers. |
| `malloc(...)` | state-changing in process memory | Library-level dynamic memory allocation | Low-level implementation not treated as a standardized system call here. |

### Minimal shell flow shown by the source

```text
read command
    ↓
fork()
    ├─ parent → waitpid()
    └─ child  → execve()
```

The source also gives the shell command example:

```sh
cp file1 file2
```

Class: state-changing; it copies `file1` to `file2`.

## UNIX file interfaces

| Item | Class | Effect |
|---|---|---|
| `open(...)` | read-only or state-changing | Opens a file; `O_CREAT` may create one |
| `close(...)` | state-changing process state | Releases a file descriptor |
| `read(...)` | read-only | Reads data |
| `write(...)` | state-changing | Writes data |
| `lseek(...)` | state-changing process/file-offset state | Repositions file offset |
| `stat(...)` | read-only | Gets file metadata |
| `fstat(...)` | read-only | Gets metadata for an open file |

## UNIX directory/filesystem interfaces

| Item | Class | Effect | Rollback from chapter |
|---|---|---|---|
| `mkdir(...)` | state-changing | Creates directory | `rmdir` if empty |
| `rmdir(...)` | state-changing | Removes empty directory | `[Needs confirmation]` |
| `link(old,new)` | state-changing | Creates another directory entry for the same inode | `unlink` removes an entry |
| `unlink(...)` | state-changing / potentially destructive | Removes a directory entry; file is deleted when no entries remain | `[Needs confirmation]` |
| `mount(...)` | state-changing | Attaches a filesystem into the directory tree | `umount` |
| `umount(...)` | state-changing | Detaches a mounted filesystem | remount details `[Needs confirmation]` |
| `chdir(...)` | state-changing process state | Changes current working directory | previous directory must be known |
| `chmod(...)` | state-changing | Changes file permission bits | restore previous mode; previous value must be known |
| `kill(...)` | state-changing | Sends a signal; an unhandled signal may terminate target | `[Needs confirmation]` |
| `time(...)` | read-only | Returns time in seconds from the stated epoch | Not applicable |

Source examples:

```c
link("/usr/jim/memo", "/usr/ast/note");
mount("/dev/sdb0", "/mnt", 0);
chdir("/usr/ast/test");
chmod("file", 0644);
```

## Win32 API examples

The chapter emphasizes that Win32 API calls are not guaranteed to be one-to-one kernel system calls.

| UNIX concept | Win32 API shown |
|---|---|
| `fork` + `execve` | `CreateProcess` |
| `waitpid` | `WaitForSingleObject` |
| `exit` | `ExitProcess` |
| `open` | `CreateFile` |
| `close` | `CloseHandle` |
| `read` | `ReadFile` |
| `write` | `WriteFile` |
| `lseek` | `SetFilePointer` |
| `stat` | `GetFileAttributesEx` |
| `mkdir` | `CreateDirectory` |
| `rmdir` | `RemoveDirectory` |
| `unlink` | `DeleteFile` |
| `chdir` | `SetCurrentDirectory` |
| `time` | `GetLocalTime` |

The chapter’s Win32 comparison table lists no direct equivalents for standalone `execve`, `link`, `mount`/`umount`, `chmod` and `kill`.

## Build/development tools

| Tool | Class | Source-grounded role |
|---|---|---|
| C preprocessor | workload-generating | Expands `#include`, macros and conditional compilation |
| C compiler | workload-generating / creates artifacts | Converts `.c` files to `.o` object files |
| `make` | workload-generating / creates artifacts | Uses `Makefile` dependencies to rebuild only required objects |
| linker | workload-generating / creates artifact | Combines object files and libraries into an executable |

## Review-exercise tools

- `sync` — state-changing persistence operation; the source instructs flushing filesystem buffers before the intentionally disruptive process-creation experiment in question 35.
- `od` — read-only inspection tool in the UNIX directory-structure exercise.
- MS-DOS `DEBUG` — used by the source as an alternative raw-inspection tool in question 36.

Question 35 deliberately describes an experiment that can exhaust process resources and hang a machine. The source restricts it to a personal/disposable UNIX-like system and explicitly warns against running it on a shared time-sharing system without administrator permission. No runnable fork-bomb script is reproduced here.
