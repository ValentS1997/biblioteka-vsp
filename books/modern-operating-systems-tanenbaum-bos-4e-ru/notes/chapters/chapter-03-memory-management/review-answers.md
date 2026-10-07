# Review answers — RAG-grounded

These answers are derived from chapter 3 only. They are not an official publisher answer key. Calculations use the models and assumptions stated in the chapter. Figure-only or environment-dependent information remains `[Needs confirmation]`.

1. Two reasonable disadvantages follow from the scheme itself: (a) protection granularity is coarse because every 2-KiB block has one key, so independently protecting smaller regions is impossible; (b) a 4-bit key gives only 16 values, so independently protected simultaneously resident domains are limited unless keys are reused. These are deductions from the mechanism; the source does not present a unique official pair.

2. **[Source contradiction]** The values are not inherently required to be equal: the chapter describes the base as the physical start and the limit as a size/bound. However, the source variants conflict. Review question 2 says figure 3.3 shows `16384/16384`, while prose on PDF 220 says the second program uses `16384/32768` even though it also calls the limit the program length. Exact numeric interpretation of the figure is therefore `[Needs confirmation]`; see `source-findings.md`.

3. A 32-bit word is 4 bytes. Moving nearly all 4 GiB requires about `2^30` words; each moved word needs one 4-ns read and one 4-ns write. Approximate time: `2^30 × 8 ns ≈ 8.59 s`. So roughly **8.6 s** in the stated worst case.

4. Applying the algorithms sequentially and splitting holes when needed:
   - first fit: **20, 10, 18 MiB**;
   - best fit: **12, 10, 9 MiB**;
   - worst fit: **20, 18, 15 MiB**;
   - next fit: **20, 18, 9 MiB**, assuming the next search resumes immediately after the previous placement as described in §3.2.3.

5. A **virtual address** is generated in the process's address space. A **physical address** identifies the actual RAM location placed on the memory bus after MMU translation. Virtual addresses from different processes may map to different physical locations.

6. Page number = `floor(address/page_size)`; offset = remainder.
   - 4 KiB pages: 20,000 → **page 4, offset 3616**; 32,768 → **page 8, offset 0**; 60,000 → **page 14, offset 2656**.
   - 8 KiB pages: 20,000 → **page 2, offset 3616**; 32,768 → **page 4, offset 0**; 60,000 → **page 7, offset 2656**.

7. From the text surrounding figure 3.9:
   - a) virtual 20 is page 0, which maps to frame 2 → **8192 + 20 = 8212**;
   - b) virtual 4100 is page 1, offset 4; the text layer does not expose page 1's frame number from the figure → **[Needs confirmation]**;
   - c) virtual 8300 is page 2, offset 108; page 2 maps to frame 6 → **24576 + 108 = 24684**.

8. Put the MMU **outside the CPU**, between the CPU and memory/bus. PDF 230 explicitly notes that an MMU can logically reside in a separate chip. The external MMU can translate addresses and generate page-fault/protection events even if the 8086 itself does not implement them.

9. At minimum: an MMU/address-translation mechanism, page tables or equivalent translation state, a present/absent indication, protection checking, a trap/page-fault mechanism, and enough CPU/OS support to restart the faulting instruction. A TLB improves speed but is not logically required. R/M bits are useful for replacement and may be emulated if hardware does not provide them.

10. The mechanism is useful whenever a smartphone OS creates processes that initially share address-space contents: unchanged pages can remain shared and only written pages are copied. The chapter supports the mechanism through `fork`/copy-on-write; whether a particular smartphone process model benefits materially is **[Needs confirmation]**.

11. The condition is that successive accesses land on different pages and the reuse distance exceed TLB capacity. Assuming a 4-byte `int`, a 4-KiB page holds 1024 array elements, so one valid example is **M = 1024**. For repeated loops, use more than 64 distinct pages, e.g. **N > 64×1024**. With 64 or fewer distinct pages, later passes can hit after warm-up; exact behavior also depends on TLB replacement policy.

12. In the simple model where resident RAM pages need not simultaneously consume swap space, the minimum backing-store capacity is approximately **`n·v − r` bytes**, bounded below by zero. It is a pessimistic sizing model because real processes often use only part of their virtual space and clean executable/shared-library pages can be reread from files instead of swap.

