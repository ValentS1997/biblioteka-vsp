# Review answers — RAG-grounded

These answers are derived from chapter 5 only. They are not an official publisher answer key. Calculations use the chapter's models and the assumptions stated in the questions. Missing figure detail, unstated parameters and empirical program results remain `[Needs confirmation]`.

1. The logical model still separates device behavior from the interface presented to the system, but the electronic controller no longer needs to be a large separate board. It can be integrated into a low-cost chip, motherboard logic or the device itself. The abstraction survives; the physical packaging changes.

2. There is a source mismatch: Table 5.1 contains **802.11n = 37.5 MB/s**, while the question asks about **802.11g**. Using the table entry actually present in RAG, a 1 MB/s scanner can be carried easily because `1 < 37.5 MB/s`. The exact 802.11g-specific answer is **[Needs confirmation]**.

3. Parallel probing moves toward the source's “snooping/forwarding” alternative: I/O logic must observe memory-bus addresses fast enough to decide whether to respond. The chapter explicitly notes that slower I/O devices may not be able to inspect high-speed memory-bus requests at memory speed, so the optimization increases hardware complexity and timing pressure.

4. **Precise interrupts** greatly simplify OS recovery/restart because architectural state has a clean boundary. Their cost is more CPU logic, bookkeeping and silicon area. **Imprecise interrupts** can simplify/faster the processor core, but force the OS to reconstruct partially completed/out-of-order work and can make interrupt handling and restart much slower.

5. The wording is ambiguous about whether request and response are serial bus occupancy. Under the conservative serial interpretation, one 32-bit word consumes `40 + 40 = 80 ns`; one channel therefore needs 50 MB/s and five simultaneous channels need **250 MB/s**. If the 40-ns requests can be fully pipelined with responses, the aggregate data rate can reach **500 MB/s**. Exact expected convention: **[Needs confirmation]**.

6. Including one command and one acknowledgement:
   - a) word-at-a-time mode: **`1002(t1 + t2)`**;
   - b) burst mode: command `(t1+t2)` + one acquisition for the 1000-word burst `(t1+1000t2)` + acknowledgement `(t1+t2)` = **`3t1 + 1002t2`**.
   
   Because `t1 >> t2`, burst mode saves almost all repeated bus-acquisition overhead.

7. DMA can copy memory→memory by first issuing a memory read into the DMA controller and then a second bus transaction to write the word to the destination. Advantage: CPU is freed from doing the copy and can execute other work. Disadvantage: this DMA mode needs two bus cycles per word and the chapter notes that DMA hardware may be slower than the CPU for some workloads.

8. The interrupt pushes `32 + 1 + 1 = 34` words. At 5 ns per memory write, state saving alone takes **170 ns**, giving a theoretical upper bound of about **5.88 million interrupts/s**. This ignores handler execution and state restoration, so it is only an upper bound.

9. Interrupt latency becomes dependent on how long all already-issued instructions need to finish. A long or stalled instruction can therefore delay interrupt service substantially, which is especially bad for real-time I/O.

10. Immediate acknowledgement is possible only if the system is ready for another interrupt. The chapter explains why acknowledgement is often delayed: keeping the interrupt controller from issuing another interrupt prevents competition/nesting until important state has been saved and the handler is ready for new events.

11. Not necessarily. With a filled pipeline, the saved PC is not by itself a clean boundary between completed and uncompleted work; older instructions can still be in flight when the handler's first instruction is fetched. Without flushing, completion tracking or rollback, the four precise-interrupt conditions are not guaranteed.

12. A page has `50×80 = 4000` characters. At 6 pages/min, the printer produces **400 characters/s**. Interrupt handling consumes `400×50 µs = 20 ms/s`, or **2% of one CPU**. Under the source model, interrupt-driven output is therefore reasonable.

13. Define a standard driver interface/function table and allow a new driver to be loaded/registered against it. The device-independent layer talks to the standard interface rather than being rewritten for each device; this is the architecture the chapter describes.

14. 
   - a) track/sector/head calculation — **device driver**;
   - b) writing device registers — **device driver**;
   - c) access-permission check — **device-independent I/O software**;
   - d) binary integer → ASCII formatting — **user-space I/O library**.

