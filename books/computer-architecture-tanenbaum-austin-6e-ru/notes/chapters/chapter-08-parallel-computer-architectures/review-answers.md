# RAG-grounded ответы — глава 8

**Provenance:** questions `p0696:c01`–`p0698:c01`. Answers use chapter RAG `p0590:c01`–`p0698:c01`. Not an official publisher key.

## 1

No.

A long variable-length x86 instruction still describes one architectural instruction. VLIW means that one instruction word/bundle explicitly contains several operations intended for parallel functional units.

Instruction length alone does not make an ISA VLIW.

## 2

The chapter's Core-i7 discussion lists several alternatives to simply adding cores:

- raise clock frequency;
- add functional units;
- deepen the pipeline;
- use hardware multithreading.

Each has limits: heat/power, issue bandwidth, branch/miss penalties or extra context resources.

## 3

For the source's saturating/clipping model with representable range 0–255:

```text
96  → 96
-9  → 0
300 → 255
256 → 255
```

## 4

Using table 8.1 and treating the listed operation order as command slots:

1. **Not compatible.** The third operation is a load, but load/store operations are supported only in slots 4 and 5, not slot 3.
2. **Compatible.** Integer ALU/shift/immediate operations have broad slot support, and integer multiply can occupy its supported multiplier slot.
3. **Not compatible.** The floating-point ALU operation in the second listed slot does not match the FP-ALU slot placement shown in table 8.1.

TriMedia does not repair an incompatible bundle dynamically; the compiler must schedule a legal combination.

## 5

**[Needs confirmation].**

The exact commands occupying cycles 13–15 are encoded visually in figure 8.5, while the text RAG explains the scheduling rules but does not expose every box/command in the figure.

The source-supported rules are:

- fine-grained: rotate among available threads each cycle;
- coarse-grained: continue one thread until a stall, then switch, losing the switch/flush cycle described in the text.

## 6

**k threads**, under the exercise's definition that the miss operation occupies k machine cycles before the same thread may safely depend on it.

Round-robin fine-grained scheduling revisits a given thread only after the other contexts have had their turns, thereby hiding the k-cycle latency when enough contexts exist.

## 7

**SIMD.**

The source explicitly describes Fermi streaming multiprocessors as executing identical operations across multiple CUDA cores in SIMD style.

## 8

**MIMD.**

The workers pursue the same overall goal, but individual bees move independently, inspect different locations and need not execute the same step at the same instant.

## 9

Because implementations may reorder, overlap, cache and replicate memory operations.

Software therefore needs a defined contract specifying which observations are legal. Without such a contract, the programmer cannot distinguish an allowed reordering from a broken memory system.

Stronger models simplify programming but restrict implementation freedom; weaker models require explicit synchronization.

## 10

Only one processor can own/use the shared bus for the transaction.

Bus arbitration chooses one request; the other processor waits until the bus becomes available.

## 11

Again, one request is serviced while the other two wait.

With the exercise's queueing assumption, waiting requests are serialized in the bus arbitration order/FIFO queue.

## 12

For the chapter's **invalidate-based write-through** protocol, address snooping is sufficient for coherence.

A remote cache needs to know **which line** was written so it can invalidate its copy; it does not need the new data value because the writer also updates main memory.

If the protocol used remote **update** rather than invalidation, seeing the data value would matter.

## 13

The shared bus can service at most one memory-using instruction at a time.

If one of every four instructions needs the bus, the bus can support at most:

```text
4 instructions per bus-occupied instruction interval
```

across the whole machine.

Relative to one processor issuing one instruction per interval, the asymptotic system speedup is therefore only about:

```text
4×
```

not 64×.

## 14

The easiest MESI state to remove is **Exclusive**.

Then a clean line that exists in only one cache is treated as Shared. Correctness is preserved, but a later write may require an unnecessary bus upgrade/invalidation transaction because hardware no longer knows that no other copy exists.

Removing other states is more costly:

- **Modified:** memory would have to remain current, effectively pushing the design toward write-through/more write traffic.
- **Shared:** multiple read-only cached copies could no longer be represented naturally; replication would need to be restricted or represented another way.
- **Invalid:** the cache would lack a normal state for an absent/stale line, making replacement/coherence semantics impractical.

Best 3-state choice: **M/S/I**, dropping E.

## 15

Yes.

A common case is a **write to a Shared line**. The data is already present locally, but the processor must use the bus/coherence network to invalidate the other shared copies before obtaining exclusive/modified ownership.

## 16

Independent request probability per processor = `p`.

### No requests

```text
P(0) = (1-p)^n
```

### Exactly one

```text
P(1) = n p (1-p)^(n-1)
```

### More than one

```text
P(>1) = 1 - (1-p)^n - n p (1-p)^(n-1)
```

## 17

Main advantage: **nonblocking connectivity**. If the target memory module is free, an unused processor can be connected even while other independent pairs communicate.

Main disadvantage: **hardware cost**. A crossbar for n processors and k memory modules requires on the order of `n×k` crosspoints/wiring, which scales poorly.

## 18

The text/figure description implies **129 crossbar fabrics** for a fully populated E25K:

- per one of 18 board sets: 4 level-0 + 2 level-1 + 1 level-2 = 7 small crossbars;
- `18×7 = 126`;
- central panel: 3 crossbars of 18×18 for addresses, responses and data.

```text
126 + 3 = 129
```

This count is derived from the textual description of figure 8.31. The page also contains a separate processor-count inconsistency recorded in `source-findings.md`.

## 19

**[Needs confirmation].**

The exact endpoints whose unique omega paths traverse wire 2A→3B depend on the visual perfect-shuffle wiring in figure 8.27. The RAG text explains routing examples but does not encode that complete edge map.

## 20

Yes, although the symptom differs.

