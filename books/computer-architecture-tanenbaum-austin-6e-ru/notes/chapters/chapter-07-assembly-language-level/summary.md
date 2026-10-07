# Краткое содержание главы 7

**Provenance:** `p0586:c01`–`p0587:c01`.

## Assembly language

Assembly language is a symbolic representation of machine language and is translated by an assembler.

The source recommends high-level languages for most software. Assembly is justified mainly by strict performance/resource constraints, direct hardware access, compiler/toolchain work and architecture study.

## Macros

Macros give names to source-code sequences. They may have parameters and local labels.

Macro expansion is source-text processing, not a runtime procedure call.

## Two-pass assembly

Pass 1 builds the information required to resolve symbolic names, especially forward references. It maintains an instruction-location counter and constructs symbol/macro/literal metadata.

Pass 2 generates object code and the metadata needed for linking.

Symbol tables can be implemented by sequential lookup, binary search over a sorted table or hashing.

## Linking and loading

Separately translated procedures become object modules. The linker combines them into one executable address space, relocates address-sensitive references and resolves external symbols.

The chapter distinguishes multiple possible binding times, from translation/link time to load or execution time.

## Dynamic linking

Dynamic linking postpones some binding until program load or first use.

Examples:

- MULTICS linkage segments;
- Windows DLLs;
- UNIX shared libraries.

Shared libraries reduce duplication and allow independently replaceable library implementations.

## Chapter synthesis

```text
symbols + translation
→ object module
→ relocation + external resolution
→ executable
→ optional dynamic binding
```
