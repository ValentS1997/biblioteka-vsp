# RAG-grounded ответы — глава 7

**Provenance:** questions `p0587:c01`–`p0589:c01`. Main answers use chapter RAG `p0555:c01`–`p0589:c01`. Exercise 25 additionally uses canonical cross-reference RAG `p0294:c01` and `p0298:c01`–`p0300:c01` from chapter 4. Not an official publisher key.

## 1

Let execution time of the all-C program be `T`.

### Strategy 1 — all C

Programming effort:

```text
100 person-months
```

Execution:

```text
T
```

### Strategy 2 — all assembler

Assembler is 10× harder to write:

```text
100 × 10 = 1000 person-months
```

Assembler runs 4× faster:

```text
T / 4 = 0.25T
```

### Strategy 3 — C + optimize only the hot 2%

Initial C implementation:

```text
100 person-months
```

2% of C-development effort:

```text
0.02 × 100 = 2 person-months
```

Rewriting that fraction in assembler at 10× effort:

```text
2 × 10 = 20 person-months
```

Total programming effort:

```text
120 person-months
```

Runtime:

- hot 2% of source accounts for 50% of execution: `0.5T`;
- making it 4× faster reduces that part to `0.125T`;
- remaining code stays `0.5T`.

```text
0.125T + 0.5T = 0.625T
```

So the hybrid version is **1.6× faster than all-C** with only about **20% more development effort**, while full assembler costs 10× the development effort.

## 2

The general multi-pass idea applies, but not identically.

### Compiler emits object modules

The compiler must still discover/resolve source-level names and emit enough relocation/external-symbol information for the linker. It may therefore use multiple passes/phases analogous to assembler pass 1/pass 2.

### Compiler emits assembly text

Final machine addresses and assembler-level forward references can be left to the assembler. The compiler still needs its own semantic/type/control-flow processing, but it does not have to perform the final assembler symbol-to-address resolution itself.

Therefore the **principle** applies, but compiler phases are not simply the assembler's two passes copied verbatim.

## 3

Hardware does not care about assembler operand order; the problem is the human/tooling contract.

If one assembler reverses the established:

```text
destination, source
```

order, the same-looking mnemonic may mean the opposite data flow to programmers accustomed to another syntax.

Consequences:

- easy source-porting mistakes;
- misleading code reviews;
- incompatible macros/examples/documentation;
- accidental generation of semantically reversed operations.

A different syntax is possible, but it must be unambiguous and consistently documented.

## 4

A simple two-pass assembler of the chapter's model cannot resolve the chain immediately during pass 1:

```text
P → Q → R → S → 4
```

When `P EQU Q` is first seen, `Q` is unknown; similarly for Q and R.

Two source passes are still sufficient **if** pass 1 stores unresolved EQU expressions/dependencies and, after all definitions are known, resolves that dependency chain before pass 2.

Without deferred expression resolution, additional passes would be needed.

## 5

Alphabet size:

```text
26 letters - Q = 25 symbols
```

A fixed 5-bit code can represent 32 values, enough for 25 letters.

With a 40-bit word:

```text
40 / 5 = 8 characters
```

So maximum fixed-length symbol = **8 letters**.

One encoding:

- map the 25 permitted letters to values 0–24;
- encode each in 5 bits;
- use eight 5-bit fields per 40-bit word;
- reserve unused codes 25–31.

Also, `25^8 < 2^40` but `25^9 > 2^40`, so eight characters is also the maximum for a packed base-25 representation.

## 6

**Instruction:** represents a machine operation that becomes executable machine code.

**Directive/pseudocommand:** tells the assembler what to do while translating, for example:

- define data;
- define a symbolic constant;
- start a segment;
- define/expand a macro.

A directive is processed by the assembler and normally has no runtime CPU instruction of its own.

## 7

The concepts are analogous but exist at different times.

### Instruction Location Counter (ILC)

Assembler-time variable:

```text
address assigned to next emitted instruction/data item
```

It advances while translating source.

### Program Counter (PC)

Runtime CPU register:

```text
address of current/next instruction being executed
```

Thus both track an instruction location, but ILC belongs to the translator while PC belongs to the executing processor.

## 8

Starting address = 1000.

| Label | Instruction length | Address |
|---|---:|---:|
| EVEREST | 1 | 1000 |
| K2 | 1 | 1001 |
| WHITNEY | 2 | 1002 |
| MCKINLEY | 3 | 1004 |
| FUJI | 1 | 1007 |
| KIBO | 3 | 1008 |

