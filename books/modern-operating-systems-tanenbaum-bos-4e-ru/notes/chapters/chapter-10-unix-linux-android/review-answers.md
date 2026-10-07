# RAG-grounded review answers — Chapter 10

These are chapter-grounded answers, not an official answer key. Calculations are derived from values in the exercises. Where the chapter does not provide enough information or an exercise requires a live environment, the gap is explicit.

1. **Portability from C.** Most of the operating system can be recompiled for a new machine once a C compiler exists. Only a comparatively small machine-dependent layer, such as low-level interrupt/memory code and device drivers, must be rewritten, while hidden architectural assumptions must be found and removed.

2. **Why POSIX standardizes library procedures.** A stable procedure-level API lets applications call names such as `open`, `read` and `fork` across conforming UNIX systems even if each kernel uses a different raw trap/syscall ABI. The library is the portability boundary.

3. **Dependence on gcc.** Advantage: one portable compiler/toolchain substantially reduces the work needed to bring Linux and its C code to a new architecture. Disadvantage: the port now depends on gcc itself being available/portable/correct for that architecture; a compiler limitation becomes an OS-port limitation.

4. **`ls [abc]*e*`.** Only `bonefish`. The name must begin with `a`, `b` or `c` and contain an `e` later.

5. **`grep nd xyz | wc -l`.** `grep` emits lines of `xyz` containing the string `nd`; `wc -l` counts those output lines. The result is the number of matching lines.

6. **Eighth line of `z`.** One source-supported pipeline is:
   ```sh
   head -8 z | tail -1
   ```

7. **stdout vs stderr.** They are separate streams so normal program output and diagnostics can be redirected independently even though both default to the terminal.

8. **Two three-stage background pipelines.** Six new command processes: three for `a|b|c` and three for `d|e|f`. The shell itself is not counted as new.

9. **Environment inheritance.** Yes. `fork` creates the child from the parent's process state, and the chapter also describes environment strings being copied into the new image on `exec`. Changes made independently afterward do not retroactively alter the other process.

10. **Approximate process-creation time.** Text is shared, so copy data + stack + task structure + user structure:
    `20 + 10 + 1 + 5 = 36 KiB`.
    That is `36×1024/4 = 9216` 32-bit words. At 50 ns/word, copying takes `0.4608 ms`; adding the 1 ms kernel-entry cost gives approximately **1.4608 ms**. This uses the exercise's simplified cost model only.

11. **Preserving `fork` semantics without eager copying.** Linux gives parent and child separate page tables pointing at the same physical pages and marks those pages read-only. A write triggers a protection fault; the kernel copies that page for the writer and makes the private copy writable. This is copy-on-write.

12. **Why negative `nice` is privileged.** In the chapter's priority model, negative nice improves CPU service. If every user could request it, a process could unfairly take CPU time from other users; therefore improved service is administrator-controlled.

13. **Initial static priority.** Normal tasks span priorities 100–139 while `nice` spans −20…+19. The natural mapping is `static_priority = 120 + nice`: nice 0 → 120, −20 → 100, +19 → 139. Lower numeric priority is higher service.

14. **Zombie memory.** Yes, the process's ordinary address space/resources can be reclaimed because it no longer executes. Only the small termination/accounting identity needed so the parent can collect status must remain until `wait`/`waitpid`.

15. **Signal analogy and uses.** A signal is analogous to a hardware interrupt: normal control flow is interrupted and a handler may run. Source examples include `SIGFPE` for divide-by-zero and `SIGALRM` after an `alarm`; interactive termination is another use.

16. **Process-group signaling restriction.** It limits interference to related jobs/processes and prevents an ordinary process from arbitrarily disrupting unrelated users' work. This answer follows the protection rationale implied by the source's process-group signal model.

17. **Ordinary Pentium procedure call for syscall.** A plain user-space call does not by itself perform the protected user→kernel mode transition described by the chapter; the source explicitly uses an emulated/software interrupt for that boundary. A Pentium-specific alternative mechanism and its exact conditions are not described in the chapter RAG: **[Needs confirmation]**.

18. **Daemon vs interactive priority.** Interactive tasks generally receive more favorable dynamic treatment because the scheduler detects sleeping/wakeup behavior and boosts responsiveness. CPU-bound background work receives what remains.

19. **PID counter alone.** Not if the PID space is finite. Eventually the counter wraps while some older PID may still be active. The chapter states that Linux searches for a PID not currently used and updates a PID hash table.

20. **Why keep parent PID.** Parent/child relationships are needed for operations such as collecting child termination with `waitpid`, maintaining process ancestry and managing related process behavior. Storing the parent PID makes that relationship directly available to the kernel.

