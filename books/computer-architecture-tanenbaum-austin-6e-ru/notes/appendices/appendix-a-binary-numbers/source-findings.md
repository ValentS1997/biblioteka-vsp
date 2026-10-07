# Source findings — Appendix A

Policy: **rag_only**.

## AF-A01 — table A.2 row for decimal 40

**Classification:** [Source table/extraction inconsistency]

**Provenance:** `p0716:c01`.

The row labeled decimal `40` shows the positive binary value as `10101000`, while the same row's signed representations and ordinary radix conversion imply a different positive bit pattern.

**Handling:** review calculations use positional conversion from the appendix, not the suspicious cell.

## AF-A02 — exercise 9 bit-count wording

**Classification:** [Source wording ambiguity]

**Provenance:** `p0718:c01`.

The exercise calls the operands “3-bit binary numbers”, then separately asks about the result sign bit and whether the “lower three bits” are zero. That phrasing can be read as implying a fourth carry/sign-related bit.

**Handling:** the answer reports the fixed-width 3-bit result, its sign bit, zero state and overflow explicitly.

## AF-A03 — exercise 15 output width

**Classification:** [Task underspecification]

**Provenance:** `p0719:c01`.

A two's-complement representation is width-dependent, but the exercise does not state the output width.

**Handling:** the solution is parameterized by width `W`; a unique bit string requires `W` to be chosen.