Next free address after the last instruction:

```text
1011
```

The operand symbol `X` is referenced but not defined in the supplied fragment; whether the assembler enters an unresolved placeholder for it depends on symbol-table implementation.

## 9

Yes, if the assembler grammar can distinguish the namespaces/fields unambiguously.

For example, a colon can force interpretation as a label:

```text
MOV:
```

But an assembler that identifies fields only by token position/whitespace and uses one shared namespace may reject this because `MOV` is already an opcode.

So this is a language/parser design choice, not a machine-architecture restriction.

## 10

Sorted list has 12 elements.

For an even-size range the exercise says to choose the element immediately after the midpoint.

1. 12 elements → choose element 7: **Palo Alto**.
   Berkeley is earlier → search first 6.
2. 6 elements → choose element 4: **Eugene**.
   Berkeley is earlier → search first 3.
3. 3 elements → middle element: **Berkeley**.

Search path:

```text
Palo Alto → Eugene → Berkeley
```

## 11

Yes.

Binary search only requires a sorted range and a rule for choosing a midpoint.

Whether the number of elements is prime, even or odd has no effect on correctness.

## 12

Letter values: a=1, b=2, ..., z=26.

Modulo 19:

### els

```text
e+l+s = 5+12+19 = 36
36 mod 19 = 17
```

### jan

```text
10+1+14 = 25
25 mod 19 = 6
```

### jelle

```text
10+5+12+12+5 = 44
44 mod 19 = 6
```

### maaike

```text
13+1+1+9+11+5 = 40
40 mod 19 = 2
```

Results:

| Symbol | Hash |
|---|---:|
| els | 17 |
| jan | 6 |
| jelle | 6 |
| maaike | 2 |

Collision: **jan/jelle**.

Using the chapter's hash-table design, place both in the linked list for slot 6.

## 13

Let fraction of occupied slots be `R`.

For a probe whose slot is effectively independent:

```text
P(empty) = 1 - R
```

The number of probes until success is geometric, so:

```text
E[probes] = 1 / (1 - R)
```

As `R → 1`, insertion cost grows rapidly.

## 14

Use the processors as parallel compare cells.

One source-consistent organization:

- each processor stores one or a few `(key,value)` pairs in local memory;
- shared register 1 receives the search key;
- shared register 2 carries command/mask/control information;
- every processor compares the key against its local entry simultaneously;
- a matching processor participates in an arbitration/reduction step and places the result or match identity in shared register 3.

The key property of associative memory is achieved because **all entries compare in parallel**, rather than one table element being searched sequentially.

If multiple matches are legal, the design additionally needs a way to return a set of matches or serialize winners.

## 15

Yes.

If code/data may be emitted into independent segments, one scalar ILC is no longer sufficient because each segment has its own next location.

A practical assembler maintains:

```text
ILC[segment]
```

When `SEG N` is processed:

- save current segment's counter;
- switch to segment N;
- resume that segment's saved counter.

Thus addresses advance independently inside each segment.

## 16

Not necessarily.

A single giant DLL might reduce the number of library files, but the chapter already notes that virtual memory can map/load DLL pages on demand, so unused code need not all become resident just because it belongs to one DLL.

A monolithic DLL also reduces modularity:

- unrelated procedures share one update/version unit;
- more programs become dependent on the same large binary;
- library maintenance becomes coarser.

Therefore the source does not support a general claim that “one giant DLL is more efficient”.

## 17

Yes, if the code can tolerate different virtual locations.

Problem:

- two processes may map the same physical library pages at different virtual addresses;
- absolute addresses embedded in shared read-only code would need different relocation values per process, which conflicts with sharing one identical physical code page.

Solutions supported by the chapter's relocation discussion:

- position-independent/PC-relative code;
- indirection/linkage tables containing process-specific addresses;
- alternatively map the library at the same virtual address in each process.

Data that must be process-specific should not rely on one shared writable absolute layout.

## 18

A single sequential library scan can fail.

Example:

1. unresolved symbol A is in the initial required list;
2. linker scans past module B, which is not yet required;
3. later it extracts module A;
4. module A introduces an external reference to B;
5. but the scan has already passed B.

Fixes:

- rescan the library until a full pass adds no new modules/symbol requirements; or
- build/use a library index mapping exported symbols directly to object modules.

