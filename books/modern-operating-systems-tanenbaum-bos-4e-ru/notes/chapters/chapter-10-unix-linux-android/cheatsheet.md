# Chapter 10 cheatsheet — Unix, Linux and Android

## Symptom / problem framing

| Observation | First boundary to inspect |
|---|---|
| command behaves differently than expected | shell parsing, redirection, pipeline, environment |
| child differs unexpectedly from parent | `fork` / copy-on-write / `exec` |
| thread/process sharing is surprising | `clone` sharing flags |
| latency or CPU share is wrong | scheduler class, nice/static priority, CFS vruntime |
| page fault occurs | valid VMA/demand paging vs invalid address |
| memory pressure is high | page reclaim, swap, dirty pages, Android process importance |
| file access/offset is surprising | fd table → open-file description → inode/VFS |
| permission changed but access persists | existing open descriptor |
| device behaves like a file | special file, major/minor number, driver |
| remote file semantics differ | NFS state/cache model |
| Android component starts unexpectedly | manifest + intent resolution + ActivityManager |
| Android app disappears under pressure | process importance / `oom_adj` / saved activity state |
| Binder caller/object identity matters | Binder capability and transaction identity |

## Baseline / context

### Linux interface stack

```text
shell / application
        ↓
C library / runtime
        ↓
system-call interface
        ↓
kernel subsystems
  ├─ process/scheduler
  ├─ memory
  ├─ VFS/I/O/network
  └─ protection
        ↓
hardware
```

### Process creation

```text
fork
  ↓
child task + page tables
  ↓
parent pages shared read-only
  ↓
write → protection fault → private page copy
  ↓
exec → replace address space
```

### File access path

```text
process fd
  ↓
open-file state (offset, mode)
  ↓
VFS file/dentry
  ↓
inode
  ↓
filesystem / device / NFS
```

### Android application path

```text
manifest / intent
      ↓
PackageManager + ActivityManager
      ↓
zygote fork → app UID sandbox
      ↓
Dalvik process
      ↓
activity/service/receiver/provider
      ↕
Binder IPC
```

## Read-only checks

1. Identify whether the behavior is user-space, syscall, scheduler, VM, VFS, driver or Android-framework level.
2. For a process issue, distinguish PID/process identity from task/thread identity.
3. For `fork`, determine whether a page is still shared read-only or has been copied after a write.
4. For `clone`, identify which resources are shared: VM, filesystem context, descriptors, signal handlers, parent relationship.
5. For CPU behavior, identify real-time vs normal task and the source-described priority/nice relationship.
6. For a page fault, determine whether the address belongs to a valid VMA.
7. For mapped files, verify mapping base, length, page alignment, protection, sharing flags and file offset.
8. For file behavior, separate pathname lookup, inode metadata, open-file offset and per-process descriptor number.
9. For permissions, distinguish real UID/GID from effective UID/GID and remember that access is checked at open time in the chapter model.
10. For a device, identify block vs character semantics and the major/minor driver mapping.
11. For NFS, identify version/state assumptions and whether cached data may be stale.
12. For Android, identify the component type, intent, owning UID, Binder boundary and process importance.
13. Before interpreting Android process death as application failure, check whether user-visible state was intentionally preserved outside the process.

## Interpretation

### O(1) vs CFS

| Scheduler | Core structure | Priority effect |
|---|---|---|
| O(1) | active/expired priority arrays | higher priority gets preferential selection and a larger quantum |
| CFS | red-black tree by `vruntime` | lower-priority tasks accumulate virtual runtime faster |

### Memory layers

- Text is normally read-only and can use the executable file as backing store.
- Data and stack are private writable regions.
- `mmap` can map files and provide shared-memory-style communication.
- Linux page reclaim distinguishes discardable, syncable and swappable pages.
- A swap partition avoids filesystem block mapping and fragmentation overhead.
- Buddy allocation provides power-of-two physical blocks; slab allocation subdivides them for kernel objects.

### File locks

- Shared locks may overlap other shared locks.
- An exclusive lock conflicts with any overlapping lock.
- Blocking acquisition can create wait dependencies and therefore deadlock if processes retain earlier locks.

### Permissions

`rwxr-xr-x = 0755`

Owner: read/write/execute.  
Group: read/execute.  
Others: read/execute.

For directories, `x` means search/traversal.

### Android process lifetime

Process lifetime is not application-state lifetime. ActivityManager can keep a small saved state while killing a process, then recreate the process/activity later and restore the visible state from persistent data plus saved UI state.

### Binder identity

A Binder object behaves like a capability. The kernel preserves remote object identity, but a capability can be passed to another process. Possession therefore proves access to the object, not necessarily that the current caller is the original recipient.

## Next action

For Linux/Android troubleshooting:

`locate abstraction → inspect identity/state → verify kernel-visible object → reproduce read-only → change one layer → verify semantics`.

## Modifying action

Source-confirmed state-changing operations include:

- process creation/replacement: `fork`, `clone`, `execve`, `exit`;
- signals and timers: `kill`, `alarm`, signal-mask/action calls;
- mappings: `brk`, `mmap`, `unmap`;
- file operations: `open`, `creat`, `write`, `link`, `unlink`, `chdir`, locks;
- permissions/identity: `chmod`, `chown`, `setuid`, `setgid`;
- terminal configuration and module loading;
- Android component/process creation mediated by system services.

Exact modern administration commands are outside this chapter's `rag_only` scope unless explicitly present in the source.

## Verification / acceptance checks

- child/parent state follows the intended `fork`/COW/`exec` semantics;
- scheduler outcome matches class and priority/nice assumptions;
- valid mapped addresses resolve to the intended file offset;
- invalid VM access produces the expected fatal fault rather than silent corruption;
- fd/open-file/inode sharing matches the intended file-position semantics;
- permission changes affect new opens as intended; existing descriptors are treated separately;
- device access resolves to the intended special file and driver;
- Android component runs under the intended application UID;
- Binder access is available only to processes holding the corresponding reference/capability;
- activity state can be reconstructed after process removal;
- memory pressure removes less-important Android processes before foreground/system work.

## Rollback

- File mode/ownership change: restore the previously recorded mode/UID/GID.
- Mapping change: restore the prior mapping layout or restart the process from known state.
- Scheduler/nice change: restore the previous value/class.
- Module load/unload: exact safe rollback is platform/version dependent — `[Needs confirmation]`.
- Android lifecycle/process intervention: do not rely on manual process resurrection; restore through the framework/application state model.
