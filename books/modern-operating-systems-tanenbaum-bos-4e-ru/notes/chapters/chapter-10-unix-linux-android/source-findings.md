# Source findings — Chapter 10

## [Source extraction issue] Terminal input-speed getter token

- PDF page 844 / chunk `p0844:c01`.
- The extracted POSIX terminal-control table contains `cfgtetispeed`.
- The surrounding entries are readable, but the exact identifier in the text layer is not trustworthy.

Handling: preserve the malformed extracted token as a finding and do not silently rewrite it from model memory.

## [Needs confirmation] Review question 50 asks for a performance guess

The chapter asks which Linux system call is likely to be fastest, but the RAG chapter does not provide a benchmark or authoritative ranking.

Handling: answer only with a reasoned candidate and label the exact result `[Needs confirmation]`.

## [Needs confirmation] Review question 52 lacks enough ext2 sizing parameters

- The chapter states the ext2 block-group layout and that an i-node is 128 bytes.
- The floppy exercise specifies capacity and 1 KiB blocks.
- The number of i-nodes / resulting i-node-table size is not supplied in the question text.

Handling: compute the fixed layout constraints but do not invent an exact maximum user-data byte count.

## [Needs confirmation] Review question 56 requires live `/proc` observation

The exercise asks the reader to inspect a real `/proc/####` directory and report file sizes, timestamps and permissions. Those values depend on a live Linux system and are not present in chapter RAG.

Handling: preserve the chapter's general `/proc` semantics; empirical values remain `[Needs confirmation]`.

## [Needs confirmation] Review questions 63–66 require external execution environments

- Q63 requires an x86 BIOS/boot-floppy assembly environment.
- Q64 requires two Linux systems and serial hardware.
- Q65 requires implementing and benchmarking two IPC/file-transfer designs.
- Q66 requires implementing a user-level threads library and comparing schedulers.

Handling: provide source-grounded designs and acceptance criteria, but do not fabricate measured results or unprovided implementation details.

## Historical implementation boundary

The chapter describes implementation details current to its edition, including O(1), CFS, Dalvik, chapter-era Android `oom_adj`, historical UNIX login/password behavior and NFS variants. No external modernization is applied under `rag_only`.
