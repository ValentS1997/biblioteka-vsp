# Краткое содержание главы 6

**Provenance:** explicit chapter summary `p0547:c01`, with structure from chapter RAG.

## Operating-system level

The operating system can be viewed as an interpreter that adds abstractions not directly present at the instruction-set level.

The chapter concentrates on three groups:

1. virtual memory;
2. virtual I/O/file operations;
3. parallelism and synchronization.

## Virtual memory

Virtual memory separates the program-visible address space from installed physical memory.

Paging divides virtual space into fixed-size pages and physical memory into same-size frames. Page tables map one to the other. Access to a nonresident page causes a page fault that the operating system resolves.

Demand paging, locality and working sets explain why a program can use a virtual address space larger than RAM without constant faults, provided its active working set fits.

The chapter contrasts LRU and FIFO replacement and explains thrashing.

Segmentation provides multiple logical address spaces of variable size and supports protection appropriate to logical objects. Pure segmentation may suffer external fragmentation; segmentation may also be combined with paging.

Core i7 supports segmentation plus paging, while OMAP4430 uses paging and TLB-based translation.

## Virtualization

Hardware virtualization permits multiple operating systems to share one physical machine. A hypervisor controls access to processor state, memory and I/O. Core i7 VMX/EPT is the chapter's hardware example.

## Virtual I/O

The file is the central abstraction.

Applications issue open/read/write/close-like operations while the OS handles device-specific details, file metadata, allocation and error handling.

Files may occupy contiguous or noncontiguous blocks. Free disk space can be represented by a free list or bitmap. Directories group names and map them to filesystem metadata.

## Parallelism

A process is a running program plus its execution state. Multiple processes can execute truly in parallel on multiple CPUs or be time-sliced on one CPU.

Shared state creates race conditions when check/update sequences are not atomic.

Semaphores provide atomic `up` and `down` operations. They preserve wakeup information and allow producer/consumer synchronization without the lost-wakeup race demonstrated earlier in the chapter.

## UNIX and Windows

Both example systems support:

- paged virtual memory;
- memory-mapped files;
- hierarchical filesystems;
- processes and threads;
- synchronization mechanisms.

Their APIs and protection models differ, but the abstractions correspond to the same OS-machine-level functions.
