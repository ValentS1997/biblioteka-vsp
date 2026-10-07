# Cheatsheet — глава 4 «Уровень микроархитектуры»

**Provenance:** RAG `p0270:c01`–`p0376:c01`. Policy: **rag_only**.

## Problem framing

When an ISA-level instruction is slow, ask which layer is responsible:

- excessive microcode path length;
- long datapath critical path;
- instruction-fetch overhead;
- pipeline dependency;
- branch misprediction;
- cache/memory latency;
- false register dependency;
- speculation/recovery overhead.

## Mic-1 baseline

### Datapath

- H supplies ALU input A.
- One selected source drives B bus.
- ALU/shifter output returns over C bus.
- Multiple registers may load from C in one cycle.
- Only one B source should drive the bus.

### Memory

| Path | Registers | Granularity |
|---|---|---|
| data | MAR/MDR | word |
| instruction stream | PC/MBR | byte |

`MAR=2` addresses byte range 8–11 in the source machine; `PC=2` addresses byte 2.

### One microcycle

1. control signals settle;
2. selected register drives B bus;
3. ALU + shifter execute;
4. result propagates over C bus;
5. registers/flags capture at edge.

## Microinstruction / sequencing

Mic-1 control fields:

- next address;
- JAM/JMPC;
- ALU/shifter;
- C destinations;
- memory control;
- B source.

Dispatch pattern:

```text
Main1:
PC = PC + 1
fetch next byte
goto(MBR)
```

JMPC ORs MBR opcode bits into the low control-store address bits.

## IJVM

Core state:

| Register | Role |
|---|---|
| PC | bytecode position |
| SP | top-of-stack word address |
| LV | local-variable frame pointer/link area in source layout |
| CPP | constant-pool base |
| TOS | cached top-of-stack value |
| OPC | temporary |
| MAR/MDR | word memory path |
| MBR | instruction byte |

Stack arithmetic pops two words and pushes one result.

## Performance ladder

### Mic-1
Simple microcoded sequential control.

### Mic-2
Adds IFU:

- prefetch 4-byte words;
- MBR1 = next byte;
- MBR2 = next two bytes;
- dedicated PC/IMAR incrementing;
- removes Main1-style fetch work from many instruction paths.

### Mic-3
Pipeline datapath work:

```text
fetch
→ read operands
→ ALU/shifter
→ write back
```

Single instruction spans multiple stages, but steady-state throughput can approach one new operation per cycle.

### Mic-4
Adds decode and micro-op queueing before a deeper pipeline.

## Dependency checklist

- **RAW** — real dependency; consumer must wait.
- **WAR** — false name dependency; renaming can remove.
- **WAW** — false name dependency; renaming can remove.
- structural hazard — required functional unit unavailable.
- control hazard — branch outcome/target unresolved.

## Cache checklist

- spatial locality;
- temporal locality;
- direct mapped vs set associative;
- line size;
- replacement policy;
- write-through vs write-back;
- write-allocate vs no-write-allocate;
- L1/L2/L3 latency/capacity trade-off.

## Branch prediction

A 1-bit predictor flips after one miss; the source 2-bit FSM requires two consecutive failures before changing direction.

For deeper pipelines, misprediction penalty grows because more in-flight work must be canceled.

## Out-of-order / renaming

```text
architectural register name
        ↓ rename map
physical register
        ↓
issue when operands + unit ready
        ↓
execute out of order
        ↓
reorder / commit architectural state
```

## Speculation rule

Do work early only if:

- side effects can be delayed/canceled;
- exceptions can be deferred/represented safely;
- wrong-path work can be discarded.

## Next action

For a microarchitecture performance analysis:

1. count cycles/micro-ops;
2. identify serial critical path;
3. separate latency from throughput;
4. identify dependencies and branch hazards;
5. inspect cache/memory path;
6. distinguish true dependencies from name dependencies;
7. quantify recovery cost before adding speculation.

## Modifying action

**[Not applicable].**

No operational CPU/firmware command sequence is provided.

## Acceptance

Reader should be able to explain Mic-1 state/datapath/control, IJVM dispatch, why IFU shortens paths, why pipelining changes throughput, why renaming removes WAR/WAW but not RAW, and why speculation requires recoverable state.
