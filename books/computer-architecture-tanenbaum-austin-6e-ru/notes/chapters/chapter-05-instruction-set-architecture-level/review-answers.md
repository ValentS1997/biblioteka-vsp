# RAG-grounded ответы — глава 5

**Provenance:** questions `p0470:c01`–`p0474:c01`. Main answers use chapter RAG `p0377:c01`–`p0474:c01`; exercise 33 additionally uses cross-referenced canonical RAG `p0212:c01`–`p0214:c01`. Not an official publisher key.

## 1

Assuming the chapter's common 32-bit word interpretation, value 3 is:

```text
00 00 00 03
```

If the bytes are copied to the same byte indexes of a machine using the opposite byte order, the new numeric interpretation is:

```text
03 00 00 00 = 0x03000000 = 50,331,648
```

If a different word width were intended, the result would depend on that width.

## 2

The OS loader must operate through a privileged mechanism that can initialize instruction memory even though ordinary program stores address only the data space.

One valid architecture is a privileged loader/device path or special control operation that writes program memory before execution begins. The key distinction is that “application cannot self-modify through normal data stores” does not imply “hardware/OS cannot initialize instruction storage”.

Exact machine-specific loader mechanism: **[Needs confirmation]**.

## 3

Use opcode expansion.

Two 12-bit addresses + 4-bit register = 28 operand bits, leaving **4 opcode bits**. Use `0000..1110` for the 15 two-address commands and reserve `1111` as escape.

For one-address commands, one 12-bit address + one 4-bit register consumes 16 bits. After the 4-bit escape, another 12 bits can extend the opcode, giving 4096 possible extended codes. Assign 650 of them and reserve one unused pattern as a second escape.

The remaining 16 bits can then extend that escape for zero-operand commands, providing far more than the required 80 codes.

Therefore the requested encoding is possible.

## 4

A two-address instruction consumes 12 address bits, leaving 4 opcode bits → 16 top-level opcode patterns.

If `n` are used for two-address commands, `16-n` patterns remain as escapes.

A one-address instruction needs one 6-bit address, so each escape supplies `2^6=64` one-address opcodes.

```text
maximum = 64(16-n)
```

## 5

No.

Three registers require 9 bits, leaving 3 opcode bits → 8 top-level codes.

- 4 are consumed by the four three-register commands.
- 4 remain as escapes.
- A one-register instruction uses 3 register bits, so each escape supplies `2^6=64` one-register codes.
- Total = `4×64=256` one-register codes.

Using 255 leaves only one extended pattern. Extending that pattern through the final 3 bits yields only `2^3=8` zero-register commands, but 16 are required.

## 6

Given `M[20]=40`, `M[30]=50`, `M[40]=60`, `M[50]=70`:

| Instruction | Accumulator |
|---|---:|
| LOAD IMMEDIATE 20 | 20 |
| LOAD DIRECT 20 | 40 |
| LOAD INDIRECT 20 | 60 |
| LOAD IMMEDIATE 30 | 30 |
| LOAD DIRECT 30 | 50 |
| LOAD INDIRECT 30 | 70 |

## 7

Expression: `X=(A+B*C)/(D-E*F)`.

### Zero-address

```text
PUSH A
PUSH B
PUSH C
MUL
ADD
PUSH D
PUSH E
PUSH F
MUL
SUB
DIV
POP X
```

7 memory-reference stack ops ×24 bits + 5 arithmetic ops ×8 bits = **208 bits**.

### One-address

```text
LOAD E
MUL F
STORE T
LOAD D
SUB T
STORE T
LOAD B
MUL C
ADD A
DIV T
STORE X
```

11×24 = **264 bits**.

### Two-address

```text
MOV R1,B
MUL R1,C
ADD R1,A
MOV R2,E
MUL R2,F
MOV R3,D
SUB R3,R2
DIV R1,R3
MOV X,R1
```

7 memory/register instructions ×28 + 2 register/register ×16 = **228 bits**.

### Three-address

```text
MUL R1,B,C
ADD R1,A,R1
MUL R2,E,F
SUB R2,D,R2
DIV X,R1,R2
```

44 + 32 + 44 + 32 + 32 = **184 bits**.

## 8

Use the 6-bit field as an index into a 64-entry address table:

```text
6-bit selector → address-table[0..63] → full effective address
```

The table may contain arbitrary, noncontiguous addresses.

## 9

The chapter already lists readability, multiprocessor sharing, split instruction cache and separate code/data-space problems.

A further disadvantage is not explicitly supported by the chapter RAG. Therefore a source-only answer is **[Needs confirmation]**.

## 10

