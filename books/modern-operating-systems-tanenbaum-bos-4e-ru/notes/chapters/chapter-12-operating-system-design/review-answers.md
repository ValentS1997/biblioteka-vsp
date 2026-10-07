# RAG-grounded review answers — Chapter 12

These are chapter-grounded answers, not an official answer key. Design questions are answered conservatively from the chapter's principles; empirical/current-data tasks keep explicit limitations.

1. **Limits to hardware growth.** Physical and engineering constraints eventually dominate: power consumption, heat removal, memory/interconnect latency, finite parallelism, manufacturing limits and economic cost can all slow exponential improvement.

2. **Paradigm choice.** Compiler: algorithmic/sequential. Photo editor: event-driven. Payroll: algorithmic/batch. Hybrids are possible, but these choices minimize unnecessary state machinery.

3. **Filesystem vs DNS naming direction.** No fundamental reason requires either text order. Both encode traversal in a hierarchy; the difference is convention and parsing direction.

4. **Redundant calls.** The clearest examples are `creat`, which can be expressed with `open` plus create/truncate/write flags, and `dup`, which can be expressed through `fcntl` descriptor-control functionality. Extending the list without semantic loss is `[Needs confirmation]`.

5. **Swapping layers 3 and 4.** In Fig. 12.1, layer 3 provides threads/scheduling/synchronization and layer 4 models drivers as threads. Moving drivers below the thread layer removes the clean dependency on ordinary scheduling and mutexes, forcing ad-hoc low-level execution/synchronization machinery.

6. **Semaphores over message passing.** Yes. A user-space semaphore server can hold semaphore state. `down` and `up` become messages; when the count is unavailable the server delays the reply until another client performs `up`.

7. **System-call optimization.** Over 10 s there are about 1000 calls. At 2 ms each they consume 2 s. Halving them to 1 ms saves 1 s, reducing total time to about 9 s. Speedup = `10/9 ≈ 1.11×`, or about **11.1%**.

8. **External vs internal names.** External names are typically longer human-readable strings, often hierarchical and not necessarily globally unique. Internal names are commonly compact integers/indices, unique within a table/namespace while valid, and usually flat.

9. **2× vs 1.5× table growth.** Doubling causes fewer reallocations/copies but wastes more spare memory. Growing by 1.5× reduces unused capacity but expands/copies more often.

10. **Eliminating `found`.** Yes. If no match is found, `p` reaches `&proc_table[PROC_TABLE_SIZE]`; if a match is found, `break` leaves `p` inside the table. A post-loop boundary test can replace the flag.

11. **Conditional compilation for IDE vs SCSI.** It can be done, but is usually poor design. CPU architecture/word length may require different binaries; IDE and SCSI are runtime device differences that can coexist and are better handled behind driver/device interfaces.

12. **Costs of indirection.** Extra lookup time, lookup tables, more state to maintain, potential stale mappings and more difficult debugging. Flexibility is purchased with overhead and complexity.

13. **Reentrancy and static globals.** Immutable globals are fine. Mutable static/global state must be synchronized or otherwise concurrency-safe; unprotected mutable global state breaks reentrancy.

14. **Macro disadvantages.** Code expansion, possible multiple evaluation of arguments, weaker type checking, side-effect hazards, precedence mistakes and harder debugging.

15. **Fast 32-bit parity.** A 65,536-entry table fits in 64 KiB if each entry is one byte. XOR the two 16-bit halves and index a parity table:
   ```c
   #define parity32(x) parity16[((uint32_t)(x) >> 16) ^ ((uint32_t)(x) & 0xffff)]
   ```
   The measured speedup over a 32-iteration loop is `[Needs confirmation]`.

16. **24-bit palette.** For ordinary 24-bit RGB compression it is not useful: the index is already 24 bits per pixel while the palette adds large overhead. It only makes sense if the palette carries richer semantics than the original pixel representation.

17. **Palette break-even.**
   - 8-bit palette: 256 × 3 = 768 bytes; indexed pixels save 2 bytes each, so break-even is **384 pixels**.
   - 16-bit palette: 65,536 × 3 = 196,608 bytes; indexed pixels save 1 byte each, so break-even is **196,608 pixels**.
   This uses the chapter's simplified RGB/palette model.

18. **Keeping root files open.** It can save some inode loads for root entries, but pathname lookup still has to search directories and resolve deeper components. It does not replace pathname caching and gives limited benefit.

19. **Metadata for a remote-file hint.** Add validation data such as modification time/version, file size and preferably a stable file identifier or content hash. A hint must still be checked before use.

20. **Delete/recreate aliasing.** Add a generation number, stable object/file ID or creation/version token to the hint and validate it remotely. Reusing a pathname will then not silently identify a different file.

21. **When locality hurts streaming.** Yes. A placement policy optimized around directory locality can interleave input/output extents and increase seeks or fragmentation. Sequential-access detection, read-ahead/write-behind and extent preallocation can mitigate this.

22. **Brooks vs MINIX.** Brooks' estimate concerns large projects where planning, interfaces, coordination, integration and system testing dominate. Early MINIX was much smaller, had a tightly controlled scope and essentially no large-team communication overhead.

23. **Naive Windows cost.** Using the chapter's 50–100 million line estimate:
   - 50,000–100,000 programmer-years at 1000 lines/year;
   - × $100,000 = **$5–10 billion**.
   This is exercise arithmetic, not an estimate of actual Microsoft expenditure. Reused code, uncertain line-count boundaries and the heuristic itself weaken the model.

24. **100 GiB RAM-disk PC.** Chapter RAG has no current RAM-price dataset. Formula: `100 GiB × current price/GiB + battery-backed persistence/control + remaining PC hardware`. Current numeric cost and competitiveness are `[Needs confirmation]`.

25. **Features removable from an embedded appliance.** Depending on requirements: multiuser login, arbitrary program installation, shell/desktop GUI, dynamic device discovery, broad driver loading, general-purpose swapping/VM, many filesystems, legacy compatibility and support for arbitrary workloads.

26. **Double-precision addition.** Standard C already abstracts this:
   ```c
   double add_double(double a, double b) { return a + b; }
   ```
   If conditional compilation is required, only the truly machine-dependent representation/helper should vary with a configuration macro; duplicating identical addition logic would violate the chapter's orthogonality principle.

27. **Linear vs indexed string search.** Compare a linear scan with a hash table or sorted array plus binary search. Linear search can win for small arrays due to tiny setup cost; indexed methods scale better. The requested crossover is runtime-dependent and remains `[Needs confirmation]`.

28. **In-memory filesystem simulator.** Minimal components: in-memory inode/file table, hierarchical directories mapping names to internal IDs, file-data buffers, allocation/free logic, create/open/read/write/unlink operations and consistency checks. The requested working program and test output remain `[Needs confirmation]` until implemented and run.