A shared bus is already a global serialized resource, so all traffic competes there. A hot memory location can additionally concentrate requests on one memory module/cache line and increase coherence traffic.

Thus hot spots still hurt, even though there is no multi-stage route whose one internal link alone becomes the hot path.

## 21

4096 endpoints require:

```text
log2(4096) = 12 stages
```

A LOAD request traverses 12 switches and the reply traverses 12 more.

With 5 ns per switch:

```text
24 × 5 ns = 120 ns
```

CPU cycle = 60 ns:

```text
120 / 60 = 2 cycles
```

So the network contributes **2 machine-cycle delay slots** under the exercise's ideal infinitely-fast-memory assumption.

## 22

**[Needs confirmation].**

The requested “small topology change” depends on the exact visual wiring of figure 8.27 and the processor-to-memory pairing. The text RAG does not encode enough of that figure to identify the intended IBM RP3/BBN Butterfly modification without reconstructing the image externally.

## 23

Remote access costs:

```text
120 ns
```

Local access:

```text
20 ns
```

Saving per access after migration:

```text
100 ns
```

Page P receives `0.01N` accesses, so total possible saving is:

```text
0.01N × 100 ns = N ns
```

Copy locally when:

```text
C < N ns
```

If `C=N`, the choices break even.

## 24

Per node:

```text
8 MiB / 64 B = 131072 = 2^17 cache lines
```

512 nodes require 9 bits to identify a node. Following the chapter's directory scheme, add one state/presence bit, giving about **10 bits per directory entry**.

Directory size:

```text
2^17 × 10 bits
= 1,310,720 bits
= 163,840 bytes
```

Relative to 8 MiB:

```text
163840 / 8388608 × 100
= 1.953125%
```

Answer: about **1.95%**.

As node count increases, the node-identity field needs more bits, so this form of directory overhead **increases slowly (logarithmically in node count)**.

## 25

Both provide one shared architectural address space where remote memory is reachable by ordinary LOAD/STORE.

- **NC-NUMA:** no caching of remote data; coherence is simpler, but remote latency is paid repeatedly.
- **CC-NUMA:** caches remote data and maintains coherence, typically with a directory, reducing repeated remote-access cost at the price of coherence metadata/protocol complexity.

## 26

Text-supported diameter formulas:

- star: **2** between two outer nodes;
- full interconnect: **1**;
- tree: **2h** for a balanced tree whose leaves are h links below the root;
- ring of N nodes: **floor(N/2)**;
- `m×n` mesh: **(m-1)+(n-1)**;
- `m×n` torus: **floor(m/2)+floor(n/2)**;
- 2×2×2 cube shown by source: **3**;
- 4-dimensional hypercube: **4**.

The RAG does not expose every node count/height drawn in figure 8.33, so an exact numeric value for its tree/ring/mesh instances beyond these formulas is **[Needs confirmation]**.

## 27

Using the exercise's definition: maximum number of arbitrary link failures guaranteed not to partition the network.

- star: **0**;
- full interconnect with 8 nodes: **6** (the source explicitly notes connectivity after loss of six links);
- tree: **0**;
- ring: **1**;
- ordinary 2D mesh: **1**;
- 2D torus: **3**;
- 3D cube: **2**;
- 4D hypercube: **3**.

These values are one less than the edge connectivity of the corresponding regular graph.

## 28

For a `k×k` 2D torus, maximum distance in one dimension is `floor(k/2)`.

Therefore:

```text
D = 2 floor(k/2)
```

So:

- even `k`: `D=k`;
- odd `k`: `D=k-1`.

## 29

Cut an 8×8×8 cube into two equal 4×8×8 halves.

The cut crosses:

```text
8 × 8 = 64 links
```

At 1 GB/s per duplex link:

- bisection bandwidth in one direction = **64 GB/s**;
- if the metric sums simultaneous traffic in both directions of every full-duplex link = **128 GB/s aggregate duplex**.

## 30

Amdahl:

```text
S(n) = n / (1 + (n-1)f)
```

As `n→∞`:

```text
Smax = 1/f
```

For `f=0.1`:

```text
Smax = 10
```

## 31

Let each bus/link have bandwidth `b`.

### Shared bus

- 4 processors: `b/4` per processor.
- 16 processors: `b/16`.
- 64 processors: `b/64`.
- `N→∞`: **0** per processor.

### 2D mesh

The source counts aggregate physical link bandwidth divided by processors.

4-node 2×2 mesh:

```text
4 links / 4 processors = b
```

16-node 4×4 mesh:

```text
24 links / 16 = 1.5b
```

64-node 8×8 mesh:

```text
links = 2×8×7 = 112
112/64 = 1.75b
```

For an `n×n` mesh:

```text
links/processors = 2n(n-1)/n^2
                 = 2(1-1/n)
→ 2
```

Limit: **2b per processor** by this aggregate-link metric.

## 32

One useful fourth semantic is an **acknowledged buffered send**:

- sender blocks only until the destination communication subsystem has accepted/copied the message into a safe receive-side buffer;
- it does not wait for the destination application to execute `receive`.

Advantage over fully synchronous send: sender can continue before the receiver process actually consumes the message, and its original buffer is reusable.

Disadvantage: requires destination/network buffering and acknowledgement machinery; it still blocks if that buffering path is unavailable.

This is a design extension consistent with the chapter's synchronous/buffered/nonblocking trade-offs.

## 33

Reads do not modify shared state. Once data is replicated/cached, many reads may be served locally without broadcasting a state change.

Writes change shared state and therefore require coherence actions such as invalidation or update of other copies.

On a hardware-broadcast network:

```text
more writes
→ more broadcasts/coherence traffic
→ more contention
```

Therefore read-heavy workloads can exploit replication much more efficiently than write-heavy workloads.
