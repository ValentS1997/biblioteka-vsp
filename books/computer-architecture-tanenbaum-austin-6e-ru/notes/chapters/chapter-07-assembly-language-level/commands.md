# Ассемблерные примитивы — глава 7

**Provenance:** RAG `p0555:c01`–`p0589:c01`.

These are source-language/directive examples, not host shell commands.

## Machine-instruction examples

The chapter uses x86/MASM-like mnemonics such as:

- `MOV`
- `ADD`
- `SUB`
- `MUL/IMUL`
- `DIV`
- `PUSH`
- `POP`
- `JMP`
- `CALL`

Exact encodings are not reproduced unless required by the source exercise.

## Directive examples

| Directive | Role in chapter |
|---|---|
| `DD` | define/reserve doubleword data |
| `EQU` | assign symbolic value |
| `SEGMENT` | begin segment |
| `END` | terminate assembly input/pass processing |
| `MACRO` | begin macro definition |
| `ENDM` | end macro definition |
| `LOCAL` | make macro-expansion labels unique/local |
| conditional assembly constructs | choose source text during assembly |

## Macro example model

```text
CHANGE MACRO P1,P2
    ...
ENDM

CHANGE P,Q
```

The macro processor substitutes actual source strings for formal parameters.

## Assembler internal primitives

Conceptual operations from the source:

- increment instruction-location counter;
- enter/lookup symbol;
- lookup opcode/directive;
- save macro definition;
- expand macro invocation;
- emit object bytes;
- emit relocation information;
- emit external-reference information.

## Linker primitives

Conceptual operations:

- assign object-module base;
- relocate local references;
- resolve external names;
- build executable address space;
- create/load shared-library linkage.

## Runtime boundary

Assembler directives disappear before execution.

Macros disappear after expansion.

Machine instructions remain in the generated program.

Link metadata may remain in object/executable files for relocation or dynamic linking.
