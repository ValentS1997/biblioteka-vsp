# Mermaid — глава 1 «Введение»

Источник: RAG `p0020:c01`–`p0075:c01`, PDF pages 20–75. Все связи ниже синтезированы только из главы.

## 1. Многоуровневая машина

```mermaid
flowchart TD
  USER["Человеческая задача"] --> HLL["High-level language"]
  HLL -->|translation or interpretation| ASM["Assembly / symbolic level"]
  ASM -->|assembler / translation| OS["Operating-system level"]
  OS -->|OS interpreter for added features| ISA["ISA level"]
  OS -->|ISA-identical commands| ISA
  ISA --> MICRO["Microarchitecture"]
  MICRO --> LOGIC["Digital logic"]
  LOGIC --> PHYS["Physical devices / transistors"]
```

Примечание: source model не требует, чтобы каждый конкретный program path буквально проходил через каждый блок. Диаграмма показывает иерархию уровней и типичные механизмы поддержки.

## 2. Translation vs interpretation

```mermaid
flowchart LR
  P1["Program in L1"] --> T{"Execution method"}
  T -->|Translation| P0["Complete program in L0"]
  P0 --> HW["Execute L0"]
  T -->|Interpretation| I["Interpreter in L0"]
  I --> C["Read one L1 command"]
  C --> E["Execute equivalent L0 sequence"]
  E --> C
```

## 3. Architecture vs implementation

```mermaid
flowchart TD
  LEVEL["One abstraction level"] --> ARCH["Architecture: visible types, operations, properties"]
  LEVEL --> IMPL["Implementation: how the level is built"]
  ARCH --> USER["User/programmer of this level"]
  IMPL --> LOWER["Lower-level mechanisms"]
  LOWER --> TRADE["cost • speed • reliability • change frequency"]
```

## 4. Historical development

```mermaid
flowchart LR
  M["Mechanical"] --> V["Vacuum tubes"]
  V --> T["Transistors"]
  T --> IC["Integrated circuits"]
  IC --> VLSI["VLSI / personal computers"]
  VLSI --> INV["Small / embedded / invisible computers"]
```

## 5. Architectural ideas accumulated over time

```mermaid
flowchart TD
  WIRED["Hardwired early machines"] --> MICROPROG["Microprogramming"]
  MICROPROG --> OS["Operating-system virtual operations"]
  OS --> FAMILY["Compatible computer families"]
  FAMILY --> RISC["RISC / simpler instructions"]
  RISC --> SUPER["Superscalar execution"]
  SUPER --> MULTI["Multicore / explicit parallelism"]
  FAMILY --> FPGA["FPGA flexibility for specialized hardware"]
```

## 6. Computer spectrum

```mermaid
flowchart LR
  RFID["Disposable / RFID"] --> MCU["Microcontrollers"]
  MCU --> MOBILE["Mobile / gaming"]
  MOBILE --> PC["Personal computers"]
  PC --> SERVER["Servers"]
  SERVER --> CLUSTER["Clusters / data centers"]
  CLUSTER --> MAIN["Mainframes / large transaction systems"]
```

Это не строгая шкала мощности: глава показывает разные назначения и trade-offs, а не единственную линейную иерархию.

## 7. Centralization cycle

```mermaid
flowchart LR
  MF["Mainframe + remote terminals"] --> PC["Personal/local computing"]
  PC --> CLOUD["Data centers / cloud"]
  CLOUD --> CLIENT["Simple client devices"]
  CLIENT --> CLOUD
```

## 8. Три сравнительных ISA

```mermaid
flowchart TD
  ISA["Comparative ISA examples"] --> X86["x86: PC / servers"]
  ISA --> ARM["ARM: mobile"]
  ISA --> AVR["AVR: embedded / microcontrollers"]
```
