# Source findings — глава 9

Policy: **rag_only**. Findings are preserved without silent correction.

## SF-01 — spelling anomalies in bibliography titles/venues

**Classification:** [Needs confirmation]

**Provenance:** `p0700:c01`–`p0701:c01`.

Canonical RAG contains forms including:

- `Programming Distributed Sysytems`;
- `Software Engeneering`;
- `Computer Sysytem`.

Without direct canonical-page inspection or external bibliographic verification, this analysis does not decide whether each form is a print typo or extraction/OCR defect.

**Handling:** preserve the RAG form when quoting metadata; do not silently normalize it from model knowledge.

## SF-02 — collapsed spacing / punctuation

**Classification:** [Source extraction issue]

**Provenance:** examples in `p0700:c01`, `p0702:c01`, `p0706:c01`.

Examples include visibly collapsed token boundaries such as:

- `Software-DrivenMarket`;
- `Conf.On`;
- `ANovelCryptoprocessor`;
- `Microprocessorsand Microsystems`.

**Handling:** chapter analysis does not rely on these strings for technical claims. External metadata cleanup belongs to a separate verification workflow.

## SF-03 — suspicious venue abbreviation in entry 124

**Classification:** [Needs confirmation]

**Provenance:** `p0706:c01`.

Entry 124 contains:

```text
Proc. 7th Int'l. Conf. on Arch. Support for Prog. Long. and Oper. Syst.
```

The token `Prog. Long.` is suspicious in context, but the intended wording is not reconstructed in rag_only mode.

## Adjudication status

No direct page-image inspection, DOI lookup, publisher metadata or external web source was used. The canonical RAG remains authoritative for this chapter artifact set.
