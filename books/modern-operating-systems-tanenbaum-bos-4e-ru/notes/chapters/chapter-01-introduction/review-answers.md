# Review answers — RAG-grounded

These answers are derived from chapter 1 only. They are not an official publisher answer key. Unsupported details are marked `[Needs confirmation]`. Source inconsistencies are preserved rather than silently corrected.

1. **Two functions:** provide convenient abstractions over raw hardware (“extended machine”) and manage/protect shared resources (“resource manager”).

2. **One application per OS class:**
   - mainframe — large batch/transaction/database workloads;
   - server — network file/print/web services;
   - multiprocessor — systems combining multiple CPUs/cores for parallel work;
   - personal computer — interactive single-user desktop/laptop applications;
   - handheld/mobile — smartphones and tablets;
   - embedded — controllers in appliances, cars and dedicated devices;
   - sensor-node — unattended distributed sensing such as fire/weather/perimeter monitoring;
   - real-time — industrial/avionics/control workloads with timing constraints;
   - smart-card — constrained payment or multi-applet card systems.

3. **Time sharing vs multitasking:** both multiplex execution, but time sharing is framed around interactive sharing of a computer among users/jobs with responsiveness as a goal; multitasking/multiprogramming more generally keeps several programs progressing and uses the processor efficiently.

4. **Cache line advantage:** fetching a whole nearby block exploits locality and avoids repeated slower memory transfers when adjacent bytes/words are used.

5. Without DMA, the CPU must participate in every byte transfer, consuming processor time that could otherwise run another task; I/O therefore interferes much more with effective multitasking.

6. Direct I/O controls shared hardware. Restricting such instructions to kernel mode prevents user programs from interfering with devices, other programs, or the OS itself.

7. Yes. The chapter traces IBM System/360 compatibility through later 370/4300/3080/3090 families and zSeries descendants, showing that the compatible-family idea remained alive.

8. **Assumption:** one byte per text character because the question does not specify separate attribute storage.
   - text screen: 25 × 80 = **2000 bytes** ≈ 1.95 KiB;
   - bitmap: 1200 × 900 × 24 / 8 = **3,240,000 bytes** ≈ 3164 KiB;
   - at $5/KiB in 1980: about **$9.77** and **$15,820.31** respectively.
   - present-day RAM cost: `[Needs confirmation]` because current market data is outside the chapter’s RAG-only source policy.

9. Example: maximizing resource utilization may favor long batches/large queues, while responsiveness/timeliness favors serving interactive work quickly. Reliability can also conflict with performance when additional isolation/checking adds overhead.

10. Kernel mode has privileged hardware/instruction access; user mode has a restricted instruction set. The split isolates applications from critical hardware and kernel state, reducing the blast radius of application errors and enforcing controlled entry through system calls/traps.

11. From the chapter’s binary storage convention:
   - heads = 255 GiB / (65,536 cylinders × 255 sectors/track × 512 B) = **32 heads**;
   - with two recording surfaces per platter: **16 platters**.
   - transfer time for 400 KiB at 100 Mbit/s = **32.768 ms**;
   - seek + rotational wait + transfer = 11 + 7 + 32.768 = **50.768 ms**.

   **[Source contradiction]** The question also says the 400 KiB are read “from one sector”, while it defines a sector as 512 bytes. Literal execution is impossible. The timing above treats 400 KiB as the transfer amount after positioning and does not silently repair that wording.

12. Kernel-only according to the chapter’s privilege model: **a)** disable interrupts, **c)** set the hardware clock, **d)** change memory-allocation/mapping state. Reading time **b)** need not itself control the machine.

13. In the simplified model where the four hardware threads are schedulable execution contexts and all three programs can start concurrently, completion time is the longest job: **20 ms**. Exact hyperthreading contention behavior is not modeled by the question.

14. After pipeline fill, one instruction completes every 1 ns: **10⁹ instructions/s**.

15. Using the stated hit probabilities:
   `0.95×1 ns + 0.05×(0.99×10 ns + 0.01×10 ms) = 5001.445 ns`,
   approximately **5.0 μs** average access time.

16. The chapter states that after starting I/O the OS blocks the caller **if necessary**. It does not define the exact write-buffer ownership/completion contract for this scenario. Therefore whether the caller can safely continue before physical disk completion is implementation-dependent here: `[Needs confirmation]`.

17. A **trap** is a controlled instruction/transition from user mode into kernel mode. The OS uses it to enter the kernel for a system call, validate/identify the requested service, execute it, and return to user mode.

18. A process table is needed to retain state for many processes that alternate on the CPU or are blocked. It is also needed on a single-user UNIX/Windows PC because one logged-in user can still have many application and background processes.

