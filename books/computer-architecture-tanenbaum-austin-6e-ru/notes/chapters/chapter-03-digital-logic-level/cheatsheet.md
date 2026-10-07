# Cheatsheet — глава 3 «Цифровой логический уровень»

**Provenance:** RAG `p0172:c01`–`p0269:c01`. Policy: **rag_only**.

## Symptom / problem framing

For hardware-level reasoning, separate four problem classes:

1. **logic error** — wrong Boolean function;
2. **state error** — wrong latch/flip-flop/register behavior;
3. **timing error** — value not stable when sampled;
4. **selection/contention error** — wrong device selected or multiple devices drive a shared line.

## Baseline

| Question | What to identify |
|---|---|
| Function | truth table / Boolean expression |
| Circuit type | combinational or stateful |
| Timing | level-triggered, edge-triggered, synchronous, asynchronous |
| Memory | address width, word width, control signals |
| Bus | master/slave, data/address width, clock/handshake |
| Arbitration | who can become master and priority policy |
| I/O | separate I/O space or memory-mapped |
| Decode | full or partial; aliases possible? |

## Read-only checks

### Boolean equivalence

Two circuits are equivalent iff outputs match for **every** input combination.

Use:

```text
truth table A == truth table B
```

or Boolean identities.

### Combinational vs stateful

- combinational: output = function(current inputs);
- latch/flip-flop: output depends on stored prior state.

### Latch vs flip-flop

- latch: level-sensitive;
- flip-flop: edge-sensitive.

The source itself contains an inconsistent falling-edge phrase on p198; see `source-findings.md`.

### Memory chip

Typical conceptual signals in the chapter:

- address `A...`;
- data `I/O...`;
- `CS` — chip select;
- `RD` — read/write distinction in the worked example;
- `OE` — output enable.

Check that an unselected/non-reading chip does **not** drive the shared data lines.

### SRAM vs DRAM

| SRAM | DRAM |
|---|---|
| stable state while powered | charge leaks |
| no refresh | periodic refresh |
| fast | denser |
| more transistors/bit | transistor + capacitor/bit |
| cache-oriented in chapter | main-memory-oriented |

### Synchronous bus

Verify setup/hold constraints against the clock. If slave is too slow, source inserts `WAIT` cycles.

### Asynchronous bus

Full handshake:

1. master asserts request + `MSYN`;
2. slave completes and asserts `SSYN`;
3. master captures data and drops `MSYN`;
4. slave drops `SSYN`.

### Arbitration

Check:

- centralized or decentralized;
- fixed/daisy-chain priority;
- whether CPU competes with DMA/I/O;
- whether arbiter is a single point of failure.

### Address decoding

**Full decoding:** all required high address bits participate; each intended address range maps uniquely.

**Partial decoding:** fewer bits; cheaper logic, but aliases appear.

Source example:

```text
EPROM → lower half by A15=0
RAM   → region beginning 10...
PIO   → region beginning 11...
```

Partial decoding is acceptable only if unused aliases do not block future expansion.

## Performance formulas / patterns

### Ripple carry

Carry latency grows with bit width because carry propagates stage by stage.

### Bus bandwidth

```text
bandwidth = transfers/sec × bytes/transfer
```

But protocol overhead and wait states reduce useful throughput.

### Block transfer

Transaction setup is amortized across many words, so useful throughput rises toward one word per data cycle.

### PCIe

Treat as point-to-point lanes + switch + packets, not as a traditional shared parallel bus.

### USB

Root hub schedules frame-oriented traffic; isochronous transfer prioritizes predictable timing over retransmission.

## Next action

When a hardware interface fails:

1. verify Boolean selection conditions;
2. verify no two outputs drive the same bus simultaneously;
3. verify address/data/control ordering;
4. verify setup/hold or handshake causality;
5. verify arbitration ownership;
6. verify only intended address range activates the device;
7. then change the design.

## Modifying action

**[Not applicable].**

No live-system CLI/firmware procedure is given in the chapter.

## Acceptance

Reader should be able to:

- simplify Boolean circuits;
- explain mux/decoder/adder/ALU roles;
- distinguish latch and flip-flop;
- explain memory chip organization;
- compare SRAM/DRAM/ROM/flash;
- explain FPGA trade-offs;
- read address/data/control bus contracts;
- compare synchronous and asynchronous buses;
- explain arbitration;
- explain PCI → PCIe conceptual shift;
- explain memory-mapped I/O and full/partial decoding.

## Rollback

**[Not applicable].**
