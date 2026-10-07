# Mermaid — глава 7 «Уровень ассемблера»

Источник: RAG `p0555:c01`–`p0589:c01`.

## 1. Translation

```mermaid
flowchart LR
  SRC["assembly source"] --> ASM["assembler"]
  ASM --> OBJ["object module"]
  OBJ --> LINK["linker"]
  LINK --> EXE["executable"]
  EXE --> RUN["machine execution"]
```

## 2. Two-pass assembler

```mermaid
flowchart TD
  S["source"] --> P1["pass 1"]
  P1 --> ST["symbol table"]
  P1 --> IR["intermediate form"]
  ST --> P2["pass 2"]
  IR --> P2
  P2 --> O["object code + relocation/link info"]
```

## 3. Forward reference

```mermaid
flowchart LR
  USE["BRANCH L"] --> UNKNOWN["L not yet known"]
  UNKNOWN --> P1A["pass 1 finds L"]
  P1A --> P2A["pass 2 encodes address"]
```

## 4. Macro expansion

```mermaid
flowchart LR
  DEF["macro definition"] --> TABLE["macro table"]
  CALL["macro call + actual params"] --> EXP["expander"]
  TABLE --> EXP
  EXP --> TEXT["expanded source text"]
```

## 5. Symbol lookup

```mermaid
flowchart TD
  NAME["symbol"] --> LIN["linear search"]
  NAME --> BIN["sorted + binary search"]
  NAME --> HASH["hash → bucket chain"]
```

## 6. Linking

```mermaid
flowchart TD
  A["object A"] --> L["linker"]
  B["object B"] --> L
  C["object C"] --> L
  L --> BASE["assign bases"]
  BASE --> REL["relocate internal refs"]
  REL --> EXT["resolve external refs"]
  EXT --> EXE2["one executable address space"]
```

## 7. Dynamic linking

```mermaid
sequenceDiagram
  participant P as Program
  participant D as Dynamic linker
  participant L as Shared library
  P->>D: first unresolved call
  D->>L: locate/map procedure
  D-->>P: install resolved address
  P->>L: retry/call
  P->>L: later direct/indirect calls
```

## 8. Binding time

```mermaid
flowchart LR
  SRC2["source"] --> TRANS["translation"] --> LINK2["link"] --> LOAD["load"] --> EXEC["execution"]
```

Later binding increases relocation flexibility.
