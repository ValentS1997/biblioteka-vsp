# RAG-grounded ответы — глава 3

**Provenance:** questions `p0264:c01`–`p0269:c01`. Answers use only chapter RAG `p0172:c01`–`p0269:c01` and explicit arithmetic/logical derivation from it. Not an official publisher key.

## 1
No. Digital encoding gives a **noise margin**, not immunity. The source defines voltage ranges representing 0 and 1 and a forbidden/intermediate region. Noise small enough not to cross the decision threshold is tolerated; sufficient noise can change the interpreted logical value.

## 2
With XOR used for “OR”, the two syntactically possible parses are:

- `H XOR (D AND F)`;
- `(H XOR D) AND F`.

Across the listed exact meal combinations, at least one permitted parse is true for **1, 4, 5 and 6**.

## 3
Ask either biker: **“Which road would a member of the other gang say leads to Disneyland?”** Then take the opposite road. Both a truth-teller reporting the liar and a liar misreporting the truth-teller indicate the wrong road.

## 4

| X | Y | X AND Y | X AND NOT Y | OR | X |
|---:|---:|---:|---:|---:|---:|
|0|0|0|0|0|0|
|0|1|0|0|0|0|
|1|0|0|1|1|1|
|1|1|1|0|1|1|

Therefore the expressions are equivalent.

## 5
An n-variable truth table has `2^n` rows, and each row output can independently be 0 or 1.

Number of functions:

```text
2^(2^n)
```

For n=3: `2^8 = 256`.

## 6
For n=4: `2^16 = 65,536`.

## 7
Let `N = NAND(X,Y)`. Invert it with a second NAND whose inputs are tied together:

```text
AND(X,Y) = NAND(N,N)
```

## 8
Use A,B,C as select bits. Set mux data inputs to the odd-parity truth table:

```text
D0..D7 = 0,1,1,0,1,0,0,1
```

Thus output is 1 for 001,010,100,111.

## 9
For each fixed A,B,C combination there are two truth-table rows, one for D=0 and one for D=1. The corresponding mux data input can therefore be one of four sources:

- 0;
- 1;
- D;
- NOT D.

This implements any four-variable Boolean function with an 8:1 mux.

The source's specific “number-word letter parity” function requires the exact lexical spelling for all 16 values; only several examples are present in retrieved RAG. Full D0…D7 wiring for that lexical task is therefore **[Needs confirmation]** rather than completed from model memory.

## 10
For one-hot inputs I0…I3 and outputs Y1Y0 encoding the active input number:

```text
Y1 = I2 OR I3
Y0 = I1 OR I3
```

## 11
With data input D and select bits A,B:

```text
O0 = D AND NOT A AND NOT B
O1 = D AND NOT A AND B
O2 = D AND A AND NOT B
O3 = D AND A AND B
```

## 12
**[Needs confirmation].** The question depends on a source figure whose internal wiring is not represented as addressable text RAG.

## 13
Signal pins:

- 4 A inputs;
- 4 B inputs;
- carry-in;
- 4 sum outputs;
- carry-out.

Total = **14 signal pins**. Adding power and ground gives **16 physical pins**, matching a common IC package size.

## 14
Define generate and propagate terms for bit i:

```text
Gi = Ai AND Bi
Pi = Ai XOR Bi
C(i+1) = Gi OR (Pi AND Ci)
```

Then expand recursively so each carry is a direct Boolean function of lower input bits and C0. Example:

```text
C1 = G0 OR P0 C0
C2 = G1 OR P1 G0 OR P1 P0 C0
C3 = G2 OR P2 G1 OR P2 P1 G0 OR P2 P1 P0 C0
```

This computes carries in parallel rather than waiting for ripple propagation, at the cost of additional gates.

## 15
**[Needs confirmation].** The exact critical gate path in figure 3.18 is graphical and not encoded in text RAG. A numeric delay would require reconstructing figure topology.

## 16
Yes, for one subtraction direction. The source ALU can invert A (`INVA`), select addition, and use `INC` as carry-in.

```text
B - A = B + NOT A + 1
```

So B−A is directly realizable. For A−B, operands must be swapped or equivalent B-inversion hardware added.

## 17
Under serial carry propagation:

- 16 stages ×10 ns computation;
- 15 inter-stage transfers ×1 ns.

Worst case:

```text
16×10 + 15×1 = 175 ns
```

## 18
Control order used here: `ENA, ENB, INVA, F0, F1, INC`. Source function select is 00=AND, 01=OR, 10=B, 11=A+B.

Force internal A to all ones by `ENA=0, INVA=1` and internal B to zero by `ENB=0`.

Two methods:

1. OR path: **0,0,1,0,1,0**
2. ADD path: **0,0,1,1,1,0**

Both produce all-one bits, i.e. −1 in the chapter's word-level context.