13. Average instruction time is **`1 + n/k` ns**: every instruction costs 1 ns and one in each k instructions adds n ns.

14. Page size 8 KiB = `2^13`, so a 32-bit space has `2^19 = 524,288` PTEs. Copying them at 100 ns/word takes **52.4288 ms**. In a 100-ms run interval, about **52.4%** is spent loading the page table.

15. 
   - a) `48 − 12 = 36` virtual-page bits → **`2^36` PTEs** in a single-level table.
   - b) TLB efficiency is still high for sequential array traversal: the code page remains hot, and after the first miss for each data page, many consecutive array elements are serviced from that same translation. The TLB does not need to retain thousands of old pages because the access stream moves forward.

16. This question supplies the parameters used by question 17; there is no separate computation.

17. Treating a TLB miss without page fault as 1 ns TLB lookup + 100 ns PTE lookup, and a fault as adding 6 ms:
   `0.99×1 + 0.0099×101 + 0.0001×6,000,101 ≈ 602 ns`.
   Effective translation time is therefore about **602 ns**. The rare page faults dominate the average.

18. 
   - a) A multilevel table saves memory for sparse address spaces because lower-level tables need not exist for unused regions.
   - b) A 16-KiB page has 14 offset bits, leaving 24 VPN bits. One second-level table that fits in one 16-KiB page holds `16384/4 = 4096 = 2^12` PTEs, so the natural split is **12 bits + 12 bits**.

19. PTE width does not by itself determine addressable memory. Pentium Pro used 64-bit entries, but the hierarchy still had only 4 top entries, 512 directory entries, 512 page-table entries and 4-KiB pages: `4×512×512×4096 = 2^32` bytes = **4 GiB**. Extra PTE bits can carry flags or future/extended address information without increasing the currently reachable page count.

20. Offset bits = `32 − 9 − 11 = 12`, so page size is **4096 bytes (4 KiB)**. VPN bits = 20, so the address space contains **`2^20 = 1,048,576` pages**.

21. 
   - a) Single-level: one PTE for every virtual page → **1,048,576 entries**.
   - b) Two-level 10+10: the top table has 1024 entries. Only two second-level tables are needed—one for the lowest region and one for the highest stack region—so allocated entries are **1024 + 2×1024 = 3072**.

22. The text layer supplies page size, addresses and instruction sizes but not enough machine-specific stack/call semantics to derive one unambiguous full trace. Confirmed portions are: instruction at 1020 → page 1; data 6144 → page 12; subsequent instruction at 1024 → page 2; procedure at 5120 → page 10; stack accesses just below 8192 → page 15. The exact complete reference string is **[Needs confirmation]**.

23. On a TLB hit, cost is 1 ns. On a miss, the 1-ns associative lookup is followed by the 5-ns page-table access, for 6 ns total. Solve `h·1 + (1−h)·6 = 2`: **h = 0.8 = 80%**.

24. Associative memory compares the requested virtual-page key **in parallel against all TLB entries**, using dedicated comparators. This gives very fast lookup but scales poorly in area, wiring, power and comparison hardware as the number of entries grows, which is why TLBs remain relatively small.

25. Page size 8 KiB = `2^13`; a 48-bit virtual address therefore has 35 page-number bits. A conventional one-level table requires **`2^35` entries**.

26. RAM contains `256 KiB / 8 KiB = 32` physical frames, so the inverted table has 32 resident mappings. To make average hash-chain length strictly less than 1, use more than 32 buckets. The next power of two is **64 buckets**.

27. A compiler cannot in general know the exact future page-reference sequence because it depends on runtime control flow, data and input, so it cannot implement the online optimal algorithm. The chapter does note that a trace from one simulator run can be used to evaluate optimal replacement on a second run for the same program/input. Practical improvement instead relies on locality, working-set/prepaging information or replacement approximations rather than perfect future knowledge.

28. 
   - a) With a 512-page cyclic scan and fewer than 512 frames, the reuse distance is larger than the resident set. LRU/FIFO/clock therefore repeatedly evict pages shortly before the next cycle needs them, causing sustained faults.
   - b) Exploit knowledge of the repeating sequence: preferentially evict pages just passed in the cycle—the pages whose next use is farthest away—while retaining the pages coming soon. This approaches the optimal policy far better than recency/FIFO for this synthetic pattern.

29. Simulating four initially empty frames:
   - FIFO: **6 page faults**;
   - LRU: **7 page faults**.

