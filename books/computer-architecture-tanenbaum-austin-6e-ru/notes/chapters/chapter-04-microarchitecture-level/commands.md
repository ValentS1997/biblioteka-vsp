# Команды и микроархитектурные примитивы — глава 4

**Provenance:** RAG `p0270:c01`–`p0376:c01`.

## Shell / administrative commands

**[Not applicable].**

No source-confirmed Linux/firmware/performance-tool commands are present. Commands such as `perf`, `rdmsr`, `cpupower` or simulator invocations are intentionally not added from model memory.

## MAL-style operations explicitly used by the source

| Primitive | Meaning |
|---|---|
| `rd` | initiate word read via MAR/MDR |
| `wr` | initiate word write via MAR/MDR |
| `fetch` | fetch instruction byte via PC/MBR |
| `goto label` | next microinstruction |
| `goto(MBR)` | opcode dispatch through JMPC |
| `if(Z) goto ... else ...` | conditional microbranch via JAMZ |
| `if(N) goto ... else ...` | conditional microbranch via JAMN |

These are **microprogram notation**, not shell commands.

## Example source micro-operations

```text
SP = MDR = SP + 1
MAR = SP; rd
PC = PC + 1; fetch
MDR = TOS; wr
```

The source explicitly warns that MAL expressions must match physical datapath connectivity; arbitrary register-to-register expressions are not valid.

## IJVM instructions discussed

`IADD`, `ISUB`, `IAND`, `IOR`, `ILOAD`, `ISTORE`, `BIPUSH`, `LDC_W`, `IINC`, `GOTO`, `IFEQ`, `IFLT`, `IF_ICMPEQ`, `DUP`, `POP`, `SWAP`, `WIDE`, `INVOKEVIRTUAL`, `IRETURN`, `NOP`.

These are ISA/bytecode operations, not host commands.

## State-changing actions

**[Not applicable]** for a real machine.

## Verification

Any future operational command added here requires explicit source evidence or a separately authorized external workflow.

## Rollback

**[Not applicable].**
