# RAG-grounded ответы — глава 6

**Provenance:** questions `p0548:c01`–`p0554:c01`. Answers use chapter RAG `p0475:c01`–`p0554:c01`. Not an official publisher key.

## 1

Уровень ОС содержит почти все команды ISA плюс новые виртуальные команды — системные вызовы.

Обычная ISA-команда уже имеет аппаратную реализацию и проходит непосредственно на уровень микроархитектуры. ОС должна интерпретировать только те операции, которые она добавляет сама: файлы, управление процессами, виртуальные ресурсы и другие services.

Поэтому:

```text
ISA instruction → hardware
system call     → OS interpreter → hardware/services
```

## 2

32-bit byte-addressed space:

```text
2^32 bytes
```

4 KiB page:

```text
4096 = 2^12 bytes
```

Количество virtual pages:

```text
2^32 / 2^12 = 2^20 = 1,048,576
```

Ответ: **1 048 576 страниц**.

## 3

Теоретически страница размером 4000 байт возможна: translation может использовать division/modulo вместо простого разбиения address bits.

Но глава специально подчёркивает power-of-two page sizes, потому что при `2^k`:

```text
high bits → page number
low k bits → offset
```

Это существенно упрощает MMU, alignment и вычисление адреса.

Следовательно, **теоретически да, практически неудобно и неоправданно для обычной binary-addressed architecture**.

## 4

Page size = 1024 words.

Page map:

```text
VP0 → frame 3
VP1 → frame 1
VP2 → absent
VP3 → absent
VP4 → frame 2
VP5 → absent
VP6 → frame 0
VP7 → absent
```

### 4.1 Page-fault ranges

Fault вызывает любой virtual address на pages 2, 3, 5, 7:

```text
2048–4095
5120–6143
7168–8191
```

### 4.2 Given addresses

| VA | VP | offset | result |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 3072 |
| 3728 | 3 | 656 | **page fault** |
| 1023 | 0 | 1023 | 4095 |
| 1024 | 1 | 0 | 1024 |
| 1025 | 1 | 1 | 1025 |
| 7800 | 7 | 632 | **page fault** |
| 4096 | 4 | 0 | 2048 |

Formula:

```text
physical = frame × 1024 + offset
```

## 5

Reference string:

```text
0, 7, 2, 7, 5, 8, 9, 2, 4
```

4 frames, initially empty.

### LRU

Only the second access to page 7 is a hit.

Faults:

```text
0 F
7 F
2 F
7 H
5 F
8 F
9 F
2 F
4 F
```

**LRU: 8 page faults.**

### FIFO

After loading `0,7,2,5`, page 8 evicts 0, page 9 evicts 7, the later access to 2 is still a hit, and page 4 then evicts 2.

```text
0 F
7 F
2 F
7 H
5 F
8 F
9 F
2 H
4 F
```

**FIFO: 7 page faults.**

## 6

The chapter's FIFO description increments the age counter of every resident page at each fault.

Equivalent but cheaper bookkeeping:

- maintain one global monotonically increasing generation/timestamp counter;
- when a page is loaded, store the current generation in that frame;
- increment only the global generation;
- evict the resident page with the **smallest load timestamp**.

No resident counters need periodic incrementing.

This preserves FIFO ordering while updating only the newly loaded page.

## 7

If the page-fault handler itself is absent, handling the original page fault can cause another page fault before the system has restored the mechanism required to resolve faults.

This creates recursive/unserviceable fault handling.

Solution: keep the fault-handling critical path **nonpageable/pinned in physical memory**, including the code and essential data/page-table structures needed to bring another page in.

## 8

Use write protection as a software dirty-bit trap.

Procedure:

1. when a page is loaded, mark it readable/executable as appropriate but **not writable**;
2. first write causes a protection fault;
3. OS records that the page is dirty;
4. OS enables write permission and restarts the instruction;
5. subsequent writes proceed normally.

Thus first-write trapping emulates a dirty bit.

## 9

Page size = 2 KiB = 2048 bytes.

### Segment 0 — read only
- p0 → frame 9
- p1 → frame 3
- p2 → disk
- p3 → frame 12

### Segment 1 — read + execute
- p0 → disk
- p1 → frame 0
- p2 → frame 15
- p3 → frame 8

### Segment 2 — read/write/execute
Its page table is not resident.

### Segment 3 — read + write
- p0 → frame 14
- p1 → frame 1
- p2 → frame 6
- p3 → disk

Results:

