# Mermaid — глава 16 «Компиляция программ из исходного кода на языке C»

Источник: **RAG `p0442:c01`–`p0457:c01`**, PDF/печатные страницы 442–457. Диаграммы синтезированы только из текстово подтверждённых связей главы.

## 1. Source-build lifecycle

```mermaid
flowchart TD
  PKG["Source package archive"] --> INSPECT["Inspect archive + README/INSTALL"]
  INSPECT --> EXTRACT["Extract to isolated source tree"]
  EXTRACT --> CONF["./configure"]
  CONF --> MAKE["make"]
  MAKE --> TEST["make check"]
  TEST --> PREVIEW["make -n install"]
  PREVIEW --> APPLY{"Install paths/actions expected?"}
  APPLY -->|No| STOP["Adjust prefix or flags"]
  APPLY -->|Yes| INSTALL["make install"]
  INSTALL --> VERIFY["Verify installed files + runtime"]
```

## 2. Archive inspection boundary

```mermaid
flowchart TD
  TAR["Source archive"] --> LIST["List archive members"]
  LIST --> ROOT{"Grouped under package-version/?"}
  ROOT -->|Yes| OK["Extract into controlled directory"]
  ROOT -->|No| LOOSE["Create separate directory first"]
  LIST --> ABS{"Absolute-path members?"}
  ABS -->|Yes| REJECT["Source guidance: reject suspicious archive"]
  ABS -->|No| ROOT
```

## 3. Autoconf generation flow

```mermaid
flowchart LR
  SRC["Source tree"] --> CFG["configure"]
  IN1["Makefile.in"] --> CFG
  IN2["config.h.in"] --> CFG
  HOST["Host probes"] --> CFG
  CFG --> MF["Makefile"]
  CFG --> CH["config.h"]
  CFG --> CACHE["config.cache"]
  CFG --> LOG["config.log"]
```

## 4. Configure flag routing

```mermaid
flowchart TD
  NEED["Nonstandard dependency / build option"] --> STAGE{"Which stage?"}
  STAGE -->|Preprocessor/header| CPP["CPPFLAGS"]
  STAGE -->|Compiler| C["CFLAGS"]
  STAGE -->|Linker/library| LD["LDFLAGS"]
  CPP --> CFG["./configure"]
  C --> CFG
  LD --> CFG
  CFG --> LOG["config.log if probe fails"]
```

## 5. Isolated prefix strategy

```mermaid
flowchart TD
  TEST["Learning/testing build"] --> PREFIX["Explicit home-directory prefix"]
  PREFIX --> BUILD["configure + make + check"]
  BUILD --> DRY["Preview install"]
  DRY --> INSTALL["Install to isolated prefix"]
  INSTALL --> TREE["Self-contained install tree"]
  TREE --> RB["Rollback: remove isolated tree"]
```

## 6. pkg-config dependency metadata

```mermaid
flowchart LR
  PC["package .pc file"] --> PKG["pkg-config"]
  PKG --> CF["Cflags"]
  PKG --> LF["Libs"]
  CF --> BUILD["configure / compiler"]
  LF --> BUILD
  PATH["Extra pkgconfig path or linked/copied metadata"] --> PKG
```

## 7. Patch path-level decision

```mermaid
flowchart TD
  PATCH["Read patch header paths"] --> CWD["Choose working directory"]
  CWD --> P{"Leading component needs stripping?"}
  P -->|No| P0["Use strip level 0"]
  P -->|One component| P1["Use strip level 1"]
  P0 --> PROMPT{"Unexpected file-selection prompt?"}
  P1 --> PROMPT
  PROMPT -->|Yes| STOP["Wrong cwd / strip level / source version likely"]
  PROMPT -->|No| VERIFY["Inspect changed files + rebuild/test"]
```

## 8. Configure failure workflow

```mermaid
flowchart TD
  FAIL["configure fails"] --> MSG["Capture visible error"]
  MSG --> LOG["Open config.log"]
  LOG --> END["Search backward near failure"]
  END --> CAUSE["Find actual failed compiler/linker invocation"]
  CAUSE --> FIX["Correct flag/dependency/path"]
  FIX --> RETRY["Reconfigure cleanly"]
```

## 9. Recursive make error chain

```mermaid
flowchart TD
  COMP["Compiler/preprocessor/tool error"] --> M3["Nested make target fails"]
  M3 --> M2["Parent make target fails"]
  M2 --> M1["Higher recursive target fails"]
  M1 --> TOP["Top-level make exits nonzero"]
  TOP --> RULE["Diagnose the first causal error above the cascade"]
```

## 10. Install-location policy

```mermaid
flowchart TD
  NEED["Need software not adequately covered by distro?"] --> YES{"Manual build justified?"}
  YES -->|No| DIST["Prefer distribution package lifecycle"]
  YES -->|Yes| LOC{"Small local package?"}
  LOC -->|Yes| USR["Use local-install prefix"]
  LOC -->|Many/custom packages| PKG["Create/manage package artifacts"]
  USR --> UPDATE["Manual update/security ownership"]
  PKG --> UPDATE
```

## 11. Chapter transition

```mermaid
flowchart LR
  AUTOCONF["Autoconf/source builds"] --> OTHER["CMake / SCons / distro source packages"]
  OTHER --> KERNEL["Kernel build as specialized case"]
  OTHER --> DEV["Deeper software development"]
```

§16.7 explicitly points beyond basic Autoconf package builds.
