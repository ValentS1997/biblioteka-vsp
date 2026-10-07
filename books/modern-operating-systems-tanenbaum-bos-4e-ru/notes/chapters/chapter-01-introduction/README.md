# Глава 1 — Введение

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 1 — «Введение»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `22–110`
- Addressable RAG chunk range: `p0022:c01 … p0110:c01`
- Chunks in chapter range: `89`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 22 begins with `Глава 1. Введение`;
  - PDF page 111 begins with `Глава 2. Процессы и потоки`.
- Chapter boundary: `VERIFIED`

The chapter-end summary is present on PDF pages 106–107. Review questions are present on PDF pages 107–110.

## Main principle

The chapter gives two complementary views of an operating system:

1. **Extended machine** — hide inconvenient hardware details behind stable abstractions that are easier for applications to use.
2. **Resource manager** — allocate processors, memory, storage and I/O devices among competing programs and users in an ordered, protected way.

The rest of the chapter connects these two views to kernel/user mode, hardware, processes, address spaces, files, I/O, security, system calls and alternative OS structures.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 1.1 | What is an operating system? Extended machine and resource manager | 24–27 |
| 1.2 | History of operating systems | 27–42 |
| 1.3 | Computer hardware overview | 42–59 |
| 1.4 | Operating-system “zoo” | 59–63 |
| 1.5 | Core OS concepts | 63–75 |
| 1.6 | System calls | 75–88 |
| 1.7 | Operating-system structure | 88–99 |
| 1.8 | The world according to C | 99–103 |
| 1.9 | Operating-systems research | 103–104 |
| 1.10 | Short overview of the remaining book | 104–105 |
| 1.11 | Units of measurement | 105–106 |
| 1.12 | Short conclusions | 106–107 |
| — | Review questions | 107–110 |

Section/page mapping is derived from the RAG table of contents on PDF pages 6–7.

## Key concepts

- Kernel mode has privileged access to hardware; user mode exposes a restricted execution environment.
- OS abstractions include processes, address spaces and files.
- Resource sharing can be multiplexed **in time** or **in space**.
- Hardware relevant to OS design includes processors, caches and memory hierarchy, disks/SSDs, device controllers/drivers, buses and boot firmware.
- The chapter distinguishes multiple OS deployment classes: mainframe, server, multiprocessor, PC, handheld/mobile, embedded, sensor-node, real-time and smart-card systems.
- System calls are the application-visible boundary to core OS services.
- UNIX examples cover process management, files, directories/filesystems and miscellaneous services; Win32 is shown as a deliberately different API layer.
- Six structural approaches are introduced: monolithic, layered, microkernel, client-server, virtual machine and exokernel.
- OS implementation is discussed as a large C project using headers, conditional compilation, make/build dependencies, compilation and linking.
- Research directions include reliability, recovery, power management, storage, I/O, memory, multicore systems, security and virtualization.

## Practical interpretation

For infrastructure work, the most useful mental model from this chapter is:

`application → API/system call → kernel policy/mechanism → hardware/resource`

When troubleshooting, first identify which abstraction is failing, then locate the corresponding resource and privilege boundary. Do not treat a user-space interface as identical to the kernel mechanism beneath it.

## Artifacts

- [cheatsheet.md](cheatsheet.md) — operational/conceptual cheatsheet
- [commands.md](commands.md) — source-confirmed commands, system calls and tools
- [diagram.md](diagram.md) — Mermaid chapter logic
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary
- [summary.md](summary.md) — chapter-end conclusions
- [review-questions.md](review-questions.md) — source review questions
- [review-answers.md](review-answers.md) — RAG-grounded answers; not an official publisher key
- [source-findings.md](source-findings.md) — extraction findings affecting section 1.11

## Limitations

- RAG text extraction does not preserve all typographic superscripts reliably. See `source-findings.md`.
- Figures are referenced by extracted text but are not independently encoded as multimodal RAG objects.
- Current external facts requested by a review question are not supplied from the web because chapter work is `rag_only`.
- Unsupported answer details remain `[Needs confirmation]`.
