# Source commands/tools — Appendix C

**Important:** these commands are historical textbook material. Do not apply setup/configuration changes to a modern system without separate verification.

## Read-only / low-risk source examples

Assemble example:

```sh
as88 HlloWrld.s
```

Historical UNIX path form:

```sh
./as88 HlloWrld.s
```

Run tracer:

```sh
t88 HlloWrld
```

Historical source rebuild:

```sh
make
```

Verification expected by source after successful assembly:

```text
HlloWrld.$
HlloWrld.#
HlloWrld.88
```

## Tracer commands

Source table includes:

- Enter / empty command → execute one processor instruction;
- numeric count → execute that many instructions;
- `g` → run;
- `b` → set breakpoint;
- `c` → clear breakpoint;
- `n` → run to next source line;
- `r` → run to breakpoint/end;
- `+`, `-`, `=` → move by subroutine-level behavior;
- data/source label display forms;
- `q` → quit.

## Historical modifying action — do not execute blindly

The source describes Windows 2000/XP terminal-driver configuration such as adding an `ansi.sys` line to `config.nt`.

Classification: **state-changing / obsolete environment-specific**.

- Effect: modifies historical DOS/console subsystem configuration.
- Risk: irrelevant or harmful on unsupported/current Windows versions.
- Verification: **[Needs external/current platform verification]**.
- Rollback: restore the previous configuration file.
- Recommendation: do not apply as part of this book-analysis workflow.

## Source syscall ABI names

The tracer exposes examples such as:

- `_OPEN`
- `_CREAT`
- `_READ`
- `_WRITE`
- `_CLOSE`
- `_LSEEK`
- `_EXIT`
- `_GETCHAR`
- `_PUTCHAR`
- `_PRINTF`
- `_SPRINTF`
- `_SSCANF`

These are part of the appendix's educational runtime ABI, not a claim about current OS APIs.
