# Глава 11 — Изучение конкретных примеров: Windows 8

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 11 — «Изучение конкретных примеров: Windows 8»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `931–1057`
- Addressable RAG chunk range: `p0931:c01 … p1057:c01`
- Chunks in chapter range: `127`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 931 begins with `Глава 11. Изучение конкретных примеров: Windows 8`;
  - PDF page 1058 begins with `Глава 12. Разработка операционных систем`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 1052 and continues onto page 1053. Review questions occupy PDF pages 1053–1057 and are explicitly numbered 1–42.

## Main principle

The chapter presents Windows as a layered object-oriented operating-system implementation:

`documented API → native NT services → executive objects/managers → kernel/HAL → drivers/hardware`.

The recurring engineering idea is separation of mechanism and representation through kernel objects, handles, namespaces and manager components. The same structure is then applied to scheduling, virtual memory, I/O, NTFS, power management and security.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 11.1 | История Windows вплоть до Windows 8.1 | 931–938 |
| 11.1.1 | 80-е годы прошлого века: MS-DOS | 932–933 |
| 11.1.2 | 90-е годы: Windows на базе MS-DOS | 933 |
| 11.1.3 | 2000 год: Windows на базе NT | 933–936 |
| 11.1.4 | Windows Vista | 936–937 |
| 11.1.5 | 2010-е годы: современная Windows | 937–938 |
| 11.2 | Программирование в Windows | 938–952 |
| 11.2.1 | Собственный API NT | 942–946 |
| 11.2.2 | Win32 API | 946–950 |
| 11.2.3 | Реестр Windows | 950–952 |
| 11.3 | Структура системы | 952–983 |
| 11.3.1 | Структура операционной системы | 952–968 |
| 11.3.2 | Загрузка Windows | 968–970 |
| 11.3.3 | Реализация диспетчера объектов | 970–980 |
| 11.3.4 | Подсистемы, DLL и службы пользовательского режима | 980–983 |
| 11.4 | Процессы и потоки в Windows | 983–1003 |
| 11.4.1 | Фундаментальные концепции | 983–990 |
| 11.4.2 | API управления заданиями, процессами, потоками и волокнами | 990–996 |
| 11.4.3 | Реализация процессов и потоков | 996–1003 |
| 11.5 | Управление памятью | 1003–1019 |
| 11.5.1 | Фундаментальные концепции | 1004–1008 |
| 11.5.2 | Системные вызовы управления памятью | 1008–1009 |
| 11.5.3 | Реализация управления памятью | 1009–1019 |
| 11.6 | Кэширование в Windows | 1019–1020 |
| 11.7 | Ввод-вывод в Windows | 1020–1029 |
| 11.7.1 | Фундаментальные концепции | 1020–1022 |
| 11.7.2 | API ввода-вывода | 1022–1024 |
| 11.7.3 | Реализация ввода-вывода | 1024–1029 |
| 11.8 | Файловая система Windows NT | 1029–1040 |
| 11.8.1 | Фундаментальные концепции | 1029–1030 |
| 11.8.2 | Реализация NTFS | 1030–1040 |
| 11.9 | Управление электропитанием в Windows | 1040–1042 |
| 11.10 | Безопасность в Windows 8 | 1042–1052 |
| 11.10.1 | Фундаментальные концепции | 1044–1046 |
| 11.10.2 | API безопасности | 1046 |
| 11.10.3 | Реализация безопасности | 1046–1049 |
| 11.10.4 | Облегчение условий безопасности | 1049–1052 |
| 11.11 | Краткие выводы | 1052–1053 |
| — | Вопросы / упражнения | 1053–1057 |

## Key concepts

- **NTOS:** kernel-mode core split into the executive and the lower-level kernel.
- **HAL:** hardware-abstraction layer for interrupts, DMA, timers, low-level synchronization and platform configuration.
- **Hyper-V:** optional hypervisor layer that isolates partitions and schedules virtual processors.
- **Native NT API:** low-level system-service interface used by Windows components and wrapped by higher APIs.
- **Win32 API:** documented compatibility-oriented user API implemented mainly by DLL wrappers around NT services.
- **Registry:** persistent configuration namespace organized in hives and mounted into the NT namespace.
- **Object Manager:** common lifecycle, naming, security and handle machinery for kernel/executive objects.
- **Handle:** user-mode-safe opaque reference resolved through a per-process handle table to a kernel object.
- **Job / process / thread / fiber:** resource group → address-space/resource container → scheduled execution unit → user-mode cooperative execution context.
- **Priority scheduling:** 32 priority levels; ready thread with highest current priority wins, with temporary dynamic boosts.
- **Autoboost:** temporary priority elevation for a thread holding a resource required by a higher-priority waiter.
- **Working set:** resident pages assigned to a process; memory pressure trims working sets and moves pages through PFN lists.
- **Soft vs hard page fault:** satisfied from RAM/zeroed state vs requiring storage I/O.
- **Cache Manager:** file-oriented virtual-address cache coordinated with the Memory Manager and filesystems.
- **IRP:** I/O Request Packet passed through a stack of device/filter/filesystem drivers.
- **NTFS MFT:** master file table containing records for files/directories and filesystem metadata.
- **NTFS attributes/streams:** a file is a set of attributes, including one or more named/unnamed data streams.
- **Reparse point:** indirection mechanism used for symbolic links, mount points and filesystem filters.
- **EFS / BitLocker:** file/directory encryption vs volume-level encryption.
- **Hibernation / HiberBoot / Connected Standby:** power-state mechanisms for persistence, fast startup and low-power connected operation.
- **SID / access token:** principal identity plus groups, privileges, restricted SIDs and defaults.
- **Security descriptor:** owner/security metadata plus DACL/SACL and integrity information.
- **Integrity level:** mandatory write restriction independent of discretionary DACL decisions.
- **Mitigations:** /GS, hardened exception handling, NX, ASLR, heap hardening, VTGuard, code integrity, PatchGuard, Windows Update and Defender.

## Operational interpretation

For troubleshooting, first identify the Windows boundary that owns the state:

`Win32/WinRT` → public API contract  
`NT native service` → kernel transition  
`Object Manager/handle` → object identity and lifetime  
`scheduler` → thread readiness/current priority/processor choice  
`Memory Manager` → VAD, working set, PFN state and backing store  
`I/O Manager/IRP stack` → driver/device/filesystem request path  
`NTFS/MFT` → persistent file attributes and extents  
`Security Monitor/token/ACL` → authorization and impersonation  
`Power Manager` → system/device/app power state

Do not confuse:

- a process with a scheduled entity: Windows schedules threads;
- a handle with a raw pointer: handles are validated object references;
- a process priority class with final thread priority: thread-relative priority and dynamic boosts also matter;
- a reserved virtual region with committed physical memory;
- a soft page fault with disk I/O;
- a file with one byte stream: NTFS can attach multiple streams/attributes;
- DACL authorization with integrity-level policy;
- hibernation with ordinary shutdown;
- historical Windows 8/Vista implementation descriptions with current Windows behavior.

## Historical scope

The chapter's title is Windows 8, but the text explicitly says the implementation described is effectively Windows 8.1 and repeatedly carries forward Windows Vista/NT terminology and mechanisms. Artifacts preserve the edition's model without silently modernizing it.

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

- Figures and tables are grounded through the extracted text layer, not independently encoded as multimodal objects.
- Empirical tasks requiring a live Windows/UNIX system remain partially `[Needs confirmation]`.
- Version-specific behavior is not updated from external sources.
- Where a review question depends on an unstated figure detail or implementation parameter, the gap is marked rather than filled from model memory.
