# Source findings — Appendix C

Policy: **rag_only**.

## CF-C01 — PUSH stack-pointer contradiction

**Classification:** [Source internal contradiction]

**Provenance:** `p0738:c01`, `p0742:c01`, `p0746:c01`.

Pages 738 and 746 state that a word PUSH decreases SP by **2** bytes before storing the word.

Page 742 says PUSH decreases SP by **1**.

**Handling:** artifacts use the repeated word-size-consistent rule `SP -= 2`; the contradictory sentence is not silently discarded and is recorded here.

## CF-C02 — review question 7 missing destination

**Classification:** [Source/extraction ambiguity]

**Provenance:** `p0790:c01`.

The extracted expression is:

```text
= a + b + 2
```

with no visible left-hand destination.

**Handling:** the answer computes the expression into AX and marks any final destination store as [Needs confirmation].

## CF-C03 — SPRINTF argument typo

**Classification:** [Source extraction issue]

**Provenance:** `p0753:c01`.

The table displays the first SPRINTF argument approximately as `but`, while the description calls it buffer `buf`.

**Handling:** artifacts refer to the conceptual buffer argument; exact spelling in the table is preserved as a finding.

## CF-C04 — historical installation instructions

**Classification:** [Historical environment boundary]

**Provenance:** `p0766:c01`.

The setup instructions reference Windows 2000/XP, `ansi.sys`, historical directory layouts and book websites.

**Handling:** these are source history, not current installation guidance. No external availability/current compatibility is assumed.