19. Yes. The chapter explicitly notes that mounting a filesystem on a non-empty directory hides the directory’s previous contents while the mount is active. That can intentionally overlay a tree, although the source notes that mounts are normally made on empty directories.

20. Exact failure conditions for `fork`, `exec`, and `unlink` are not enumerated in chapter 1. The chapter only gives the general rule that failed system calls return an error indication and programs must check results. **[Needs confirmation]** for a complete per-call error list.

21. Derived from the chapter’s time/space multiplexing definitions:
   - CPU — time;
   - memory — primarily space;
   - disk — space for stored data and time for device access;
   - network card — time;
   - printer — time;
   - keyboard — time/event sharing;
   - display — can involve both space (screen regions/windows) and time.
   This mapping is an application of the definitions, not a source table.

22. Chapter 1 explicitly explains short results for `read`, but does not specify partial-write semantics for `write`. A complete answer is therefore **[Needs confirmation]** under the RAG-only rule.

23. **[Source wording/code mismatch]** The source says `lseek(fd, 3, SEEK_SET)` moves to the “third byte”, which would yield **4, 1, 5, 9** from the displayed sequence. The code/wording relationship is not reconciled elsewhere in the retrieved chapter, so the artifact preserves the mismatch rather than silently choosing a different offset convention.

24. Seek 50 cylinders: 50 ms. Rotational wait: 5 ms. Transfer 10 MiB at 200 MiB/s: 50 ms. Total: **105 ms**.

25. A block special file models a random-addressable device made of blocks, such as a disk. A character special file models a character/byte stream device, such as a printer or modem.

26. The names do not have to match. The chapter shows that an application-facing API/library procedure can be distinct from the actual kernel system call (especially in Win32). For source compatibility, the programmer-visible API name/interface is the relevant contract.

27. Two benefits:
   - **isolation/protection:** one process does not directly overwrite another process or the OS;
   - **abstraction/virtual memory:** a process-visible address space is independent of physical RAM layout and may be larger than installed memory.

28. Functionally, usually not: a library/API can hide whether work is done in user space or via a kernel call. It can matter for performance because entering the kernel has additional cost and can block. Chapter 1 does not enumerate a broader set of circumstances.

29. The table shows no direct Win32 equivalents for standalone `execve`, `link`, `mount`/`umount`, `chmod`, and `kill`. A UNIX program using those semantics cannot be translated one-for-one; the programmer must redesign or emulate the behavior using Windows facilities. Exact replacement APIs are not supplied by this chapter.

30. Full portability is impossible because some OS work is inherently architecture-specific: privileged instructions, interrupts, device/I/O access, memory-management hardware and context switching differ by machine. The chapter supports keeping most code in C while isolating architecture-specific fragments with headers/conditional compilation. The question’s exact “two upper levels” wording is not explicitly resolved by the retrieved RAG, so that subpart remains **[Needs confirmation]** rather than being reconstructed from outside knowledge.

31. Put **mechanism** in the small privileged kernel and implement **policy** in less-privileged user-space services. The chapter’s scheduling example keeps the mechanism for selecting/running the highest-priority ready process in the kernel while letting user-space policy assign priorities. This reduces kernel size and improves replaceability/isolation.

32. One disadvantage is **overhead/performance loss**. The chapter describes software interpretation/translation as historically expensive and discusses the implementation complexity needed to trap/emulate privileged operations efficiently.

33. Using the chapter’s stated unit conventions:
   1. nanoyear, with a 365-day year assumption: **0.031536 s ≈ 31.5 ms**;
   2. megamicron: **1 m**;
   3. 1 Pbyte of memory under the chapter’s binary convention: **2⁵⁰ = 1,125,899,906,842,624 bytes**;
   4. 6000 Yg = **6 × 10²⁴ kg**.

34. The source gives the core control flow: prompt/read command → `fork` → parent `waitpid`; child `execve`. A testable shell additionally needs concrete input parsing, error checking and termination behavior. Redirection, pipes and background-job semantics are not specified enough in this chapter for a complete source-only implementation, so those details are **[Needs confirmation]**.

35. Expected result: resource exhaustion and potentially an unusable/hung system. The source explicitly restricts the experiment to a personal/disposable UNIX-like machine and warns not to run it on a shared time-sharing system without administrator permission. It also instructs `sync` first to flush filesystem buffers. No runnable unbounded-process script is reproduced in these artifacts.

36. The source proposes inspecting raw directory data with UNIX `od` or MS-DOS `DEBUG`, possibly by creating a directory on removable media under one OS and reading raw data under another OS that permits it. The filesystem-specific byte interpretation is **[Needs confirmation]** in chapter 1.
