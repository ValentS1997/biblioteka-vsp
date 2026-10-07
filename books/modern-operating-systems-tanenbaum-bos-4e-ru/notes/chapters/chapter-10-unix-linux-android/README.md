# Глава 10 — Изучение конкретных примеров: Unix, Linux и Android

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 10 — «Изучение конкретных примеров: Unix, Linux и Android»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `784–930`
- Addressable RAG chunk range: `p0784:c01 … p0930:c01`
- Chunks in chapter range: `147`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 784 begins with `Глава 10. Изучение конкретных примеров: Unix, Linux и Android`;
  - PDF page 931 begins with `Глава 11. Изучение конкретных примеров: Windows 8`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 923 and continues onto page 924. Review questions/exercises occupy PDF pages 924–930 and are explicitly numbered 1–67.

## Main principle

The chapter uses Linux and Android as concrete realizations of the abstractions developed earlier in the book:

`interfaces → processes → memory → I/O → filesystem → protection → Android specialization`.

The central engineering lesson is that a small set of UNIX abstractions—processes, file descriptors, virtual memory, files, user identities and system calls—can support both a general-purpose Linux system and a substantially different application platform such as Android.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 10.1 | История UNIX и Linux | 785–793 |
| 10.1.1 | UNICS | 785 |
| 10.1.2 | PDP-11 UNIX | 786 |
| 10.1.3 | Переносимая система UNIX | 787–788 |
| 10.1.4 | Berkeley UNIX | 788–789 |
| 10.1.5 | Стандартная система UNIX | 789–790 |
| 10.1.6 | MINIX | 790–791 |
| 10.1.7 | Linux | 791–793 |
| 10.2 | Обзор системы Linux | 794–804 |
| 10.2.1 | Задачи Linux | 794–795 |
| 10.2.2 | Интерфейсы системы Linux | 795–797 |
| 10.2.3 | Оболочка | 797–800 |
| 10.2.4 | Утилиты Linux | 800–802 |
| 10.2.5 | Структура ядра | 802–804 |
| 10.3 | Процессы в системе Linux | 804–825 |
| 10.3.1 | Фундаментальные концепции | 805–807 |
| 10.3.2 | Системные вызовы управления процессами | 807–811 |
| 10.3.3 | Реализация процессов и потоков | 811–818 |
| 10.3.4 | Планирование | 818–823 |
| 10.3.5 | Загрузка Linux | 823–825 |
| 10.4 | Управление памятью в Linux | 826–840 |
| 10.4.1 | Фундаментальные концепции | 826–829 |
| 10.4.2 | Системные вызовы управления памятью | 829–830 |
| 10.4.3 | Реализация управления памятью | 830–837 |
| 10.4.4 | Подкачка | 837–840 |
| 10.5 | Ввод-вывод в Linux | 840–848 |
| 10.5.1 | Фундаментальные концепции | 840–841 |
| 10.5.2 | Работа с сетью | 841–843 |
| 10.5.3 | Системные вызовы ввода-вывода | 843–844 |
| 10.5.4 | Реализация ввода-вывода | 844–847 |
| 10.5.5 | Модули | 847–848 |
| 10.6 | Файловая система UNIX | 848–872 |
| 10.6.1 | Фундаментальные принципы | 848–853 |
| 10.6.2 | Вызовы файловой системы | 853–857 |
| 10.6.3 | Реализация файловой системы Linux | 857–866 |
| 10.6.4 | NFS | 866–872 |
| 10.7 | Безопасность в Linux | 872–876 |
| 10.7.1 | Фундаментальные концепции | 872–875 |
| 10.7.2 | Системные вызовы безопасности | 875 |
| 10.7.3 | Реализация безопасности | 875–876 |
| 10.8 | Android | 876–923 |
| 10.8.1 | Android и Google | 877–878 |
| 10.8.2 | История Android | 878–881 |
| 10.8.3 | Цели разработки | 881–883 |
| 10.8.4 | Архитектура Android | 883–885 |
| 10.8.5 | Расширения Linux | 885–888 |
| 10.8.6 | Dalvik | 888–890 |
| 10.8.7 | Binder IPC | 890–898 |
| 10.8.8 | Приложения Android | 898–909 |
| 10.8.9 | Намерения | 909–911 |
| 10.8.10 | Песочницы приложений | 911–912 |
| 10.8.11 | Безопасность | 912–918 |
| 10.8.12 | Модель процесса | 918–923 |
| 10.9 | Краткие выводы | 923–924 |
| — | Вопросы / упражнения | 924–930 |

