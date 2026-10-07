# Review questions — Chapter 11

Provenance: PDF pages 1053–1057; source questions are explicitly numbered 1–42. The wording below is condensed while preserving each exercise's task.

1. Give one advantage and one disadvantage of the Registry compared with separate `.ini` files.
2. Does HAL hide differences between one-, two- and three-button mice from the rest of the OS? Why?
3. Give an application that benefits from HAL measuring time from 1601.
4. How could a sequence-number field reduce stale-handle races when one thread closes a handle another thread still uses? What system changes are required?
5. Give three examples of one executive component calling another, using six different components.
6. If Win32 had signals, should they be process-bound, thread-bound, both, or unbound? Defend the design.
7. If DLLs were replaced by static linking, would that make more sense on clients or servers?
8. Why do user-mode and kernel-mode execution use separate stacks?
9. Why do 2 MiB pages improve TLB efficiency, and why are large pages not used everywhere?
10. Is there a limit to the number of operations definable for an executive object? Explain.
11. Can `WaitForMultipleObjects` wait on two semaphores, one mutex and one critical section? Why?
12. Why is double initialization of a global variable dangerous, and how could `InitOnceExecuteOnce` be implemented?
13. Give three reasons a process can terminate. What extra reason applies to a modern application process?
14. Why must modern applications save state on every switch away instead of simply resuming from the old instruction point?
15. Why is LIFO reuse of process/thread IDs problematic in Windows, why does FIFO help, and why is the issue different in UNIX?
16. With a 20 ms quantum, a priority-24 thread has just begun running and I/O wakes a priority-28 thread. Roughly how long does the latter wait?
17. Would it ever make sense for current priority to fall below base priority? Explain.
18. Explain how Autoboost can reduce priority inversion.
19. Why can kernel threads attach to another process address space more easily than user-mode threads, and why might such a facility be useful?
20. Give two ways to reduce response time for threads in an important process.
21. Why can paging-related writes occur frequently even when plenty of free memory exists and working sets do not need trimming?
22. Why can whole-process swapping of modern applications be more efficient than page-by-page working-set trimming?
23. Why does the x86 self-map for a process always occupy the same kernel virtual-address range?
24. Why would 32-bit PTEs make the self-map occupy 4 MiB rather than 8 MiB?
25. If a virtual-address region is reserved but not committed, does it still have a VAD? Explain.
26. Which transition in Fig. 11.20 is a policy/strategy choice rather than a transition forced by an event?
27. If a physical page is shared by two working sets, where does it go when removed from the first, and then from the second?
28. Where does a modified stack page go when unmapped, and why is there no transition to the modified list in that case?
29. Why is using a notification event to signal release of an exclusive lock a bad design? How do lock hold time, quantum length and multiprocessors affect the answer?
30. Show how `NtCreateProcess` could be used as a checkpoint technique analogous to historical UNIX `dump` using `fork`.
31. Given the supplied logical-to-disk block map, determine the NTFS MFT extent entries.
32. If the Fig. 11.25 stream grows by one logical block allocated at disk block 66, how does its MFT record change?
33. In Fig. 11.28b, are the first two 8-block extents equal by accident or because of the compression scheme?
34. For a hypothetical Windows Vista Lite, which access-token fields from Fig. 11.29 could be removed without weakening security?
35. How can an information leak help defeat ASLR in a return-oriented programming attack?
36. Is an in-process DLL extension model safe for an RPC service that impersonates clients before loading the DLL? Explain.
37. Why does the Memory Manager prefer a NUMA page from the node of a thread's ideal processor? What if the thread runs elsewhere?
38. Give examples where an application can recover easily from a volume-shadow-copy backup.
39. Besides growing a process heap, give virtual-memory operations that require zero-filled pages for security.
40. Why is patching a cloud hypervisor/host OS harder than patching a guest OS, and what can be done?
41. Repeatedly export the Registry with `regedit` and observe changes during a session and after installing/removing software or hardware.
42. Implement a UNIX container format that emulates NTFS multiple streams, plus a second program that reports and extracts the components.
