# Краткое содержание главы 4

**Provenance:** `p0372:c01`, PDF page 372.

## Datapath and microcode

The central component is the datapath: registers, buses and functional units such as ALU/shifter.

A sequencing controller fetches microinstructions from control memory. Each microinstruction selects operands, controls the functional units, selects destinations and determines the next microinstruction.

## IJVM / Mic-1

IJVM is a stack machine with byte opcodes. Chapter 4 implements an IJVM interpreter as Mic-1 microcode.

Mic-1 is deliberately simple and mostly sequential. Its simplicity reduces hardware complexity but limits performance.

## Mic-2 / Mic-3 / Mic-4

Adding an instruction-fetch unit reduces repeated PC/fetch work and shortens common instruction paths.

Pipelining divides datapath work into shorter stages. Mic-4 combines deeper pipelining with decode and micro-op queueing, increasing parallelism and hardware complexity.

## Performance mechanisms

The chapter then broadens from the teaching machines to common implementation techniques:

- multi-level caches;
- branch prediction;
- out-of-order execution;
- register renaming;
- speculative execution.

These techniques aim to keep functional units busy while preserving the architectural result expected by software.

## Real processors

The source contrasts:

- Core i7: legacy CISC ISA translated to internal micro-ops, deep caching, prediction, out-of-order execution and renaming;
- Cortex A9/OMAP4430: simpler RISC-oriented microarchitecture;
- ATmega168: small, inexpensive, mostly single-cycle embedded design.

## Chapter synthesis

```text
same ISA behavior
can be realized by
very different microarchitectures
depending on
performance • cost • power • complexity • compatibility
```
