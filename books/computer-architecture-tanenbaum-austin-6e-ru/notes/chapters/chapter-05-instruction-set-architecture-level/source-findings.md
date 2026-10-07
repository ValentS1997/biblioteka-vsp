# Source findings — глава 5

Policy: **rag_only**. Findings are preserved without silent correction.

## SF-01 — programmed-I/O ready loop contradicts surrounding explanation

**Classification:** [Source code/text mismatch]

**Provenance:** `p0429:c01`–`p0430:c01`.

The prose says the CPU repeatedly reads display status **until** the ready bit becomes 1, then writes the character.

Listing 5.5 computes:

```text
ready = (status >> 7) & 0x01;
```

but the extracted loop condition is:

```text
} while (ready == 1);
```

That condition repeats while ready is already 1 and exits when it is 0, opposite to the prose.

**Handling:** the chapter artifacts retain the conceptual rule “poll until ready”, while the listing mismatch remains unresolved.

## SF-02 — exercise 17 cites figure 5.17, but its bit-23/variant wording belongs to figure 5.16

**Classification:** [Source cross-reference mismatch]

**Provenance:** `p0472:c01` versus `p0414:c01`–`p0415:c01`.

Exercise 17 asks how format variants 1, 2 and 3 are distinguished and specifically mentions bit 23.

The chapter text describing **figure 5.16** states that bit 23 selects variant 2 and that variant 3 is used for branch/call-like opcodes. Figure 5.17 is instead introduced as a two-address format with 8-bit opcode plus two 12-bit operand specifications.

**Handling:** review answer 17 explicitly treats the exercise as referring to figure 5.16; no silent renumbering is made.

## SF-03 — exercise 38 cites figure 5.25 for a frame pointer, but figure 5.25 is the procedure/coroutine control-flow illustration

**Classification:** [Source cross-reference mismatch]

**Provenance:** `p0474:c01` versus `p0448:c01`–`p0449:c01`.

Page 448 discusses stack frames and frame pointers around figure 5.24. Page 449 identifies figure 5.25 as ordinary procedure A/B control transfer.

Exercise 38 says “in figure 5.25 the frame pointer points to the first local variable”.

**Handling:** review answer uses the surrounding frame-model text, but the exact figure reference is flagged as inconsistent.

## Adjudication status

Direct page-image inspection and external documentation are outside the current chapter contract. Findings remain unresolved.
