# Mermaid — глава 5 «Уровень архитектуры набора команд»

Источник: RAG `p0377:c01`–`p0474:c01`.

## 1. ISA as contract

```mermaid
flowchart TD
  SRC["High-level source"] --> COMP["Compiler"]
  COMP --> ISA["ISA program"]
  ISA --> HW["Microarchitecture / hardware"]
  ISA --> MEM["Memory model"]
  ISA --> REG["Architectural registers"]
  ISA --> ENC["Instruction encodings"]
  ISA --> CTRL["Control flow / exceptions"]
```

## 2. Instruction bit budget

```mermaid
flowchart LR
  W["fixed instruction width"] --> OP["opcode"]
  W --> MODE["addressing mode"]
  W --> R["register fields"]
  W --> IMM["immediate / displacement"]
```

## 3. Opcode expansion

```mermaid
flowchart TD
  SHORT["short opcode"] --> MANY["many operand bits"]
  ESC["escape pattern"] --> LONG["longer opcode"]
  LONG --> FEWER["fewer operand bits"]
  ESC2["second escape"] --> ZERO["zero-operand / rare operations"]
```

## 4. Effective address

```mermaid
flowchart TD
  EA["effective address"] --> DIRECT["direct: displacement/address"]
  EA --> RI["register indirect: R"]
  EA --> IDX["indexed: R + disp"]
  EA --> REL["base + index + disp"]
  EA --> PCR["PC + signed disp"]
```

## 5. Stack / postfix

```mermaid
flowchart LR
  A["push operands"] --> OP["execute operator"]
  OP --> POP["pop right + left"]
  POP --> RES["push result"]
```

## 6. Procedure frame

```mermaid
flowchart TD
  CALL["call"] --> RET["save return address"]
  RET --> FRAME["save old frame/link"]
  FRAME --> LOC["allocate locals"]
  LOC --> BODY["procedure body"]
  BODY --> EP["restore frame/registers"]
  EP --> BACK["return"]
```

## 7. I/O progression

```mermaid
flowchart LR
  PIO["programmed I/O: polling"] --> IRQ["interrupt-driven I/O"]
  IRQ --> DMA["DMA block transfer"]
```

## 8. Interrupt control transfer

```mermaid
sequenceDiagram
  participant D as Device
  participant C as CPU
  participant T as Vector table
  participant I as ISR
  D->>C: interrupt request
  C->>D: acknowledge
  D-->>C: source/type number
  C->>C: save PC + PSW
  C->>T: index table
  T-->>C: ISR address
  C->>I: transfer control
  I-->>C: restore + return
```

## 9. ISA comparison

```mermaid
flowchart TD
  ISA2["ISA design"] --> X86["x86: compatibility / irregular CISC"]
  ISA2 --> ARM["ARM: regular load/store RISC"]
  ISA2 --> AVR["AVR: compact embedded ISA"]
  ISA2 --> IA64["IA-64: EPIC / explicit parallelism"]
```

## 10. IA-64

```mermaid
flowchart LR
  COMP2["compiler"] --> SCHED["schedule independent instructions"]
  SCHED --> BUNDLE["groups / bundles"]
  COMP2 --> PRED["predication"]
  COMP2 --> SPEC["speculative loads"]
  BUNDLE --> CPU2["simpler runtime scheduling"]
  PRED --> CPU2
  SPEC --> CPU2
```
