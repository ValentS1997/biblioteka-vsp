# Команды и аппаратные примитивы — глава 3

**Provenance:** RAG `p0172:c01`–`p0269:c01`.

## Shell / administrative commands

**[Not applicable].**

Chapter 3 contains no source-confirmed OS or firmware command sequence. Familiar tools such as `lspci`, `setpci`, `devmem`, HDL toolchains or FPGA vendor CLIs are not added from model memory.

## Logic primitives

| Primitive | Meaning |
|---|---|
| NOT | invert one Boolean value |
| NAND / NOR | functionally complete gate families |
| AND / OR / XOR | core Boolean operations used in combinational circuits |
| MUX | select one of multiple inputs |
| decoder | activate one output corresponding to input code |
| comparator | compare words |
| half/full adder | sum bits; full adder includes carry-in |
| ALU | selected arithmetic/logic operation over bit slices |

## State primitives

| Primitive | Source role |
|---|---|
| SR latch | stores one stable bit state |
| D latch | samples D while clock/control level is active |
| D flip-flop | samples around a clock edge |
| register | multiple flip-flops sharing timing/control |
| SRAM | stable state elements |
| DRAM | charge storage + refresh |
| ROM/PROM/EPROM/EEPROM/flash | nonvolatile families with different erase/write properties |

## Bus/interface signals

| Signal | Source role |
|---|---|
| `CS` | select memory/interface chip |
| `RD` | distinguish read/write in worked memory/bus examples |
| `OE` | permit device to drive output lines |
| `MREQ` | memory request |
| `WAIT` | extend synchronous transfer |
| `MSYN` | asynchronous master synchronization/request |
| `SSYN` | asynchronous slave response |
| address lines | identify location/device |
| data lines | carry values |
| control lines | define operation/timing |

These are **hardware signals**, not commands.

## FPGA flow

The source describes:

```text
hardware description
→ synthesizer
→ map to FPGA LUTs/interconnect
```

No HDL syntax or vendor command is provided.

## State-changing actions

**[Not applicable].**

## Verification

Any future CLI or HDL snippet added here must be explicitly supported by chapter RAG or by a separately authorized external-source workflow.

## Rollback

**[Not applicable].**
