# Краткое содержание главы 5

**Provenance:** `p0468:c01`–`p0469:c01`, PDF pages 468–469.

## ISA model

The instruction-set architecture is the machine interface seen by compiled programs. It defines memory organization, architectural registers, instruction behavior and control-transfer mechanisms.

Most modern systems use byte-addressed memory with multi-byte words. Some require natural alignment; others allow unaligned accesses at additional cost.

## Instructions and addressing

Instructions commonly have zero to three explicit operands and use addressing modes such as:

- immediate;
- direct;
- register;
- register indirect;
- indexed/relative;
- stack.

Typical instruction classes move data, perform arithmetic/logical operations, compare values, branch, call procedures, control loops and perform or initiate I/O.

## Control flow

Branches redirect sequential execution.

Procedures require a recoverable return path and frame state. A stack supports nested and recursive procedure calls.

Coroutines, exceptions and interrupts are additional forms of control transfer. Interrupts let I/O proceed in parallel with normal computation and return control transparently after service.

## ISA examples

The chapter contrasts:

- Core i7: large historically layered CISC ISA;
- OMAP4430/ARM: regular load/store RISC ISA;
- ATmega168/AVR: compact embedded ISA.

## IA-64

IA-64/Itanium uses EPIC to expose parallelism to the compiler. The compiler schedules nonconflicting operations, while predication reduces conditional branches and speculative loads move memory latency earlier.

## Chapter synthesis

```text
ISA quality
= implementable efficiently in hardware
+ compilable efficiently from software
+ stable enough for compatibility
+ explicit enough to define observable behavior
```
