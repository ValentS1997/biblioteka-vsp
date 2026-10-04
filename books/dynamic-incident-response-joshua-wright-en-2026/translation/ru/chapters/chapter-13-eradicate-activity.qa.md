---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 13
translated_chapter: "chapter-13-eradicate-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0300:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0404:c01"
source_pdf_page_range: "300-404"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
source_repair:
  references_26_36:
    status: "RESTORED"
    canonical_chunk: "p0404:c01"
    authoritative_source: "https://dynamicincidentresponse.com/chapters/eradicate.html"
---

# QA — Chapter 13

## Result

`ACCEPTED`

## Completeness

- PASS — all source headings/prose ranges p0300:c01–p0404:c01 represented.
- PASS — Figures 91–121 represented as captions/references.
- PASS — Listings 62–114 represented or explicitly fail-closed where reproducing executable malicious payload material is inappropriate.
- PASS — Tables 26–31 represented.
- PASS — references [1]–[38] preserved.
- PASS — bibliography extraction gap [26]–[36] repaired in canonical RAG from the official book HTML.
- PASS — all nine Eradicate Step-by-Step sections represented.
- PASS — Chapter 14 excluded.

## Semantic fidelity

- PASS — investigation, RCA, persistence removal, identity remediation, rebuild decision, vulnerability remediation, eradication challenges, validation, documentation, and both operational examples preserved.
- PASS — no known reversed condition, causality, or modality mismatch.

## Technical integrity

- PASS — commands, paths, identifiers, CVEs, cloud/account IDs, and framework/product names preserved where represented.
- PASS — reference tail [26]–[38] matches repaired canonical RAG.

## Provenance

- PASS — PDF 300–404.
- PASS — first chunk p0300:c01.
- PASS — last chunk p0404:c01.
- PASS — p0405:c01 begins Recover Activity and is excluded.

## Licensing / fail-closed handling

- PASS — CC BY 4.0 attribution/adaptation notice present.
- PASS — third-party figures/quotes/screenshots remain fail-closed where required.
- PASS — executable malicious payload material is not duplicated verbatim in reader-facing translation where explicitly flagged.