21. **COW with `p1`, `p2`, `p3`.** All three may initially map the same read-only physical page. The kernel tracks sharing/reference state. When any one writes, that task receives a private writable copy while the remaining tasks continue to share the original. Subsequent writers are handled the same way until sharing collapses naturally.

22. **`clone` flags.** For the flags listed in the chapter, traditional `fork` corresponds to not sharing VM, filesystem context, file descriptors or signal handlers; the new task is a separate process and the caller is its parent. A UNIX-thread-like task shares VM, FS state, file descriptors and signal handlers (`CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND`); using `CLONE_PARENT` also gives it the caller's parent. The chapter emphasizes that Linux permits finer combinations than traditional UNIX.

23. **Give A more CPU than B.** In O(1), assign A a higher priority so it is selected from a higher-priority queue and receives a larger quantum. In CFS, priority/nice changes the rate at which `vruntime` advances; A's weighted virtual time advances more slowly, so it returns to the leftmost/eligible position more often.

24. **Tickless operation.** Periodic timer interrupts consume CPU cycles and energy even when there is little useful scheduling work. Tickless mode avoids that overhead and is especially sensible for an idle or single-process embedded system where periodic preemption may add no scheduling value.

25. **Why a second-stage boot loader.** Sector 0 provides only a very small bootstrap (the chapter describes 512 bytes). A larger loader can understand a filesystem or block map, locate/load the kernel and handle machine/storage details. The tiny first stage cannot conveniently contain all of that logic.

26. **Three editor copies.**
    - Shared text: one 100 KiB text segment + three × (30 + 50 + 10) KiB private data/BSS/stack = **370 KiB**.
    - No shared text: three × (100 + 30 + 50 + 10) KiB = **570 KiB**.
    This ignores other process/kernel metadata because the exercise supplies only these regions.

27. **Why open-file tables exist.** An inode alone cannot hold a single current file position when unrelated opens need independent offsets, and a per-process descriptor entry alone cannot express inherited/shared open-file state across `fork`. Linux therefore separates the per-process descriptor table, open-file description/state and inode.

28. **Why text comes from executable, data/stack from swap.** Text is normally read-only, so a discarded page can be reconstructed from its executable file. Writable data/stack pages may contain values that exist nowhere else; when evicted, they need swap backing unless another valid backing store exists.

29. **`mmap` + signals IPC.** Two processes map the same temporary file as a shared mapping. They exchange bulk data by reading/writing that common memory. A signal can notify the peer that new data/state is ready, separating high-throughput storage from event notification.

30. **Address 72000.** Mapping base = 65536, so offset inside the mapping is `72000 − 65536 = 6464`. Because the file offset passed to `mmap` is 0, the access corresponds to file byte offset **6464** (zero-based).

31. **Partial `munmap`.** Yes: 65536 and 8192 are page-aligned for 8 KiB pages. It removes the first page of the mapping. File offsets **8192–32767** remain mapped (virtual addresses 73728–98303).

32. **Fatal page fault.** Yes. Demand paging faults on valid VMAs are normal, but a reference into a hole/unmapped or disallowed address cannot be satisfied and can terminate the process, for example through the source-described invalid-address/`SIGSEGV` path.

33. **Adjacent equal-size buddy blocks.** Yes, if they are adjacent but are not each other's buddy at that order. Example: a free 4-page upper half of one 8-page parent can sit directly next to a free 4-page lower half of the next 8-page parent; each can merge only with its own sibling, not with the merely adjacent block.

34. **Swap partition vs swap file.** A dedicated swap area avoids filesystem block→disk mapping, permits physical writes sized independently of filesystem blocks, and can keep a page in one contiguous disk extent. A swap file can add mapping and fragmentation overhead.

35. **Relative-path advantages.** They are shorter/more convenient when operating within a subtree, and they can reduce pathname traversal because lookup starts at the current-directory inode rather than always from root. They also let a subtree be relocated without rewriting every path that is internal to it.

36. **Five lock requests.**
    1. A shared 0–10: granted.
    2. B exclusive 20–30: granted; no overlap with A.
    3. C shared 8–40: blocked because it overlaps B's exclusive 20–30 (its overlap with A's shared lock is compatible).
    4. A shared 25–35: blocked because it overlaps B's exclusive lock.
    5. B exclusive byte 8: blocked because it overlaps A's shared 0–10.
    At this point A waits for B while B waits for A, so the retained locks can form a deadlock cycle.

