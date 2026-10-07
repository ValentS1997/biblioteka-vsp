# Chapter 5 cheatsheet — Ввод и вывод информации

## Symptom / problem framing

Classify the failure before changing state:

- device request never completes → controller/driver/interrupt/DMA path;
- CPU saturated while waiting for a slow device → polling / programmed I/O;
- interrupt rate is excessive → per-byte/per-word interrupt path may be too fine-grained;
- data arrives faster than software consumes it → buffering/ring-buffer/producer-consumer mismatch;
- device works but application sees inconsistent semantics → device-independent interface/naming/block-size layer;
- disk latency is high → seek/rotation/scheduling/cache path;
- repeated media errors → controller remapping/driver error handling/stable-storage recovery path;
- terminal input behaves unexpectedly → canonical/noncanonical mode and special-character handling;
- display/UI issue → event queue, graphics context, X client/server or terminal escape path;
- battery drains during idle → device power-state policy, wakeups, CPU frequency/voltage or application behavior.

## Baseline / context

### Hardware path

```text
CPU
  ├─ port-mapped I/O (IN / OUT)
  └─ memory-mapped I/O
        ↓
controller registers / buffers
        ↓
device
```

### DMA path

```text
CPU programs DMA + device
        ↓
device/controller obtains data
        ↓
DMA transfers buffer to/from memory
        ↓
one completion interrupt
```

### Software stack

```text
user process / I/O library / spooler
              ↓
device-independent I/O software
              ↓
device driver
              ↓
interrupt handler
              ↓
controller / device
```

## Read-only checks

1. Identify whether the target behaves as a block, character or exceptional device such as a clock/display.
2. Determine whether control registers use separate I/O ports or memory-mapped addresses.
3. For MMIO, verify that control-register pages are not treated like ordinary cacheable RAM.
4. Determine transfer mode: programmed I/O, interrupt-driven I/O or DMA.
5. Measure whether interrupts occur per byte/word or per completed buffer.
6. Check DMA direction, memory address, byte/word count and transfer mode before blaming the device.
7. Separate controller buffering from OS buffering; both may exist independently.
8. Locate the request in the four software layers before modifying a driver.
9. Check whether the device is shared or exclusive; for exclusive devices inspect allocation/spooling semantics.
10. For disk latency, separate seek time, rotational latency and transfer time.
11. Determine disk-scheduling policy and whether multiple requests are actually queued; reordering cannot help a queue of length one.
12. For media errors, distinguish correctable/retryable errors, remapped bad sectors and unrecoverable errors.
13. For terminal input, distinguish canonical from noncanonical mode and identify special control characters.
14. For timer problems, distinguish physical clock frequency from software-managed virtual timers.
15. For energy problems, identify which component wakes or remains powered and whether the workload has slack that permits lower CPU frequency/voltage.

## Interpretation

### Programmed I/O vs interrupts vs DMA

| Method | CPU role | Interrupt pattern | Main trade-off |
|---|---|---|---|
| Programmed I/O | CPU polls and moves each unit | none required | simple, but busy-waits |
| Interrupt-driven | CPU initiates and handles each completion/unit | potentially frequent | frees CPU between events, interrupt overhead |
| DMA | DMA controller moves block | typically one per buffer | low CPU overhead, bus/DMA complexity |

### Interrupt correctness

A **precise interrupt** has a recoverable architectural boundary: older instructions are complete, younger instructions have no visible effects, and the interrupted instruction's state is known. Imprecise interrupts can save CPU hardware complexity but transfer substantial reconstruction work to the OS.

### Buffering

- user-space buffering may require pinned pages;
- a kernel buffer allows the caller to resume sooner;
- double buffering lets one buffer fill while the other is copied/consumed;
- ring buffers continuously separate producer and consumer positions;
- every additional copy can lower end-to-end throughput.

### Disk scheduling

- **FCFS:** arrival order; simple and predictable.
- **SSF:** nearest cylinder first; reduces movement but can starve distant requests.
- **Elevator:** continues in one direction, then reverses; bounds service movement.
- **Circular scan:** always serves in one direction, improving positional uniformity.

### RAID

- RAID 0: striping, no redundancy.
- RAID 1: mirroring; higher read concurrency, duplicate capacity.
- RAID 4: block striping + dedicated parity; parity disk bottleneck.
- RAID 5: distributed parity; removes dedicated parity bottleneck.
- RAID 6: additional parity; more write work, greater failure tolerance.
- RAID 2/3: synchronized bit/word-level arrangements described mainly as historical designs.

### Stable storage

```text
write+verify disk 1
        ↓
write+verify disk 2
        ↓
success
```

After a crash, compare the two copies and use ECC validity plus the defined ordering rule to reconstruct a consistent pair. This guarantee depends on the chapter's explicit failure model.

### Terminal / GUI

- canonical input performs line editing before delivery;
- noncanonical input exposes a less processed stream;
- ANSI escape sequences move the cursor and insert/delete screen content;
- X uses an event-driven client/server protocol and a separate window manager;
- Windows GDI uses a device context carrying the target, clipping region and graphics attributes.

## Next action

For an I/O incident:

`identify layer → capture transfer/interrupt/buffer state → distinguish device latency from software overhead → test the narrowest hypothesis → change one layer only → remeasure end-to-end behavior`.

## Modifying action

Source-supported state-changing actions include:

- writing I/O ports or memory-mapped controller registers;
- programming DMA address/count/direction/mode;
- acknowledging an interrupt;
- opening/closing an exclusive device;
- changing terminal input behavior or special-character handling;
- enqueueing output into a spool directory;
- formatting/partitioning a disk;
- changing disk scheduling/order of queued requests;
- writing/remapping bad sectors;
- stable-storage write/recovery;
- programming clock/timer registers;
- changing device power state or CPU voltage/frequency.

These actions affect hardware state or persistent data. Do not combine them into an opaque troubleshooting step.

## Verification / acceptance checks

After a change verify:

- request completes and returns the expected byte/block count;
- interrupt rate matches the intended transfer granularity;
- no lost/duplicate buffer data occurs under sustained load;
- DMA destination/source range is correct and completion occurs once expected;
- driver error is either recovered locally or propagated with a defined error result;
- exclusive device ownership is released;
- disk request latency improves for the target workload, not just one synthetic queue;
- stable-storage copies agree and pass the chapter's ECC/readback assumptions;
- timer expirations occur in deadline order;
- terminal control characters/escape sequences affect only the intended session/output;
- power saving does not violate workload deadlines or required responsiveness.

## Rollback

- Controller/DMA/timer register changes require device/platform-specific reset procedures: `[Needs confirmation]`.
- Disk formatting, partitioning and overwriting are persistent and may not have an in-place rollback; recovery requires preserved data/backups: `[Needs confirmation]`.
- Scheduling/power-policy changes can normally be reverted by restoring the prior policy, but exact commands are not supplied by the chapter.
- Stable-storage recovery follows its own two-copy algorithm; do not invent a separate rollback sequence.
- Terminal/application-mode changes should restore the prior input/output mode; exact platform procedure is `[Needs confirmation]`.
