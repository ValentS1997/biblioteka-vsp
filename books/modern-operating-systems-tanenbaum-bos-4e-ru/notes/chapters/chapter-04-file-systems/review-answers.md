# Review answers — RAG-grounded

These answers are derived from chapter 4 only. They are not an official publisher answer key. Calculations use the chapter's models and the assumptions stated in the questions. Figure-only and environment-dependent results remain `[Needs confirmation]`.

1. Five pathnames that resolve to the same file are, for example:
   - `/etc/passwd`
   - `/etc/./passwd`
   - `/./etc/passwd`
   - `/etc/../etc/passwd`
   - `/etc/../../etc/passwd`
   
   The chapter notes that `.` refers to the current directory and `..` to the parent; in the root directory `..` points back to the root itself.

2. Two source-supported approaches are:
   - use the **filename extension** and its registered owner/application association;
   - inspect the **file contents/header**, such as a magic number identifying a recognized file format.

3. The chapter explicitly says the magic number lets the OS recognize a valid executable and prevents accidental execution of a file in the wrong format. The exact historical reason that the numeric value itself was chosen as a particularly non-random value is **[Needs confirmation]** from the available chapter text.

4. `open` is not logically indispensable: a system could resolve the pathname and retrieve file metadata/block locations on every `read` or `write`. The consequence would be repeated pathname lookup and metadata work, loss of the efficient open-file-table state described in the chapter, and a more cumbersome way to maintain current file position. `open` exists to do this setup once and return a descriptor for later calls.

5. No separate rewind primitive is required. A random-access system can move the current position back to offset 0 using its seek operation.

6. They are not equivalent in cost or object identity. `rename` can change namespace information without copying all file data. Copy-then-delete creates a separate file representation, copies the bytes, may create different metadata, and then removes the old directory entry. Existing hard-link relationships therefore need not be preserved by copy/delete.

7. Conceptually, the mapped region must correspond to a defined byte range of the file and be represented through virtual-memory pages; accesses outside that region must not silently become accesses to unrelated file data. Page-granularity alignment and handling of a partial first/last page are natural implementation constraints, but the exact API restrictions are not specified in chapter 4 and are therefore **[Needs confirmation]**.

8. Yes. Encode hierarchy into the flat filename namespace, for example by treating a separator inside a long filename as a simulated directory delimiter and letting a user-level program interpret prefixes as directories. The physical file system remains flat; the hierarchy exists by naming convention.

9. Supply the desired byte offset as an argument to each read/write request instead of mutating a shared current-position pointer. The chapter does not name a specific API for this alternative.

10. **`/usr/ast/x`**.

11. **Internal fragmentation.** The unused space lies inside the allocated final block, analogous to unused space inside a fixed-size page in memory management.

12. 
   - a) **Contiguous allocation:** damage normally corrupts the contents of that block, but later block locations are still computable from the starting block and offset.
   - b) **Linked allocation:** because the next-block pointer is stored in the block, damage can corrupt both local data and the chain pointer, potentially making the rest of the file unreachable.
   - c) **Indexed/table allocation:** corruption of one data block damages that block's contents, while the mapping to later blocks remains available in the separate index/table. Damage to the index structure itself would be a different and broader failure.

13. For an 8-KB file at 8 MB/s, transfer time is about 1 ms. One read therefore costs about `5 + 4 + 1 = 10 ms`; reading and rewriting the file costs about **20 ms**.  
   If half of a 16-GB disk means about 8 GB of such files, the operation is roughly **5.6–5.8 hours**, depending on whether decimal or binary GB/KB units are assumed. Using binary units gives about **5.81 h**.

14. No. The per-file seek/rotation overhead makes compaction after every deletion far too expensive. The chapter instead treats defragmentation as an occasional optimization when fragmentation has accumulated enough to hurt rotating-disk performance.

15. The chapter gives **CD, DVD, Blu-ray and other write-once optical media** as the natural case: file sizes are known in advance and do not grow after the image is written. DVD movie files are described as contiguous extents.

16. The exact figure 4.10 layout is not independently encoded in RAG. If the figure is interpreted according to the surrounding text as **10 direct data addresses plus one single-indirect address**, then a 1024-KB indirect block with 8-byte addresses holds `1,048,576 / 8 = 131,072` addresses. Maximum data is therefore `(10 + 131,072) × 1 MiB = 137,449,439,232 bytes ≈ 128.01 GiB`. Because this depends on the unavailable figure layout, the exact expected answer is **[Needs confirmation]**.

