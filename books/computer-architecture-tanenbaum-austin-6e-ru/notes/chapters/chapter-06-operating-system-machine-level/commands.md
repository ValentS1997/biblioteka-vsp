# System calls / API primitives — глава 6

**Provenance:** RAG `p0475:c01`–`p0554:c01`.

This artifact records OS-level calls named in the source. It is descriptive, not a current production API guide.

## UNIX file operations

| Primitive | Source role |
|---|---|
| `creat(name, mode)` | create file |
| `unlink(name)` | remove directory link |
| `open(name, mode)` | open/create and return file descriptor |
| `close(fd)` | close open file |
| `read(fd, buffer, count)` | read bytes |
| `write(fd, buffer, count)` | write bytes |
| `lseek(fd, offset, w)` | reposition file pointer |
| `stat(name, buffer)` | return file metadata |
| `chmod(name, mode)` | change protection mode |
| `fcntl(fd, cmd, ...)` | control operations, including locking |

## UNIX directory operations

- `mkdir`
- `rmdir`
- `opendir`
- `readdir`
- `closedir`
- `chdir`
- `link`
- `unlink`

## UNIX process / IPC examples

- `fork` — create process copy;
- `exec` — replace process program/data;
- `wait`, `waitpid` — wait for child termination;
- `exit` — terminate;
- pipes — byte-stream IPC;
- `msgget`, `msgsnd`, `msgrecv` — message queues;
- shared-memory calls named in source: `shmat`, `shmop`;
- semaphores — `up` / `down` conceptual operations.

## POSIX thread primitives

- `pthread_create`
- `pthread_exit`
- `pthread_join`
- `pthread_mutex_init`
- `pthread_mutex_destroy`
- `pthread_mutex_lock`
- `pthread_mutex_unlock`
- `pthread_cond_init`
- `pthread_cond_destroy`
- `pthread_cond_wait`
- `pthread_cond_signal`

## Windows file/API examples in source

- `CreateFile`
- `DeleteFile`
- `CloseHandle`
- `ReadFile`
- `WriteFile`
- `SetFilePointer`
- `SetFileAttributes`
- `LockFile`
- `UnlockFile`
- `CreateFileMapping`
- `MapViewOfFile`
- `UnmapViewOfFile`
- `OpenFileMapping`

Directory examples include `CreateDirectory`, `RemoveDirectory`, `FindFirstFile`, `FindNextFile`, `MoveFile`, `SetCurrentDirectory`.

## Windows process / synchronization examples

- `CreateProcess`
- `CreateThread`
- `CreateSemaphore`
- `ReleaseSemaphore` — source analogue of `up`;
- `WaitForSingleObject` — source analogue of blocking `down`/wait;
- `DuplicateHandle`
- `ReleaseMutex`
- `EnterCriticalSection`
- `LeaveCriticalSection`
- `SetEvent`
- `PulseEvent`

## Memory-mapping example

UNIX source form:

```text
paddr = mmap(virtual_address, length, protection, flags, fd, file_offset)
```

Windows chapter uses file-mapping objects plus map/unmap API calls.

## Safety boundary

These names come from a historical textbook chapter. Exact signatures, current availability, security model and modern best practices are **[Needs confirmation]** outside this RAG-only analysis.
