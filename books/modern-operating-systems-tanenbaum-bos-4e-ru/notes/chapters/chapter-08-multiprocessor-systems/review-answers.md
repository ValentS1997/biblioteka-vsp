# Review answers — RAG-grounded

These answers are derived from chapter 8 only. They are not an official publisher answer key. Figure-only values and actual program/benchmark results remain `[Needs confirmation]`.

1. Yes. Both fit the chapter's distributed-system model better than a shared-memory multiprocessor or tightly coupled multicomputer: they use complete, independently administered computers connected by a network. The exact subcategory labels drawn in figure 8.1 are not fully represented in text RAG, so figure-specific placement is **[Needs confirmation]**.

2. The memory/interconnect must serialize the accesses to that word. Concurrent reads can all observe the same value; concurrent writes or read-modify-write sequences race unless an atomic/coherence mechanism orders them. This is why ordinary shared-memory access is insufficient for mutual exclusion.

3. Without cache, each CPU generates `200×10^6` memory/bus accesses per second. A 400 MHz bus can perform `400×10^6` one-cycle accesses/s, so **2 CPUs saturate the bus**; more than two overload it.

   With 90% cache hit, only 10% of accesses reach the bus: `20×10^6` accesses/s per CPU. Therefore **20 CPUs saturate the bus**.

   For 32 CPUs:
   [
   32 × 200M × (1-h) ≤ 400M
   ]
   so `1-h ≤ 0.0625`, hence **h ≥ 93.75%**.

4. The exact switch connectivity and route alternatives of figure 8.5 are not encoded in the text RAG. **[Needs confirmation]**.

5. Figure 8.7 is the per-CPU-OS model. Each CPU has its own OS tables and process set, so a signal for a process must be handled by the OS instance/CPU that owns that process. The exact signal-routing path in the figure is not described explicitly in the retrieved prose; cross-CPU delivery detail is **[Needs confirmation]**.

6. Figure 8.8 is the master–slave model. A trap/system call occurs on the CPU executing the user process, but the OS tables and system-call handling live on the master CPU. The request and required process state/arguments therefore have to be redirected to the master, processed there, and the result returned to the slave process. This redirection is the extra immediate problem absent from the per-CPU-OS model.

7. Source-consistent pattern:

```text
enter_region:
    while ordinary_read(lock) != 0:
        continue
    old = atomic_TSL(lock)
    if old != 0:
        goto enter_region
    return
```

   Ordinary reads keep the cache line shared while the lock is busy; TSL is executed only when the lock appears free. The read is not a guarantee: simultaneous contenders still rely on atomic TSL to select one winner.

8. The chapter does not prescribe a single definitive choice. A reasonable chapter-grounded conclusion is that parallelizing common OS/library services can benefit many applications without rewriting each one, while application-level parallelism is necessary when the application's own computation dominates. For general-purpose many-core systems, shared scalable services give broader leverage, but both layers must scale.

9. Mutexes on shared structures are necessary but not always sufficient as a design discipline. The chapter recommends independent kernel critical regions plus mutexes for shared tables used by more than one region. If all invariants could be expressed solely as correctly ordered per-structure locks, a separate coarse critical-region lock would be redundant; in practice cross-structure operations and lock ordering still require explicit critical-section design.

10. Each failed TSL makes the 16-word cache block move to the requester, and the owner's intervening write moves it back: `16 + 16 = 32` bus cycles per 50-cycle polling interval. Wasted fraction:

[
32/50 = 0.64
]

   **64% of bus bandwidth** is consumed by cache-block ping-pong under the stated model.

11. Mutual-exclusion safety can still hold because TSL remains atomic, but without a maximum the delay can double without bound after repeated failures. A waiter can therefore respond arbitrarily late after the lock becomes free. The source's maximum bounds this responsiveness/performance failure.

12. Yes. Initialize a register to 1 and atomically `SWP` it with the lock word. If the value returned from memory is 0, the caller changed the lock from 0 to 1 and acquired it. If the returned value is nonzero, retry/back off. Release by writing 0 to the lock. Atomicity of SWP is the essential property.

13. TSL requires two bus cycles: one read and one write. CPU instruction execution takes 5 ns; two bus cycles take `2×10=20 ns`. One loop therefore takes 25 ns, of which the bus is occupied for 20 ns:

