# Chapter-end summary

Provenance: PDF pages 923–924; chunks `p0923:c01` and `p0924:c01`.

The chapter's explicit conclusions are:

- Linux began as an open-source UNIX clone and became a general-purpose system used across machines ranging from small computers to supercomputers.
- Linux exposes three main programming/user interfaces: the shell, the C library and system calls; graphical environments are layered above these.
- The shell supports commands, pipelines, redirection, background execution and scripting.
- The C library wraps system calls and adds higher-level routines; the system-call layer is the kernel interface.
- Linux represents runnable execution contexts as tasks. Process creation uses `fork` semantics, while copy-on-write avoids eagerly duplicating every page.
- Linux scheduling is task/thread oriented. The chapter contrasts the historical O(1) scheduler with CFS, which tracks weighted virtual runtime in a red-black tree.
- A process address space contains text, data and stack regions; Linux uses virtual memory, demand paging, page replacement and page-oriented swapping.
- I/O devices are integrated into the filesystem through special files; block, character and network I/O are handled through drivers and related kernel subsystems.
- The UNIX/Linux filesystem is a single hierarchical mounted namespace. Opening a file yields a file descriptor; Linux separates per-process descriptors, open-file state and i-nodes.
- Traditional Linux protection uses UID/GID ownership and read/write/execute permissions for owner, group and others.
- Android builds on the Linux kernel but uses it as the foundation for a different application architecture.
- In the chapter's Android model, application code is compiled from Java bytecode to Dalvik bytecode and application processes are created from zygote.
- Binder provides protected object-oriented IPC across process boundaries.
- Android packages describe components and permissions in manifests; major component types include activities, services, receivers and content providers.
- Intents provide late binding between components.
- Android isolates applications using per-application Linux UIDs and treats applications as mutually untrusted.
- Android application processes are managed by importance: cached/background processes can be removed under memory pressure while user-visible work is protected longer.