## Key concepts

- **POSIX:** standardizes a portable programming interface around library procedures such as `open`, `read` and `fork`.
- **Shell:** user-space command interpreter supporting redirection, pipelines, background jobs and shell scripts.
- **System-call boundary:** switches execution from user mode to protected kernel mode.
- **task_struct:** Linux kernel representation of an execution context/task.
- **fork / exec:** create a process image by copying process context and then replacing its address space.
- **Copy on write:** parent and child initially share read-only physical pages; a writer receives a private copy.
- **clone:** Linux-specific process/thread creation with fine-grained sharing flags.
- **O(1) scheduler:** priority-indexed active/expired queues.
- **CFS:** red-black tree ordered by virtual runtime, weighted by task priority/nice.
- **Demand paging:** code/data pages are fetched as referenced rather than loaded eagerly.
- **Buddy + slab allocation:** page-level power-of-two allocation plus smaller object-oriented kernel allocations.
- **mmap:** maps a file into a process address space and can provide shared memory.
- **Special files:** expose devices through the filesystem; block and character devices use normal file operations.
- **Sockets:** file-descriptor-based network endpoints.
- **VFS:** common abstraction layer above local and remote filesystems.
- **i-node / dentry / file:** persistent file metadata, path-component cache, and per-open-file state.
- **NFS:** remote filesystem integrated into the local namespace through mounting.
- **UID/GID + rwx:** traditional Linux ownership and protection model; SETUID changes effective identity for a program.
- **Android app sandbox:** each installed application receives a distinct Linux UID.
- **Dalvik:** the chapter's Android runtime using compact register-oriented bytecode.
- **Binder:** capability-like, object-oriented IPC with identity-preserving remote object references.
- **Intent:** late-bound request used to find and activate an Android component.
- **ActivityManager:** coordinates application processes/components and assigns memory-importance classes.
- **zygote:** preinitialized Android process forked to create application processes efficiently.
- **oom_adj:** chapter-era Android process-importance ordering used by low-memory handling.

## Operational interpretation

When troubleshooting a Linux/Android behavior, identify the abstraction boundary before changing state:

`shell/library` → user-space interface  
`system call` → kernel entry  
`task/scheduler` → execution and CPU allocation  
`VMA/page` → virtual-memory mapping  
`fd/file/inode/VFS` → file and device access  
`UID/GID/mode` → protection  
`Binder/intent/component` → Android IPC/application lifecycle

Do not confuse:

- a process with an address space: Linux can vary what tasks share through `clone`;
- a file descriptor with an inode: open-file state includes a file position and may be shared differently;
- a pathname with an already-open file: later permission changes do not revoke an existing descriptor;
- a page fault with an error: demand paging intentionally uses page faults, but invalid mappings can be fatal;
- Android application state with process lifetime: a process can be killed while the activity's minimal saved state remains;
- Binder object identity with process identity: capabilities can be delegated.

## Historical scope

The chapter describes Linux and Android implementations current to the book's edition. Artifacts preserve that source model—including O(1), CFS, Dalvik, chapter-era Android `oom_adj`, historical login/password descriptions and NFS behavior—without silently modernizing them from external sources.

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

- Figures/tables are text-RAG grounded but are not independently encoded as multimodal objects.
- Empirical exercises requiring a live Linux system, BIOS environment, serial hardware, benchmarking or external runtime remain partially `[Needs confirmation]`.
- The chapter is not updated with current kernel, Android, filesystem or security behavior.
- Exact platform procedures not represented in chapter RAG are not filled from model memory.
