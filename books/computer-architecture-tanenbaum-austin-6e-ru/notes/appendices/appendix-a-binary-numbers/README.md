# Приложение А — Двоичные числа

**Source policy:** `rag_only`.

## Boundary

- PDF: **708–719**
- RAG: `p0708:c01`–`p0719:c01`
- Review: **16 questions**
- Next unit: `p0720:c01` — Appendix B

## Purpose

Appendix A builds the numeric foundation used throughout the book:

```text
finite precision
→ positional notation
→ base conversion
→ signed binary representations
→ binary arithmetic / overflow
```

## Core ideas

1. Computer integers are finite-precision values; ordinary algebraic identities can fail when intermediate results overflow.
2. Positional notation with radix `r` represents a value as a weighted sum of powers of `r`.
3. Binary, octal and hexadecimal are structurally convenient because 8 and 16 are powers of 2.
4. Decimal↔binary conversion can be done by decomposition into powers of two or repeated division by 2.
5. Four signed representations are discussed: sign-magnitude, ones' complement, two's complement and biased representation.
6. Ones' complement has two zeros and uses end-around carry.
7. Two's complement has one zero, discards carry out of the sign position and has an asymmetric range.
8. Signed overflow occurs when adding operands with the same sign produces a result with the opposite sign; equivalently, carry into and carry out of the sign bit differ.

## Operational relevance

For systems work this appendix explains why:

- integer width matters;
- overflow is representation-dependent;
- hex is a compact view of binary state;
- masks, flags, addresses and register dumps are naturally read in bases 2/8/16;
- two's-complement arithmetic can use the same binary adder for positive and negative operands.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Conditional artifact

`summary.md`: **[Not applicable]** — the source has no explicit appendix-end summary section.
