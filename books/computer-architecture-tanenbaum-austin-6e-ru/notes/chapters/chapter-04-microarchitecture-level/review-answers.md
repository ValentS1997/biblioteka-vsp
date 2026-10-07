# RAG-grounded ответы — глава 4

**Provenance:** questions `p0373:c01`–`p0376:c01`. Answers use only chapter RAG `p0270:c01`–`p0376:c01` plus explicit arithmetic/logical derivation. Not an official publisher key.

## 1

At the abstract execution level used in the chapter:

1. fetch instruction;
2. decode it;
3. fetch/prepare operands;
4. execute and store/update results/state.

Mic-1 expands these into multiple microcycles as needed.

## 2

Only **one** source may drive B bus in a cycle, so one-of-nine selection can be encoded in 4 bits and decoded.

C bus may write **several registers simultaneously**, so destinations are represented as independent bits. A one-hot encoded selector would prevent multi-register write-back.

## 3

Text on p282 gives the Boolean function directly:

```text
F = (JAMZ AND Z) OR (JAMN AND N) OR NEXT_ADDRESS[8]
```

This is the new high bit of MPC. A circuit is therefore two AND gates for `JAMZ·Z` and `JAMN·N` feeding an OR together with `NEXT_ADDRESS[8]`.

## 4

No useful effect. `0x1FF` already has all nine address bits equal to 1. OR-ing the eight MBR bits into its low eight bits cannot change the address, so JMPC cannot select a different microinstruction.

## 5

The added `k=5` makes the earlier `k=0` assignment dead. The conditional is still needed because the else path changes j.

One valid optimized tail is:

```text
ILOAD i
BIPUSH 3
IF_ICMPEQ L1
ILOAD j
BIPUSH 1
ISUB
ISTORE j
L1:
BIPUSH 5
ISTORE k
```

The initial `i=j+k` remains:

```text
ILOAD j
ILOAD k
IADD
ISTORE i
```

## 6

Two semantically equivalent IJVM sequences:

Variant A:

```text
ILOAD k
ILOAD n
IADD
BIPUSH 5
IADD
ISTORE i
```

Variant B:

```text
ILOAD k
BIPUSH 5
IADD
ILOAD n
IADD
ISTORE i
```

## 7

The stack computation is:

```text
(j - k)
→ (j - k - 6)
→ duplicate
→ add the two copies
```

So the Java-level meaning is:

```text
i = 2 * (j - k - 6);
```

## 8

Yes. Mic-1 conditional microbranch chooses between two control-store addresses differing only in bit 8.

`0x040` and `0x140` have identical low eight bits and differ by `0x100`, exactly matching JAMZ/JAMN addressing.

## 9

Mic-1 does not have two general full-width source buses. ALU input A is the H register; B comes from one selected B-bus source.

Therefore MDR and TOS cannot both be arbitrary direct operands in one cycle. The microprogram first copies MDR into H, later places the other operand on B bus and performs the comparison-producing subtraction.

For equality, subtraction direction does not matter for Z, but the physical operand routing still matters.

## 10

Source listing translates `i=j+k` to:

- ILOAD j;
- ILOAD k;
- IADD;
- ISTORE i.

Mic-1 path lengths including Main1 dispatch:

- ILOAD: 1 + 5 = 6 cycles each;
- IADD: 1 + 3 = 4 cycles;
- ISTORE: 1 + 6 = 7 cycles.

Total:

```text
6 + 6 + 4 + 7 = 23 cycles
```

At 2.5 GHz:

```text
Tcycle = 1/2.5GHz = 0.4 ns
23 × 0.4 = 9.2 ns
```

**Answer: 9.2 ns.**

## 11

Mic-2 removes Main1 and source table 4.8 gives:

- ILOAD: 3 cycles each;
- IADD: 3;
- ISTORE: 5.

Total:

```text
3 + 3 + 3 + 5 = 14 cycles
14 × 0.4 ns = 5.6 ns
```

Relative time:

```text
5.6 / 9.2 ≈ 0.6087
```

A program taking 100 ns on Mic-1 would take about **60.9 ns** on Mic-2 under the same instruction mix/rate assumption.

## 12

One valid Mic-1 design:

```text
poptwo1  SP = SP - 1
poptwo2  MAR = SP = SP - 1; rd
poptwo3
poptwo4  TOS = MDR; goto Main1
```