37. **Multiple waiters on overlapping byte locks.** The source defines lock conflicts but not a unique waiter-order policy. The added semantic issue is which waiter obtains the newly available region/fairness when C releases. Two defensible policies are FIFO queueing of conflicting requests, or wake all compatible waiters and let the lock acquisition rule arbitrate. Exact intended queue semantics: **[Needs confirmation]**.

38. **Shared vs exclusive locks.** Use shared locks for concurrent readers of a stable region; use exclusive locks when writing/updating requires all overlapping users excluded. An exclusive requester may block behind existing readers and can starve if a policy continuously admits new shared readers ahead of it.

39. **0755.** Owner: `rwx`; group: `r-x`; others: `r-x`. For a regular executable, only the owner may write; everyone may read and execute. For directories, `x` means search/traverse.

40. **Filesystem on rewritable numbered tape blocks.** Conceptually yes if the driver can expose independently addressable/rewriteable blocks with the block-device semantics expected by the filesystem. The device would likely be extremely inefficient because physical tape access is not disk-like; the chapter does not provide a performance guarantee.

41. **Hard-link symmetry.** The two names refer to the same inode, so file contents, owner and mode are the same object. Access is not absolutely symmetric at the pathname level because creating/removing/renaming each directory entry depends on permissions of the containing directory.

42. **Efficient absolute/relative lookup.** Keep pointers to the root inode and each process's current-directory inode. Absolute lookup starts at root; relative lookup starts at the current-directory inode. Resolve each pathname component through directory entries, using the dentry cache to avoid repeated disk traversal.

43. **Disk accesses for `/usr/ast/work/f`.** With root inode already in memory and one block per directory: read root directory (1), `usr` inode (2), `usr` directory (3), `ast` inode (4), `ast` directory (5), `work` inode (6), `work` directory (7), and `f` inode (8): **8 disk accesses**, assuming none of these are otherwise cached.

44. **Maximum file size.** Addressable data blocks =
    `12 + 256 + 256² + 256³ = 16,843,020` blocks.
    At 1 KiB/block: **17,247,252,480 bytes**, about **16.063 GiB**.

45. **In-memory inode reference count.** It records how many active kernel/open-file references still depend on that inode so the kernel knows whether the in-memory inode may be reclaimed and so one user's close does not discard metadata still needed by another reference.

46. **Per-CPU run queues.** Yes, with a tradeoff. They improve scalability and processor/cache affinity by avoiding one heavily contended global queue. The chapter therefore also requires periodic load balancing between CPU run queues so one CPU is not overloaded while another is idle.

47. **Loadable-module disadvantages.** They allow executable code to be inserted into the running kernel, enlarging the trusted/security boundary and allowing buggy or malicious code to run with kernel power. They also add runtime relocation/resource/vector/table-update complexity, so failures during insertion can destabilize the running system.

48. **Why flush old dirty pages.** Without periodic writeback, modified data could remain only in volatile memory for an unbounded time. `pdflush` bounds that age, reduces the amount of dirty state accumulated and limits how much old modified data is exposed to loss on a crash.

49. **Repair link count 2 vs one directory entry.** Yes, after recovery has scanned the namespace and established that only one directory entry references the inode, it can correct the inode's link count from 2 to 1. The directory scan is the evidence for the repaired value.

50. **Fastest syscall.** A plausible candidate is a trivial identity/query syscall that only returns already-resident process metadata, rather than one requiring I/O or blocking. The chapter does not benchmark syscalls or establish a winner, so the exact answer is **[Needs confirmation]**.

51. **`unlink` without an extra hard link.** Yes. The original directory name is itself a link to the inode. If it is the last link, `unlink` removes that directory entry and the file becomes eligible for deletion under the filesystem's open-reference semantics.

52. **Maximum ext2 user data on 1.44 MiB floppy.** The chapter gives the layout—boot block, superblock, group descriptor, block bitmap, inode bitmap, inode table, then data—and 128-byte inodes. But it does not specify how many inodes the floppy filesystem is created with, so the inode-table size is unknown. An exact maximum therefore cannot be derived from chapter data alone: **[Needs confirmation]**. With 1 KiB blocks, the fixed pre-inode-table overhead is at least five blocks; additional inode-table and directory/reserved blocks must then be subtracted.

53. **Why superuser exists.** Some administration must legitimately override ordinary ownership and protection rules: changing identities/ownership, managing protected devices/system resources and configuring the system. Concentrating those powers in a privileged identity enables administration while ordinary users remain constrained.

54. **File changed after permissions were fixed.** The chapter explicitly states that permissions are checked when `open` succeeds; later `read`/`write` calls do not recheck the mode. A student could have opened the file for writing while it was world-writable and kept the descriptor after `chmod`. Prevention requires eliminating stale writable opens—for example, coordinating/stopping writers and replacing the object under controlled directory permissions—rather than assuming `chmod` revokes existing handles.

