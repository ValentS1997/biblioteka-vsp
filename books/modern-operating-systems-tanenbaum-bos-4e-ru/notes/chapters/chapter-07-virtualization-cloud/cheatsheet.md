# Chapter 7 cheatsheet — Виртуализация и облако

## Symptom / problem framing

| Symptom | Check first |
|---|---|
| guest works but is very slow | VM exits, binary translation, shadow/EPT path, I/O emulation |
| guest cannot execute privileged operation | trap/emulation or hypercall path |
| excessive page-fault/VM-exit overhead | shadow-page synchronization vs nested/EPT tables |
| host memory exhausted while guests think RAM is available | overcommit, ballooning, deduplication |
| pass-through device accesses wrong memory | I/O MMU mapping/isolation |
| high type-2 I/O overhead | host driver path and world switches |
| migration never converges | dirty-page rate, storage/network state |
| one guest affects another | isolation boundary failure |

## Baseline / context

### Hypervisor goals

1. control/isolation;
2. equivalence with real hardware;
3. efficiency: most guest code executes without hypervisor intervention.

### Type 1 vs type 2

| Type | Placement | Main source trade-off |
|---|---|---|
| Type 1 | directly on hardware | strong direct control; hypervisor must handle platform/device support |
| Type 2 | on host OS | reuses host drivers/services; additional host/VMM transitions |

### Full vs para

- Full virtualization: unmodified guest believes it owns real hardware.
- Paravirtualization: guest knows about virtualization and issues hypercalls.
- Process virtualization: runs an application built for another OS/architecture without emulating a complete machine.

## Read-only checks

1. Identify type 1 or type 2.
2. Identify whether guest is unmodified or paravirtualized.
3. Determine whether CPU virtualization uses trap-and-emulate, hardware assist, binary translation, or a mix.
4. Check whether expensive guest operations cause VM exits.
5. For memory, map the full chain: guest virtual → guest physical → host/machine physical.
6. Determine shadow tables vs nested/EPT.
7. Check overcommit ratio and whether ballooning/deduplication are active.
8. For deduplication, verify identical pages are actually compared after hash match.
9. For device pass-through, verify I/O MMU mapping and interrupt remapping.
10. For SR-IOV, distinguish PF (administrator/configuration) from VF (guest-facing function).
11. For migration, identify shared storage assumptions, network identity and dirty-page rate.
12. For cloud use, separate isolation, provider trust, jurisdiction and vendor lock-in.

## Interpretation

### CPU virtualization

`ordinary guest user code → direct execution`

`sensitive/privileged guest-kernel operation → trap/hypercall/translated sequence → hypervisor`

Binary translation can outperform repeated traps because VM exits/context disruption are expensive.

### Memory virtualization

Without hardware nesting:

`guest virtual → hypervisor-maintained shadow mapping → machine physical`

With EPT/nested tables:

`guest virtual → guest physical → hardware nested/EPT translation → machine physical`

Nested walks can increase memory references, but substantially reduce VM exits and software shadow-table maintenance.

### Memory reclamation

- Overcommit: promise more aggregate guest RAM than installed physical RAM.
- Ballooning: guest driver pins pages; guest OS chooses what to evict.
- Deduplication: identical pages become one shared page.
- Copy-on-write: first writer gets a private copy.

### I/O

- Emulation: hypervisor translates guest device operations.
- Device domain: dedicated VM/OS performs I/O for guests.
- I/O MMU: remaps DMA and interrupts and isolates device access.
- SR-IOV: hardware exposes multiple virtual functions for one physical PCIe device.

### Cloud model

Five source characteristics:

1. on-demand self-service;
2. broad network access;
3. resource pooling;
4. rapid elasticity;
5. measured service.

Service layers:

- IaaS: machine/infrastructure;
- PaaS: managed application platform;
- SaaS: specific application/service.

### Migration

Pre-copy live migration:

`copy pages while running → track dirty pages → recopy → short pause → transfer final state → resume at destination`

High write rates can increase repeated copying.

### Checkpoints

A checkpoint can save CPU, memory and storage state; copy-on-write avoids immediate full-disk copies. External communication state cannot simply be rewound with the VM.

## Next action

For a virtualization performance problem:

`classify CPU/memory/I/O path → measure where exits/emulation occur → verify isolation mappings → change one mechanism → verify guest correctness and host isolation`.

## Modifying action

State-changing chapter operations include:

- enabling/disabling virtual interrupt state;
- loading/changing guest page-table roots;
- updating shadow/nested mappings;
- inflating/deflating balloon memory;
- assigning pass-through/SR-IOV device functions;
- migrating/suspending/resuming a VM;
- creating/restoring a checkpoint;
- performing VMware-style world switches.

Before changing state, preserve current VM/device/memory ownership.

## Verification / acceptance checks

- guest-visible behavior remains equivalent after change;
- guest cannot access another VM or hypervisor memory;
- VM-exit/page-fault rate decreases if performance was the goal;
- memory accounting remains consistent under overcommit;
- balloon reclaim does not push guest into pathological paging;
- DMA reaches only mapped guest memory;
- migrated VM preserves network/storage identity and resumes;
- checkpoint restoration does not silently assume remote peers rolled back too.

## Rollback

- CPU/memory virtualization policy: restore prior hypervisor configuration.
- Ballooning/overcommit: return prior memory allocation; exact platform procedure `[Needs confirmation]`.
- Device pass-through/SR-IOV: detach/reassign only with device-specific lifecycle; rollback `[Needs confirmation]`.
- Migration: return VM to source only if state ownership is still unambiguous; exact procedure `[Needs confirmation]`.
- Checkpoint restoration is itself a rollback and can conflict with external side effects.
