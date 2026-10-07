# Глава 3 — Управление памятью

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 3 — «Управление памятью»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `214–300`
- Addressable RAG chunk range: `p0214:c01 … p0300:c01`
- Chunks in chapter range: `87`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 214 begins with `Глава 3. Управление памятью`;
  - PDF page 301 begins with `Глава 4. Файловые системы`.
- Chapter boundary: `VERIFIED`

The chapter-end summary begins on PDF page 290 and continues onto PDF page 291. Review questions/exercises occupy PDF pages 291–300.

## Main principle

The chapter builds memory management as a sequence of abstractions and implementation trade-offs:

1. **Physical memory without abstraction** is simple but does not safely isolate or relocate unrelated programs.
2. **Address spaces** separate a process's addresses from physical placement and provide a basis for protection.
3. **Swapping** moves whole processes between RAM and disk when RAM cannot hold all processes.
4. **Virtual memory** decouples a process's address space from the amount of resident physical memory; paging maps virtual pages to physical page frames.
5. **Page tables and TLBs** implement and accelerate address translation.
6. **Page replacement** decides which resident page to evict after a page fault.
7. **Working-set/load-control policies** prevent excessive page-fault activity (thrashing).
8. **Segmentation** provides multiple logical address spaces with different sharing/protection properties and can be combined with paging.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 3.1 | Memory without abstractions | 215–217 |
| 3.2 | Memory abstraction: address spaces | 218–226 |
| 3.2.1 | Address spaces; base/limit registers | 218–221 |
| 3.2.2 | Swapping | 221–224 |
| 3.2.3 | Free-memory management | 224–227 |
| 3.3 | Virtual memory | 227–243 |
| 3.3.1 | Paging | 229–233 |
| 3.3.2 | Page tables | 233–235 |
| 3.3.3 | TLB / faster paging | 235–239 |
| 3.3.4 | Page tables for large memories | 239–243 |
| 3.4 | Page-replacement algorithms | 243–257 |
| 3.4.1–3.4.5 | Optimal, NRU, FIFO, second chance, clock | 244–248 |
| 3.4.6–3.4.7 | LRU, NFU and aging | 248–250 |
| 3.4.8–3.4.9 | Working set and WSClock | 250–256 |
| 3.4.10 | Replacement-algorithm comparison | 256–257 |
| 3.5 | Paging-system design | 257–270 |
| 3.5.1–3.5.3 | Local/global policy, load control, page size | 258–263 |
| 3.5.4–3.5.9 | I/D spaces, shared pages/libraries, mapped files, cleaning, VM interface | 263–270 |
| 3.6 | Implementation issues | 270–277 |
| 3.6.1–3.6.6 | Paging involvement, page faults, instruction restart, pinning, backing store, policy/mechanism | 270–277 |
| 3.7 | Segmentation | 277–290 |
| 3.7.1 | Pure segmentation | 281 |
| 3.7.2 | Segmentation + paging: MULTICS | 281–285 |
| 3.7.3 | Segmentation + paging: Intel x86 | 285–290 |
| 3.8 | Memory-management research | 290 |
| 3.9 | Short conclusions | 290–291 |
| — | Review questions / exercises | 291–300 |

Section/page mapping is derived from the RAG table of contents on PDF pages 8–9.

## Key concepts

- **Address space:** the set of addresses a process may use; distinct process address spaces are logically independent.
- **Base/limit scheme:** adds a relocation base to generated addresses and checks accesses against a limit; simple but adds work to every memory reference.
- **Swapping:** whole-process movement between RAM and disk.
- **Free-memory tracking:** bitmaps or linked lists of allocated/free segments; allocation policies include first fit, next fit, best fit and worst fit.
- **Virtual address / physical address:** the program generates a virtual address; the MMU translates it to a physical address.
- **Page / page frame:** fixed-size virtual and physical blocks; page faults occur when a referenced virtual page is not resident.
- **Page table:** maps virtual page numbers to page-frame numbers and carries presence/protection/state information.
- **TLB:** small associative cache of recent page translations; a hit avoids a normal page-table lookup.
- **Minor page fault:** mapping is missing but the page is already in memory; a disk read is unnecessary.
- **Major page fault:** required page must be read from disk.
- **Multilevel page table:** allocates lower-level structures only for populated virtual-address regions.
- **Inverted page table:** one entry per physical page frame rather than per virtual page; saves table space at the cost of harder lookup.
- **R/M bits:** referenced and modified state used by replacement approximations.
- **Replacement algorithms:** Optimal, NRU, FIFO, second chance, clock, LRU, NFU, aging, working set and WSClock.
- **Demand paging:** pages enter memory on demand.
- **Working set:** pages recently used by a process; insufficient memory for the active working set leads to thrashing.
- **Local vs global replacement:** victim is chosen only from the faulting process or from all resident pages.
- **Copy on write:** initially share read-only data pages and copy only a page that is actually modified.
- **Mapped files:** a file is mapped into virtual address space and can serve as backing storage and shared memory.
- **Page pinning:** keeps an I/O/DMA buffer resident so replacement cannot move/reuse its frame during transfer.
- **Segmentation:** variable-size logical address spaces; unlike paging it can suffer external fragmentation.

## Practical interpretation

When memory pressure or latency is observed, distinguish:

`address-space/protection problem` ≠ `TLB miss` ≠ `minor page fault` ≠ `major page fault` ≠ `replacement pressure` ≠ `thrashing`.

Changing a replacement algorithm cannot fix an invalid address, and adding page frames does not fix a protection fault.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- Figures are referenced by extracted RAG text but are not independently encoded as multimodal RAG objects.
- Questions that depend on numeric labels contained only inside a figure are marked `[Needs confirmation]` when the text layer does not expose those labels.
- Environment-dependent experiments in questions 51–56 require measurements/program execution and remain `[Needs confirmation]` where appropriate.
- A source contradiction affecting base/limit values around figure 3.3 is recorded in `source-findings.md`.
