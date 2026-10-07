# Source findings — глава 8

Policy: **rag_only**. Findings are preserved without silent correction.

## SF-01 — contradictory processor count for Sun Fire E25K

**Classification:** [Source internal numeric conflict]

**Provenance:** `p0649:c01`.

The page initially describes E25K as containing **74 UltraSPARC IV processors**. Later on the same page, using 18 board sets and the stated per-board composition, it says the complete E25K contains **144 processors**.

**Handling:** artifacts do not silently choose one count as authoritative.

## SF-02 — topology figure cross-reference drift

**Classification:** [Source cross-reference mismatch]

**Provenance:** `p0657:c01`–`p0659:c01`.

Figure 8.33 is explicitly introduced as the topology figure containing star, full interconnect, tree, ring, mesh, torus, cube and hypercube.

Subsequent prose refers to the star and four-dimensional cube as being in figure **8.31**, which conflicts with the immediately preceding figure identification.

**Handling:** topology exercises refer to figure 8.33.

## SF-03 — MMP/MPP terminology typo

**Classification:** [Source wording drift]

**Provenance:** `p0670:c01`.

The cluster discussion repeatedly contrasts clusters with **MPP** machines, but one occurrence uses **MMP** in the same context.

**Handling:** artifacts use MPP, matching the chapter's explicit expansion “Massively Parallel Processor”.

## Adjudication status

No direct page-image inspection or external documentation is used under this chapter contract.
