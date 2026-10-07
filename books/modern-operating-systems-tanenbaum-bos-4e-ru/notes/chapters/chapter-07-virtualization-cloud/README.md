# Глава 7 — Виртуализация и облако

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 7 — «Виртуализация и облако»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `527–575`
- Addressable RAG chunk range: `p0527:c01 … p0575:c01`
- Chunks in chapter range: `50`
- PDF page 568 contains two chunks: `p0568:c01`, `p0568:c02`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 527 begins with `Глава 7. Виртуализация и облако`;
  - PDF page 576 begins with `Глава 8. Многопроцессорные системы`.
- Chapter boundary: `VERIFIED`

The source does **not** contain a separate chapter-end `Краткие выводы` section. Section 7.13 is followed directly by review questions on PDF page 573. Therefore `summary.md` is not created under the conditional artifact rule.

Review questions occupy PDF pages 573–575 and are explicitly numbered 1–37.

## Main principle

Virtualization inserts a control layer between software and physical resources:

`guest software → virtual CPU/memory/I/O interface → hypervisor → real hardware`.

A useful hypervisor must preserve three properties emphasized by the chapter:

`control/isolation + behavioral equivalence + acceptable performance`.

The central engineering problem is deciding what may execute directly, what must trap, what must be translated, and what must be remapped so that one virtual machine cannot escape its resource boundary.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 7.1 | История | 529–530 |
| 7.2 | Требования, применяемые к виртуализации | 530–533 |
| 7.3 | Гипервизоры первого и второго типа | 533–535 |
| 7.4 | Технологии эффективной виртуализации | 535–540 |
| 7.4.1 | Виртуализация оборудования, не готового к виртуализации | 536–539 |
| 7.4.2 | Цена виртуализации | 539–540 |
| 7.5 | Являются ли гипервизоры настоящими микроядрами? | 540–543 |
| 7.6 | Виртуализация памяти | 543–547 |
| 7.6.1 | Аппаратная поддержка вложенных таблиц страниц | 545–546 |
| 7.6.2 | Возвращение памяти | 546–547 |
| 7.7 | Виртуализация ввода-вывода | 547–551 |
| 7.7.1 | Блоки управления памятью при вводе-выводе | 548–549 |
| 7.7.2 | Домены устройств | 549–550 |
| 7.7.3 | Виртуализация ввода-вывода в отдельно взятом физическом устройстве | 550–551 |
| 7.8 | Виртуальные устройства | 551 |
| 7.9 | Виртуальные машины на мультиядерных процессорах | 551–552 |
| 7.10 | Вопросы лицензирования | 552–553 |
| 7.11 | Облака | 553–556 |
| 7.11.1 | Облака в качестве услуги | 554 |
| 7.11.2 | Миграция виртуальных машин | 554–555 |
| 7.11.3 | Установка контрольных точек | 555–556 |
| 7.12 | Изучение конкретных примеров: VMware | 556–573 |
| 7.12.1 | Ранняя история VMware | 556–558 |
| 7.12.2 | VMware Workstation | 558–559 |
| 7.12.3 | Сложности внедрения виртуализации в x86 | 559–560 |
| 7.12.4 | VMware Workstation: обзор решения | 560–570 |
| 7.12.5 | Развитие VMware Workstation | 570–571 |
| 7.12.6 | ESX Server: гипервизор первого типа VMware | 571–573 |
| 7.13 | Исследования в области виртуализации и облаков | 573 |
| — | Вопросы / упражнения | 573–575 |

## Key concepts

- **VMM / hypervisor:** provides one or more virtual machines while retaining control of physical resources.
- **Popek–Goldberg requirements:** control/safety, equivalence and efficiency.
- **Sensitive instruction:** instruction whose behavior or effect touches privileged machine state and therefore matters to virtualization.
- **Privileged instruction:** traps when executed without sufficient privilege.
- **Full virtualization:** presents hardware-like behavior to an unmodified guest.
- **Paravirtualization:** guest is modified to use explicit hypercalls instead of executing sensitive operations directly.
- **Type 1 hypervisor:** runs directly on hardware.
- **Type 2 hypervisor:** runs with and depends on a host operating system.
- **Binary translation:** rewrites problematic guest-kernel basic blocks into safe sequences, while ordinary user code can often run directly.
- **VM exit:** transfer from guest execution back to the hypervisor; expensive because processor state/context must be saved and restored.
- **Shadow page table:** hypervisor-maintained mapping from guest virtual addresses to real machine pages.
- **Nested/EPT page tables:** hardware support for guest-physical → host-physical translation, reducing hypervisor-induced exits.
- **Memory overcommit:** advertised guest memory exceeds installed physical memory.
- **Ballooning:** a guest pseudo-driver allocates pinned pages so the guest OS itself chooses which pages to reclaim.
- **Deduplication:** identical pages are merged and later separated by copy-on-write when modified.
- **I/O MMU:** remaps device DMA addresses and interrupts, providing device isolation and pass-through safety.
- **Device domain:** a dedicated VM/OS handles I/O on behalf of other guests.
- **SR-IOV:** one PCIe device exposes physical and multiple virtual functions so VMs can access device resources with less hypervisor mediation.
- **Virtual appliance:** packaged VM containing the application plus required OS/libraries/configuration.
- **Cloud:** pooled, network-accessible, elastic, measured resources delivered on demand.
- **IaaS / PaaS / SaaS:** infrastructure, platform and software service models.
- **Live migration:** copy VM state while it continues running, then pause briefly to transfer the final dirty state.
- **Checkpoint:** saved VM state that can be restored, typically using copy-on-write to avoid copying an entire disk immediately.
- **World switch:** VMware Workstation transition between host-OS context and VMM/guest context, changing system-level state rather than only user-process state.

## Operational interpretation

For virtualization incidents, separate these boundaries:

`guest application` ≠ `guest kernel` ≠ `virtual hardware/VMM` ≠ `host OS or device domain` ≠ `physical CPU/MMU/IOMMU/device`.

Typical failure questions:

- correctness issue only inside one guest → start at guest/virtual-device boundary;
- high VM-exit rate → inspect privileged/sensitive instruction path, page-table handling and I/O emulation;
- memory pressure despite free-looking guest memory → inspect overcommit, ballooning, deduplication and host allocation;
- DMA/device isolation fault → inspect I/O MMU mapping and pass-through/SR-IOV ownership;
- live migration stalls → inspect dirty-page rate plus storage/network state transfer;
- type-2 I/O overhead → distinguish guest→VMM work from host-OS driver/world-switch work;
- cloud risk → separate virtualization isolation from provider trust, jurisdiction and vendor lock-in.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- There is no explicit chapter-end summary in the source, so no `summary.md` is synthesized.
- Figure-internal labels in several RAG chunks are mojibake; surrounding prose and captions remain usable.
- Figures/tables are not independently encoded as multimodal RAG objects.
- Question 37 explicitly requests Internet research; external sources are forbidden by this chapter's `rag_only` policy, so the answer remains `[Needs confirmation]`.
- Product/version statements are preserved as historical chapter content and are not updated with current web information.
- Unsupported details remain `[Needs confirmation]`.
