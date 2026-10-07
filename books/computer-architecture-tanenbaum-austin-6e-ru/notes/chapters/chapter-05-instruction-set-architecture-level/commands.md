# ISA-команды и примитивы — глава 5

**Provenance:** RAG `p0377:c01`–`p0474:c01`.

## Shell / administrative commands

**[Not applicable].**

This artifact records ISA-level instructions from the source, not host operating-system commands.

## Generic instruction classes

| Class | Source examples |
|---|---|
| move/load/store | MOVE/MOV, LOAD/LDR, STORE/STR |
| stack | PUSH, POP |
| arithmetic | ADD, SUB, MUL, DIV, INC, DEC, NEG |
| logical | AND, OR, XOR/EOR, NOT |
| shifts/rotates | SHL/SHR, SAL/SAR, ROL/ROR |
| compare/test | CMP, TST |
| control transfer | JMP/BR/Bcc, CALL/BL, RET |
| interrupt | INT, IRET, SWI |
| I/O | IN, OUT |
| synchronization/prefix | LOCK, SYNC-like ordering primitive discussed in memory model |

## Core i7 examples

Source lists, among others:

`MOV`, `PUSH`, `POP`, `XCHG`, `LEA`, `ADD`, `SUB`, `MUL`, `DIV`, `ADC`, `SBB`, `INC`, `DEC`, `NEG`, `AND`, `OR`, `XOR`, `NOT`, shifts/rotates, `CMP`, `JMP`, conditional `Jxx`, `CALL`, `RET`, `IRET`, `INT`, `ENTER`, `LEAVE`, `IN`, `OUT`.

Prefixes discussed include `REP`, `REPZ`, `REPNZ` and `LOCK`.

## ARM / OMAP4430 patterns

The chapter describes a load/store architecture:

- arithmetic/logical work primarily on registers;
- `LDR*` loads;
- `STR*` stores;
- `Bcc` branches;
- `BLcc` procedure calls;
- `MOV` can target PC for register-indirect control transfer;
- `SWI` initiates a software interrupt/system function.

## AVR / ATmega168 patterns

Compact 16-/32-bit encodings operate on 8-bit registers, with register, immediate, direct and register-indirect addressing.

## IJVM extensions used in chapter 5

For RPN examples, the source explicitly introduces:

- `IMUL`;
- `IDIV`.

These complement chapter-4 IJVM operations such as `BIPUSH`, `IADD` and `ISUB`.

## Important distinction

An instruction mnemonic is not enough to define behavior. Correct interpretation also requires:

- operand width;
- signed/unsigned semantics;
- addressing mode;
- flags affected;
- privilege/context;
- instruction format.

## State-changing actions

All ISA instructions change architectural state by definition; this file is descriptive only and is **not** an operational runbook for a live host.
