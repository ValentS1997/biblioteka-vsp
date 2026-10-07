# Chapter 11 conceptual / diagnostic flow

```mermaid
flowchart TD
    A[Application] --> API[Win32 / WinRT]
    API --> NAT[Native NT services]

    NAT --> OM[Object Manager]
    NAT --> PM[Process / Thread Manager]
    NAT --> MM[Memory Manager]
    NAT --> IO[I/O Manager]
    NAT --> SRM[Security Reference Monitor]

    OM --> H[Handles + object namespace]
    PM --> SCH[Kernel scheduler]
    SCH --> PRI[base/current priority + boosts]
    PRI --> NUMA[ideal processor / NUMA]

    MM --> VAD[VAD + page tables]
    VAD --> WS[working sets]
    WS --> PFN[PFN lists]
    MM --> CM[Cache Manager]

    IO --> IRP[IRP]
    IRP --> DS[device/filter stack]
    DS --> NTFS[NTFS]
    NTFS --> MFT[MFT + attributes + streams]

    SRM --> TOK[access token]
    SRM --> SD[security descriptor]
    TOK --> ACL[SID / groups / privileges / integrity]
    SD --> ACL

    NAT --> K[kernel]
    K --> HAL[HAL]
    HAL --> HW[hardware]
    HV[Hyper-V optional] --> HW
```

## Diagnostic boundary

```text
process ≠ scheduled entity
handle ≠ pointer
reserve ≠ commit
soft fault ≠ storage I/O
file ≠ one byte stream
DACL allow ≠ integrity-level allow
hibernate ≠ shutdown
```