[
20/25 = 0.8
]

   **80% of the bus bandwidth** is consumed.

14. Yes, affinity can reduce TLB misses: PDF 603 explicitly notes that useful TLB entries may remain on the same CPU. It does not directly reduce page faults, because page residency is a memory-management property rather than a CPU-local cache/TLB property. It may influence locality indirectly on NUMA, but the chapter does not claim a direct page-fault reduction.

15. The source identifies the topology classes but the figure's exact node counts are not fully encoded. Source-consistent diameter formulas are:
   - star with one switch: **2 links** between two hosts;
   - ring of `n` nodes: **⌊n/2⌋**;
   - `k×k` mesh: **2(k−1)**; the source confirms 32×32 has diameter 62;
   - `k×k` double torus: **2⌊k/2⌋**;
   - 2×2×2 cube: **3**;
   - 4-D hypercube: **4**.
   
   Exact figure-specific ring/grid dimensions beyond the prose are **[Needs confirmation]**.

16. In each torus dimension the greatest shortest distance is `⌊k/2⌋`. With two dimensions:
   - even `k`: **diameter = k**;
   - odd `k`: **diameter = k−1**.

17. Bisect an 8×8×8 mesh across one dimension. The cut crosses `8×8 = 64` links. At 1 Gbit/s each, bisection bandwidth is **64 Gbit/s**.

18. A 64-byte packet contains 512 bits. At 1 Gbit/s, network serialization is **512 ns**.

   A 64-byte buffer contains 16 32-bit words. One RAM↔NIC copy costs:
   `16×20 ns = 320 ns`.

   - ignoring copy time: **512 ns**;
   - three-copy path (RAM→source NIC, network, destination NIC→RAM): **320 + 512 + 320 = 1152 ns = 1.152 μs**;
   - with two extra kernel copies: **1152 + 2×320 = 1792 ns = 1.792 μs**.

19. For 512 useful bits per packet:
   - three-copy path: `512 / 1.152 μs ≈ 444.4 Mbit/s`;
   - five-copy path: `512 / 1.792 μs ≈ 285.7 Mbit/s`.

   These values use the same idealized per-packet assumptions as Q18 and ignore additional protocol overhead.

20. Pin + unpin overhead is `2 μs = 2000 ns`.

   DMA time is `N/5 = 0.2N ns`; programmed I/O is `20N ns`.

   DMA is worthwhile when:
   [
   2000 + 0.2N < 20N
   ]
   so `N > 101.01` bytes. Minimum integer size: **102 bytes**.

21. A local system call implicitly operates on the caller's OS state; after RPC the server procedure runs under the **server machine's** OS. File descriptors, current directory, process IDs, credentials, devices and other kernel-managed objects may therefore refer to the wrong machine or have no equivalent. The RPC design must either forbid such calls, marshal/virtualize the required state, or explicitly forward the operation to the machine that owns the intended resource.

22. The retrieved prose says DSM must locate the current page owner but does not explicitly enumerate the two textbook mechanisms. Two designs consistent with the chapter are:
   - a centralized directory recording current page location;
   - distributed location information/search among nodes (for example owner forwarding or broadcast/query).
   
   The exact pair intended by the source is **[Needs confirmation]**.

23. PDF 628 gives total traffic values for the two partitions shown in figure 8.24, but the individual edge weights required after moving H are only in the figure and not encoded in text RAG. **[Needs confirmation]**.

24. No. At least two major classes of state lie outside the raw memory image:
   - kernel/resource state such as open files, device state, timers and other node-local OS objects;
   - communication/location state such as active connections, queued/in-flight messages and references from other processes to the old node.
   
   Migration must preserve or redirect these resources and references, not merely copy user memory.

25. The source states that classic Ethernet detects collisions and defines a maximum cable length, but it does not spell out the timing derivation. The collision-detection model implies that propagation delay must remain bounded so a transmitter can still detect a collision while the transmission is active. The exact timing/minimum-frame derivation is **[Needs confirmation]** in chapter RAG.

