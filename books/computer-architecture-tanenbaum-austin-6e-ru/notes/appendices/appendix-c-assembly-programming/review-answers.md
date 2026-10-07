# RAG-grounded review answers — Appendix C

## 1

`702₁₀ = 02BE₁₆`.

After:

```text
MOV AX,702
```

the 16-bit AX register contains `0x02BE`:

```text
AH = 0x02 = 2
AL = 0xBE = 190
```

## 2

For `CS=4`:

```text
segment base = 4 × 16 = 64
```

A segment spans offsets `0...65535`:

```text
absolute range = 64 ... 64+65535
               = 64 ... 65599
```

## 3

8088 uses a 20-bit physical address:

```text
max = 2^20 - 1
    = 1,048,575
    = 0xFFFFF
```

## 4

Given decimal values:

```text
CS=40
DS=8000
IP=20
```

Next instruction:

```text
CS×16 + IP
= 40×16 + 20
= 660
```

For:

```text
MOV AX,(2)
```

parentheses denote direct memory addressing in the data segment.

```text
DS×16 + 2
= 8000×16 + 2
= 128002
```

AX receives the 16-bit word stored at physical byte addresses **128002 and 128003**. The actual word value is **[Needs confirmation]** because memory contents are not supplied.

## 5

After the usual prologue:

```text
PUSH BP
MOV BP,SP
```

the first argument is at `BP+4`.

Source syntax:

```text
MOV AX,4(BP)
```

## 6

`de-hw` is the distance between two labels in the same section. If the entire section is relocated by base `B`:

```text
(de+B) - (hw+B) = de-hw
```

so the difference is relocation-independent.

For a sum:

```text
(de+B) + (hw+B)
= de + hw + 2B
```

the relocation base does not cancel. A simple relocatable absolute constant cannot represent that expression in the same way.

Therefore a same-section label **difference** naturally represents length/offset; the **sum** of two relocatable labels is not generally a valid location-independent operand.

## 7

The source extraction has no visible destination on the left-hand side; see `source-findings.md`.

A valid computation with result in AX is:

```asm
MOV AX,(a)
ADD AX,(b)
ADD AX,2
```

If the intended source expression was something like `x=a+b+2`, add:

```asm
MOV (x),AX
```

The destination symbol itself is **[Needs confirmation]**.

## 8

Arguments are pushed in reverse order.

A source-consistent caller-side sequence is:

```asm
PUSH (y)
PUSH (x)
CALL footbar
ADD SP,4
```

The final `ADD SP,4` assumes caller cleanup.

The appendix also describes `RET #` as a mechanism by which a callee can remove argument bytes, so cleanup ownership is a calling-convention decision.

## 9

A source-consistent design:

1. Read an input line.
2. Parse signed integer A.
3. Parse one operator character.
4. Parse signed integer B.
5. Dispatch on the operator.
6. Print the result.
7. Repeat.

Core arithmetic dispatch:

```asm
! A in AX, B stored at (rhs), operator in AL/op variable

CMPB (op),'+'
JE addcase
CMPB (op),'-'
JE subcase
CMPB (op),'*'
JE mulcase
CMPB (op),'/'
JE divcase
JMP error

addcase:
    MOV AX,(lhs)
    ADD AX,(rhs)
    JMP print

subcase:
    MOV AX,(lhs)
    SUB AX,(rhs)
    JMP print

mulcase:
    MOV AX,(lhs)
    IMUL (rhs)
    JMP print

divcase:
    MOV AX,(lhs)
    CWD
    IDIV (rhs)
    JMP print
```

For output, the appendix's educational runtime supports `_PRINTF` with decimal `%d` formatting.

Input parsing can be implemented with `_GETCHAR` plus a decimal accumulator:

```text
value = 10*value + (digit-'0')
```

and optional leading `-`.

The appendix does not specify a complete ready-made expression-parser routine, so the answer gives the source-supported control/data path rather than inventing an external assembler library.