15. Source-model time per 1024-byte packet:
   - sender user→kernel copy: 1.024 ms;
   - kernel→controller copy: 1.024 ms;
   - 8192 bits at 10 Mbit/s: 0.8192 ms;
   - final-bit propagation delay: 0.001 ms;
   - receive interrupt/handling: 1 ms;
   - receiver controller→kernel: 1.024 ms;
   - kernel→user: 1.024 ms.
   
   Total ≈ **5.9162 ms**, so maximum payload throughput is about **173,084 B/s ≈ 1.385 Mbit/s**. This illustrates the chapter's point that copying and interrupt overhead can dominate raw link speed.

16. Spooling lets user processes finish producing output without directly owning the exclusive printer. Jobs are placed in a spool directory and one daemon, the only process permitted to use the printer special file, serializes them. This prevents a process from holding the printer open for hours.

17. 7200 rpm = 120 revolutions/s, so one revolution is 8.333 ms. With 200 sectors/track, one sector passes every `8.333/200 ≈ 0.04167 ms`. During a 1-ms track move, about **24 sectors** pass. Required skew: **24 sectors**.

18. One revolution takes 8.333 ms. With 500 sectors on the track, one sector takes **16.67 µs** to pass under the head.

19. `500 × 512 × 120 = 30,720,000` bytes/s, so maximum sequential media rate is **30.72 MB/s** (decimal).

20. RAID 2 uses a Hamming-code arrangement and can correct a single missing/error bit while delivering high aggregate transfer, but at the price of synchronized disks and substantial parity overhead. RAID 3 exploits the fact that a failed drive's position is already known, so one parity drive is sufficient. Under the chapter's comparison, RAID 2 has little practical advantage for ordinary disk-failure handling and is mainly a historically more elaborate design.

21. The array fails if at least two disks fail:
   **`P = 1 - (1-p)^k - kp(1-p)^(k-1)`**.
   For small `p`, the leading approximation is **`C(k,2)p²`**.

22. Source-level comparison:

   | RAID | Read | Write | Space overhead | Failure tolerance |
   |---|---|---|---|---|
   | 0 | high for large striped requests | high | none | no redundancy; array reliability is worse than one disk |
   | 1 | can use either mirror; read concurrency can improve | each block written twice | 100% mirror overhead | excellent for one disk of a pair |
   | 2 | very high aggregate transfer | high aggregate transfer | multiple Hamming/parity disks | one disk, with code reconstruction |
   | 3 | high sequential transfer | parity involved | one parity disk | one known failed disk |
   | 4 | independent block reads | small writes expensive; parity disk bottleneck | one parity disk | one disk |
   | 5 | good parallel reads | parity read/modify/write penalty, but parity distributed | parity capacity distributed across disks | one disk |

23. `1 ZiB = 2^70 bytes`, `1 PiB = 2^50 bytes`; therefore **`2^20 = 1,048,576 PiB`** in one ZiB.

24. The chapter itself marks this as requiring physics knowledge beyond the chapter's I/O discussion. The RAG material retrieved for chapter 5 does not supply the needed physical derivation. **[Needs confirmation]**.

25. The chapter supports only a partial comparison: magnetic disks are presented as comparatively fast read/write secondary storage, while DVD/Blu-ray optical media are important for distribution of software/data/movies. A complete source-grounded list of optical-vs-magnetic physical advantages/disadvantages is **[Needs confirmation]**.

26. No. Interleaving exists to give a controller time to move one sector from its buffer to memory before the next physical sector arrives. If the controller can stream every byte directly into memory at media rate without buffering delay, that reason for interleaving disappears.

27. Yes. Interleaving solves the within-track service-time problem; cylinder/track skew compensates for the time consumed while moving the heads to the next track/cylinder. They solve different delays.

28. 
   - a) Capacity:
     `16 × 100 × (160+200+240+280) × 512 = 720,896,000 bytes`
     = **720.896 MB ≈ 687.5 MiB**.
   - b) One revolution at 7200 rpm is 8.333 ms. A 1-ms adjacent-cylinder seek is 12% of a revolution. Minimum whole-sector skew by zone is approximately:
     **20, 24, 29, 34 sectors** for 160, 200, 240, 280 sectors/track respectively.
   - c) Fastest outer-zone transfer:
     `280×512×120 = 17,203,200 B/s`
     = **17.2032 MB/s ≈ 16.41 MiB/s**.

29. If cylinder count, physical size and rotational mechanics remain the same while linear bit density doubles, **capacity roughly doubles** and the sequential transfer rate can roughly double because more bits pass under the head per revolution. Seek time and rotational latency remain essentially unchanged under those assumptions. The chapter does not establish a parameter that must become worse.

