# Chapter-end summary

Provenance: PDF pages 290–291; chunks `p0290:c01` and `p0291:c01`.

The chapter concludes with these source-grounded points:

- The simplest systems may keep one program resident until completion and use neither swapping nor paging; variants of this model remain relevant to small embedded real-time systems.
- Address spaces provide an abstraction that separates program-visible addresses from physical placement and supports protection between processes.
- Swapping permits more processes than RAM can hold simultaneously by moving whole inactive processes to disk.
- Free memory can be tracked with bitmaps or linked lists of free regions.
- Modern systems commonly use virtual memory: each process address space is split into fixed-size pages that may occupy arbitrary physical page frames.
- Page replacement is central to paging performance. The chapter's comparison identifies **aging** and **WSClock** as particularly practical algorithms.
- Good paging requires more than a replacement algorithm; working-set size, frame-allocation policy, page size and load control also matter.
- Segmentation supports independently sized logical structures, sharing and differentiated protection, but variable-size segments create external fragmentation.
- Segmentation and paging can be combined, as illustrated by MULTICS and 32-bit x86; the chapter notes that full segmentation is not a central feature of 64-bit x86.
