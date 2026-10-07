# Source findings — Chapter 11

## [Source/version boundary] Windows 8 vs Windows 8.1 vs Windows Vista terminology

- PDF page 931 titles the chapter `Windows 8`.
- PDF page 938 explicitly states that the chapter effectively describes Windows 8.1 while retaining the shorter name Windows 8.
- Several implementation/security passages and the chapter summary refer to Windows Vista because the architecture is inherited across the NT lineage.

Handling: preserve the edition's terminology and do not rewrite the chapter as a description of current Windows.

## [Source numbering issue] Security-mitigation table is labelled 10.18

- PDF pages 1049–1050, inside Chapter 11, show `Таблица 10.18`.
- The surrounding text belongs to section 11.10.4.

Handling: record this as a source numbering inconsistency; do not silently renumber the source.

## [Source parameter variation] Large-page sizes depend on architecture/context

- PDF page 1009 describes normal x86 pages as 4 KiB and mentions a 4 MiB large-page mode.
- The same discussion also describes 2 MiB pages for kernel/large-application performance.
- Review question 9 is phrased around 2 MiB pages.

Handling: explain the TLB rationale without collapsing architecture-specific page sizes into one universal value.

## [Needs confirmation] Review question 41 requires a live Windows registry

The exercise asks for repeated `regedit` exports during a real session and for observing changes after program/device installation.

Handling: chapter mechanics can be explained, but empirical registry diffs remain `[Needs confirmation]`.

## [Needs confirmation] Review question 42 requires implementation and execution on UNIX

The exercise asks for two programs that emulate NTFS multiple streams in a container/output file and then report/extract them.

Handling: provide a source-grounded data-format/design outline and acceptance criteria; do not fabricate implementation results.

## Historical security boundary

Mitigations, service names, driver architecture, browser examples and memory-manager details are source-era material. No external modernization is applied under `rag_only`.