1. `A B + C + D + E -`
2. `A B + C D + * E +`
3. `A B * C D * + E +`
4. `A B - C D E * - F / G / * H *`

## 11

1. `A B + C +` and `A B C + +` → **equivalent** under ordinary mathematical addition.
2. `A B - C -` and `A B C - -` → **not equivalent**.
3. `A B * C +` and `A B C + *` → **not equivalent**.

## 12

1. `(A+B+C)*D`
2. `A/B + C/D`
3. `A / (B*C*(D+E))`
4. `A + B * ((C + (D*E)/F - G) / H)`

## 13

Every well-formed postfix expression composed of operators with known arity can be converted to a fully parenthesized infix expression.

Only malformed postfix strings fail conversion, for example:

```text
A +
A B C +
A B + +
```

## 14

1. `A B AND C OR`
2. `A B OR A C OR AND`
3. `A B AND C D AND OR`

## 15

Postfix:

```text
5 2 * 7 + 4 2 / 1 + -
```

Chapter 5 explicitly introduces IJVM `IMUL` and `IDIV` for RPN examples.

```text
BIPUSH 5
BIPUSH 2
IMUL
BIPUSH 7
IADD
BIPUSH 4
BIPUSH 2
IDIV
BIPUSH 1
IADD
ISUB
```

Result = **14**.

## 16

The operand format described around figure 5.17 uses a 5-bit register field.

```text
2^5 = 32
```

So it can name **32 registers**.

## 17

The exercise cross-reference is inconsistent; see `source-findings.md`.

Using the text associated with figure 5.16:

- bit 23 distinguishes variant 1 from variant 2 for general operations;
- variant 3 is recognized from **reserved opcode values themselves**.

The opcode therefore determines that the remaining 24 bits form the branch/call displacement format.

## 18

If the only required result is membership in `A≤X≤B`, two Boolean condition results are sufficient:

```text
C1 = (X >= A)
C2 = (X <= B)
inside = C1 AND C2
```

So **two condition bits** can represent the two comparisons.

## 19

Advantage: compact relocatable control flow. Moving a code block preserves relative displacements.

Disadvantage: limited range. Targets farther than the signed displacement can represent need another mechanism.

## 20

Carry out of bit 3 supports decimal/BCD adjustment.

The Core i7 list includes decimal/ASCII correction instructions such as `DAA`, `DAS`, `AAA` and `AAS`; the auxiliary carry indicates a carry between low/high decimal nibbles.

## 21

This is the already-described prefix/escape-opcode idea.

Core i7 prefixes and IJVM `WIDE` use one opcode to modify or extend interpretation of the following opcode. The idea is therefore not new within the chapter.

## 22

One efficient design is a combined compare-and-branch:

```text
CMPBR condition, operand1, operand2/immediate, displacement
```

Fields: opcode, condition code, source 1, source 2 or immediate, PC-relative signed target.

Examples:

```text
CMPBR EQ, k, 0, L
CMPBR GT, a, b, L
CMPBR LT, k, 5, L
```

## 23

Initial: `1001 0101 1100 0011`.

1. logical right 4 → `0000 1001 0101 1100`
2. arithmetic right 4 → `1111 1001 0101 1100`
3. left 4 → `0101 1100 0011 0000`
4. rotate left 4 → `0101 1100 0011 1001`
5. rotate right 4 → `0011 1001 0101 1100`

## 24

If XOR permits the destination word as both operands:

```text
XOR M,M
```

Every bit XOR itself is zero.

## 25

```text
A = 1101 0000 1010 1101
B = 1111 1111 0000 1111
A AND B
  = 1101 0000 0000 1101

C = 0000 0000 0010 0000

result
  = 1101 0000 0010 1101
```

Answer: **`1101 0000 0010 1101`** (`0xD02D`).

## 26

```text
A = A XOR B
B = A XOR B
A = A XOR B
```

The original values are exchanged without a temporary register.

## 27

Useful when the constant is a small sum/difference of powers of two.

Example:

```text
K = 2^a + 2^b
K*x = (x << a) + (x << b)
```

The sequence helps only when those few shifts/adds are cheaper than multiplication.

## 28

### IJVM

Assuming normal 1-byte local indexes:

- `i=3` → `BIPUSH 3` + `ISTORE i` = **4 bytes**.
- `i=j` → `ILOAD j` + `ISTORE i` = **4 bytes**.
- `i=j-1` → `ILOAD j` + `BIPUSH 1` + `ISUB` + `ISTORE i` = **7 bytes**.

### Core i7

The chapter gives variable-length format structure but not enough byte-level opcode/modR/M encodings to derive unique exact lengths without an external x86 encoding table.

Source-supported structure:

```text
i=3     → move immediate constant to local destination
i=j     → load j to register; store register to i
i=j-1   → load j; decrement/subtract 1; store to i
```

Exact Core i7 byte counts: **[Needs confirmation]**.

## 29

One possible dedicated top-tested instruction:

```text
WHILEcc src1, src2/immediate, exit_disp
```

At the loop header it compares operands; if condition is false it branches to the exit, otherwise execution enters the body. The body ends with a backward branch to the WHILE instruction.

This permits zero iterations.

## 30

```text
moves = 2^64 - 1
      = 18,446,744,073,709,551,615
```

At one move/minute and 365 days/year:

```text
≈ 3.51×10^13 years
```

About **35 trillion years**.

## 31

The identifier tells the CPU which interrupt class/source to dispatch after acknowledging a shared interrupt mechanism.

```text
device → request
CPU → acknowledge
device → small identifier
CPU → index interrupt table
```

A memory table can contain handler addresses, but the CPU still needs an efficient index; otherwise it must poll candidate sources or use another hardware identification scheme.

## 32

Track payload:

```text
64 × 512 = 32,768 bytes
```

16-bit bus = 2 bytes/cycle:

```text
32,768/2 = 16,384 DMA cycles
16,384 × 500 ns = 8.192 ms
```

One track arrives every 16 ms:

```text
8.192/16 = 51.2%
```

DMA occupies **51.2% of bus time**. A fully bus-bound CPU is left about 48.8% of the bus capacity, so execution time is roughly **2.05×** the no-DMA case.

## 33

Figure 5.20 makes DMA perform an I/O-side and a memory-side transfer.

The cross-referenced architecture in `p0212:c01`–`p0214:c01` separates memory and I/O buses and allows an I/O controller to master memory for DMA.

A better design buffers between the buses and overlaps I/O-bus and memory-bus activity where the protocols allow it, avoiding two phases serialized on one shared bus and reducing CPU-memory contention.

## 34

Interrupts are asynchronous external events with different service deadlines, so higher-priority devices may need to preempt lower-priority handlers.

Ordinary procedures are synchronously invoked by the running program; normal call order already determines when they execute.

## 35

Yes.

Itanium 2 has **64 one-bit predicate registers**. Predication attaches conditions to instructions, allowing multiple conditional paths to coexist in a linear stream while only selected results are committed.

Many predicate registers allow many simultaneously live conditions without branches.

## 36

A speculative load can place a tentative result or invalid marker in a register and defer an exception until use.

A store modifies shared architectural memory. Wrong-path memory writes may be externally visible and cannot simply be undone after the fact.

Therefore speculative stores must be buffered/delayed until speculation is validated; they are not symmetric with speculative loads.

## 37

Handler capacity:

```text
1 / 250 µs = 4000 packets/s aggregate
```

For equal maximum traffic from two LANs:

```text
2000 packets/s per LAN
2000 × 1024 bytes = 2,048,000 bytes/s
                  = 16.384 Mbit/s
```

Maximum symmetric rate ≈ **16.384 Mbit/s per LAN**.

## 38

The exact figure reference is inconsistent; see `source-findings.md`.

Return must recover enough caller state to reconstruct execution:

- return address / old PC;
- previous frame pointer or link;
- previous stack position, or enough frame layout information to reconstruct SP;
- registers required by the calling convention to be preserved.

The epilogue removes locals/frame data, restores FP/SP and returns to the saved address.

## 39

Architecture-neutral assembly-style algorithm:

```text
if N < 0:
    emit '-'
    N = -N

if N == 0:
    emit '0'
    return

while N != 0:
    Q = N / 10
    R = N - Q*10
    push(R)
    N = Q

while stack not empty:
    R = pop()
    emit(R + '0')
```

A concrete assembler encoding requires choosing a calling convention and syntax not fixed by the exercise.

## 40

Use the chapter's Dijkstra-style operator stack:

```text
push(end_marker)

for each token:
    if operand:
        emit token
    else if '(':
        push token
    else if operator:
        while top has >= precedence:
            emit pop()
        push operator
    else if ')':
        while top != '(':
            emit pop()
        pop '('

at end:
    while top != end_marker:
        emit pop()
```

The output is postfix/RPN.

## 41

Assembly-style recursive factorial:

```text
factorial(n):
    if n == 0:
        return 1

    push n
    call factorial(n - 1)
    n = pop
    return n * result
```

The stack preserves return address and current n across recursive calls.

## 42

The chapter states that iterative Hanoi solutions exist but are much more complicated than the recursive form.

It does **not** provide the requested nonrecursive/non-explicit-stack algorithm.

Under the RAG-only contract, a complete external algorithm is therefore **[Needs confirmation]**.
