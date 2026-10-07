# Chapter-end summary

Provenance: PDF page 374; chunk `p0374:c01`.

The chapter's explicit conclusions are:

- Externally, a file system is a collection of files/directories and operations on them. Modern systems commonly use hierarchical directories.
- Internally, designers must decide how storage is allocated and how file blocks are tracked.
- The chapter compares contiguous allocation, linked allocation, FAT-style tables and i-nodes.
- Directory structures and the location of file attributes vary between file systems.
- Free disk space can be managed using free-block lists or bitmaps.
- Reliability is improved through backup and consistency-repair mechanisms.
- Performance can be improved through caching, read-ahead and placing related blocks close together.
- Log-structured file systems improve write behavior by writing larger accumulated segments.
- ISO 9660, MS-DOS/FAT and UNIX are examples with materially different allocation, directory and free-space designs.
