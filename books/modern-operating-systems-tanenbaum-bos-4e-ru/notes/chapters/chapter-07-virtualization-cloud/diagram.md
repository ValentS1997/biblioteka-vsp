# Chapter 7 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Guest workload"] --> B{"Operation type"}
    B -->|ordinary user code| C["Direct CPU execution"]
    B -->|sensitive / privileged| D{"Virtualization method"}
    D --> D1["Trap / VM exit + emulate"]
    D --> D2["Binary translation"]
    D --> D3["Paravirtual hypercall"]

    A --> M["Guest virtual memory"]
    M --> M1["Guest physical"]
    M1 --> M2{"Translation"}
    M2 -->|shadow| M3["Hypervisor shadow page table"]
    M2 -->|EPT / nested| M4["Hardware second-level walk"]
    M3 --> P["Machine physical memory"]
    M4 --> P

    P --> R{"Memory pressure"}
    R --> R1["Ballooning"]
    R --> R2["Dedup + copy-on-write"]
    R --> R3["Hypervisor paging"]

    A --> I["Guest I/O"]
    I --> I1["Emulated device"]
    I --> I2["Device domain"]
    I --> I3["Pass-through / SR-IOV"]
    I3 --> I4["I/O MMU: DMA + interrupt remap"]

    A --> H{"Hypervisor placement"}
    H --> H1["Type 1: hardware"]
    H --> H2["Type 2: host OS"]
    H2 --> H3["Host drivers / world switch"]

    A --> CL["Cloud / operations"]
    CL --> CL1["IaaS / PaaS / SaaS"]
    CL --> CL2["Live migration"]
    CL --> CL3["Checkpoint"]
```

## Diagnostic boundary

```text
guest app
  ≠ guest kernel
  ≠ virtual CPU/MMU/device
  ≠ hypervisor/VMM
  ≠ host OS or device domain
  ≠ physical CPU/MMU/IOMMU/device
```
