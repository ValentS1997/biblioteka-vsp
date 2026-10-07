# Cheatsheet — Appendix C

## 8088 address calculation

```text
physical_address = segment × 16 + offset
```

Examples:

- instruction fetch → `CS:IP`;
- default data → `DS:offset`;
- stack → `SS:SP` / `SS:BP`.

## Key registers

| Group | Registers | Source role |
|---|---|---|
| General | AX BX CX DX | arithmetic/data; BX can address memory; CX count; DX high half / I/O-related roles |
| Pointer/index | SP BP SI DI | stack/frame/string/index addressing |
| Segment | CS DS SS ES | 64-KiB segment bases |
| Control | IP/PC, FLAGS | next instruction and condition state |

## Operand order

Source as88 syntax:

```text
MOV destination,source
ADD destination,source
```

Parentheses mean memory:

```text
MOV AX,BX    ; value in BX
MOV AX,(BX)  ; word at DS:BX
MOV AX,(20)  ; word at DS:20
MOV AX,20    ; immediate constant 20
```

## Stack

```text
PUSH word:
    SP -= 2
    memory[SS:SP] = word

POP word:
    word = memory[SS:SP]
    SP += 2
```

## Subroutine frame

Caller:

```text
push args in reverse order
CALL routine
```

Callee:

```text
PUSH BP
MOV BP,SP
SUB SP,locals_size
...
MOV SP,BP
POP BP
RET
```

After the prologue:

- return address → `2(BP)`;
- arg1 → `4(BP)`;
- arg2 → `6(BP)`;
- locals → negative offsets.

## Syscall convention in tracer

```text
push arguments in reverse order
push syscall_number
SYS
```

Return:

- word → AX;
- long → DX:AX.

## as88 sections

- `.SECT .TEXT`
- `.SECT .DATA`
- `.SECT .BSS`

Common data directives/examples in source:

- `.BYTE`
- `.ASCII`
- `.ASCIZ`
- `.SPACE`, `.SPACE2`, `.SPACE4`
- `.ALIGN2`

## Toolchain

```text
source .s
→ as88
→ object/load/list metadata
→ t88 tracer
```

## Debug mental model

```text
single step
→ inspect registers/flags
→ inspect stack/call depth
→ inspect source position
→ inspect data memory
→ verify next control-flow edge
```
