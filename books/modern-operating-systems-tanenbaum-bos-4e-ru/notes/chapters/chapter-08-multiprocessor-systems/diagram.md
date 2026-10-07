# Chapter 8 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Multiple execution nodes"] --> B{"Shared physical memory?"}
    B -->|yes| M["Multiprocessor / SMP"]
    B -->|no| C{"Tightly coupled dedicated interconnect?"}
    C -->|yes| MC["Multicomputer"]
    C -->|no| D["Distributed system"]

    M --> M1["UMA / NUMA"]
    M --> M2["Kernel locking"]
    M2 --> M21["read-before-TSL / backoff"]
    M --> M3["Scheduling"]
    M3 --> M31["affinity"]
    M3 --> M32["space sharing"]
    M3 --> M33["gang scheduling"]

    MC --> C1["Message passing"]
    C1 --> C11["send / receive"]
    C1 --> C12["RPC + stubs + marshalling"]
    MC --> C2["DSM"]
    C2 --> C21["page fault → remote page"]
    C2 --> C22["replication / invalidation"]
    C2 --> C23["false sharing"]
    MC --> C3["Load balancing"]
    C3 --> C31["sender initiated"]
    C3 --> C32["receiver initiated"]

    D --> D1["Network services / TCP/IP"]
    D --> D2["Middleware"]
    D2 --> D21["documents / Web"]
    D2 --> D22["distributed files"]
    D2 --> D23["objects / CORBA"]
    D2 --> D24["Linda / pub-sub"]
```

## Diagnostic boundary

```text
shared-memory contention
  ≠ message-copy/RPC overhead
  ≠ DSM coherence/page movement
  ≠ distributed-network latency
  ≠ middleware semantics
```
