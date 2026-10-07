# Source-confirmed instructions and control operations

Scope: chapter 7 RAG only, PDF pages 527–575.

| Item | Class | Source-grounded role | Risk / verification |
|---|---|---|---|
| `POPF` | state-changing | Example x86 instruction whose interrupt-related behavior exposed old virtualization problems | Guest-visible flags must not alter host/hypervisor interrupt state. |
| `CLI` | state-changing | Guest requests interrupts disabled; translated implementation may update virtual IF state | Verify only guest interrupt delivery is affected. |
| load/write `CR3` | state-changing | Selects page-table root; sensitive operation intercepted/virtualized | Verify mapping belongs to the guest. |
| `INVLPG` | state-changing | Invalidates a TLB mapping; intercepted to keep shadow mappings coherent | Verify stale shadow mapping is removed. |
| hypercall | state-changing | Paravirtualized guest explicitly requests privileged hypervisor service | Guest and hypervisor API must agree. |
| `VMCALL` | state-changing | Chapter's Dune example uses it for system-call transfer | Privileged transition semantics depend on environment. |
| VM exit | state-changing | Hardware returns control from guest to hypervisor and saves guest state/reason | Expensive; verify exit reason before emulation. |
| write `IDTR` / change interrupt-table context | state-changing | VMware world-switch example installs VMM interrupt-table state | Restore host context when switching back. |

## Source patterns

### Trap / emulate

```text
guest sensitive operation
    → trap / VM exit
    → hypervisor validates and emulates
    → resume guest
```

### Paravirtualization

```text
guest kernel
    → explicit hypercall
    → hypervisor service
```

### Shadow-table lazy synchronization

```text
guest changes its page table
    → shadow mapping may remain unchanged
    → first access faults
    → hypervisor inspects guest mapping
    → shadow mapping updated
```

Deletion is handled by intercepting operations such as `INVLPG`.

## Safety boundary

The source does not provide current product CLI commands for VMware, Xen, KVM, Hyper-V, cloud providers, SR-IOV or live migration. Production commands must not be invented in this RAG-only artifact.
