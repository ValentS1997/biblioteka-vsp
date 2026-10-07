# Chapter 3 cheatsheet — Управление памятью

## Symptom / problem framing

Memory-management failures and slowdowns may look similar but occur at different layers:

- invalid virtual address / protection violation;
- TLB miss;
- page-table miss with page already resident (minor page fault);
- page absent and requiring I/O (major page fault);
- poor page-replacement choice;
- insufficient resident frames for working sets (thrashing);
- free-space fragmentation;
- I/O buffer page being incorrectly considered for replacement.

Identify the layer before changing policy.

## Baseline / context

### Address translation

```text
virtual address
   │
   ├─ virtual page number
   └─ offset
          │
          ▼
        MMU
          │
      TLB lookup
       /      \
    hit        miss
     │          │
 frame      page-table lookup
     │          │
     └────┬─────┘
          ▼
physical frame + unchanged offset
          │
          ▼
physical address
```

If the page-table entry is not present, a page fault transfers control to the OS.

### Memory-management layers

| Layer | Purpose | Typical issue |
|---|---|---|
| Base/limit | relocation + protection | per-reference add/check overhead |
| Swapping | reclaim RAM by moving whole processes | large I/O cost |
| Paging | virtual pages mapped to frames | page faults + page tables |
| TLB | cache translations | capacity/conflict misses |
| Replacement | choose victim page | unnecessary re-faults |
| Working set | preserve locality | thrashing if undersized |
| Segmentation | logical independently protected/shared regions | external fragmentation |

## Read-only checks

For a memory-management diagnosis, establish:

1. What is the virtual address, page number and offset?
2. Is the translation present in the TLB?
3. If not, is the page-table entry valid/present?
4. If the PTE is absent, is the page already resident through another mapping (minor fault) or must it be read from backing storage (major fault)?
5. What are the R/M bits or equivalent replacement metadata?
6. Which replacement policy is active: local or global?
7. Is the process's working set resident?
8. Is the total active working-set demand larger than RAM?
9. Are dirty pages forcing writeback before reuse?
10. Are pages involved in DMA/I/O pinned?
11. For shared memory/COW, which mappings refer to the same physical frame?
12. Is wasted space internal fragmentation (fixed-size pages) or external fragmentation (variable-size segments)?

## Interpretation

### Page replacement

| Algorithm | Chapter assessment |
|---|---|
| Optimal | unrealizable online; benchmark for comparison |
| NRU | simple, coarse approximation using R/M classes |
| FIFO | simple; can evict important old pages |
| Second chance | FIFO improved with R bit |
| Clock | efficient implementation of second chance |
| LRU | strong policy, expensive to implement exactly |
| NFU | poor approximation because old history persists |
| Aging | practical approximation to LRU |
| Working set | good concept, expensive direct implementation |
| WSClock | practical working-set/clock hybrid |

The chapter identifies **aging** and **WSClock** as particularly practical choices.

### Locality / thrashing

Demand paging works because programs exhibit locality. The active set of recently used pages is the working set.

If the sum of working sets exceeds physical memory, repeated faults dominate useful execution: the system is thrashing. Load control may need to swap entire processes out so the remaining processes have enough frames.

### Free-space allocation

- first fit: first sufficiently large hole;
- next fit: resume search where the previous search stopped;
- best fit: smallest sufficient hole;
- worst fit: largest sufficient hole.

The chapter notes that best fit can leave many small unusable holes and is not necessarily better than first fit.

### Page size trade-off

Smaller pages:
- reduce internal fragmentation;
- increase page-table size and potentially TLB pressure.

Larger pages:
- reduce page-table overhead;
- may transfer/store unused data and increase internal fragmentation.

### Sharing

- read-only code pages can be shared;
- copy-on-write allows initially shared data after `fork`;
- mapped files can provide shared memory and file-backed virtual pages;
- position-independent code enables one shared library image to appear at different virtual addresses.

## Next action

For a page-fault or memory-pressure issue:

`classify fault → inspect translation/residency → measure fault/writeback pattern → determine working-set pressure → only then change allocation/replacement policy`.

## Modifying action

Source-supported state-changing mechanisms include:

- page-table/TLB mapping changes;
- swapping a process in/out;
- page replacement and dirty-page writeback;
- changing page protection (for example READ ONLY → READ-WRITE during copy-on-write);
- pinning/unpinning I/O pages;
- mapping/unmapping a file;
- loading/evicting shared-library pages.

These are OS mechanisms, not generic user-shell procedures. Exact production commands are `[Needs confirmation]`.

## Verification / acceptance checks

A memory-management change is acceptable when:

- virtual-to-physical translation remains correct;
- protection faults are not masked as page faults;
- page-fault rate decreases or remains within the intended bound;
- no DMA/I/O buffer frame is recycled while transfer is active;
- dirty data reaches backing storage before its frame is reused;
- working sets fit without sustained thrashing;
- shared/COW mappings preserve process isolation after a write;
- the intended metric improves without excessive table/TLB or I/O overhead.

## Rollback

Kernel/MMU/page-policy rollback is platform-specific and not prescribed by this chapter: `[Needs confirmation]`.

For chapter-described mechanisms, rollback conceptually means restoring the prior page-table/protection mapping, replacement/allocation policy or process residency state after verifying that the previous state is still valid.