## 19
For a NAND-based SR latch, S and R are active-low, so the idle/hold state is:

```text
S=1, R=1
```

## 20
Invert the clock before the rising-edge pulse/flip-flop logic. A falling edge of the original clock becomes a rising edge of the inverted clock. Equivalently, mirror the short-pulse generator so it emits the sampling pulse on the falling transition.

## 21
The 4×3 source design's 22 AND gates decompose as:

- 4 address-decoder ANDs;
- 4 write-select ANDs;
- 4×3 =12 read-data ANDs;
- 2 control ANDs.

For 256×8 using the same topology:

```text
256 + 256 + (256×8) + 2 = 2562 AND gates
```

One OR per output bit gives **8 OR gates**.

## 22
The design is coherent as a four-bit register:

- 4 D inputs;
- 8 Q/NOT-Q outputs;
- 1 shared clock;
- power + ground.

That is 15 pins, so a 16-pin package can accommodate it with one spare pin. A shared clock intentionally loads all four bits together.

## 23
Multiplex the address in time: present one part of the address (for example row bits), latch it, then reuse the same pins for the remaining column bits. This is the row/column technique described for dense memory chips. Roughly n/2 address pins can represent n address bits, with additional control strobes.

## 24
A 32-bit data word requires 32 one-bit-wide DRAM chips in parallel.

```text
32 × 1M bits = 32 Mbit = 4 MiB
```

Minimum memory = **4 MiB**.

## 25
With a 20-ns clock cycle, the interval corresponding to the original two 10-ns segments becomes 40 ns. Subtract worst-case 3 ns MREQ assertion delay and 2 ns data setup:

```text
40 - 3 - 2 = 35 ns
```

So memory has **35 ns** after worst-case MREQ assertion.

## 26
Yes. At 100 MHz the source timing calculation leaves **19 ns from worst-case address availability** and **15 ns from worst-case MREQ/RD assertion** to required data setup. A 10-ns memory fits both limits.

## 27
It is electrically possible only if the interface does not treat MREQ as meaning “the current address is already valid.” A negative TML means request assertion overlaps address settling; the slave must defer address-sensitive action until the address becomes valid or use another sampling event. Without such a protocol, transient selection could occur. Therefore: **possible by contract/design, unsafe as an unstated assumption**.

## 28
Source block example transfers four words in 6 cycles versus 12 cycles separately. For long blocks, setup overhead becomes negligible:

- separate transfer ≈3 cycles/word;
- block transfer ≈1 cycle/word.

Asymptotic throughput gain ≈ **3×**.

Changing bus width from 8 to 32 bits multiplies absolute bytes/cycle by 4, but the **relative block-vs-separate protocol gain remains ≈3×** if transaction timing is otherwise unchanged.

## 29
Minimum causal ordering supported by the source full-handshake description:

```text
address/MREQ/RD valid  < MSYN asserted
MSYN asserted          < slave data valid
data valid             < SSYN asserted
SSYN asserted          < master captures data
SSYN asserted          < master drops address/MREQ/RD/MSYN
MSYN dropped           < slave drops SSYN
```

Using the question's timing labels, this implies at least:

```text
TA1, TMREQ1, TRD1 < TMSYN1 < TSSYN1
TD1 < TSSYN1
TSSYN1 < TA2, TMREQ2, TRD2, TMSYN2
TMSYN2 < TSSYN2
```

Exact hold inequalities tied to figure-only arrows are **[Needs confirmation]**.

## 30
Compared with several PCs over Ethernet, processors on one multicore chip have:

- much shorter physical communication paths;
- lower communication latency;
- shared-memory options rather than explicit network messaging;
- less duplicated chassis/I/O infrastructure;
- lower space/power overhead for tightly coupled computation.

The trade-off is stronger contention for shared on-chip resources and the need for parallel software.

## 31
The chapter connects multicore development to limits on raising clock frequency, heat/power constraints and communication delay. Moore's-law transistor growth still supplies more transistors; when simply increasing frequency becomes unattractive, those transistors can implement additional cores/caches/functional units. Thus Moore's law enables multicore density even when frequency scaling slows.

## 32
A memory bus is a tightly timed processor↔memory path optimized for memory transactions and specific memory technology. PCI is a standardized peripheral interconnect designed for multiple I/O devices, arbitration/configuration and broader compatibility. They differ in devices served, timing/protocol and expansion requirements.

## 33
There is no ambiguity if the protocol identifies active byte lanes. For a 32-bit bus, a 16-bit transfer can target the lower or upper halfword using address/byte-enable information. Without lane-selection information, it would indeed be ambiguous.

## 34
An interrupt acknowledge cycle gives the CPU a defined bus transaction for accepting an interrupt and allows the interrupting controller/device to provide identifying/vector/status information. This matters when multiple devices can request interrupts.