17. **Contiguous allocation** is the strongest fit if the file size is stable: fixed-size records and random access allow direct calculation of the target block with no chain traversal. If substantial growth is expected, indexed allocation becomes more attractive.

18. **Indexed/table-based allocation.** The file can grow and shrink without being moved to a new contiguous region, while random access remains much faster than following a linked chain.

19. The exact number of bytes requires the field sizes/layout shown in figure 4.10, which are not exposed by the text RAG. Therefore the numeric answer is **[Needs confirmation]**. The general optimization is to reuse pointer/address space in the i-node for inline data when the file is small enough.

20. **Eleanor is right.** The chapter's i-node scheme gains memory efficiency by keeping metadata for active/open files in memory. Re-reading duplicate copies on every open wastes memory and risks having multiple in-memory copies of state associated with the same file; looking up an already resident i-node preserves one shared metadata object.

21. Hard-link advantage: it refers directly to the same underlying file/i-node, avoiding pathname indirection and remaining valid when another name for that file is removed. Symbolic-link advantage: it can cross disk/file-system boundaries and can even name a file on a remote machine.

22. A **hard link** is another directory entry containing the same i-node number as the original file. A **symbolic link** has its own file/i-node and stores a pathname that is resolved later to the target.

23. A 4-TB disk with 4-KB blocks has `2^28` blocks, so a block number needs 28 bits and is naturally stored in 4 bytes. A 4-KB free-list block has 1024 such words; reserving one word for the pointer to the next free-list block leaves **1023 block addresses**.

24. Bitmap size is `B` bits. A simple free list needs approximately `F·D` bits for F free block addresses. The list is smaller when:
   `F·D < B`, or `F/B < 1/D`.
   
   For `D = 16`, the disk must be less than **1/16 = 6.25% free** for the list to use less space than the bitmap, ignoring small list-link overhead.

25. Using 1 = allocated and allocating from the lowest free block:
   - a) after B (5 blocks): **`1111 1111 1111 0000`**
   - b) after deleting A: **`1000 0001 1111 0000`**
   - c) after C (8 blocks): **`1111 1111 1111 1100`**
   - d) after deleting B: **`1111 1110 0000 1100`**

26. **UNIX/i-node style:** the free-space structure can be reconstructed by scanning all i-nodes, marking every block referenced by files as allocated, then treating the complement as free—the same principle used by the chapter's consistency checker.  
   **FAT-16:** the FAT is not merely a free-space bitmap; it also stores each file's block chain. If only an in-memory copy is lost but the on-disk FAT survives, it can be reloaded. If the FAT structure itself is completely lost, directory entries provide only the starting block and size, so fragmented chains generally cannot be reconstructed reliably from chapter information alone.

27. Yes. The chapter explicitly warns that backing up an active file system while files/directories are created, deleted or modified can produce a contradictory backup assembled from different moments in time. Its mitigation is to create a fast stable snapshot-like copy of critical structures and back up that frozen view.

28. Compare each file's modification time with the chosen backup cutoff—the last full or incremental backup time. Logical backup in the chapter archives files changed since a specified baseline date.

29. Exact changes to all four bitmaps depend on figures 4.22/4.23, whose bit positions are not available in text RAG. At minimum, inode/file 21 would no longer be marked as a changed file; ancestor directories would remain marked only if still needed to reach other changed descendants. Exact four arrays: **[Needs confirmation]**.

30. It improves locality. The chapter notes that short files normally require one disk access for the i-node and another for the first data block. Putting initial data with the i-node can collapse those accesses and avoid a head movement on a rotating disk.

31. Yes, severe corruption could in principle make the same block appear multiple times among allocated references and multiple times in a free list. The repair principles described by the chapter are: rebuild/remove duplicates from the free list, and when one data block is referenced by multiple files allocate a new free block, copy the data and redirect one file to the copy.

32. Taking 1 ms for a hit and 40 ms for a miss serviced from disk:
   `T(h) = h·1 + (1-h)·40 = 40 - 39h ms`.
   
   Thus `T(0)=40 ms`, `T(1)=1 ms`; the graph is a straight decreasing line.

33. **Write-through caching** is safer for a removable external disk. The chapter explains that delayed dirty blocks can be lost and can damage file-system consistency if media is removed before a flush, whereas write-through pays more I/O cost to reduce that risk.

