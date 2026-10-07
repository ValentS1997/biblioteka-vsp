# Source findings — глава 7

Policy: **rag_only**. Findings are preserved without silent correction.

## SF-01 — malformed macro internal representation

**Classification:** [Source extraction/code issue]

**Provenance:** `p0566:c01`.

The extracted internal form of macro CHANGE contains:

```text
MOV EAX,&P1;MOV EBX,&P2;MOV &P2EAX;MOV &P1,EBX;
```

The third operation lacks a visible separator/comma between `&P2` and `EAX`.

**Handling:** artifacts use the macro-expansion concept and clean surrounding source examples, not this string as executable syntax.

## SF-02 — pass-two variable name mismatch

**Classification:** [Source extraction/code issue]

**Provenance:** `p0571:c01`.

The listing declares approximately:

```text
boolean morejnput = true;
```

but later uses:

```text
while (more_input)
```

These are different identifiers.

**Handling:** listing is treated as algorithmic pseudocode, not copy/paste Java.

## SF-03 — DDL/DLL wording drift

**Classification:** [Source wording/extraction issue]

**Provenance:** `p0584:c01`–`p0585:c01`.

The section consistently discusses Windows **DLL** files, but one sentence says approximately “при создании DDL”.

**Handling:** artifacts use DLL as the section's explicit term and record the inconsistent occurrence here.

## Adjudication status

No direct page-image inspection or external documentation is used under the current chapter contract.
