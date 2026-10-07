# Глава 8 — Многопроцессорные системы

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 8 — «Многопроцессорные системы»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `576–658`
- Addressable RAG chunk range: `p0576:c01 … p0658:c01`
- Chunks in chapter range: `83`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 576 begins with `Глава 8. Многопроцессорные системы`;
  - PDF page 659 begins with `Глава 9. Безопасность`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 652 and continues onto page 653. Review questions/exercises occupy PDF pages 653–658 and are explicitly numbered 1–37.

## Main principle

The chapter compares systems with multiple execution nodes by asking two questions:

1. **Is memory physically shared?**
2. **How tightly are the nodes coupled?**

The resulting progression is:

`shared-memory multiprocessor → multicomputer/message passing → distributed system/middleware`.

As coupling becomes weaker, direct shared-memory coordination gives way to explicit communication, RPC/DSM abstractions and finally middleware that presents a coherent application model over heterogeneous machines.

## Chapter map

The table follows the chapter TOC numbering. The body text contains several numbering defects; these are preserved in `source-findings.md`.

| Section | Topic | PDF pages |
|---|---|---:|
| 8.1 | Мультипроцессоры | 579–607 |
| 8.1.1 | Мультипроцессорное аппаратное обеспечение | 579–591 |
| 8.1.2 | Типы мультипроцессорных операционных систем | 591–595 |
| 8.1.3 | Синхронизация мультипроцессоров | 595–600 |
| 8.1.4 | Планирование работы мультипроцессора | 600–607 |
| 8.2 | Мультикомпьютеры | 607–630 |
| 8.2.1 | Аппаратное обеспечение мультикомпьютеров | 608–612 |
| 8.2.2 | Низкоуровневые коммуникационные программы | 612–615 |
| 8.2.3 | Коммуникационные программы пользовательского уровня | 615–619 |
| 8.2.4 | Вызов удаленной процедуры | 619–621 |
| 8.2.5 | Распределенная совместно используемая память | 621–626 |
| 8.2.6 | Планирование мультикомпьютеров | 626–627 |
| 8.2.7 | Балансировка нагрузки | 627–630 |
| 8.4 | Распределенные системы | 630–651 |
| 8.4.1 | Сетевое оборудование | 633–636 |
| 8.4.2 | Сетевые службы и протоколы | 636–640 |
| 8.4.3 | Middleware на основе документа | 640–641 |
| 8.4.4 | Middleware на основе файловой системы | 641–646 |
| 8.4.5 | Middleware на основе объектов | 646–648 |
| 8.4.6 | Middleware на основе взаимодействия | 648–651 |
| 8.5 | Исследования в области многопроцессорных систем | 651–652 |
| 8.6 | Краткие выводы | 652–653 |
| — | Вопросы / упражнения | 653–658 |

## Key concepts

- **UMA:** every memory word has essentially uniform access time from every CPU.
- **NUMA:** memory-access cost depends on which CPU/node owns or is near the memory.
- **SMP:** one shared OS image can run on any CPU; shared kernel structures require synchronization.
- **Big kernel lock:** simple but highly serializing way to protect an SMP kernel.
- **Fine-grained kernel locking:** separate locks protect independent critical regions and shared tables.
- **TSL / atomic swap:** atomic read-modify-write basis for multiprocessor mutexes.
- **Spin lock:** CPU repeatedly tests a lock instead of sleeping.
- **Read-before-TSL:** poll with ordinary reads and execute TSL only when the lock appears free, reducing cache-line bouncing.
- **Binary exponential backoff:** increase delay between lock probes to reduce interconnect traffic.
- **Affinity scheduling:** prefer the CPU that recently ran a thread so cache/TLB state may still be useful.
- **Space sharing:** allocate processors to a related group of threads at the same time.
- **Gang scheduling:** related threads run simultaneously and share aligned time quanta.
- **Multicomputer:** each node has private memory; inter-node communication is message passing.
- **RDMA:** remote memory transfer can bypass some copies/kernel work, but notification and page pinning still matter.
- **RPC:** hides message passing behind procedure-call semantics using client/server stubs and marshalling.
- **DSM:** page faults fetch memory pages from another node, presenting the illusion of shared memory.
- **False sharing:** unrelated data sharing one coherence/page unit causes needless migration/invalidation.
- **Sender-initiated load balancing:** overloaded nodes search for underloaded nodes.
- **Receiver-initiated load balancing:** underloaded nodes search for work.
- **Distributed system:** loosely coupled complete computers connected by a network.
- **Middleware:** software layer above heterogeneous OS/network substrate that provides one application interaction model.
- **Session semantics:** local changes to an open distributed file become visible elsewhere on close.
- **CORBA:** object-oriented distributed middleware using ORBs and IDL-generated stubs/skeletons.
- **Linda:** distributed tuple space with `out`, `in`, `read`, and `eval`.
- **Publish/subscribe:** producers and consumers are decoupled by topic-based dissemination.

## Operational interpretation

Use the hardware/memory boundary first:

`shared RAM` → multiprocessor/SMP synchronization problem  
`private RAM + dedicated interconnect` → multicomputer/message-passing problem  
`independent computers + general network` → distributed-system/middleware problem

For incidents:

- lock contention on SMP: inspect cache-line movement, spin duration and lock granularity;
- poor scaling with more CPUs: inspect shared kernel structures, central schedulers and coherence traffic;
- NUMA slowdown: inspect CPU/memory affinity;
- multicomputer latency: count copies, kernel crossings and network-interface handoffs;
- RPC failure: inspect marshalling, pointer/global-state assumptions and remote syscall semantics;
- DSM thrashing: inspect page ownership, replication and false sharing;
- load imbalance: compare sender- vs receiver-initiated probing under current load;
- distributed-file anomalies: identify consistency/session semantics before treating data as corrupted;
- middleware performance: identify where the abstraction hides remote communication.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- Figures and tables are referenced through text RAG and are not independent multimodal objects.
- Figure-dependent review questions remain `[Needs confirmation]` when topology/state details are not recoverable from prose.
- Programming exercises retain `[Needs confirmation]` for compilation/runtime/measurement results.
- Product/network examples are preserved as chapter content rather than updated from the web.
- No external source or model-memory content is used to fill missing book evidence.
- Source numbering defects are preserved explicitly rather than silently corrected.