30. Reading the order in the question as B,C,D,E,F,G,H,A with R bits `1,1,0,1,1,0,1,1`, second chance skips B and C after clearing their R bits and removes **D**, the first page encountered with R=0.

31. Starting all aging counters at zero and, at each tick, shifting right then inserting R as the MSB gives:
   - page 0: **01101110** (110);
   - page 1: **01001001** (73);
   - page 2: **00110111** (55);
   - page 3: **10001011** (139).

32. Example: **0,1,2,0,3**, assuming the clock hand initially points at the oldest frame 0. Before reference 3, LRU regards page 1 as least recently used, while clock sees R=1 on 0,1,2, clears them during a full pass, then evicts page 0. Thus first victims differ: **LRU → 1; clock → 0**.

33. The answer depends on the last-use timestamp printed only inside figure 3.19, which is not exposed by the chapter's text RAG. Exact yes/no results for `τ=400` and `τ=1000` are **[Needs confirmation]**.

34. 
   - a) The chapter's working-set model says the timer periodically clears R. Therefore the entries whose R=1 (pages 1 and 2) become R=0; other fields are unchanged by that timer action.
   - b) Exact WSClock behavior also depends on the clock-hand starting position, which is not present in the extracted question/table, so the unique final table is **[Needs confirmation]**. If the hand starts at page 0, a source-consistent scan would schedule dirty old page 0 for writeback, refresh/clear recently referenced pages 1 and 2, then select old clean page 3; page 4 would become valid in that frame with a current-use timestamp and read state.

35. 
   - a) FIFO uses **time/order of arrival into memory**; LRU uses **time/order of most recent reference**; optimal uses **time until the next future reference**.
   - b) Maintain the relevant attribute for resident pages; on a fault, choose the page whose attribute makes it least valuable under that policy (oldest arrival, oldest past use, or farthest future use), evict/write it if required, and install the demanded page.

36. Average per-page overhead is 5 ms seek + 5 ms rotational delay. If 5 ms is average rotational latency, one full rotation is about 10 ms; transferring 2 KiB from a 1-MiB track takes about 0.0195 ms and 4 KiB about 0.0391 ms.
   - 2-KiB pages: 32 pages → **≈320.625 ms**.
   - 4-KiB pages: 16 pages → **≈160.625 ms**.

37. 
   - NRU: page **2** is the only class-0 page (R=0,M=0).
   - FIFO: page **3** was loaded earliest (time 110).
   - LRU: page **1** has the oldest last reference (265).
   - second chance: starting with FIFO order, pages 3 and 0 receive a second chance because R=1; page **2** is then the first R=0 victim.

38. The chapter explicitly describes a **minor page fault** where a page is already resident—possibly because another process brought it in—but the process's PTE has not yet been installed. Therefore B's PTE may be updated lazily until B actually references the shared page. The cost is an extra minor fault, page-table/TLB update and trap/restart, but **no disk read**. Exact eager-versus-lazy update policy is implementation-specific `[Needs confirmation]`.

39. Row-major fragment **B** is much better. One page holds 128 integers = two 64-integer rows. Sequential row-major traversal touches each of the 32 data pages once → **32 data page faults**. Fragment A walks by columns; for each column it cycles through all 32 data pages with only three data frames, so it faults once per page per column → **32×64 = 2048 faults**.

40. 
   - a) Keep or discover a copy of the page in another server's RAM and transfer it over the network into A's free frame, then update A's mapping as for an ordinary page-in.
   - b) It is useful only when remote-RAM transfer latency/bandwidth is better than local-disk page-in and when the system can locate the page, enforce protection and maintain valid ownership/coherence. Exact transport/protocol is not supplied by the chapter and is **[Needs confirmation]**.

41. The drum matches whole-memory swapping well: its 4K words correspond to the machine's entire 4K-word memory image, there is no seek arm, and transfer can begin at an arbitrary word as the drum rotates. This gives predictable, relatively low-overhead sequential swap transfer compared with a general disk layout.

42. With 4-KiB pages: text needs 8 pages, data needs 5 because 16,386 exceeds 4 pages by 2 bytes, stack needs 4 → **17 pages**, but the address space has only 16 → **does not fit**. With 512-byte pages: 64 + 33 + 31 = **128 pages**, exactly the available `65536/512 = 128` → **fits exactly**.