Final SP points to the old third word, and TOS is refreshed from memory. Exact control-store placement/opcode assignment is a design choice.

## 13

Use dedicated 1-byte opcodes for local indexes 0..3 and dispatch directly to specialized micro-routines rather than fetching an index byte.

Best-case design also decodes the low opcode information into a small constant/index path so the local address can be formed without consuming a byte from the instruction stream.

This trades a little control/decode hardware or duplicated microcode for shorter code and fewer fetch cycles.

## 14

Arithmetic right shift by two corresponds to division by 4 with sign propagation at the bit level.

Mic-1 already has `SRA1`, so a variable shift can conceptually be implemented as:

1. pop/retain shift count;
2. mask to low 5 bits;
3. retain the operand;
4. loop count times applying `SRA1`;
5. collapse the two source stack words to one result.

The chapter does not provide a ready mask-31 path or a complete MAL routine for this added opcode, so an exact cycle-by-cycle implementation is **[Needs confirmation]** rather than invented.

## 15

Left shift by two is multiplication by 4 modulo the 32-bit word width.

The exercise wording itself is damaged: it says the low five bits are used but only “the remaining 2 bits” are ignored; see `source-findings.md`.

Mic-1 lacks arbitrary left shift but can double a value through addition, so repeated doubling can implement left shift by one. A variable ISHL can therefore be designed as a count-controlled loop, but the exact MAL sequence for extracting/masking the five-bit count is **[Needs confirmation]**.

## 16

INVOKEVIRTUAL needs parameter count to locate OBJREF / the base of the new frame relative to the current SP.

The source procedure layout stores the parameter count in the called procedure metadata. Subtracting that count from SP allows the interpreter to determine where the caller-supplied argument area begins and where to establish LV/linkage state.

## 17

Source-grounded Mic-2 design:

1. form `LV + MBR1U` and read the indexed word;
2. push it to the stack;
3. read the next word at index+1;
4. increment SP again;
5. push the second word;
6. dispatch through the already-prefetched next opcode.

This is essentially two adjacent ILOAD-like word transfers sharing one byte index. Exact optimized micro-op scheduling depends on when MDR data becomes available and is **[Needs confirmation]** at individual-cycle level.

## 18

A finite implementation can use states up to 3–3 explicitly, then collapse extended scoring into:

- D = deuce/tie at 3–3 or higher;
- AA = advantage A;
- AB = advantage B;
- WA = A wins;
- WB = B wins.

Before deuce, states are score pairs `(a,b)` with `0≤a,b≤3` except terminal cases. From D: A→AA, B→AB. From AA: A→WA, B→D. From AB: B→WB, A→D.

## 19

Yes. All tied states at or above 3–3 are behaviorally equivalent:

```text
(3,3) ≡ (4,4) ≡ (5,5) ...
```

All A-one-ahead states above deuce are equivalent to advantage A; all B-one-ahead states are equivalent to advantage B. All already-won A states can be one terminal state, likewise for B.

## 20

Use six states:

```text
N0 N1 N2   = predict not-taken, 0/1/2 consecutive misses
T0 T1 T2   = predict taken,     0/1/2 consecutive misses
```

On a correct prediction: return to same-direction state 0.

On an incorrect prediction: 0→1→2; the **third** consecutive miss switches direction and resets miss count:

```text
N2 --miss--> T0
T2 --miss--> N0
```

## 21

**5 bytes:** yes, with a modified refill policy. A 4-byte refill can occur when occupancy is 0 or 1, producing at most 4 or 5 bytes.

**4 bytes:** not with the same simple design while still guaranteeing a 2-byte MBR2 operand without additional stalls/reordering. Refilling at occupancy 1 would overflow a four-byte buffer; waiting until 0 can leave MBR2 unavailable.

Thus 5 is feasible with control changes; 4 is insufficient for the same service guarantees.

## 22

Yes. A larger buffer can help if memory latency/burst behavior changes or if the consumer can drain bytes faster than refills arrive. More prefetched bytes can hide longer memory delays and tolerate bursts.

Under the chapter's simple one-word-ahead assumptions, 6 bytes are sufficient, so 12 bytes would mostly add cost/complexity without benefit.

## 23

Functionally, T performs the same operation as `goto1`: form `PC-1` and continue at `goto2`.

Direct branching to `goto1` is only possible if control-store address-placement constraints for the conditional pair are satisfied. Even then, **it does not save a cycle**, because T already occupies exactly the same one microcycle; it only avoids duplicated control-store content.