55. **Why file-only identity is useful.** It supports least privilege: a server/helper can access files as a target user without acquiring all powers associated with changing its effective UID. That narrows privilege to the operation that actually needs impersonation—filesystem access.

56. **Live `/proc/####` observations.** The chapter establishes that these are virtual files generated from live process/kernel state rather than ordinary on-disk files, and that much of `/proc` is readable by unprivileged users while some entries are writable. Actual reported sizes, timestamps and permission modes require a live Linux instance and may vary: **[Needs confirmation]**.

57. **Minimal saved browser-activity state.** Save only enough UI/navigation state to reconstruct what the user was seeing—for example the page/message identifier or URL plus scroll/selection/UI position. Keep the actual page/content in persistent/cache storage and reload it during recreation. The chapter explicitly advocates small saved activity state rather than embedding the full content.

58. **Android network download considerations.** In addition to ordinary socket behavior, code must account for mobile power and lifecycle semantics: the device may sleep unless the work is protected by the wake-lock handoff model, and a background process may be killed under memory pressure. Long-running work belongs in an appropriate service/lifecycle component, and sandbox/permission boundaries still apply.

59. **Threads in a zygote-like design.** Start them **after** the child is forked. The chapter's multithreaded-`fork` discussion shows the hazards of inherited locks/state when only one execution context safely survives. Android's process-start description likewise says runtime threads such as the garbage collector are started after zygote forks the child.

60. **Binder object comes back with the same identity.** You can infer that the caller possesses a capability derived from the Binder object you sent. You cannot prove it is the original recipient process, because Binder objects can be delegated to other processes while preserving object identity.

61. **Browser consumes memory after launcher → mail sync → camera → browser.** Browser remains FOREGROUND and is protected longest. Processes no longer needed become CACHED and are first candidates; the launcher is HOME and background mail synchronization is SERVICE, so progressively less-important processes are killed as memory pressure rises. A camera process that is no longer visible/needed can fall to cached status and be reclaimed. The exact moment depends on current component dependencies, but the chapter's order is cached → home → service → more important categories, while foreground/system work is preserved.

62. **Minimal shell design.** Repeatedly read a command, parse arguments and optional trailing `&`, call `fork`, and in the child call `execve` (or the corresponding library wrapper). In the parent, call `waitpid` for a foreground command and return immediately to the prompt for a background command. Pipelines additionally require connected file descriptors. The chapter supports this design; a complete parser implementation is outside the supplied source.

63. **BIOS boot-floppy program.** The chapter supports the boot sequence: BIOS loads and runs sector 0, whose tiny bootstrap then loads a larger program/kernel. It does not provide the Pentium BIOS keyboard/video interrupt API or assembly listing needed to implement this exercise. Exact code is **[Needs confirmation]**.

64. **Serial dumb terminal.** Source-supported design: open the serial device, configure input/output speed and terminal attributes using the POSIX terminal-control interface, use raw/unprocessed mode for transparent byte transport, and relay bytes between stdin/stdout and the serial file descriptor. Exact device names, wiring and complete code require the target systems: **[Needs confirmation]**.

65. **Sockets vs shared-memory file transfer.** The chapter supports both mechanisms: sockets traverse the networking/socket path, while a shared `mmap` lets processes exchange bytes through common mapped pages. Shared memory should avoid some protocol/copying work for local peers, but actual crossover points and measured throughput depend on implementation, file size and hardware. Required benchmark results are **[Needs confirmation]**.

66. **User-level threads library.** Source-grounded architecture: define thread control blocks, ready/wait queues, a round-robin dispatcher and mutex wait queues; implement create/join/exit/yield/self around that state. Then replace round-robin with a policy inspired by the chapter's Linux 2.6 scheduler—priority-aware O(1)-style queues or, for the later described default, CFS-like weighted runtime. Exact implementation, preemption mechanism and measured comparison require running code: **[Needs confirmation]**.

67. **System-information shell script.** The chapter supplies shell scripting/control flow, standard text utilities and `/proc` as a virtual source of process/CPU/kernel information. A source-aligned solution can combine those to report the requested fields, but exact paths/formatting vary by live system. A representative outline is:
    ```sh
    echo "HOME=$HOME"
    echo "PWD=$PWD"
    cat /proc/cpuinfo
    cat /proc/loadavg
    ```
    Counting only numeric `/proc/<pid>` directories and formatting a concise report require additional shell details not specified by the chapter; live output is **[Needs confirmation]**.