43. Original extra fault cost is `15,000 × 2 ms = 30 s`, so useful non-fault execution accounts for the other 30 s. Doubling memory doubles the mean fault interval, halving faults to 7500 → 15 s fault overhead. New runtime = **30 + 15 = 45 s**.

44. 
   - a) Read-only program text can be discarded instead of stored in swap and reread from its executable file when needed; the chapter explicitly describes this optimization.
   - b) Data can use the same idea only while a valid file-backed copy exists and the page has not diverged from it. Modified anonymous/data pages need separate backing storage unless they are otherwise reconstructible.

45. In the worst alignment, the **instruction itself can straddle two pages** and the referenced 32-bit operand can straddle another two pages. Therefore a single execution can require up to **4 page faults**, with restart after each missing page is supplied.

46. **Internal fragmentation** is unused space inside an allocated fixed-size unit, e.g. the unused tail of a page; paging causes this. **External fragmentation** is free memory split into holes between variable-size allocations; pure segmentation causes this and may require compaction.

47. **Yes.** The TLB can cache the final translation keyed by the virtual identity including segment/page information, so a hit yields the physical frame without repeating both the segment-descriptor and page-table walks. The MULTICS discussion explicitly describes TLB use to bypass those lookups.

48. Offset is 10 bits, so page size = 1024 bytes.
   - a) segment 1/page 1 → frame 14; physical = `14×1024 + 3 = 14339`.
   - b) write to segment 0 violates read+execute protection → **protection fault**.
   - c) segment 1/page 4 is on disk → **page fault**.
   - d) executing from segment 1 violates read+write protection → **protection fault**.

49. Virtual memory can be unacceptable when deterministic timing is required, especially small embedded/real-time systems where unpredictable page-fault I/O is undesirable. Omitting VM can provide simpler hardware/software, lower translation overhead and more predictable memory-access timing, at the cost of smaller/fixed physical-memory constraints and weaker abstraction.

50. Two guest OSes cannot both directly control the same physical frames, MMU and page tables as if each owned the machine. Their virtual-to-physical mappings must be isolated and then translated again to real machine memory. The chapter points ahead to **shadow or nested page tables** as mechanisms used when virtual machines each require their own virtual memory.

51. This requires scanning the user's actual computer and measuring executable sizes, so numeric histogram/mean/median and a fitted PTE size are **[Needs confirmation]**. Source-grounded procedure: enumerate the specified executables, exclude scripts (the source mentions `file` on UNIX), compute size distribution, then compare expected internal-fragmentation loss and page-table overhead for candidate page/PTE sizes.

52. Source-grounded simulator design: keep frame state, one R bit and an aging counter per resident page; at each simulated timer tick shift counters right and insert R at the MSB, then clear R; on a fault evict the smallest counter. Run the same reference file across different frame counts and report faults/1000 references. The requested graph/data require execution and are **[Needs confirmation]**.

53. Use a circular list of resident frames containing page id, R, M (fixed to 0 in the miniature version) and last-use time, plus the WSClock hand and threshold `τ`. Timer events update reference-history state; on fault scan from the hand: clear/refresh recently used pages, reclaim old clean pages, otherwise continue around the clock. Supporting writes requires an M bit, dirty-page writeback scheduling and logic for continuing the scan while writes complete. Experimental outputs/graph are **[Needs confirmation]**.

54. A suitable experiment traverses a large array with controlled strides so the number of simultaneously reused page translations crosses TLB capacity; measure access time per step and compare regimes with good locality versus repeated TLB misses. Exact timing, confirmation on the current computer and comparison with an older architecture are **[Needs confirmation]** because no measurements are available in RAG.

55. Represent each process with its own generated reference stream and frame ownership/state. For **local** policy choose victims only among that process's frames; for **global** policy choose from all frames. The generator keeps the same page with probability p1, otherwise selects uniformly among other states. The requested validation and fault-rate comparisons require executing the simulator and are **[Needs confirmation]**.

56. Model each TLB entry as `(process_tag, virtual_page, frame/translation_state)`. With tags, entries from both processes can coexist and survive context switches; without tags, require all valid entries to belong to the current process, effectively forcing invalidation/refill on switches. Count refills/updates and their supplied cost, then normalize per 1000 references. Numeric results and graph require execution and are **[Needs confirmation]**.
