# Source findings — Appendix B

Policy: **rag_only**.

## BF-B01 — historical IEEE framing

**Classification:** [Historical source boundary]

**Provenance:** `p0724:c01`–`p0726:c01`.

The appendix describes IEEE 754 from the edition's historical perspective, including the 1985 standard and then-current processor/JVM wording.

**Handling:** this artifact preserves the source model and does not update it to later IEEE revisions.

## BF-B02 — exercise 6 purchase question

**Classification:** [Subjective task]

**Provenance:** `p0727:c01`–`p0728:c01`.

After requesting range and precision calculations, the source asks whether the reader would buy either hypothetical machine.

**Handling:** the answer separates the objective numeric trade-off from the subjective purchase decision.

## BF-B03 — exercise 8 accuracy target

**Classification:** [Task underspecification]

**Provenance:** `p0728:c01`.

The exercise asks for a “quick approximate” square root without specifying an error tolerance.

**Handling:** the answer gives the exponent-halving approximation strategy and states that refinement/accuracy criteria are implementation choices.
