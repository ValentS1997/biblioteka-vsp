---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 4
translated_chapter: "chapter-04-getting-started.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0061:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0075:c01"
source_pdf_page_range: "61-75"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 4

## Completeness

- PASS — canonical chapter boundary confirmed as PDF pages 61–75.
- PASS — Chapter 5 begins at PDF page 76 / chunk `p0076:c01` and is excluded.
- PASS — all primary sections represented:
  - Incident
  - Malicious Incidents
  - Accidental Incidents
  - Environmental Incidents
  - Event
  - Event of Interest
  - Organizational Definition of EOI
  - Indicator of Compromise
  - Indicators of Attack sidebar
  - Mean Time to Detect
  - Mean Time to Respond
  - incident response metrics guidance
  - MTTR quality scoring
  - Incident Management and Response
  - Incident Response
  - Incident Management
- PASS — Listing 25 represented.
- PASS — Listing 26 represented.
- PASS — Figures 12–15 represented as captions/references with fail-closed visual handling.
- PASS — references [1]–[10] represented.

## Source gaps / fail-closed handling

- PASS — MTTD equation is absent from the extracted canonical RAG text layer and is preserved as `RAG_MISS`; no formula was reconstructed from model memory.
- PASS — MTTR equation is absent from the extracted canonical RAG text layer and is preserved as `RAG_MISS`; no formula was reconstructed from model memory.
- PASS — the subsequent source expression for total occurrence-to-resolution time is also absent from extracted text and remains `RAG_MISS`.
- PASS — CrowdStrike direct quotation in the IOA sidebar is not translated or reproduced; marked `THIRD_PARTY_REVIEW_REQUIRED`.
- PASS — verbatim FortiGuard advisory excerpt preceding Listing 26 is not translated or reproduced; marked `THIRD_PARTY_REVIEW_REQUIRED`.

## Semantic fidelity

- PASS — malicious / accidental / environmental incident distinctions preserved.
- PASS — event → EOI → aggregate EOI progression preserved.
- PASS — distinction among atomic, computed, and behavioral IOC preserved.
- PASS — IOA vs behavioral IOC distinction preserved without inventing differences.
- PASS — MTTD and MTTR definitions, limitations, and measurement caveats preserved.
- PASS — warning that MTTR measures speed rather than response quality preserved.
- PASS — quality-score complement to MTTR preserved.
- PASS — distinction between incident response and incident management preserved.

## Technical integrity

- PASS — SQL in Listing 25 preserved verbatim from canonical RAG.
- PASS — Sigma rule in Listing 26 preserved verbatim from canonical RAG.
- PASS — identifiers preserved: EOI, IOC, IOA, MTTD, MTTR, SIEM, EDR, NDR, SOC, CTI, WAF, WSAL, CVE-2024-55591.
- PASS — values preserved, including 40,592 failures, 204-day breach identification figure, 69%, 48 hours, P0/P1/P2/P3, P50 and P90.
- PASS — URLs, CVE identifiers, rule ID, product names and log literals preserved where rights allow verbatim reproduction.

## Glossary consistency

- CORRECTED — baseline glossary used `IoC`, while canonical English RAG consistently uses `IOC` in Chapter 4.
- PASS — glossary normalized to canonical `IOC`.
- PASS — IOA, MTTD and MTTR baseline entries added with Chapter 4 evidence.

Glossary correction commit:
`3ce503fb701098333edf75e7862f532fc8fd402d`

## Licensing

- PASS — unofficial translation/adaptation notice present.
- PASS — attribution points to `../ATTRIBUTION.md`.
- PASS — Figures 12–15 remain `THIRD_PARTY_REVIEW_REQUIRED`.
- PASS — direct third-party quotations/excerpts are fail-closed rather than silently translated.

## Recorded corrections

1. `IoC` → `IOC` in glossary to follow canonical source spelling.
2. Added IOA, MTTD and MTTR glossary entries.
3. Removed verbatim FortiGuard advisory excerpt pending separate rights verification.
4. Marked the FortiGuard excerpt as `THIRD_PARTY_REVIEW_REQUIRED`.
5. Corrected Russian grammar for the “40,592 failed login attempts” annotation.

Chapter/license correction commit:
`3ef545a3dcf1ccf681eb3934e51186f445fd2e82`

## Result

`ACCEPTED`
