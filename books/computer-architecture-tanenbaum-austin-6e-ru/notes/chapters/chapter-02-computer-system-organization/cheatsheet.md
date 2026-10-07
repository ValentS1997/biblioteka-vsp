# Cheatsheet — глава 2 «Организация компьютерных систем»

**Provenance:** RAG `p0076:c01`–`p0171:c01`, PDF pages 76–171. Policy: **rag_only**.

## Symptom / problem framing

Когда система «медленная» или architecture statement выглядит подозрительно, сначала локализовать bottleneck:

- CPU issue/decode/dependency;
- cache miss / memory latency;
- storage seek/rotation/transfer;
- shared-bus contention;
- I/O controller/device;
- insufficient parallelism;
- reliability overhead.

Не сводить performance к clock rate.

## Baseline / context

| Area | Baseline question |
|---|---|
| CPU | instruction latency или instruction throughput? |
| Pipeline | сколько stages и где dependencies/resource conflicts? |
| Parallelism | SIMD/vector, shared-memory multiprocessor или message-passing multicomputer? |
| Cache | line size, hit ratio, cache/main-memory latency |
| Memory | capacity, access latency, ECC/parity |
| Storage | seek, rotational latency, sequential throughput, redundancy |
| I/O | controller, DMA, interrupt path |
| Interconnect | shared bus arbitration или switched point-to-point |
| Display/data | resolution × bytes/pixel × refresh/frame rate |
| Encoding | common character code and representation |

## Read-only checks

Глава не содержит shell/CLI-команд. Checks здесь архитектурные.

### CPU cycle

1. fetch instruction;
2. advance PC;
3. decode;
4. resolve memory operand location if needed;
5. load operand if needed;
6. execute;
7. repeat.

Skipping PC advance can cause повторное выполнение одной и той же команды.

### Throughput vs latency

Для pipeline с cycle time `T` и `n` stages:

- latency одной команды ≈ `nT`;
- steady-state throughput ≈ одна завершенная команда за `T`, если hazards не создают stalls.

### RISC-style checklist

- common instructions execute directly in hardware;
- high issue rate;
- easy decode / regular formats;
- memory access concentrated in LOAD/STORE;
- many registers.

### Cache

Source model:

```text
average access = c + (1 - h) m
```

где `c` — cache lookup, `m` — main-memory access, `h` — hit ratio.

### Disk access

Разделять:

```text
seek time + rotational latency + transfer time
```

Random I/O dominated by positioning/rotation; sequential I/O approaches media throughput.

### I/O path

```text
program → controller command
controller → device
device/controller → DMA → memory
controller → interrupt → CPU
```

### Bus contention

Если CPU и controller одновременно требуют shared bus, arbiter выбирает владельца. Source говорит, что I/O часто получает приоритет; отбор cycles у CPU называется cycle stealing.

## Interpretation

### CPU parallelism

| Form | Key idea |
|---|---|
| Pipeline | overlap stages of different instructions |
| Superscalar | multiple independent instructions to parallel functional units |
| SIMD | one instruction stream applied to multiple data elements |
| Vector | pipelined functional unit operating on vectors |
| Multiprocessor | multiple CPUs, shared memory |
| Multicomputer | private memory per node, messages between nodes |

### Memory hierarchy

```text
registers
  ↓ fastest / smallest / most expensive per bit
cache
  ↓
main memory
  ↓
SSD / magnetic disk
  ↓
tape / optical archive
  ↓ slowest / largest / cheapest per bit
```

### Cache locality

Sequential instruction fetch, loops and repeated matrix/data access create locality. Cache fetches a line, not only one word.

### RAID

- RAID 0: striping, no redundancy.
- RAID 1: mirroring.
- RAID 2/3: bit/word-level error/parity schemes.
- RAID 4: dedicated parity.
- RAID 5: distributed parity.

Exact stripe geometry remains figure-dependent.

### Interconnect evolution

```text
shared PCI-style bus
→ contention / bandwidth pressure
→ PCIe point-to-point serial lanes + switching
```

## Next action

For a performance problem:

1. identify dominant path;
2. distinguish latency from throughput;
3. localize CPU vs cache/memory vs storage vs I/O;
4. identify serialization/contention;
5. check whether locality or parallelism can hide latency;
6. quantify bandwidth/latency;
7. only then choose a modifying action.

## Modifying action

**[Not applicable].**

Chapter 2 does not provide operator commands for changing a live machine. No BIOS, kernel, RAID, PCIe or storage commands are added from model memory.

## Verification / acceptance checks

Reader should be able to:

- reproduce fetch-decode-execute;
- distinguish latency from throughput;
- explain pipeline/superscalar hazards;
- distinguish SIMD/vector/multiprocessor/multicomputer;
- explain hierarchy and locality;
- calculate basic Hamming/cache/storage/bandwidth exercises;
- decompose disk latency;
- explain RAID trade-offs;
- explain DMA + interrupt + arbitration;
- distinguish PCI from PCIe;
- calculate display/video bandwidth;
- explain indexed color and UTF-8 motivation.

## Rollback

**[Not applicable].**
