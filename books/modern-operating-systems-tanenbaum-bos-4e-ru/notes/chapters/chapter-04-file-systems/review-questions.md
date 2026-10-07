# Review questions — source extract

Provenance: chapter-end questions/exercises, PDF pages 374–379, chunks `p0374:c01 … p0379:c01`.

Numbering follows the source. Only structural/extraction cleanup was applied.

1. Give five different pathnames for the file `/etc/passwd`. Hint: use directory entries `.` and `..`.

2. When a Windows user clicks a file in Windows Explorer, a program is started and the file is passed to it. Give two different ways the OS could determine which program to run.

3. Early UNIX executable `a.out` files began with a specially chosen magic number. Why might executables use a deliberately special value while other file types may use more arbitrary magic numbers?

4. Is the `open` system call logically indispensable to UNIX? What would be the consequences of removing it?

5. Sequential-file systems have a rewind operation. Is a separate rewind operation needed in a system supporting random-access files?

6. Is `rename` equivalent to copying a file under a new name and then deleting the old file? What differences remain?

7. Some systems allow only part of a file to be memory-mapped. What restrictions are needed and how can partial mapping be implemented?

8. A simple OS supports only one directory but allows arbitrarily many arbitrarily long file names. Can something resembling a hierarchical file system be simulated?

9. UNIX and Windows use a system call that moves the current file-position pointer for random access. Propose an alternative design for random access without that call.

10. Using the directory tree in figure 4.5, if `/usr/jim` is the working directory, what is the absolute pathname of `../ast/x`?

11. Wasted space in the last block of a file whose size is not an exact multiple of block size: is this internal or external fragmentation?

12. Describe the consequences of damage to a data block under:
   - a) contiguous allocation;
   - b) linked allocation;
   - c) indexed/table-based allocation.

13. Suppose deletion is followed by disk compaction so all files remain contiguous. Seek = 5 ms, rotational latency = 4 ms, transfer rate = 8 MB/s, average file size = 8 KB. How long does it take to read one average file into memory and write it to a new position? How long to compact half of a 16-GB disk?

14. Based on question 13, does compacting a disk after each deletion make practical sense?

15. Name modern consumer devices or media for which contiguous file allocation is a good fit.

16. Consider the i-node in figure 4.10. What maximum file size can it support if it has 10 direct addresses of 8 bytes each and disk blocks are 1024 KB?

17. Student records have fixed size and are accessed/updated in random order. Which allocation scheme—contiguous, linked or indexed/table-based—is best suited?

18. A file varies between 4 KB and 4 MB during its life. Which of contiguous, linked or indexed/table-based allocation is most suitable?

19. It is proposed to store short-file data directly inside the i-node. How many bytes of data can be stored in the i-node shown in figure 4.10?

20. Carolyn proposes reading a fresh copy of an i-node into the in-memory i-node table on every open instead of searching the existing table. Eleanor disagrees. Who is right?

21. Give one advantage of hard links over symbolic links and one advantage of symbolic links over hard links.

22. Explain the i-node-level difference between hard links and symbolic links.

23. A 4-TB disk uses 4-KB blocks and a free-block linked list. How many block addresses can one free-list block hold?

24. Free space may be represented by a linked list or bitmap. Disk addresses are D bits. For a disk of B blocks with F free blocks, when does the linked list use less space than the bitmap? Express the free-space percentage for D = 16.

25. A newly formatted partition begins with bitmap `1000 0000 0000 0000`; block 0 is the root directory. The allocator always searches from the beginning. After writing file A of 6 blocks the bitmap is `1111 1110 0000 0000`. Show the bitmap after:
   - a) writing B of 5 blocks;
   - b) deleting A;
   - c) writing C of 8 blocks;
   - d) deleting B.

26. What happens if the free-block bitmap/list is completely lost in a crash? Can it be reconstructed? Answer separately for UNIX-style and FAT-16 file systems.

27. A backup is running while a text editor modifies the same live file system. Is there a problem?

28. Windows can use an archive bit to decide whether to back up a file. UNIX lacks that bit. How can a UNIX backup program decide which files need backup?

29. Suppose file 21 in figure 4.22 has not changed since the previous backup. How do the four bitmaps in figure 4.23 change?

30. A proposal stores the beginning of each UNIX file in the same disk block as its i-node. What is the benefit?

31. In figure 4.23, can both consistency-check counters for one block have value 2? How can such a problem be repaired?

32. Cache hit time is 1 ms and a disk-serviced request is 40 ms. Derive average request time as a function of cache hit ratio `h`, for `0 ≤ h ≤ 1`.

33. For an external removable USB hard disk, which is more appropriate: write-through caching or ordinary delayed block caching?

34. A student-record application repeatedly looks up one student ID, reads, updates and writes that record. Is block read-ahead useful?

35. A disk has data blocks 14–23. Files `f1` and `f2` begin at blocks 22 and 16. FAT entries are:
`(14,18); (15,17); (16,23); (17,21); (18,20); (19,15); (20,-1); (21,-1); (22,19); (23,14)`.
Which blocks belong to each file?

36. For a disk with average seek 6 ms, 15,000 rpm and 1,048,576 bytes per track, what transfer rate is obtained for block sizes 1, 2 and 4 KB?

37. A file system uses 4-KB blocks and average file size is 1 KB. If every file were exactly 1 KB, what fraction of disk space would be wasted? Would actual waste likely be higher or lower?

38. What maximum file size is addressable with 10 direct addresses and one single-indirect block if block size is 4 KB and block addresses are 4 bytes?

39. In FAT-16, one file occupies `k` FAT entries. What limit does this impose on the total length of all other files?

40. A UNIX file system uses 4-KB blocks and 4-byte disk addresses. What maximum file size is supported by an i-node with 10 direct addresses plus one single-, double- and triple-indirect address?

41. How many disk operations are required to read the i-node of `/usr/ast/courses/os/handout.t` if only the root-directory i-node is initially in memory and each directory occupies one disk block?

42. Consider allocating an i-node when a file is created and storing it at the beginning of that file's first block instead of keeping i-nodes in a fixed area near the disk start. Give arguments for and against.

43. Write a program that reverses the byte order of a file so the last byte becomes first. It must handle arbitrary file sizes efficiently.

44. Write a program that recursively walks a directory tree, records file sizes, and prints a histogram using a configurable bucket width.

45. Write a UNIX program that scans the file-system directories, finds all i-nodes having two or more hard links, and lists every pathname referring to each such file.

46. Write a new UNIX `ls` that accepts one or more directory names and prints one formatted line per file; include at most the first disk address, or omit addresses.

47. Write a program measuring the effect of application buffer size on large-file I/O. Vary the buffer, e.g. 64 bytes to 4 KB, and use timing functions such as `gettimeofday` and `getitimer`. Analyze total and per-write time.

48. Build a simulated file system stored completely inside one ordinary disk file. It should contain directories, i-nodes, free-block information and file data blocks; choose a free-space and allocation strategy and support commands for directory/file creation/deletion, open/read/write and directory listing.