34. Generally **no**. The application performs random record access based on student IDs. The chapter says read-ahead is useful for sequential access and can waste bandwidth/cache space for random access.

35. Follow the FAT chains:
   - `f1`: **22 → 19 → 15 → 17 → 21 → -1**
   - `f2`: **16 → 23 → 14 → 18 → 20 → -1**

36. At 15,000 rpm one revolution takes 4 ms, so average rotational latency is 2 ms. For a block of `k` bytes:
   `T = 6 ms + 2 ms + 4 ms·k/1,048,576`.
   
   Approximate transfer rates:
   - 1 KB: **127,938 B/s ≈ 125 KiB/s**
   - 2 KB: **255,750 B/s ≈ 250 KiB/s**
   - 4 KB: **511,002 B/s ≈ 499 KiB/s**

37. A 1-KB file consumes one 4-KB block, so **3/4 = 75%** of its allocated space is wasted. Real aggregate waste is likely **lower**, because the chapter's measurements show that a relatively small number of larger files consume most disk blocks and use their final-block slack much more efficiently.

38. One 4-KB indirect block holds `4096/4 = 1024` block addresses. Total data blocks = `10 + 1024 = 1034`. Maximum file size:
   **`1034 × 4096 = 4,235,264 bytes`** (about 4.04 MiB).

39. FAT-16 has about 65,536 table entries in the simplified model. If one file consumes `k` entries, all other files together can consume at most about **`65,536 − k` data blocks**, so their total bytes are bounded by `(65,536 − k) × cluster_size`, ignoring reserved/special FAT entries.

40. A 4-KB indirect block with 4-byte addresses holds 1024 pointers. Addressable data blocks:
   `10 + 1024 + 1024^2 + 1024^3 = 1,074,791,434`.
   
   Maximum file size:
   **`1,074,791,434 × 4096 = 4,402,345,713,664 bytes ≈ 4.004 TiB`**.

41. Starting with only the root i-node in memory, each path component requires reading the current directory block and then the next component's i-node. For `usr/ast/courses/os/handout.t`: 5 directory-block reads (root, usr, ast, courses, os) plus 5 i-node reads (usr, ast, courses, os, handout.t) = **10 disk operations**.

42. Advantages: first-file data can be physically close to metadata; a short-file open/read may need fewer seeks; i-nodes need not live in one fixed disk region. Disadvantages: locating an i-node by a stable i-number becomes harder; directory entries may need physical-location information; moving/rewriting the first block complicates metadata identity; hard-link/shared-reference handling becomes less clean than a stable independent i-node table.

43. Source-grounded design: open the file for random access, maintain two buffers, seek to equal-sized chunks from the front and back, read both, reverse the byte order inside each buffer, then write each reversed buffer to the opposite position. For an odd middle chunk, reverse it in place. This reduces system calls compared with swapping bytes individually. Exact implementation/testing output is **[Needs confirmation]**.

44. Recursively use directory iteration (`opendir`/`readdir`/`closedir` in the chapter model), obtain each regular file's size via file attributes, compute `bucket = floor(size / bucket_width)`, increment the bucket counter, and recurse into subdirectories while avoiding `.` and `..`. Empirical histogram output is **[Needs confirmation]**.

45. Traverse all directories and collect a map `inode_number → [pathnames]`. UNIX directory entries identify files by i-node number, so after the scan report every map entry with two or more distinct names. Symbolic links have their own i-nodes and should not be counted as hard links to their targets. Actual program/run results are **[Needs confirmation]**.

46. For each directory argument: open it, iterate entries, obtain the source-required attributes for each entry, format one line per file, and close the directory. The chapter explicitly describes `ls` as an example program using directory-open/read operations. Exact field layout and implementation output are **[Needs confirmation]**.

47. Write/read the same large file repeatedly while varying the application buffer size (e.g. 64 B, 128 B, …, 4 KB); measure elapsed time with the question's suggested `gettimeofday`/`getitimer`; record total throughput and time per call. The measured relationship depends on the actual machine/file system/cache and is **[Needs confirmation]** until executed.

48. A source-consistent simulated image can contain: superblock, free-space bitmap/list, i-node table, directory records and data blocks. Choose one allocation scheme (contiguous, linked/FAT-like or indexed/i-node), implement pathname lookup and open-file state, then support create/delete directory, create/delete/open file, read/write and directory listing. Validate that allocation and free-space metadata remain consistent after each operation. Actual implementation and tests are **[Needs confirmation]**.
