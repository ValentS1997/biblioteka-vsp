# Chapter 1 conceptual flow

```mermaid
flowchart TD
    HW["Hardware<br/>CPU · memory · disks · I/O · buses"] --> K["Kernel mode<br/>privileged OS mechanisms"]
    K --> A["OS as extended machine<br/>stable abstractions"]
    K --> R["OS as resource manager<br/>allocation + protection"]
    A --> P["Processes"]
    A --> M["Address spaces"]
    A --> F["Files / directories / pipes"]
    R --> TM["Time multiplexing<br/>CPU · printer · I/O"]
    R --> SM["Space multiplexing<br/>memory · disk"]
    P --> SC["System-call / API boundary"]
    M --> SC
    F --> SC
    SC --> U["User mode<br/>applications · shell · GUI"]
    K --> S["OS structures"]
    S --> MON["Monolithic"]
    S --> LAY["Layered"]
    S --> MIC["Microkernel"]
    S --> CS["Client-server"]
    S --> VM["Virtual machines"]
    S --> EXO["Exokernel"]
    HW --> BOOT["Boot path<br/>firmware → loader → OS → drivers/services"]
    K --> DEV["Controllers + device drivers"]
    DEV --> HW
    S --> CDEV["C implementation model<br/>headers · conditional compilation · make · linker"]
```

## Reading path

```text
raw hardware
   ↓ hidden/controlled by
operating system
   ├─ abstractions for applications
   └─ resource allocation/protection
            ↓
       system-call/API boundary
            ↓
 processes · memory · files · I/O · security
            ↓
 detailed mechanisms in later chapters
```
