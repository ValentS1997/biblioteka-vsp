# Chapter 10 conceptual / diagnostic flow

```mermaid
flowchart TD
    U["User / application"] --> SH["Shell / Android component"]
    SH --> LIB["C library / framework API"]
    LIB --> SC["System-call / Binder boundary"]

    SC --> P["Process / task management"]
    SC --> M["Virtual memory"]
    SC --> IO["I/O + VFS"]
    SC --> SEC["UID/GID protection"]

    P --> F["fork / clone / exec"]
    P --> S["O(1) / CFS scheduling"]
    F --> COW["copy on write"]

    M --> VMA["VMA / page tables"]
    VMA --> MMAP["mmap / shared mappings"]
    VMA --> PFRA["page reclaim / swap"]
    PFRA --> BUD["buddy + slab"]

    IO --> FD["fd → open file → inode"]
    IO --> DEV["special files / drivers"]
    IO --> NET["sockets"]
    IO --> NFS["NFS"]
    FD --> VFS["VFS / ext2/ext4"]

    SEC --> MODE["owner/group/other rwx"]
    SEC --> SET["effective UID / SETUID"]

    SH --> AND["Android framework"]
    AND --> Z["zygote"]
    AND --> ACT["ActivityManager"]
    AND --> INT["intents / components"]
    AND --> BIN["Binder IPC"]
    Z --> UID["per-app UID sandbox"]
    ACT --> OOM["process importance / oom_adj"]
    BIN --> CAP["identity-preserving capability references"]
```

## Diagnostic boundary

```text
process identity ≠ address-space sharing
file descriptor ≠ inode
pathname permission ≠ already-open access
page fault ≠ necessarily invalid memory
Android application state ≠ Linux process lifetime
Binder object identity ≠ proof of original recipient process
```
