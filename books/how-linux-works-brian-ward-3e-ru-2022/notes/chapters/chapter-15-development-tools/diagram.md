# Mermaid — глава 15 «Инструменты разработки»

Источник: **RAG `p0419:c01`–`p0441:c01`**, PDF/печатные страницы 419–441. Диаграммы синтезированы из текстово подтверждённых связей главы; исходный рис. 15.1 не реконструируется.

## 1. C build pipeline

```mermaid
flowchart LR
  SRC[".c source"] --> CPP["C preprocessor"]
  CPP --> CC["Compiler"]
  CC --> OBJ[".o object file"]
  OBJ --> LD["Linker"]
  LIB["Static/shared libraries"] --> LD
  LD --> EXE["Executable"]
```

The chapter separates preprocessing, compilation to object files, and final linking (§15.1, §15.1.4).

## 2. Missing dependency by stage

```mermaid
flowchart TD
  ERR["Build error"] --> Q{"Stage?"}
  Q -->|Preprocess/compile| HDR["Missing header / include path"]
  Q -->|Link| SYM["Undefined symbol"]
  SYM --> LIB{"Library symbol or own object?"}
  LIB --> LFLAG["Add correct -l/-L dependency"]
  LIB --> OBJ["Add missing object file"]
  HDR --> IFLAG["Use correct #include / -I path"]
```

The source explicitly says an undefined reference is not always a missing library; it can be an omitted object file (§15.1.2).

## 3. Static vs shared library

```mermaid
flowchart TD
  LINK["Link program"] --> TYPE{"Library type"}
  TYPE -->|Static .a| COPY["Required code copied into executable"]
  TYPE -->|Shared .so| REF["Executable stores runtime references"]
  REF --> LOAD["ld.so resolves/loads at runtime"]
  LOAD --> SHARE["Multiple processes can share library code"]
```

This is the chapter's central shared-library model (§15.1.3).

## 4. Runtime shared-library search

```mermaid
flowchart TD
  EXE["Start executable"] --> RPATH["Embedded runtime search path if present"]
  RPATH --> CACHE["/etc/ld.so.cache"]
  CACHE --> CONF["Paths derived from loader configuration"]
  ENV["LD_LIBRARY_PATH"] --> RISK["Global override/conflict risk"]
  RISK --> LOAD["Resolved shared object"]
  CONF --> LOAD
```

The source strongly discourages global `LD_LIBRARY_PATH` and arbitrary additions to `/etc/ld.so.conf` (§15.1.3).

## 5. Narrow nonstandard-library strategy

```mermaid
flowchart TD
  LIB["Library in nonstandard directory"] --> BUILD{"Can rebuild program?"}
  BUILD -->|Yes| RP["Embed rpath at link time + -L"]
  BUILD -->|No| PATCH["Source names patchelf"]
  PATCH --> VERIFY["Verify dependency resolution"]
  BUILD -->|Legacy workaround| WRAP["Wrapper with scoped LD_LIBRARY_PATH"]
  WRAP --> VERIFY
  RP --> VERIFY
```

The wrapper approach is presented as a constrained exception, not a global policy.

## 6. Make dependency graph

```mermaid
flowchart TD
  ALL["all"] --> PROG["myprog"]
  PROG --> A["aux.o"]
  PROG --> M["main.o"]
  AS["aux.c"] --> A
  MS["main.c"] --> M
  A --> LINK["Link myprog"]
  M --> LINK
```

This reconstructs the text-confirmed dependencies behind fig. 15.1; original figure geometry is unavailable.

## 7. Make rebuild decision

```mermaid
flowchart TD
  TARGET["Target exists"] --> DEP{"Any prerequisite newer?"}
  DEP -->|No| NONE["Nothing to be done"]
  DEP -->|Yes| RULE["Run rule to update target"]
  RULE --> NEXT["Dependent targets may now become stale"]
  NEXT --> DEP2["Re-evaluate upward dependency chain"]
```

The source uses `touch aux.c` to demonstrate the cascading rebuild (§15.2.4).

## 8. Safe install workflow

```mermaid
flowchart TD
  SRC["Unfamiliar Makefile"] --> READ["Inspect install target"]
  READ --> DRY["make -n install"]
  DRY --> OK{"Expected files/paths?"}
  OK -->|No| STOP["STOP / adjust build config"]
  OK -->|Yes| INSTALL["make install"]
  INSTALL --> VERIFY["Read back installed files/runtime"]
```

The dry-run-before-install rule is explicit in §15.2.7.

## 9. Shebang execution model

```mermaid
flowchart LR
  SCRIPT["Executable script"] --> SB["#! interpreter path"]
  SB --> INT["Interpreter/runtime"]
  INT --> CODE["Script body"]
  BAD["Wrong interpreter path"] --> FAIL["bad interpreter"]
```

The chapter highlights interpreter-path correctness as a common script failure (§15.4).

## 10. Java model

```mermaid
flowchart LR
  JAVA[".java source"] --> JAVAC["javac / JDK"]
  JAVAC --> CLASS[".class bytecode"]
  CLASS --> JRE["Java runtime / VM"]
  JAR[".jar archive of classes"] --> JRE
```

The source distinguishes Java source compilation from bytecode execution (§15.5).

## 11. Tool-choice / chapter transition

```mermaid
flowchart TD
  TOOLS["Compiler + linker + make + interpreters"] --> PKG["Package build systems"]
  PKG --> NEXT["Chapter 16: compile/install source packages"]
```

§15.6 explicitly transitions from individual development tools to package compilation.
