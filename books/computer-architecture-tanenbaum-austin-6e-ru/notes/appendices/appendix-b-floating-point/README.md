# Приложение Б — Числа с плавающей точкой

**Source policy:** `rag_only`.

## Boundary

- PDF: **720–728**
- RAG: `p0720:c01`–`p0728:c01`
- Review: **10 questions**
- Next unit: `p0729:c01` — Appendix C

## Purpose

Appendix B explains why floating-point representation separates **range** from **precision**.

```text
sign × significand × radix^exponent
```

## Core ideas

1. Fixed-point formats become inefficient when the required numeric range is enormous but measurement precision is limited.
2. Floating-point representation stores a significand and an exponent.
3. Normalization removes multiple encodings of the same nonzero value.
4. More exponent bits expand range; more significand bits increase precision/density.
5. Floating-point values are discrete, not a continuum; many real numbers require rounding.
6. Relative spacing is roughly stable across magnitudes even though absolute spacing grows with exponent.
7. IEEE 754 single precision uses 1 sign bit, 8 exponent bits and 23 stored fraction bits; double precision uses 1/11/52.
8. Normalized IEEE numbers use an implicit leading 1.
9. Special exponent patterns represent denormalized values, signed zero, infinity and NaN.
10. Addition requires exponent alignment, significand arithmetic, normalization and rounding.
11. Subtraction of nearly equal values can cause catastrophic loss of significant bits.

## Systems relevance

Floating-point state must be interpreted with:

- field width;
- exponent bias;
- radix;
- hidden/explicit leading bit;
- normalization rule;
- rounding and special-value rules.

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

`summary.md`: **[Not applicable]** — no explicit appendix-end summary exists.