| # | Access | Result |
|---:|---|---|
| 1 | read S0 P1 off 1 | `3×2048+1 = 6145` |
| 2 | read S1 P1 off 10 | `0×2048+10 = 10` |
| 3 | read S3 P3 off 2047 | **page fault** |
| 4 | write S0 P1 off 4 | **protection fault**: S0 read-only |
| 5 | write S3 P1 off 2 | `1×2048+2 = 2050` |
| 6 | write S3 P0 off 14 | `14×2048+14 = 28686` |
| 7 | jump S1 P3 off 100 | `8×2048+100 = 16484` |
| 8 | read S0 P2 off 50 | **page fault** |
| 9 | read S2 P0 off 5 | page table itself is not resident; translation must fault/load metadata before a physical address can be determined |
| 10 | jump S3 P0 off 60 | **protection fault**: S3 is not executable |

## 10

Compaction moves user memory to new physical addresses.

If a device/DMA engine is concurrently writing directly into a user-space buffer using the old physical location, compaction can make the device write into stale or unrelated memory.

Safe approaches include:

- pinning the I/O pages until transfer completion;
- deferring compaction for those pages;
- using an address-translation mechanism for device DMA.

The chapter-level requirement is that the I/O target must remain physically valid for the duration of direct transfer.

## 11

Page tables map whole pages.

If a file mapping began at an arbitrary byte such as virtual address 5000, the first virtual page would contain a mixture of bytes belonging to the mapping and bytes outside it. Translation/protection would no longer be expressible as a simple page-table entry.

Page-aligned mappings preserve the invariant:

```text
one mapped virtual page ↔ one file-page-sized region
```

Offsets within a page remain offsets within the corresponding mapped file region.

## 12

When a selector is loaded, Core i7 fetches its descriptor from LDT/GDT and stores it in hidden MMU state.

Reason: later memory references need BASE, LIMIT and protection information constantly. Caching the descriptor avoids a descriptor-table memory access on every reference.

It also means the active descriptor state remains stable until the segment register is reloaded.

## 13

Given:

```text
BASE = 10000
offset = 8000
linear address = 18000
```

With 4 KiB pages:

```text
page number = floor(18000 / 4096) = 4
offset      = 18000 - 4×4096 = 1616
```

For the 32-bit two-level Core i7 scheme:

- DIR field = **0**;
- PAGE field = **4**;
- OFF = **1616**.

So Core i7 uses directory entry 0, then page-table entry 4.

The final physical address cannot be computed without the frame number stored in that page-table entry.

## 14

Pure segmentation uses variable-sized contiguous regions, so replacement must consider both recency/usefulness and enough contiguous free space.

Source-compatible policies include:

- FIFO-like removal of old resident segments;
- LRU-like removal of least recently used segments;
- evicting one or several segments until enough space exists;
- coalescing adjacent holes;
- compaction if total free space is sufficient but fragmented.

Unlike fixed pages, a single victim may not free a large enough contiguous hole.

The chapter does not prescribe one optimal segment-replacement algorithm.

## 15

### Internal fragmentation

Unused space **inside** an allocated fixed-size unit, e.g. unused tail of the last page.

Mitigation:

- smaller pages/blocks;
- finer allocation granularity.

Trade-off: larger tables/metadata and more transfer/translation overhead.

### External fragmentation

Free memory exists but is split into holes **between** variable-size segments.

Mitigation:

- merge adjacent holes;
- compact memory;
- avoid contiguous variable-sized physical allocation by paging segments.

## 16

Prefer **LRU** as the more demand-sensitive analogy.

A product that has not been selected for a long time is a more plausible eviction candidate than one that merely arrived on the shelf earliest.

FIFO ignores current popularity.

As with memory, pathological access patterns can still make LRU poor.

## 17

Most page-size arguments have cache-line analogues.

Larger unit:

- amortizes fetch/transfer overhead;
- needs fewer tags/metadata entries for the same covered range;
- may exploit spatial locality;
- may fetch many unused bytes and increase pollution.

Smaller unit:

- wastes less transferred/storage capacity on sparse locality;
- increases metadata/tag pressure and the number of misses required for sequential regions.

The mechanisms differ — cache misses are normally hardware-managed and cache lines are much smaller — but the locality/granularity trade-off is conceptually similar.

## 18

The chapter gives the direct reason:

`open` locates the file and brings the information required for access into memory.

In UNIX examples, the i-node of an open file is copied into a main-memory table and retained while the file stays open.

This lets later `read`/`write` operations use a small descriptor instead of repeating pathname traversal and metadata lookup.

## 19

Disk sectors:

```text
800 cylinders × 5 tracks × 32 sectors
= 128,000 sectors
```

Bitmap size:

```text
128,000 bits = 16,000 bytes
```

One free-list hole record:

```text
32 bits = 4 bytes
```

Equal size occurs at:

```text
16,000 / 4 = 4,000 holes
```

Therefore the free-list becomes larger when there are **more than 4000 holes**, i.e. starting at **4001 holes**.

## 20

