# Cheatsheet — глава 15 «Инструменты разработки»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0419:c01`–`p0441:c01`, PDF/печатные страницы 419–441. Только `rag_only`.

## Symptom / problem framing

Глава предлагает диагностировать build/runtime проблему по стадии:

1. preprocessor/include;
2. compiler/object file;
3. linker/library;
4. runtime shared-library loader;
5. make dependency/rule;
6. interpreter/runtime path for scripts/Java.

Главный operational принцип: **сначала определить стадию отказа, затем менять только относящийся к ней dependency/path/flag**.

## Baseline / context

| Стадия | Модель главы | PDF |
|---|---|---:|
| C source | `.c` human-readable input | 419–421 |
| Compile | `cc -c` → `.o` object files | 421 |
| Link | object files + libraries → executable | 421–423 |
| Static lib | `.a`; required code copied into executable | 423–424 |
| Shared lib | `.so`; resolved/loaded at runtime | 424–428 |
| Loader | `ld.so` + rpath/cache/search path | 425–427 |
| Headers | include search via defaults and `-I` | 428–429 |
| Preprocessor | `#include`, `#define`, `#if`/ `#ifdef` | 429–430 |
| Make | targets + dependencies + rules | 430–437 |
| Scripts | shebang selects interpreter | 437–440 |
| Java | source → bytecode → JRE/JVM | 440–441 |

## Read-only checks

```sh
ldd /bin/bash
nm --defined-only libcurses.a
locate libcurses.a
make -n
make -n install
make --help
cc --help
```

Source-supported inspection points:

- Read the exact compiler/linker error before changing flags.
- For `undefined reference`, decide whether the missing symbol belongs to a library or one of your own omitted object files.
- For a missing header, inspect the referenced `#include` and known include directories.
- For shared-library runtime failure, inspect required libraries with `ldd` and loader search configuration.
- For a Makefile, identify the first/default target, prerequisites, rule commands and standard targets before execution.

## Interpretation

| Observation | Meaning from source | Still unchecked |
|---|---|---|
| `fatal error: x.h: No such file` | Header/include search problem | Whether header should come from package vs project tree |
| `undefined reference to symbol` | Link stage cannot resolve symbol | Missing library vs missing object file |
| `ldd` maps library to path | Runtime loader resolved that dependency | API/ABI compatibility still separate |
| Library is not found at runtime | Loader search path/cache/rpath problem is plausible | Exact config cause |
| `make` says “Nothing to be done” | Targets are not older than dependencies under its rules | Whether rules themselves are correct |
| `missing separator` | Makefile command indentation/rule syntax is broken | Exact line/content |
| `make -n install` prints system copies | Install target would modify those paths | Permissions/conflicts/backups |
| Script says bad interpreter | Shebang interpreter path is not usable in that environment | Correct interpreter path |
| Java runtime cannot find class | Runtime/class path issue is plausible | Exact JRE/JDK/project structure [Needs confirmation] |

## Next action

1. Capture exact command, working directory and error.
2. Classify stage: preprocess / compile / link / runtime / make / interpreter.
3. Inspect the narrow dependency relevant to that stage.
4. Prefer local build flags/rpath over global loader/environment changes.
5. For Makefile targets with installation/cleanup effects, inspect with dry-run/source before execution.
6. Rebuild only the minimum necessary target where make can do so.
7. Verify both build completion and runtime dependency resolution.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| `cc -c file.c` | Creates/overwrites object file | Working-tree artifact change |
| `cc -o prog ...` | Links executable | Overwrites output executable |
| `-I/path` | Changes header search | Can select unintended header version |
| `-L/path -lname` | Changes link library search | Can select unintended library |
| `-Wl,-rpath=...` | Embeds runtime library path | Persistent executable behavior change |
| `ldconfig -v` | Rebuilds shared-library cache | System-wide loader state change |
| `patchelf` | Modifies existing ELF binary | Binary corruption/loader behavior risk |
| `make` | Executes Makefile rules | Arbitrary build commands may run |
| `make clean` | Removes generated build files | Destructive to build artifacts |
| `make install` | Installs/copies artifacts | System path changes |
| `touch aux.c` | Updates mtime | Triggers dependency rebuild |
| `javac file.java` | Produces bytecode | Build artifact change |

## Verification / acceptance checks

| Change | Verification | Acceptance |
|---|---|---|
| Add include path | compile same target again | Header error gone; no new unintended header conflict |
| Add library/link flag | link same target again | No unresolved symbol; output created |
| Add rpath | `ldd executable` + runtime test | Intended library resolves from intended path |
| Rebuild cache | loader/library resolution check | Intended library visible without breaking other required libs |
| Makefile change | `make -n target`, then real target | Dry-run matches intent; minimum expected commands run |
| Install target | `make -n install` first, then readback installed files | Only intended files/locations changed |
| Script shebang fix | run script in fresh environment | Correct interpreter starts |
| Java compile | expected `.class`/JAR artifact + runtime test | Bytecode created and runs as intended |

## Rollback

- Build outputs: remove/rebuild from source where artifacts are reproducible.
- `make clean`: deleted build artifacts must be rebuilt; source files should remain intact if target is correct.
- `make install`: no generic rollback is defined in this chapter. Prior installed state/package ownership must be captured → **[Needs confirmation]**.
- `ldconfig`: restore prior library files/configuration and rebuild cache; exact prior state must be known.
- rpath/binary patch: rebuild from original objects/source or restore original binary; exact `patchelf` reverse command is not provided.
- `LD_LIBRARY_PATH`: unset/avoid the wrapper/session assignment; the source explicitly discourages global persistence.

## Guardrails

- Do not add arbitrary directories to `/etc/ld.so.conf`.
- Do not set global `LD_LIBRARY_PATH` in shell startup files.
- Prefer embedded rpath for narrow nonstandard library locations when following the source model.
- Run `make -n install` before `make install`.
- Treat unknown Makefiles as executable code, not passive metadata.
- Distinguish missing headers from missing linker symbols; they are different stages.
- Current compiler/runtime/package availability is **[Needs confirmation]** on a live target.
