# Cheatsheet — глава 5 «Уровень архитектуры набора команд»

**Provenance:** RAG `p0377:c01`–`p0474:c01`; exercise 33 cross-reference: `p0212:c01`–`p0214:c01`. Policy: **rag_only**.

## ISA boundary

ISA-visible:

- memory/address model;
- architectural registers;
- instruction encodings;
- data types;
- addressing modes;
- flags/conditions;
- control flow;
- exceptions/interrupt interface;
- privilege restrictions.

Usually not ISA-visible:

- exact pipeline;
- hidden physical registers;
- internal micro-ops;
- cache implementation details unless exposed semantically.

## Memory checks

| Property | Question |
|---|---|
| address unit | byte or word? |
| word size | 32/64/etc.? |
| alignment | required or only faster? |
| byte order | little/big endian? |
| code/data space | unified or separate? |
| ordering | strict or relaxed? |
| synchronization | explicit SYNC/fence needed? |

## Registers

- general purpose → fast compiler temporaries;
- PC → next/current instruction location;
- SP/FP → stack/frame;
- PSW/flags → N, Z, V, C and architecture-specific state;
- privileged registers → OS/hardware management.

## Instruction-format rule

```text
instruction bits
= opcode bits
+ operand/address/register/mode/immediate bits
```

More operand information leaves less opcode space.

Opcode expansion:

```text
short opcode → many operand bits
escape prefix → longer opcode → fewer operand bits
further escape → longest opcode → no operands
```

## Addressing modes

| Mode | Effective operand/address |
|---|---|
| immediate | constant inside instruction |
| direct | address inside instruction |
| register | architectural register |
| register indirect | memory[register] |
| indexed | memory[register + displacement] |
| relative indexed | memory[base + index + displacement] |
| PC-relative | PC + signed displacement |
| stack | implicit top-of-stack |

## Stack / RPN

Postfix evaluation:

1. operand → push;
2. binary operator → pop right, pop left;
3. compute;
4. push result.

IJVM chapter extension uses `IMUL` and `IDIV` for the RPN examples.

## Comparison / flags

Typical condition information:

- Z — zero/equal;
- N — negative;
- V — signed overflow;
- C — carry/borrow-related state;
- architecture-specific auxiliary/parity flags.

Signed and unsigned ordering are different interpretations of the same bit pattern.

## Procedure call

Minimum conceptual state:

```text
arguments
return address
saved frame/link state
local variables
saved registers as required by convention
```

Recursion is naturally supported when return/link state is stacked per invocation.

## I/O path

### Programmed I/O
CPU polls device state; simple but wastes CPU cycles.

### Interrupt-driven I/O
CPU continues useful work; device interrupts when service is needed.

### DMA
CPU configures address/count/device/direction; DMA transfers data and interrupts at completion.

DMA is a bus master and may steal cycles from CPU.

## Interrupt sequence

```text
device requests
→ CPU acknowledges
→ source/type identifier supplied
→ CPU saves PC + state
→ vector table selects ISR
→ ISR saves working registers
→ service device
→ restore state
→ return-from-interrupt
```

## ISA styles in chapter

| ISA | Character |
|---|---|
| Core i7/x86 | irregular CISC, variable length, strong backward compatibility |
| OMAP4430/ARM | regular load/store RISC, many registers, largely 3-address |
| ATmega168/AVR | compact embedded ISA, simple formats, 8-bit registers |
| IA-64 | EPIC: compiler-visible parallel scheduling, predicates, speculation |

## IA-64 mechanisms

- many architectural registers reduce memory traffic;
- instruction groups/bundles encode safe parallel issue;
- predication removes some branches;
- speculative load starts memory access early and defers fault use.

## Verification checklist

Given one instruction, be able to answer:

1. exact visible inputs/outputs;
2. operand locations;
3. effective-address formula;
4. instruction length/format class;
5. flags modified;
6. privilege requirements;
7. control-flow effect;
8. externally visible failure/exception behavior.

## Modifying action

**[Not applicable].**

No live-system administrative procedure is specified by the chapter.