Allocating from the largest free hole (“worst fit”) tends to leave a still-useful remainder instead of creating a very tiny unusable fragment.

Potential benefit:

```text
large hole - request → medium/large residual hole
```

rather than repeatedly producing very small leftovers.

Trade-off: it consumes the best large extent that might be needed by a future large segment. The chapter does not claim it universally outperforms first fit.

## 21

One additional purpose is **access validation at open time**.

[Inference from the chapter's protection model.]

The OS can check the requested mode against file permissions/security metadata and bind the granted access to the returned descriptor/handle. Later operations then use that already validated open-file object.

## 22

For:

```text
P(length=i) = 2^-i, i >= 1
```

expected run length:

```text
E[L] = Σ i/2^i = 2 sectors
```

Data and holes have the same distribution, so an average data+hole pair occupies:

```text
2 + 2 = 4 sectors
```

For `N >> 1`:

```text
expected holes ≈ N / 4
```

Boundary effects are negligible for large N.

## 23

Generally **no**.

The chapter explicitly explains that contiguous allocation is impractical when final file sizes are unknown and files grow dynamically: a file can collide with the next file and have nowhere to extend.

Noncontiguous allocation allows new blocks to be placed elsewhere and linked/indexed into the file.

## 24

The statistics pull in opposite directions:

- many small files → small blocks reduce internal waste;
- a small number of large files dominate total bytes → large blocks improve sequential transfer and reduce metadata/index overhead.

Therefore one fixed block size is a compromise. A filesystem can benefit from moderate small allocation units plus larger extents/clusters for large files.

The chapter's core conclusion is exactly this trade-off between wasted tail space and transfer/index efficiency.

## 25

### One CPU

**Yes**, provided disabling interrupts also prevents timer-driven process switching during the critical update.

The source explicitly notes that this is a common way to make semaphore operations indivisible on a uniprocessor.

### Two CPUs sharing memory

**No.**

Disabling interrupts on CPU 1 does not stop CPU 2 from reading/modifying the same semaphore concurrently.

A multiprocessor needs an atomic memory primitive/lock mechanism shared by all CPUs.

## 26

A waiter queue gives:

- simple tracking of blocked processes;
- deterministic wakeup selection;
- natural FIFO fairness if queue order is used;
- lower risk of starvation than arbitrary random selection.

The chapter explicitly states that blocked processes are normally collected in one queue because this simplifies tracking.

## 27

No — `peek` and `down` are two separate operations.

Example with semaphore = 1:

```text
P1: peek → 1
P2: peek → 1
P1: down → succeeds, semaphore 0
P2: down → blocks
```

Therefore the check does not guarantee that `down` will not block.

The race exists with **two processes already**, and therefore also with three or more.

## 28

Initial state:

```text
semaphore = 1
P1,P2,P3 running
```

Timeline:

| Time | Event | Semaphore after completion | P1 | P2 | P3 |
|---:|---|---:|---|---|---|
| 0 | initial | 1 | run | run | run |
| 100 | P1 down | 0 | run | run | run |
| 200 | P1 down | 0 | **blocked** | run | run |
| 300 | P2 up | 0 | run | run | run |
| 400 | P3 down | 0 | run | run | **blocked** |
| 500 | P1 down | 0 | **blocked** | run | blocked |
| 600 | P2 up | 0 | run | run | blocked |
| 700 | P2 down | 0 | run | **blocked** | blocked |
| 800 | P1 up | 0 | run | run | blocked |
| 900 | P1 up | 0 | run | run | run |
| 1000 | no new event | 0 | run | run | run |

When multiple processes wait, the exercise says the lowest-numbered one is released.

## 29

Use a binary semaphore initialized to 1:

```text
down(file_sem)
    access / update reservation file
up(file_sem)
```

Every cooperating process must obey this protocol.

Only one process can hold the semaphore at a time, so the check-and-sell transaction over the last seat is mutually exclusive.

## 30

Given the exercise semantics:

- if `X==0`, `TSL X` atomically sets `X=1` and skips the next instruction;
- if `X!=0`, it behaves like NOP.

One valid assembly-style construction:

```text
lock:
    TSL X
    JMP lock
    RET

unlock:
    MOV X, 0
    RET
```

Unlocked path:

```text
TSL sets X=1 → skips JMP → RET
```

Locked path:

```text
TSL does not skip → JMP lock
```

The crucial property is that test-and-set happens in one indivisible memory cycle.

## 31

Ring length = 65, indexes advance modulo 65.

Start:

```text
in=0, out=0
```

| Step | Operation | in | out |
|---:|---|---:|---:|
| 1 | +22 | 22 | 0 |
| 2 | -9 | 22 | 9 |
| 3 | +40 | 62 | 9 |
| 4 | -17 | 62 | 26 |
| 5 | +12 | 9 | 26 |
| 6 | -45 | 9 | 6 |
| 7 | +8 | 17 | 6 |
| 8 | -11 | 17 | 17 |

Final state: **`in=17, out=17`**, buffer empty.

## 32

Using the source inode model:

- 10 direct block addresses;
- one single-indirect block;
- one double-indirect block;
- one triple-indirect block.

Exercise gives 512 addresses per indirect block.

Data blocks addressable:

```text
10 + 512 + 512^2 + 512^3
= 134,480,394 blocks
```

At 2 KiB/block:

```text
134,480,394 × 2048
= 275,415,846,912 bytes
```

Approximately:

```text
256.501 GiB
```

A 64-bit file offset is not the limiting factor here; the inode indirection tree reaches its limit first.

## 33

The source cross-reference number is inconsistent; see `source-findings.md`.

The chapter explicitly states that:

```text
/usr/ast/bin/game3
/usr/jim/jotto
```

are two directory links to the same file.

After:

```text
unlink("/usr/ast/bin/game3")
```

the system:

1. removes the `game3` directory entry from `/usr/ast/bin`;
2. decrements the file's i-node link count;
3. does **not** delete the i-node or data blocks because another link remains;
4. leaves the file reachable as `/usr/jim/jotto`.

## 34

Without `pipe`, the same dataflow can be approximated, but not with identical streaming semantics.

Source-supported alternatives:

### Temporary file

```text
producer → file
producer finishes
consumer → reads file
```

This loses concurrent streaming and needs storage.

### Shared memory + synchronization

The chapter describes memory-mapped shared regions and semaphores. They could implement a shared circular buffer manually.

That recreates pipe-like functionality at greater complexity.

Therefore shell pipelines could be emulated, but removing `pipe` would make their implementation less direct and potentially non-streaming.

## 35

“Never reuse a descriptor number previously used by this program” causes monotonically increasing descriptor values.

Problems:

- descriptor space/table would grow without bound in long-running programs;
- programs expecting small reusable descriptors could break;
- a process could exhaust the finite descriptor namespace despite having few files open;
- extra state would be required to remember every descriptor ever issued.

The source design — smallest currently free descriptor — keeps the namespace compact and reusable.

“Fairness to descriptor numbers” has no operational value.

## 36

Windows ACL entries are processed in order, and the source says deny entries are normally placed before allow entries.

Construct ACL:

1. explicit **DENY** entry for Svetlana covering all requested file rights;
2. following **ALLOW** entry for everyone/the applicable general group with full access.

The early matching deny prevents Svetlana from gaining rights through membership in the later allowed group.

## 37

Two source-supported constructions:

### A. Two threads inside one process

- buffer: ordinary memory in the process address space;
- producer and consumer threads automatically share it;
- use `filled` and `available` semaphores;
- optionally use an additional mutex for shared-index critical sections if required.

### B. Two separate processes

- create a shared buffer by mapping the same file/mapping object into both address spaces;
- create kernel semaphores;
- share them via duplicated handles or named semaphore objects;
- use the same producer/consumer `down/up` protocol.

The chapter explicitly describes both memory-mapped shared memory and cross-process semaphore handles/named synchronization objects.

## 38

Simulator structure is source-supported:

```text
input virtual address
→ page = address / 1024
→ check page-table resident state
→ hit: update replacement metadata
→ miss:
     count page fault
     choose victim using FIFO or LRU
     replace mapping
```

Required state:

- 64 virtual-page entries;
- resident/frame mapping;
- FIFO load order or LRU last-use metadata;
- hit/fault counters.

However numeric comparison requested by the exercise is **[Needs confirmation]** because the exercise text does not fix the number of physical frames or the exact generated trace/randomization parameters.

No performance numbers are fabricated.

## 39

This is explicitly an empirical scheduling/race experiment.

The amount of inserted computation required for “approximately one hang per hour” depends on:

- CPU speed;
- JVM/runtime;
- scheduler;
- thread timing;
- optimization;
- system load.

The chapter provides no deterministic value.

Result: **[Needs confirmation by experiment]**.

The safe chapter conclusion is that changing timing changes the probability of exposing the race; it does not repair the race.

## 40

The source provides high-level directory APIs such as `opendir/readdir` and `FindFirstFile/FindNextFile`.

Those interfaces return logical directory entries. The exercise additionally requires:

- exact on-disk directory order;
- **unused directory positions**.

The chapter does not define a portable API exposing unused raw directory slots, and the required raw directory layout is filesystem-specific.

Therefore:

- a normal logical file-list program can be written from the provided APIs;
- the exact requested raw-slot implementation is **[Needs confirmation]** for a chosen filesystem/platform.
