# Глава 4 — Файловые системы

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 4 — «Файловые системы»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `301–379`
- Addressable RAG chunk range: `p0301:c01 … p0379:c01`
- Chunks in chapter range: `79`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 301 begins with `Глава 4. Файловые системы`;
  - PDF page 380 begins with `Глава 5. Ввод и вывод информации`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary starts on PDF page 374. Review questions/exercises occupy PDF pages 374–379.

## Main principle

The chapter treats a file system as two complementary views:

1. **External abstraction:** persistent named files, directories, paths, attributes and operations.
2. **Internal implementation:** mapping names to metadata and file blocks, tracking free space, preserving consistency and improving I/O performance.

The implementation problem is therefore not only “where are the bytes?” but also:

`name resolution → metadata → block mapping → free-space accounting → crash consistency → caching/performance → recovery`.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 4.1 | Files | 303–314 |
| 4.1.1 | File names | 303–305 |
| 4.1.2 | File structure | 305–306 |
| 4.1.3 | File types | 306–308 |
| 4.1.4 | File access | 308–309 |
| 4.1.5 | File attributes | 309–310 |
| 4.1.6 | File operations | 310–312 |
| 4.1.7 | File-system-call example | 312–314 |
| 4.2 | Directories | 314–319 |
| 4.2.1–4.2.4 | Flat/hierarchical directories, path names, directory operations | 315–319 |
| 4.3 | File-system implementation | 319–339 |
| 4.3.1 | File-system structure | 320–321 |
| 4.3.2 | File implementation / block allocation | 321–326 |
| 4.3.3 | Directory implementation | 326–329 |
| 4.3.4 | Shared files and links | 329–332 |
| 4.3.5 | Log-structured file systems (LFS) | 332–334 |
| 4.3.6 | Journaling file systems | 334–336 |
| 4.3.7 | Virtual file systems (VFS) | 336–339 |
| 4.4 | File-system management and optimization | 339–361 |
| 4.4.1 | Disk-space management | 339–346 |
| 4.4.2 | File-system backup | 346–352 |
| 4.4.3 | File-system consistency | 352–355 |
| 4.4.4 | File-system performance | 355–360 |
| 4.4.5 | Defragmentation | 360–361 |
| 4.5 | File-system examples | 361–373 |
| 4.5.1 | MS-DOS / FAT | 361–365 |
| 4.5.2 | UNIX V7 | 365–367 |
| 4.5.3 | CD file systems | 367–373 |
| 4.6 | File-system research | 373–374 |
| 4.7 | Short conclusions | 374 |
| — | Review questions / exercises | 374–379 |

Section/page mapping is derived from the RAG table of contents on PDF page 9.

## Key concepts

- **File:** persistent storage abstraction named independently of the process that created it.
- **Byte-stream model:** UNIX/Windows model where the OS treats file contents primarily as bytes.
- **Sequential vs random access:** read in order versus seek/read at arbitrary positions.
- **Directory hierarchy:** names are resolved through path components; paths may be absolute or relative.
- **Hard link:** another directory entry referencing the same underlying file metadata/i-node.
- **Symbolic link:** a separate small file/object containing a path to another file.
- **Contiguous allocation:** simple and fast, but file growth and external placement constraints are problematic.
- **Linked allocation:** easy growth, but random access is slow.
- **FAT:** linked allocation with the chain stored in an in-memory allocation table; improves random traversal but scales with disk size.
- **I-node:** per-file metadata/block-address structure loaded only for active/open files.
- **Directory implementation:** translates a pathname component into file metadata/block-location information.
- **LFS:** buffers small writes and appends large segments to a log; requires cleaning old segments.
- **Journaling:** records intended metadata operations before applying them so interrupted operations can be replayed/recovered.
- **VFS:** common upper interface that dispatches standard file operations to different concrete file systems.
- **Free-space management:** linked lists/runs or bitmaps.
- **Backup:** physical or logical; active file systems need a stable snapshot-like view to avoid inconsistent backups.
- **Consistency check:** reconstructs block and directory/link usage to find lost, duplicated or multiply referenced resources.
- **Cache:** memory-resident disk blocks; improves read performance but dirty metadata introduces durability/consistency trade-offs.
- **Read-ahead:** useful for sequential access, harmful or useless for random access.
- **Defragmentation:** attempts to restore locality on rotating disks; the chapter explicitly warns that SSD defragmentation is counterproductive.
- **FAT vs UNIX V7:** examples of table-based block chains versus i-node-based metadata/block mapping.

## Operational interpretation

A file-system incident should be classified before mutation:

`namespace/path problem` ≠ `permissions/attributes` ≠ `allocation/free-space issue` ≠ `metadata inconsistency` ≠ `dirty-cache durability risk` ≠ `fragmentation/performance issue` ≠ `backup/recovery problem`.

For example, defragmentation does not repair a duplicated data block, and a consistency checker does not replace a backup.

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

- Figures/tables are referenced by text RAG but are not independent multimodal RAG objects.
- Figure-dependent review answers remain `[Needs confirmation]` when exact values cannot be recovered from the text layer.
- Programming/measurement exercises requiring execution on a real system remain `[Needs confirmation]` for empirical results.
- Historical examples and product/version statements are preserved as chapter content; they are not updated with external information.
- One code-token mismatch (`ORDONLY` vs `O_RDONLY`) is recorded in `source-findings.md`.