30. Existing BIOS/boot code, operating systems and utilities that assume the four-entry MBR layout would no longer understand the modified structure. The chapter's actual migration path is a new partition scheme (GPT), so a proprietary “more than four MBR entries” design would require coordinated software support and sacrifice compatibility.

31. Starting at cylinder 20:
   - a) FCFS: total movement **146 cylinders**, so **876 ms**.
   - b) SSF sequence can be `20→22→10→6→2→38→40`: **60 cylinders**, **360 ms**.
   - c) elevator initially upward: `20→22→38→40→10→6→2`: **58 cylinders**, **348 ms**.

32. One-direction circular scanning makes waiting time more uniform with respect to disk position: after reaching the high end, the head returns and begins another pass instead of favoring requests according to alternating direction. The source describes it as a small modification giving more uniform response behavior.

33. Not necessarily. If Harry performs one synchronous random read and waits for it before issuing the next, the driver's pending-request queue contains essentially one request. There is nothing for elevator/sector reordering to optimize, so FCFS-like performance is expected even if the driver really implements those algorithms.

34. The source algorithm requires the block number to be written to nonvolatile storage **before** stable writing starts. Therefore a correct implementation does not permit “data write first, marker later.” If it did, a crash could leave recovery unaware of the only block that needs examination and the stable-storage abstraction could be broken.

35. Yes under the chapter's failure model, because recovery can be repeated. After each partial recovery step there remains at least one usable copy or a pair that can again be classified by ECC/content after reboot. Re-running recovery converges to two matching valid copies.

36. The dangerous case is when a physically corrupted write nevertheless appears to have a valid ECC.
   - a) crash before either write: old/old, safe;
   - b) crash during disk 1 write: if corrupted disk 1 falsely appears valid, recovery may see two valid-but-different blocks and copy disk 1 to disk 2, destroying the old good value — abstraction fails;
   - c) after disk 1, before disk 2: valid new disk 1 is intentionally copied to disk 2, safe;
   - d) during disk 2: valid disk 1 wins under the recovery rule, so the intended new value survives;
   - e) after both: new/new, safe.
   
   Thus the ECC-detectability assumption is essential.

37. `60 × 2 ms = 120 ms` per second. CPU time spent on timer handling = **12%**.

38. At 500 MHz one tick is 2 ns.
   - a) 1 ms requires **500,000 counts**, so at least **19 bits**.
   - b) 100 ms requires **50,000,000 counts**, so at least **26 bits**.

39. Delta-list form:
   - at time 5000: events `5008,5012,5015,5029,5037` → deltas **[8, 4, 3, 14, 8]**, next signal = **8**;
   - at time 5005: **[3, 4, 3, 14, 8]**, next = **3**;
   - at time 5013: events 5008 and 5012 have fired; remaining `5015,5029,5037` → **[2, 14, 8]**, next = **2**;
   - at 5017, after 5015 has fired, adding 5033 among 5029 and 5037 gives absolute events `5029,5033,5037` → deltas **[12,4,4]**;
   - at time 5023: **[6,4,4]**, next = **6**.

40. `2^32` seconds after 1970-01-01 is **7 February 2106**. The chapter already discusses wider counters/alternative timekeeping, so the intended expectation is that operating systems should migrate before the wrap rather than rely indefinitely on that representation.

41. The source contains an arithmetic contradiction: 80×80 is **6400**, not 6480.
   
   Using the stated dimensions and assuming the character bitmap is 1 bit/pixel, one 8×16 cell is 128 bits = 16 bytes. Moving 6400 cells therefore copies 102,400 bytes, taking **5.12 ms** at 50 ns/byte. If the source-literal 6480 count is used instead, the result is **5.184 ms**.
   
   With 80 characters per line and 5.12 ms per scroll, the equivalent character throughput is about **15,625 chars/s**; as an 8-bit raw stream that is **125 kbit/s**. Exact serial “baud” framing is not stated, so the framing-specific value is **[Needs confirmation]**.
   
   Drawing a new 80-character line costs `80×5 µs = 0.4 ms`; scroll + line drawing ≈ 5.52 ms, or about **181 lines/s**. Using the source-literal 6480 variant gives about **179 lines/s**.

42. The purpose of DEL/SIGINT is to stop the foreground computation. Pending output produced by that interrupted computation is no longer useful; allowing the queued text to keep printing would make the terminal appear not to have stopped the program. The chapter explicitly describes flushing accumulated input on INTR; the output-queue rationale here is an inference from the same interrupt semantics.

43. Move to row 5, column 7, then delete 6 characters:
   **`ESC [ 5 ; 7 H ESC [ 6 P`**
   (spaces shown only for readability).

