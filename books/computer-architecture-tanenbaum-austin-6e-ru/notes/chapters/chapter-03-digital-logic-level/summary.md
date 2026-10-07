# Краткое содержание главы 3

**Provenance:** `p0263:c01`–`p0264:c01`, PDF pages 263–264.

## Logic

Computers are built from integrated circuits containing gates. Common gates include AND, OR, NAND, NOR and NOT.

More complex digital blocks include:

- multiplexers/demultiplexers;
- encoders/decoders;
- shift circuits;
- arithmetic circuits and ALUs.

Boolean algebra can transform a circuit into an equivalent but potentially cheaper/smaller implementation.

## Arithmetic

Addition is built from half adders and full adders. Word-wide addition connects stages through carry signals; this creates propagation delay and motivates faster carry organizations.

## State and memory

Static state is built from latches and flip-flops. Registers combine multiple one-bit state elements.

The chapter distinguishes RAM, ROM, PROM, EPROM, EEPROM and flash. SRAM preserves state while powered without refresh; DRAM requires refresh.

## Buses

System components communicate through buses with:

- address lines;
- data lines;
- control lines.

Synchronous buses rely on a common clock/timing specification. Asynchronous buses use full handshaking between master and slave.

Multiple potential bus masters require arbitration.

## Examples

The chapter contrasts:

- Core i7 — high-performance x86-compatible multicore CPU;
- TI OMAP4430 — mobile/embedded ARM SoC emphasizing integration and low power;
- ATmega168 — low-cost embedded microcontroller with on-chip program/data memories and I/O.

It also examines PCI, PCI Express and USB.

## Interfaces and decoding

PIO devices can occupy a separate I/O space or be memory-mapped.

Full address decoding uniquely selects ranges using all required address bits. Partial decoding saves logic but creates aliases and can reduce room for future expansion.

## Chapter synthesis

```text
Boolean logic
→ reusable digital blocks
→ state/memory
→ timed shared interconnect
→ processor/device interfaces
→ addressable computer system
```
