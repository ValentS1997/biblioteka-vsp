# Команды и интерфейсы — глава 15 «Инструменты разработки»

**Provenance:** `p0419:c01`–`p0441:c01`, PDF/печатные страницы 419–441. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only observation/dry-run; **WG** — workload-generating build/run; **SC** — state-changing; **SC-D** — destructive/system-impacting.

## 1. C compiler / object files

```sh
cc hello.c
cc -o hello hello.c
cc -c main.c
cc -c aux.c
cc -o myprog main.o aux.o
```

Effects:
- plain compile creates `a.out` in the simple source example;
- `-o` names output;
- `-c` creates object file without final linking.

These are **WG/SC working-tree build artifacts**.

## 2. Linking with libraries

```sh
cc -o badobject badobject.o -lcurses
cc -o badobject badobject.o -lcurses -L/usr/junk/lib -lcrud
```

Source options:
- `-lNAME`: link library named `libNAME...`;
- `-L/path`: add nonstandard library search directory at link time.

Symbol inspection:

```sh
nm --defined-only libcurses.a
locate libcurses.a
```

`nm`/ `locate` are RO inspection.

## 3. Shared-library inspection and loader cache

```sh
ldd /bin/bash
ldconfig -v
```

- `ldd`: RO dependency/path observation.
- `ldconfig -v`: **SC system-wide loader cache**.

Source config paths:
- `/etc/ld.so.cache`;
- `/etc/ld.so.conf`;
- possible includes under `/etc/ld.so.conf.d`.

The chapter explicitly says not to add arbitrary library directories to `/etc/ld.so.conf`.

## 4. rpath and nonstandard runtime libraries

Literal source example:

```sh
cc -o myprog myprog.o -Wl,-rpath=/opt/obscure/lib -L/opt/obscure/lib -lweird
```

**Class:** WG/SC executable metadata.

The source says `-Wl,-rpath` embeds a runtime library search path and `-L` is still required for link-time search.

The prose introduces `libweird.so.1` at a different path (`/opt/obscure/lab`) than the command (`/opt/obscure/lib`); see `source-findings.md`.

Source names `patchelf` for changing rpath in an existing binary, but gives no concrete invocation. Do not invent one.

## 5. LD_LIBRARY_PATH wrapper

Source wrapper:

```sh
#!/bin/sh
LD_LIBRARY_PATH=/opt/crummy/lib
export LD_LIBRARY_PATH
exec /opt/crummy/bin/crummy.bin $@
```

The chapter's policy is stronger than the example:
- **do not** place `LD_LIBRARY_PATH` in shell startup files;
- **do not** use it while compiling software;
- if unavoidable for one legacy/unrebuildable program, constrain it to a wrapper.

The literal `$@` is unquoted in the source. Operational robustness of arbitrary arguments is recorded as a source limitation.

## 6. Include paths / preprocessor

```sh
cc -c -I/usr/junk/include badinclude.c
gcc -E
```

Source preprocessor constructs:
- `#include <file.h>`;
- `#include "local.h"`;
- `#define BLAH something`;
- compiler flag `-DBLAH=something`;
- `#ifdef`, `#if`, `#endif`.

`-I/path` changes header search. `gcc -E` runs preprocessing output mode; direct `cpp` is also named but no concrete options are given.

## 7. make basics

```sh
make
make aux.o
make CC=clang
make blah
make -n
make -f file
```

- normal target execution: **WG/SC build artifacts**;
- `-n`: source-described dry-run, **RO** under chapter model;
- `-f file`: select alternate makefile.

The chapter treats a Makefile as rules, targets, dependencies and shell commands. Recipe command lines require a tab in its source model.

## 8. make variables/macros

Source standard macros:
- `CC` — C compiler;
- `CFLAGS` — C compiler flags;
- `CPPFLAGS` — C preprocessor flags;
- `LDFLAGS` — linker flags;
- `LDLIBS` — library-name flags;
- `CXXFLAGS` — C++ compiler flags.

Automatic variables:
- `$@` — current target;
- `$<` — first prerequisite;
- `$*` — target basename.

## 9. Standard make targets

Source targets:
- `all`;
- `clean`;
- `distclean`;
- sometimes `realclean`;
- `install`;
- `test` or `check`;
- `depend`.

Critical source command:

```sh
make -n install
```

The chapter explicitly says to inspect this before `make install`.

Risk classes:
- `clean` / `distclean`: **SC-D build-tree cleanup**;
- `install`: **SC-D system installation**;
- `test` / `check`: WG;
- `depend`: can modify Makefile according to source.

## 10. Dependency rebuild example

```sh
touch aux.c
make
```

`touch` changes mtime; source uses it to demonstrate how make detects a newer prerequisite and rebuilds dependent targets.

## 11. Lex / Yacc

Source names:
- GNU Lex implementation: `flex`;
- possible link flags: `-ll` or `-lfl`;
- GNU parser: `bison`;
- source startup form: `bison -y`;
- possible Yacc library flag: `-ly`.

No full build pipeline is supplied, so none is invented.

## 12. Script interpreters / shebang

Source examples:

```text
#!/usr/bin/python
#!/usr/bin/env python
#!/usr/bin/tail -2
```

The chapter emphasizes that an incorrect interpreter path produces a “bad interpreter” failure and says multiple shebang arguments are not portable/reliable in its source model.

## 13. Java

Source commands:

```sh
java file.class
java -jar file.jar
javac file.java
```

Source also names:
- `JAVA_HOME`;
- `CLASSPATH`;
- JRE;
- JDK;
- `jar` utility.

These commands are preserved as literal edition content. Current target syntax/runtime behavior is **[Needs confirmation]** where operationally important.

## Command discipline

- Diagnose the failed stage before adding flags.
- Prefer local compile/link configuration over global loader environment changes.
- Inspect `make -n install` before installation.
- Capture library/cache state before `ldconfig` or binary metadata changes.
- Treat Makefiles as executable code.
- Preserve literal source syntax in findings when examples conflict; do not silently “fix” it from model knowledge.
