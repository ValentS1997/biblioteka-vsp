# Review questions — Chapter 10

Provenance: PDF pages 924–930; source questions are explicitly numbered 1–67. The wording below is condensed while preserving each exercise's task.

1. Why does writing UNIX in C make porting to new machines easier?
2. Why did POSIX standardize library procedures instead of the raw system-call interface?
3. Give one advantage and one disadvantage of Linux depending on gcc when porting to new architectures.
4. Given the source file list, which names match `ls [abc]*e*`?
5. What does `grep nd xyz | wc -l` do?
6. Write a Linux pipeline that prints the eighth line of file `z`.
7. Why distinguish stdout from stderr if both default to the terminal?
8. For background pipelines `a | b | c&` and `d | e | f&`, how many new processes are running after the shell handles both?
9. Does a child automatically receive the environment variables of a process that creates it?
10. Estimate UNIX child-process creation time from the supplied segment/structure sizes, 1 ms kernel-entry cost and 50 ns per copied 32-bit word, with text shared.
11. Linux does not eagerly copy the whole parent address space on `fork`. How are traditional `fork` semantics preserved?
12. Why may only the superuser request negative `nice` values?
13. For non-real-time priorities 100–139, what is the initial static priority and how does `nice` change it?
14. Should memory be reclaimed when a process becomes a zombie? Why?
15. What hardware concept is a signal analogous to? Give two signal-use examples.
16. Why restrict a process from signaling processes outside its process group in the model described by the chapter?
17. Can a Pentium use an ordinary procedure call instead of a simulated interrupt for system calls? Under what conditions?
18. Which usually has higher priority: daemons or interactive processes?
19. Is a monotonically incrementing PID counter alone sufficient to assign unique PIDs?
20. Why store the parent PID in each task structure?
21. If `p1` successively forks `p2` and `p3`, how can shared pages be managed with copy-on-write?
22. Which `clone` sharing flags correspond to traditional UNIX `fork` and to a UNIX-style thread?
23. How can task A receive more CPU than task B in the O(1) scheduler and in CFS?
24. Why use tickless operation, and does it make sense on an embedded system running only one process?
25. Why does sector-0 bootstrap code load a separate boot program instead of loading the whole OS directly?
26. Three editors each have 100 KiB text, 30 KiB initialized data, 50 KiB BSS and 10 KiB initial stack. Compute physical memory with and without a shared text segment.
27. Why does Linux need open-file descriptor tables?
28. Why can text pages be paged from the executable while data/stack pages need swap backing?
29. Describe IPC using `mmap` plus signals.
30. For `mmap(65536,32768,READ,FLAGS,fd,0)` with 8 KiB pages, which file byte corresponds to virtual address 72000?
31. After that mapping, does `munmap(65536,8192)` succeed, and what file bytes remain mapped?
32. Can a page fault terminate its process? Give an example.
33. Can two adjacent free equal-size blocks coexist unmerged in a buddy allocator?
34. Why is swapping to a dedicated partition faster than swapping to a file?
35. Give two advantages of relative paths over absolute paths.
36. Analyze the five supplied overlapping shared/exclusive file-lock requests by processes A, B and C.
37. If two processes queue for overlapping byte locks before C releases its lock, what semantic problem arises? Give two possible solutions.
38. When should a process use shared vs exclusive locking, and what problems can exclusive-lock requesters encounter?
39. Interpret file mode 0755 for owner, group and others.
40. Can a tape device with numbered independently rewritable blocks contain a mounted Linux filesystem?
41. After Fred and Lisa each have a hard link to file `x`, are their rights absolutely symmetric?
42. Give an efficient implementation for absolute and relative pathname lookup.
43. Count disk accesses for opening `/usr/ast/work/f` if the root inode is in memory and every directory is one block.
44. With 12 direct addresses plus single/double/triple indirect blocks, 256 addresses per indirect block and 1 KiB blocks, compute maximum file size.
45. Why does the in-memory inode table need a reference count?
46. Is a per-CPU run queue a good idea on multiprocessors? Explain.
47. Give two disadvantages of loadable kernel modules.
48. Why should `pdflush` periodically write very old dirty pages (older than about 30 s)?
49. Can recovery repair an inode link count of 2 when only one directory entry refers to it? How?
50. Guess which Linux system call is fastest.
51. Can `unlink` be used on a file for which no additional hard link was ever created? What happens?
52. Using the chapter's ext2 layout, estimate maximum user data on a 1.44 MiB floppy with 1 KiB blocks.
53. Why does the superuser concept exist despite its risk?
54. How could a file remain writable after a professor fixed world-writable permissions, and how can this be prevented?
55. Why is an `fsuid`-style identity that changes only file-access rights useful compared with full `setuid` privilege?
56. Inspect a live `/proc/####`: what are typical file sizes, timestamps and permissions?
57. For a browser activity, what minimal activity state should be saved without losing important user-visible state?
58. What must Android network-download code consider that ordinary Linux socket code may not?
59. In a zygote-like multithreaded design, should worker/runtime threads start before or after the child is forked?
60. If a Binder object sent away later returns with the same identity, what can be inferred about the caller?
61. Under Android memory pressure after launcher, background mail sync, camera and browser are started, what happens as the browser consumes all available memory?
62. Implement a minimal shell supporting simple commands and background execution.
63. Implement a bootable Pentium floppy program using BIOS keyboard input and screen echo.
64. Implement a dumb terminal between two Linux workstations over serial ports using POSIX terminal-control calls.
65. Implement file transfer using sockets and then shared memory; benchmark both and explain the kernel behavior.
66. Implement a user-level thread library with mutexes, first round-robin scheduling and then a Linux-2.6-like scheduler; compare results.
67. Write a shell script reporting process count, home/current directory, CPU type/load and similar system information.