## 19

Yes to both.

The chapter explicitly describes macro processing as **string substitution without semantic interpretation**.

Therefore an actual parameter may be:

- a register name;
- a constant;
- a memory symbol;
- another syntactically suitable token string.

The only requirement is that after substitution the expanded assembly text is valid for the intended use.

## 20

The normal source model expands macros as calls are encountered after definitions have been recorded.

If calls may appear before definitions, a single streaming pass can no longer expand immediately.

Implementation options:

1. pre-scan the source and collect all macro definitions first;
2. store unresolved macro calls and expand them after definitions become known;
3. use an additional source pass dedicated to macro discovery/expansion.

Thus the boss's aesthetic rule increases assembler state/pass complexity.

## 21

Define a recursive macro that calls itself without reaching a terminating condition.

Example conceptually:

```text
LOOP MACRO
    LOOP
ENDM
```

Or use a recursive parameterized macro whose parameter never changes toward its base case.

The source explicitly warns that such expansion continues indefinitely until assembly is manually stopped/resource limits are hit.

## 22

Assuming first module starts at address 0, relocation constants are the cumulative sizes of preceding modules.

Sizes:

```text
200, 800, 600, 500, 700
```

Bases:

```text
module 1: 0
module 2: 200
module 3: 200+800 = 1000
module 4: 1600
module 5: 2100
```

Answer:

```text
0, 200, 1000, 1600, 2100
```

If the executable is later loaded at nonzero base B, add B to every value.

## 23

Hash-table module using chaining:

```text
table = array of bucket lists

hash(symbol):
    return hash_function(symbol) mod table_size

enter(symbol, value):
    b = hash(symbol)
    for each entry in table[b]:
        if entry.symbol == symbol:
            entry.value = value
            return
    append (symbol,value) to table[b]

lookup(symbol):
    b = hash(symbol)
    for each entry in table[b]:
        if entry.symbol == symbol:
            return FOUND, entry.value
    return NOT_FOUND
```

This matches the chapter's hash-table model with linked lists for collisions.

## 24

Insertion phase:

```text
append(symbol,value) to array
```

After the last symbol is entered:

```text
sort array by symbol name
```

Lookup:

```text
lo = 0
hi = n-1

while lo <= hi:
    mid = floor((lo+hi)/2)

    if array[mid].symbol == symbol:
        return FOUND, array[mid].value
    if symbol < array[mid].symbol:
        hi = mid-1
    else:
        lo = mid+1

return NOT_FOUND
```

Search cost is approximately `log2(n)` comparisons after sorting.

## 25

Chapter 4 describes Mic-1 control-store words as 36-bit microinstructions and introduces a symbolic MAL-like notation for one-cycle micro-operations.

A simple source-consistent two-pass microassembler can be organized as follows.

### Input forms

```text
label:   MAL-operation
NAME     EQU expression
         WORD constant
```

### Pass 1

- maintain control-store location counter;
- enter microinstruction labels into symbol table;
- evaluate immediately known `EQU` constants or save deferred expressions;
- determine one 36-bit control word per microinstruction;
- expand symbolic constants used in source.

### Pass 2

For each MAL microinstruction encode the Mic-1 control fields described in chapter 4:

- NEXT_ADDRESS;
- JAM/JMPC/JAMZ/JAMN;
- ALU/shifter control;
- C-bus destination bitmap;
- memory control;
- B-bus source.

Resolve symbolic `goto` targets from the symbol table.

For:

```text
WORD expression
```

evaluate the expression and emit the resulting machine/control-store word in the chosen output image.

The exact binary field map must be taken from Mic-1's chapter-4 microinstruction specification; it is not reconstructed beyond the cross-referenced RAG.

## 26

Add a macro-processing stage before normal pass-1 encoding.

Required tables:

```text
macro_name
formal_parameter_list
macro_body
local-label metadata
```

On `MACRO`:

1. record macro name/formals;
2. save body until `ENDM`.

On a macro call:

1. parse actual parameters;
2. substitute actual strings for formals;
3. generate unique names for LOCAL labels;
4. recursively expand nested macro calls;
5. feed expanded lines to the ordinary assembler pipeline.

Then:

```text
macro expansion
→ pass 1 symbols/ILC
→ pass 2 Mic-1 encoding
```

Recursive macros require a terminating condition exactly as described in the chapter.
