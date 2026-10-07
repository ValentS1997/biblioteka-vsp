# Cheatsheet — глава 6 «Уровень операционной системы»

**Provenance:** RAG `p0475:c01`–`p0554:c01`. Policy: **rag_only**.

## OS-machine level

```text
ISA instructions → execute directly
OS virtual instructions/system calls → interpreted by OS
```

Core abstractions:

- virtual memory;
- files/directories;
- processes/threads;
- synchronization.

## Virtual address translation

For page size `2^k`:

```text
virtual address
= virtual page number | k-bit offset

physical address
= frame number        | same offset
```

Checks:

1. page-table entry exists?
2. present bit set?
3. access permitted?
4. if yes → combine frame + offset;
5. if no → fault/trap.

## Demand paging

```text
access absent page
→ page fault
→ OS chooses/gets frame
→ maybe evicts victim
→ reads page from backing store
→ updates page table/TLB
→ retries instruction
```

## Replacement

| Policy | Chooses |
|---|---|
| LRU | page unused for longest recent time |
| FIFO | page resident for longest time |

If working set > available frames → **thrashing**.

## Page-size trade-off

Large page:

- fewer page-table entries;
- better transfer amortization;
- fewer TLB entries for same mapped range;
- more internal fragmentation / unnecessary bytes.

Small page:

- less internal waste;
- better for sparse working sets;
- larger page tables and more translation overhead.

## Fragmentation

| Type | Cause | Mitigation |
|---|---|---|
| internal | fixed allocation unit larger than requested object tail | smaller pages/blocks |
| external | variable-size segments leave holes between allocations | coalescing, compaction, paging |

## Segmentation

Address:

```text
segment selector/number + offset
```

Advantages:

- independent logical spaces;
- variable-size structures;
- per-segment protection.

Cost in pure segmentation:

- external fragmentation;
- potentially expensive compaction.

## Core i7 path

```text
segment selector
→ LDT/GDT descriptor
→ BASE + offset = linear address
→ DIR / PAGE / OFF
→ page directory
→ page table
→ frame + OFF
```

## TLB

TLB hit → translation found immediately.

TLB miss → page-table walk.

Page fault → page not resident.

These are not the same event.

## Virtualization

```text
guest virtual
→ guest physical
→ host physical
```

Hypervisor controls CPU, memory and I/O sharing. Core i7 VMX/EPT supplies hardware support.

## File abstraction

Application sees:

```text
open → descriptor/handle
read/write → byte stream
seek → position
close → release open-file state
```

Filesystem sees:

```text
file
→ metadata/index
→ blocks/extents
→ disk
```

## Free-space structures

- free list: easy extent search, variable metadata size;
- bitmap: fixed size, one bit per block, harder large-run search.

## UNIX file model

Chapter examples:

- `open`, `close`, `read`, `write`, `lseek`, `stat`, `chmod`, `fcntl`;
- directory operations: `mkdir`, `rmdir`, `opendir`, `readdir`, `closedir`, `chdir`, `link`, `unlink`;
- i-node contains metadata + direct/indirect block addresses.

## Process state

At minimum:

- PC;
- PSW;
- SP;
- general registers;
- address space.

Threads in one process share address space/resources but have their own execution state/stack.

## Semaphore

```text
down(s):
  if s > 0: s--
  else: block

up(s):
  release waiter or increase availability
```

Required property: operations are **atomic**.

Producer/consumer:

```text
producer: down(available) → put → up(filled)
consumer: down(filled)   → get → up(available)
```

## Windows synchronization in chapter

- semaphore;
- mutex;
- critical section;
- event.

Named/kernel objects can coordinate across processes; critical sections are process-local.

## Verification questions

Given a memory/file/concurrency scenario:

1. what state is virtual vs physical?
2. what translation metadata is consulted?
3. what can fault?
4. what is atomic?
5. what resource may block?
6. what state must survive blocking/context switch?
7. what metadata is cached, persisted or shared?
