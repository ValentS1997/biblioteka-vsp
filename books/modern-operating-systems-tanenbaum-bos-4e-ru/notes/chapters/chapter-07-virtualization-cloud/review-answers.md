# Review answers — RAG-grounded

These answers are derived from chapter 7 only. They are not an official publisher answer key. External research is not used. Missing figure-only detail remains `[Needs confirmation]`.

1. Virtualization lets a data center consolidate many independent workloads on fewer physical servers, improving utilization while reducing hardware, rack-space and energy costs. It also simplifies centralized management, workload relocation and maintenance.

2. A type-2 hypervisor can be added to an already deployed machine without replacing the host operating system. It reuses the existing OS services and device drivers, so a company can add virtual machines to established hardware with less disruption than replacing the whole software stack.

3. A developer can run several guest operating systems and versions concurrently on one workstation, test compatibility, isolate unstable experiments and recreate environments without maintaining many physical machines or repeatedly rebooting into different partitions.

4. A home user can run applications requiring different operating systems, preserve legacy software, experiment safely with another OS, or keep multiple isolated environments on one physical computer.

5. The chapter gives two main reasons. First, personal-computer architectures such as x86 did not originally satisfy the Popek–Goldberg virtualization requirements. Second, the market focus shifted for years toward inexpensive personal computers rather than mainframe-style consolidation. VMware's binary-translation work and later Intel/AMD hardware extensions made x86 virtualization practical and broadly attractive.

6. The chapter describes two relevant classes of sensitive behavior:
   - instructions that change privileged/control state or resource configuration, such as I/O or MMU-related state;
   - instructions that expose or behave differently according to privileged machine state, such as revealing whether execution is in user or kernel mode.
   
   The exact formal category names from the original Popek–Goldberg paper are not separately spelled out in the retrieved chapter text, so those names are **[Needs confirmation]**.

7. The chapter explicitly gives **INC** as an instruction that can be executed directly without special virtualization handling. It does not enumerate two additional concrete non-sensitive opcodes in the retrieved RAG text. Therefore only one source-explicit opcode can be named; two more specific opcodes are **[Needs confirmation]**.

8. Full virtualization presents hardware-like behavior to an unmodified guest. Paravirtualization modifies the guest to issue explicit hypercalls for privileged services. Full virtualization is generally harder because the hypervisor must preserve the illusion of real hardware for code that does not know it is virtualized; paravirtualization simplifies privileged interactions at the price of modifying the guest.

9. If source code is available, paravirtualization can make sense because the guest kernel can be modified to use the hypervisor API directly. If source code is unavailable, such as the chapter's Windows example, direct modification is impractical, so full virtualization/binary translation/hardware-assisted techniques are needed.

10. Yes. A VM's virtual disk need not correspond to a primary physical partition. The chapter describes virtual disks as files or disk areas managed by the hypervisor/host OS. Therefore the number of VMs is not constrained by the PC's four-primary-partition limit.

11. Process-level virtualization runs an application written for another operating system and/or architecture without presenting a complete virtual machine. The chapter gives WINE and process-level QEMU as examples.

12. Type-2 hypervisors are useful because they can be installed on an existing host OS and reuse its abstractions and drivers. This lowers installation and hardware-support burden, especially on diverse desktop hardware, even though the extra host layer may add overhead.

13. Yes. Their strongest practical advantage in the chapter is device support: the host operating system already has drivers for a wide range of hardware. Type-2 products can delegate device access to those drivers instead of carrying a complete driver ecosystem themselves.

14. Binary translation was invented because pre-2005 x86 contained sensitive instructions that did not reliably trap when executed without privilege, so classic trap-and-emulate could not safely virtualize an unmodified guest kernel. Hardware-assisted virtualization reduced the need for binary translation, and the chapter states that modern VMware products mainly use hardware trap-and-emulate when CPU virtualization plus nested page tables are available. The chapter also notes that software translation can sometimes outperform expensive trap paths, so it is not presented as intrinsically useless.

15. A classic arrangement is:
   - ring 0: hypervisor;
   - ring 1: guest kernel;
   - ring 3: guest user applications;
   - ring 2: unused/available.
   
   The guest kernel therefore remains more privileged than its applications but less privileged than the hypervisor.

16. Hardware virtualization can cause many traps/VM exits. The chapter notes that these transitions are expensive because they disturb processor caches, TLB state and branch-prediction structures. Replacing a sensitive operation with a short translated procedure call can therefore be cheaper for some workloads.

17. The chapter's example is **CLI**. A real CLI operation may be relatively expensive, but the hypervisor only needs to change the guest's virtual interrupt-enable state. Binary translation can replace it with something equivalent to `VirtualCPU.IF = 0`, which can execute faster than the original hardware operation.

18. In principle more code could be translated ahead of execution, but the chapter's design translates one basic block at a time and caches it. The advantage is that only executed code is translated, startup work is limited, and cached blocks can later execute directly. Whole-program translation would move more work to startup and may translate code never executed. The source does not give a complete ahead-of-time design comparison beyond the described basic-block strategy, so further implementation details are **[Needs confirmation]**.