## 35
Raw bus capacity:

```text
200M cycles/s × 4 bytes = 800 MB/s
```

One 4-byte word every 4 cycles:

```text
50M words/s ×4 bytes = 200 MB/s
```

Useful data rate is **25% of theoretical bus bandwidth**.

## 36
Raw capacity:

```text
200M ×8 bytes = 1.6 GB/s
```

One 8-byte word every 4 cycles =400 MB/s, again **25% of theoretical bandwidth**.

## 37
Aligned 32-bit reads allow:

- 4 individual byte positions;
- 2 aligned halfwords;
- 1 aligned word.

Total = **7 valid combinations**.

Two implementations:

1. **3 encoded control pins** can encode at least 7 operations; fewer pins, requires decoder.
2. **4 byte-enable pins**, one per byte lane; valid patterns directly select bytes (including the 2 halfwords and full word); simpler/faster decoding, one extra pin.

## 38
One cache cannot simultaneously be extremely small/fast and large enough for high hit ratio. L1 is smallest/fastest, L2/L3 progressively larger/slower. Multiple levels bridge the CPU↔memory speed gap while controlling area/cost/power.

## 39
If the hierarchy is searched serially:

- 20% stop after L1: 1 ns;
- 60% miss L1 and hit L2: 1+2 ns;
- 20% miss both and reach memory: 1+2+10 ns.

Average:

```text
0.2×1 + 0.6×3 + 0.2×13 = 4.6 ns
```

If the listed level times were instead intended as already-total endpoint latencies, a simple weighted average would be 3.4 ns. The chapter's hierarchical lookup model supports **4.6 ns** as the stronger interpretation.

## 40
Assuming 3 bytes/pixel as used in the chapter's full-color examples:

```text
1280×960×3×30×2 = 221,184,000 bytes/s
```

Required bus bandwidth ≈ **221.184 MB/s decimal** (≈210.94 MiB/s).

## 41
**[Needs confirmation].** The answer depends on the exact labels/signals drawn in figure 3.52; that graphical detail is not represented in addressable text RAG.

## 42
**[Needs confirmation] for a unique numeric answer.** Exercise 42 states `10 Mbit/s`, while the PCIe body text gives incompatible gigabit/gigabyte-scale rates; see `source-findings.md`.

Source-supported structure:

- x16 means 16 lanes in each direction;
- the described physical link is bidirectional using separate unidirectional channels;
- with the chapter's first-generation 8b/10b coding, useful payload rate is **80% of raw coded rate**.

If `R` is the adjudicated raw per-lane rate per direction:

```text
raw x16 = 16R
useful x16 = 0.8 × 16R
```

## 43
Track payload:

```text
2048 ×512 = 1,048,576 bytes
```

32-bit DMA operations =1,048,576/4 =262,144 operations.

Bus occupation:

```text
262,144 ×10 ns = 2.62144 ms
```

If one track transfer is serviced every 5 ms, DMA occupies:

```text
2.62144 / 5 = 52.4288%
```

of the shared bus. For a CPU whose instruction stream already needs the bus continuously, the saturated-model throughput reduction is therefore about **52.4%**.

## 44
The source says USB frames occur every 1 ms. With one 1023-byte payload per frame:

```text
1023 bytes / 0.001 s = 1,023,000 bytes/s
```

≈ **1.023 MB/s** (≈0.976 MiB/s).

## 45
The partial decoder currently selects PIO for addresses beginning with `11`. Adding A13 as another positive NAND-selection condition narrows the match to prefix `111`.

So the aliased selection region is halved:

- before: top 16 KiB range with prefix 11;
- after: top 8 KiB range with prefix 111.

The actual PIO still exposes only its small register set; the remaining matched addresses are aliases because decoding is still partial.

## 46
A source-grounded simulator structure:

```text
read wiring table
validate every destination has at most one driver

for input_value in 0 .. (2^j - 1):
    set external input pins from input_value
    set every unused NAND input to 1

    evaluate NAND gates in dependency/topological order:
        gate_out = NOT (in1 AND in2)

    collect k output pins
    print input_value, output_vector
```

If the wiring table permits combinational cycles, a simple topological evaluator is insufficient; the source exercise does not define cycle semantics, so such input should be rejected or marked invalid rather than inventing sequential behavior.

## 47

```text
parse(expr1) → syntax tree
parse(expr2) → syntax tree
vars = union(all variables)

for each of 2^|vars| assignments:
    a = evaluate(expr1, assignment)
    b = evaluate(expr2, assignment)
    if a != b:
        return NOT_EQUIVALENT with counterexample

return EQUIVALENT
```

The parser needs variables, AND, OR, NOT and parentheses. This directly implements the chapter definition: two Boolean functions are equivalent iff they have identical output for every input combination.