## 24

Mic-4 decode does more than translate opcode to one address:

- determines variable IJVM instruction length;
- separates opcode bytes from operand bytes;
- handles WIDE as a special expanded opcode;
- maps an opcode to the start of a **sequence** of micro-operations;
- allows micro-op ROM layout to be independent of sparse IJVM opcode values.

Using raw opcode directly as the micro-op ROM index would lose this length/format mapping and constrain micro-op placement.

## 25

A single cache cannot be both extremely fast/small and very large.

- L1 minimizes access latency;
- L2/L3 increase capacity/hit ratio at progressively higher latency.

Multiple levels bridge the CPU/main-memory gap while keeping the critical L1 path short.

## 26

Accesses are sequential:

- 60%: L1 only = 5 ns;
- 35%: L1 miss + L2 = 5+15=20 ns;
- 5%: L1 miss + L2 miss + memory = 5+15+60=80 ns.

```text
0.60×5 + 0.35×20 + 0.05×80
= 3 + 7 + 4
= 14 ns
```

**Average = 14 ns.**

## 27

Yes. Write allocation can still help if later operations are **reads** from the same line. Loading the line on the write miss makes later reads hit in cache.

Therefore the source's “repeated writes” motivation is not the only possible benefit; temporal reuse by reads can also justify allocation.

## 28

No. The number of ways does not have to be a power of two.

The set index is derived from address bits, but within a set the tags can be compared against three entries just as they can against four. A 3-way cache is technically valid; four ways may simplify regular hardware organization, but binary arithmetic does not forbid three ways.

The reviewer was therefore not correct as a strict architectural requirement.

## 29

More pipeline stages reduce the amount of combinational work per stage, allowing a shorter clock period and higher operating frequency.

Trade-off: deeper pipelines increase register/control overhead and make stalls, hazards and branch mispredictions more expensive.

## 30

Ideal CPI ≈1. Branch penalty:

```text
0.20 × 3 = 0.6 extra cycles/instruction
CPI = 1.6
```

Relative throughput:

```text
1 / 1.6 = 0.625
```

So performance becomes **62.5% of ideal**, a **37.5% reduction**.

## 31

All four branch predictions must be correct for the prefetched instruction beyond them to remain on the correct path:

```text
0.9^4 = 0.6561
```

**65.61%.**

## 32

The chapter text states that instruction 6 originally stalls because it wants to write R1 while R1 is busy.

Changing its destination to a new R8 removes that destination-name conflict, so instruction 6 can issue earlier rather than waiting for R1.

The exact new cycle-by-cycle schedule depends on the full table 4.11 structure, whose extracted table is not reliably addressable as text; exact rows after cycle 6 are therefore **[Needs confirmation]**.

## 33

Yes. WAW is a false name dependency and can be removed by **register renaming**.

Give the later writer a different physical register. Architectural mapping is updated at the appropriate commit point, so the two operations no longer compete for the same physical destination.

RAW cannot be removed this way because it represents a true data dependency.

## 34

A redesign must move the linkage metadata away from the address held in LV.

One source-consistent scheme:

1. reserve fixed words immediately below the new local-variable base for saved PC/LV/link information;
2. set LV to the first actual local variable;
3. make ILOAD/ISTORE index directly from that LV;
4. modify INVOKEVIRTUAL to store linkage at negative/fixed offsets from LV;
5. modify IRETURN to recover saved state from those offsets.

This changes frame layout and several INVOKEVIRTUAL/IRETURN microinstructions. The chapter does not define the alternative layout, so a complete replacement table is **[Needs confirmation]** rather than silently invented.

## 35

A source-grounded direct-mapped cache simulator:

```text
parameters:
    entries
    line_size

for each memory reference address:
    line_number = address / line_size
    index = line_number % entries
    tag = line_number / entries

    if cache[index].valid and cache[index].tag == tag:
        hits += 1
    else:
        misses += 1
        cache[index].valid = true
        cache[index].tag = tag

report hits, misses, hit_ratio
```

Useful experiments:

- sequential references with several line sizes;
- repeated loop over a working set smaller/larger than cache;
- two address streams mapping to the same index to expose conflict misses.

The source supplies no concrete reference trace or expected experiment dataset, so numeric experimental results are **[Needs confirmation]** until an input trace is defined.