19. A pure hypervisor primarily preserves/emulates the machine interface so unmodified guests can run. A pure microkernel instead exposes a small explicit service interface; guest/system components call those services directly. In the chapter, once a system supports only paravirtualized guests using hypercalls and no longer needs to emulate sensitive instructions, the boundary between hypervisor and microkernel becomes very small.

20. Guest memory introduces two address-translation layers: guest virtual → guest physical and guest physical → real/machine physical. The hypervisor must preserve isolation while tracking guest page-table changes. Software shadow tables create expensive synchronization faults and VM exits; nested/EPT hardware reduces those exits but introduces deeper page-table walks.

21. Each VM carries its own OS and believes it owns a substantial private physical-memory space, so several VMs can consume large aggregate memory. The chapter's reduction mechanisms include:
   - overcommitment;
   - ballooning so the guest reclaims its own lower-value pages;
   - deduplication of identical pages;
   - copy-on-write for shared pages.

22. A shadow page table is maintained by the hypervisor and maps guest virtual addresses directly to the real physical pages assigned by the hypervisor. It lets hardware use a valid translation while preventing the guest's supposed “physical” addresses from colliding with another VM or the hypervisor.

23. The alternative described in the chapter is lazy synchronization: allow the guest to modify its own page tables without trapping each write. When it first accesses a new mapping, the resulting fault lets the hypervisor inspect the guest table and update the shadow table. Removed mappings are caught through operations such as `INVLPG`. This avoids a fault for every guest page-table write but still incurs faults on first use and requires special handling for mapping deletion.

24. Balloon drivers let the hypervisor reclaim memory while allowing the guest OS—not the hypervisor—to choose which pages are least valuable. The balloon inflates by allocating pinned/nonpageable guest pages, creating memory pressure so the guest evicts pages according to its own policy. The “deception” is that the guest experiences artificial memory pressure even though the underlying motive is host-level reallocation.

25. Ballooning depends on loading a compatible balloon pseudo-driver inside the guest. A guest that cannot or will not run that driver cannot participate in the mechanism. Also, if the guest cannot free enough useful memory without severe paging, ballooning cannot magically create cheap memory. Exact failure thresholds are **[Needs confirmation]**.

26. The hypervisor scans VM memory and hashes pages. When hashes match, it verifies that the pages are actually identical, then maps the different guests to one shared physical page. The page is protected with copy-on-write so a later writer receives a private copy and other guests do not observe the modification.

27. On a nonvirtualized system, the operating system owns the machine and can program DMA with the physical addresses appropriate to that machine; cross-VM isolation does not exist as a problem. With virtualization, a guest/device must not DMA into another VM or the hypervisor, and guest-visible addresses may not equal machine addresses. I/O MMU hardware remaps DMA addresses and isolates device access; it can also remap interrupts.

28. One advantage: the user can obtain scalable compute/storage without owning and operating the physical infrastructure. One disadvantage: the user must trust the provider with availability and data confidentiality and may face legal/jurisdictional issues or vendor lock-in.

29. Source-supported examples:
   - IAAS: **Amazon EC2**;
   - PAAS: the source defines a provider-managed environment containing components such as an OS, database and web server, but does not name a specific product in the retrieved chapter text — named example **[Needs confirmation]**;
   - SAAS: **Microsoft Office 365** or **Google Apps**.

30. Migration decouples service lifetime from one physical host. It is useful for hardware maintenance/replacement, load balancing and operational rearrangement without forcing the guest OS/application to be rebuilt or restarted. Live migration aims to make that relocation almost unnoticeable.

31. Problems include:
   - transferring memory while it is still being modified;
   - preserving storage attachment;
   - preserving network identity/connections;
   - minimizing pause time;
   - ensuring the destination hypervisor has a compatible environment.
   
   The chapter's pre-copy approach repeatedly sends dirty pages and pauses briefly only for the final state.

32. A VM carries the guest OS state together with the workload. The chapter notes that migrating a normal process requires reconstructing OS-maintained information such as open files, alarms and signal handlers. VM migration can move memory and disk images together with the guest OS tables that already contain this state.

33. Ordinary/suspended migration pauses the VM, copies its state, configures the destination and resumes it, producing a visible outage. Live migration copies most memory while the VM continues executing, tracks pages dirtied after copying, recopies them, then performs only a short final pause before resuming at the destination.

34. VMware's three primary requirements were:
   1. **compatibility** — unmodified x86 operating systems/applications should run;
   2. **performance** — virtualization overhead should remain low;
   3. **isolation** — a VM, including compromised guest software, must not interfere with the hypervisor or other VMs.

35. x86 PCs had a huge and changing variety of peripheral devices, each with vendor-specific drivers. A hypervisor could not realistically implement drivers for every possible device. VMware therefore needed a stable virtual-hardware front end and, in the type-2 architecture, could rely on the host OS to handle much of the real device diversity.

36. The chapter explicitly says ESXi's small size allowed it to be preinstalled in server firmware. Therefore the point was not primarily saving a few megabytes of server RAM; the compact image simplified embedded/preinstalled deployment of the hypervisor.

37. **[Needs confirmation]**. The source explicitly requires Internet research, while this chapter-analysis contract is `rag_only` and forbids external web fallback. No real-world examples are invented here.
