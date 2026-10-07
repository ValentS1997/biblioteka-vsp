# Cheatsheet — глава 7 «Уровень ассемблера»

**Provenance:** RAG `p0555:c01`–`p0589:c01`. Policy: **rag_only**.

## Translation chain

```text
source assembly
→ macro processing
→ pass 1
→ pass 2
→ object module
→ linker
→ executable
→ loader / dynamic linker
```

## Translation vs interpretation

| Translation | Interpretation |
|---|---|
| first produce target program | execute source semantics directly |
| target runs later | no equivalent final target required |
| assembler/compiler model | interpreter/microcode/OS service model |

## Assembly statement

```text
[label]   operation   operands   ; comment
```

- label → symbolic address;
- operation → opcode or directive;
- operands → registers/constants/memory/symbols;
- comment → human-only text.

## Directive vs instruction

**Instruction:** becomes a CPU machine instruction.

**Directive:** tells the assembler what to do.

Examples from source: reserve/define data, define symbols, segments, macro controls.

## Macro

```text
definition
→ name + formal parameters + body

call
→ actual parameters

expansion
→ textual body with substitutions
```

Macro ≠ procedure:

- macro expands at assembly time;
- procedure call happens at runtime.

Trade-off:

- macro: more generated code, no call overhead;
- procedure: less code duplication, runtime call/return overhead.

## Pass 1

Goals:

- track ILC;
- expand macros;
- record labels/symbols;
- process definitions such as `EQU`;
- determine instruction lengths/types;
- prepare intermediate representation if used.

ILC:

```text
ILC_next = ILC_current + emitted_length
```

## Pass 2

Goals:

- resolve known symbols;
- encode instructions;
- emit constants/data;
- emit relocation/external-reference metadata;
- produce listing if requested.

## Symbol table

| Structure | Lookup |
|---|---|
| unsorted array | O(n) sequential |
| sorted array | O(log n) binary search |
| hash table | near O(1) average with suitable load |

Collision handling in chapter: linked chains per hash slot.

## Forward vs external reference

- forward reference → symbol defined later in same assembly unit;
- external reference → symbol defined in another object module.

Forward refs are handled by assembly passes.

External refs are handled by the linker.

## Linker

Core tasks:

1. collect module sizes;
2. assign final module base addresses;
3. relocate internal memory references;
4. resolve external symbols.

## Object module

Chapter lists six parts:

1. identification;
2. entry-point table;
3. external-reference table;
4. machine code/constants;
5. relocation dictionary;
6. end marker.

## Relocation

If module local address `a` is linked at base `B`:

```text
final virtual address = B + a
```

Only fields marked relocatable should receive this adjustment.

## Binding time

Possible binding moments in source:

1. source authoring;
2. translation;
3. linking;
4. loading;
5. loading a relocation/base register;
6. instruction execution.

Later binding → more flexibility, usually more runtime machinery.

## Position-independent code

Prefer PC-relative/internal relative addressing where possible:

```text
target = PC + displacement
```

Moving the entire procedure preserves internal displacements.

## Dynamic linking

```text
call unresolved procedure
→ dynamic-link mechanism
→ locate/map library procedure
→ patch linkage/indirection state
→ retry/continue
→ later calls use resolved address
```

Benefits in chapter:

- shared code between processes;
- less disk/RAM duplication;
- easier library update;
- load procedures only when needed.

## Verification checklist

For an assembler/linker problem:

1. Is the symbol local, forward or external?
2. Is its value known in pass 1?
3. Does it affect ILC?
4. Is emitted address absolute or relocatable?
5. Which module defines the symbol?
6. At what stage is the final address bound?
7. Can PC-relative/position-independent form avoid relocation?
