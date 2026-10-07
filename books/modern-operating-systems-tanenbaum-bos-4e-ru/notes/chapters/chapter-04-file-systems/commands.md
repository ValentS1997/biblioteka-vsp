# Source-confirmed commands, system calls and tools

Scope: chapter 4 RAG only, PDF pages 301–379.

## Shell/program examples

| Item | Class | Source-grounded effect | Risk / verification / rollback |
|---|---|---|---|
| `copyfile abc xyz` | state-changing | Listing 4.1 example copies `abc` to `xyz`; existing `xyz` is overwritten | Risk: destination overwrite. Verify destination contents/size. Rollback requires a prior copy: `[Needs confirmation]`. |
| `cp /usr/ast/mailbox /usr/ast/mailbox.bak` | state-changing | Copies a file using absolute paths | Creates/overwrites destination according to environment semantics. Exact rollback: `[Needs confirmation]`. |
| `cp mailbox mailbox.bak` | state-changing | Same copy using relative paths when cwd is `/usr/ast` | Same risk boundary as above. |
| `rm *.o` | state-changing/destructive | Example intended to delete object files in the current directory | Destructive. Verify expansion before use. Source gives no rollback. |
| `rm * .o` | state-changing/destructive | Source example of a typo that can delete all files in the current directory | Explicitly unsafe example; do not use as a procedure. |
| `mkdir` | state-changing | Mentioned as a program used to create directories | Exact syntax/rollback not supplied. |
| `ls` | read-only | Opens/reads a directory to list contained names | No persistent mutation described. |
| `defrag` | state-changing | Windows defragmentation program; moves file blocks to restore locality | Chapter says SSD defragmentation is counterproductive. Verification/rollback are platform-specific `[Needs confirmation]`. |
| `fsck` | state-changing repair tool | UNIX consistency checker; scans block usage and directory/i-node relationships and may repair inconsistencies | Can change allocation/link metadata. Backup first when possible; exact flags/rollback are `[Needs confirmation]`. |
| `sfc` | inspection/repair tool as described by source | Chapter names it as a Windows consistency utility | Exact scope/options are not supplied; do not infer them. |
| `sync` | state-changing durability action | Flushes dirty cached data/metadata toward disk; chapter describes periodic UNIX use | Changes persistence state, not logical file contents. Verify completion per platform `[Needs confirmation]`. |
| `FlushFileBuffers` | state-changing durability API | Windows call described as equivalent in purpose to `sync` | Exact invocation/verification are `[Needs confirmation]`. |

## File system calls explicitly described

| API / operation | Class | Source-grounded role |
|---|---|---|
| `create` / `creat` | state-changing | create an empty/new file and establish attributes |
| `delete` / `unlink` | state-changing/destructive | remove a directory entry; last hard link removal releases the file |
| `open` | read-only state establishment | resolve file and load metadata/block-location information into memory; returns a descriptor |
| `close` | state-changing durability/lifecycle | release open-file-table state; chapter notes final partial block may be written |
| `read` | read-only | read from current position into a supplied buffer |
| `write` | state-changing | overwrite at current position or extend at EOF |
| `append` | state-changing | add only at end of file |
| `seek` / `lseek` | process-state change | move current file position for random access |
| get attributes | read-only | retrieve file metadata such as modification time |
| set attributes | state-changing | change protection/flags and other writable attributes |
| `rename` | state-changing namespace | change an existing file/directory name |
| `opendir` | read-only state establishment | open a directory for standardized iteration |
| `readdir` | read-only | return the next directory entry |
| `closedir` | lifecycle | release directory-open state |
| `link` | state-changing namespace | add a hard-link directory entry referring to an existing file |
| `gettimeofday`, `getitimer` | read-only measurement | question 47 suggests them for timing buffer-size experiments |

Listing 4.1 explicitly uses `open(..., O_RDONLY)`, `creat(...)`, `read`, `write`, `close` and `exit`.

## VFS interface

The chapter describes standard POSIX-style upper calls such as `open`, `read`, `write`, `lseek` routed through VFS to filesystem-specific lower operations.

A PDF 337 example spells the open-mode token as `ORDONLY`, while listing 4.1 on PDF 312 uses `O_RDONLY`. This mismatch is preserved in `source-findings.md`; this artifact uses the listing's exact `O_RDONLY` token rather than silently treating both spellings as equivalent.

## Safety boundary

Do not infer modern platform-specific flags, mount commands, `fsck` modes or recovery sequences from model memory. Exact production mutation/rollback procedures remain `[Needs confirmation]` unless explicitly present in chapter RAG.
