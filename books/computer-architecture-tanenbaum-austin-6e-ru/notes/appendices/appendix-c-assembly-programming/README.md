# Приложение В — Программирование на языке ассемблера

Author of appendix: **Эверт Ваттель**.

**Source policy:** `rag_only`.

## Boundary

- PDF: **729–790**
- RAG: `p0729:c01`–`p0790:c01`
- Review: **9 questions**
- `p0791:c01` begins the alphabetical index.

## Purpose

This appendix is a practical 8088/as88 tutorial intended to teach computer architecture through assembly programming rather than train professional assembly programmers.

## Core model

```text
8088 ISA
→ registers + segmented memory + addressing
→ instruction set + calling convention
→ system-call ABI
→ as88 assembler/linker
→ t88 tracer
→ practical examples
```

## Core ideas

1. Assembly language is a symbolic representation of ISA operations and operands.
2. 8088 exposes 16-bit registers but addresses a 20-bit physical address space through segment:offset calculation.
3. Physical address:

```text
segment_base = segment_register << 4
physical = segment_base + offset
```

4. CS:IP selects the next instruction; DS supplies the default data segment; SS:SP/BP supports stack frames; ES is an additional segment.
5. General registers AX/BX/CX/DX have conventional roles but are not fully interchangeable.
6. 8088 supports register, direct memory, register-indirect, displacement, indexed/base-indexed, immediate and implicit addressing.
7. The source assembler uses **destination, source** operand order.
8. The instruction groups include MOV/XCHG/LEA, stack operations, integer arithmetic, logic, shifts/rotates, comparisons, loops/string operations, branches, CALL/RET and SYS.
9. Near CALL pushes the return address; parameters are pushed in reverse order. A conventional frame begins with saved BP and `MOV BP,SP`.
10. First argument then appears at `4(BP)`, second at `6(BP)`; locals use negative BP offsets.
11. The tracer's syscall ABI pushes arguments in reverse order, then pushes a syscall/function number and executes `SYS`.
12. as88 uses text/data/BSS sections, symbolic labels and two-pass address resolution.
13. t88 allows single-step execution, breakpoints, source/data display and subroutine-level stepping.
14. Examples demonstrate Hello World, arithmetic/register behavior, subroutine calls, strings, dispatch tables and buffered/random file access.

## Safety boundary

The setup section targets historical Solaris/UNIX/Linux/Windows environments and Windows 2000/XP details. It is preserved as source material and is **not** current deployment guidance.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Conditional artifact

`summary.md`: **[Not applicable]** — no explicit appendix-end summary exists.