26. The common feature is the **logical middleware/application layering**: applications interact through the same middleware abstraction rather than directly with heterogeneous network/OS details. The underlying machines may differ in hardware and operating systems, so the implementation below/inside middleware can differ while the exposed application model remains coherent. Exact labels for all four platforms in figure 8.26 are **[Needs confirmation]**.

27. Based on the service descriptions:
   - a) video on demand: a **connection-oriented service that prioritizes timely delivery over retransmission-perfect reliability**; the chapter's digital-voice discussion is the analogous case;
   - b) web-page download: **reliable connection-oriented byte stream**, i.e. the TCP-style model, because all bytes must arrive correctly and in order.
   
   Exact names/cells from figure 8.29 are partly graphical; the mapping above is source-derived from the prose.

28. Partition the namespace hierarchically. Delegate subtrees/domains to separate authoritative servers, let higher-level servers store referrals rather than every record, replicate important servers, and cache resolved mappings near clients. This distributes lookup load in the same way the hierarchical names distribute administrative responsibility.

29. In the chapter's Web example the HTTP server is listening for TCP connections on **port 80**, so the browser connects to that conventional service endpoint. The source uses this as the standard HTTP port; it does not further discuss port-number assignment policy.

30. Two direct improvements:
   1. keep one TCP connection open and request multiple page objects over it instead of reconnecting for every object;
   2. fetch independent objects concurrently over several connections so network wait overlaps.
   
   Both reduce the serialized connection/setup pattern described in the question.

31. **Immediate visibility on the same machine** improves intuitive local sharing: processes using the same cache can communicate through the newest copy and behave more like ordinary shared files.  
   **Delayed visibility until close** keeps session semantics simple and uniform: every process other than the writer sees the committed/session version, avoiding special same-machine coherence rules. The trade-off is stronger coherence versus simpler semantics and lower synchronization overhead.

32. Objects encapsulate data behind methods. This allows the implementation to enforce synchronization, validation and invariants at the method boundary and lets ORB/middleware hide location, OS, hardware and transport details. With raw shared memory, every participant can manipulate representation directly, making consistency, synchronization and distribution harder to control.

33. Index tuple space using the fields that participate in matching. A practical design is to first bucket by tuple arity and field-type signature, then maintain hash/tree indexes for constant-valued fields. `in` uses the template's fixed fields to select a small candidate set; wildcard/formal fields are checked only inside that set. This follows the chapter's three matching rules.

34. Source-grounded benchmark design:
   - allocate source/destination arrays of several sizes;
   - repeat the copy many times;
   - measure with `clock` or `times`;
   - subtract/estimate loop/timing overhead from a no-copy control;
   - report time/byte versus size to expose cache/memory effects.
   
   Actual measurements on a real system are **[Needs confirmation]**.

35. Use a restricted wire structure, for example: fixed maximum format string, argument count, and tagged union entries for supported integer/string/floating types. The client stub parses the restricted format, marshals it into the structure, sends it, waits for a result; the server stub unmarshals, calls its local `printf` equivalent under the same restrictions, and returns status. Actual C compilation/execution is **[Needs confirmation]**.

36. Event-driven simulator design:
   - maintain per-node job queues and simulated completion times;
   - sender-initiated: when a new job makes a node overloaded, probe up to `Nprobe` candidate nodes for an underloaded destination;
   - receiver-initiated: when a node becomes idle, probe candidates for work;
   - count every probe sent/received per host;
   - heavy generator: average `N` jobs per AJL interval;
   - light generator: average `N/3` jobs per AJL interval;
   - report total, min and max probe counts and completed work.
   
   Expected qualitative result from the chapter: sender probing is costly under heavy load; receiver probing is costly under light load. Actual simulation output is **[Needs confirmation]**.

37. Source-consistent design:
   - central broker owns a mutex-protected history of articles and subscriber list;
   - publisher thread sends `{length, topic, article}`;
   - subscriber registers a hierarchical topic pattern with optional `*`;
   - broker first replays matching history separated by `BEGIN NEW ARTICLE`;
   - new publications are matched against all subscriptions and queued/signaled to interested subscribers;
   - terminal commands create publisher/subscriber threads dynamically;
   - a publisher terminates article input on a line containing only `.`.
   
   Shared-memory implementation can use mutexes plus condition variables/queues; the source also permits TCP IPC. Actual implementation/test result is **[Needs confirmation]**.
