# Chapter 4 cheatsheet — Файловые системы

## Symptom / problem framing

Start by locating the failure domain:

- cannot resolve/open a path → namespace/directory/VFS path;
- file exists but access is denied → attributes/protection;
- wrong/missing file data → block mapping or damaged data;
- disk appears full unexpectedly → free-space accounting, lost blocks, quotas or fragmentation;
- crash leaves inconsistent metadata → journal/recovery/consistency path;
- slow sequential I/O → cache/read-ahead/locality/block-size path;
- slow random I/O → allocation/layout/cache path;
- restore cannot recreate state → backup scope, hard links, sparse files or active-filesystem consistency.

## Baseline / context

### External view

```text
pathname
  ↓
directory hierarchy
  ↓
file metadata / attributes
  ↓
open file descriptor
  ↓
read / write / seek / close
```

### Internal view

```text
name
  ↓
directory entry
  ↓
inode / FAT / allocation metadata
  ↓
logical file block
  ↓
physical disk block
```

### Allocation comparison

| Method | Strength | Main cost |
|---|---|---|
| Contiguous | simple; excellent sequential/random locality | growth and placement constraints |
| Linked blocks | easy growth; every free block usable | random access requires chain traversal |
| FAT | chain traversal occurs in memory | table memory grows with disk size |
| I-node/indexed | metadata memory scales with open files | indirect blocks add lookup levels |

## Read-only checks

1. Resolve the exact absolute path and current working directory.
2. Confirm whether the object is a regular file, directory, special file or link.
3. Inspect attributes needed by the operation: size, protection, timestamps, ownership/link count where available.
4. Determine allocation model: contiguous, linked/FAT or indexed/i-node.
5. Check whether the problem concerns data blocks or metadata structures.
6. Compare used-block references with the free-space structure.
7. Check hard-link counts against actual directory entries.
8. Determine whether modified metadata/data may still reside only in cache.
9. Determine whether access is sequential or random before enabling/read-ahead assumptions.
10. For backup, establish whether the source is changing during the backup.
11. Preserve sparse-file holes rather than materializing them as zero-filled blocks.
12. Exclude special/internal files from backup when the source model requires it.
13. Before defragmentation, identify the underlying medium; chapter guidance distinguishes rotating disks from SSD.

## Interpretation

### Namespace and links

- absolute path: starts from root;
- relative path: starts from current working directory;
- hard link: multiple directory entries → same i-node/file;
- symbolic link: separate object containing a pathname;
- unlink removes a directory entry; the file disappears only when no remaining hard links keep it referenced.

### Crash consistency

A multi-step metadata operation can leave the file system inconsistent if interrupted. Journaling records intentions first so recovery can complete/replay interrupted work. Idempotent recovery operations are preferred.

Consistency checks look for:

- lost blocks: neither used nor free;
- duplicate entries in the free list;
- a data block referenced by multiple files;
- link-count mismatch between directory entries and i-node metadata.

### Backup

- physical backup: block-oriented, simple and fast, but poor for selective/incremental restore;
- logical backup: walks files/directories, supports selective and incremental backup;
- active source changes can create a contradictory backup;
- chapter-described mitigation is a fast stable snapshot/copy-on-write-like view before the long backup.

### Performance

- block cache avoids disk access on hits;
- dirty metadata should not simply remain indefinitely at the LRU tail;
- `sync`-style flushing reduces the loss window;
- write-through increases I/O but reduces removable-media durability risk;
- read-ahead helps sequential access only;
- placing related blocks near each other reduces head movement on rotating disks;
- SSDs remove seek/rotation concerns; chapter explicitly treats defragmenting SSDs as counterproductive.

## Next action

For a suspected file-system failure:

`freeze risky writes if needed → capture namespace/metadata state → classify allocation vs consistency vs durability → use the narrowest source-supported recovery mechanism → verify structure and data → resume writes`.

## Modifying action

Source-supported modifying actions include:

- create/delete/rename files or directories;
- write/append file data;
- link/unlink directory entries;
- update file attributes;
- flush dirty cache blocks;
- rebuild free-space metadata or correct link counts during consistency repair;
- journal/replay metadata operations;
- restore from backup;
- defragment movable files on appropriate rotating media.

Each can change persistent state. Do not substitute one mechanism for another: repair, backup restore and performance optimization solve different problems.

## Verification / acceptance checks

After a file-system change, verify:

- target path resolves to the intended object;
- file size/content and required attributes are intact;
- every allocated block is accounted for exactly as intended;
- no data block is simultaneously free and referenced;
- hard-link count matches directory references;
- dirty metadata is durably written when durability is required;
- backup restore recreates directories before dependent files/links;
- performance change improves the targeted workload rather than only a synthetic path;
- no SSD defragmentation was introduced from rotating-disk assumptions.

## Rollback

- Namespace mutations can be rolled back only if the prior name/link/object still exists or a backup provides it.
- Data overwritten by `write` is not recoverable from the chapter's mechanisms unless another copy/backup exists.
- Consistency-repair rollback is not generally defined by the chapter: preserve a backup/snapshot first when possible.
- Defragmentation rollback is normally unnecessary if data remains intact; exact platform procedure is `[Needs confirmation]`.