44. `20 cm/s = 200 mm/s`. At 0.1 mm per mickey: **2000 mickeys/s**. At 3 bytes/report: **6000 B/s = 48 kbit/s**.

45. Yes. A 24-bit RGB representation contains only `2^24` discrete triples; real intensities/colors need not fall exactly on those quantized values. A photograph can therefore contain colors that can only be approximated, not represented exactly.

### Unnumbered source item after question 45

For a 16×24-pixel true-RGB character:
- storage = `16×24×3` = **1152 bytes/character**;
- at 100 ns/byte, copy time = **115.2 µs/character**;
- output rate ≈ **8681 characters/s**.

46. The graphics case is fully determined:
   `1024×768×3 = 2,359,296 bytes`; at 10 ns/byte → **23.59296 ms**.
   
   For the 80×25 text display, the question does not state how many bytes of video memory represent one text cell. General result:
   **`2000 × bytes_per_cell × 10 ns`**.
   If one byte/cell is assumed, that is 20 µs; if two bytes/cell, 40 µs. The exact source-grounded text-mode result is **[Needs confirmation]**.

47. Windows registers a window class because the OS/message-dispatch architecture needs to associate that class with its callback procedure (`WndProc`). In the X example, the application explicitly selects events, calls `XNextEvent`, and dispatches them itself; the chapter explicitly notes that X does not have the OS call an application procedure directly. Hence no analogous `RegisterClass` call is required.

48. Yes. `hdc` identifies the device/window drawing context and carries information not present in the rectangle coordinates: target drawable, clipping region, line width/color, fill attributes, font and other GDI properties. Coordinates alone do not identify where/how to draw.

49. The question does not state color depth. If the chapter's common 24-bit RGB representation is assumed:
   `400×160×24×10 = 15,360,000 bit/s`
   = **15.36 Mbit/s**, or **15.36%** of 100-Mbit/s Fast Ethernet before protocol overhead/compression. Without a stated pixel format, the exact result is **[Needs confirmation]**.

50. Yes. A single-user 1-Mbit/s test does not model aggregate demand. Multiple video users generate sustained streams, while web users add bursty traffic; all share the same network/server path. The result can be queueing, lower per-user throughput and larger interactive latency.

51. Two source-supported advantages:
   - centralized software installation/upgrade/administration;
   - centralized backup and pooling of memory/storage/resources.
   
   Two architectural disadvantages inferred from the chapter's thin-client model and question 50:
   - dependence on network bandwidth/latency;
   - dependence on the centralized service/server, so shared failures or overload affect many users.

52. At voltage `V/n`, CPU speed is `1/n`, so the 100-ms job takes `100n ms`. It must finish within the one-second inter-keystroke interval, hence `n ≤ 10`. Energy for the job scales as power `1/n²` times active time `n`, i.e. **1/n** of baseline. Optimal **`n=10`**; energy becomes **10%** of baseline, saving **90%**.

53. The chapter establishes that power saving depends on actually reaching idle states and that display, disk and CPU activity can prevent or delay them. The exact mechanism by which the user's X session prevents those states is not supplied in the retrieved chapter evidence. A source-consistent explanation is that the graphical environment generates additional I/O/CPU/display activity and wakeups compared with the text-only workload, reducing time spent in low-power states. Exact cause for the described laptop: **[Needs confirmation]**.

54. Source-consistent design:
   - create two equal fixed-size files representing disk 1 and disk 2;
   - implement stable write as write+read/verify file 1, then write+read/verify file 2;
   - implement stable read with retry/fallback to the second file;
   - implement recovery by comparing corresponding blocks and repairing according to validity/content;
   - optionally persist the “block currently being written” marker before the first copy.
   
   Actual program and fault-injection results: **[Needs confirmation]**.

55. Implement FCFS, SSF and elevator. Generate the same random sequence of cylinders 0–999 for all three, track current head position, add `abs(next-current)` for every move, and print the total cylinders traveled by each algorithm. Use a fixed random seed if reproducibility is required. Actual measured totals: **[Needs confirmation]**.

56. Maintain current time plus a delta-ordered list of pending expirations:
   - `S n`: set current time;
   - `T`: advance one tick, decrement head delta, fire/remove all zero-delta events;
   - `E n`: insert an absolute expiration into the delta list, adjusting neighboring deltas;
   - `P`: print current time, next expiration and timer-list head/state.
   
   The program should print each expiration event as it fires. Implementation/test output: **[Needs confirmation]**.
