---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 5
translated_chapter: "chapter-05-incident-response-models-and-their-limitations.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0076:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0084:c01"
source_pdf_page_range: "76-84"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 5

## Completeness

- PASS — Chapter 5 begins at PDF page 76 / chunk `p0076:c01`.
- PASS — Chapter 5 ends at PDF page 84 / chunk `p0084:c01`.
- PASS — PDF page 85 / chunk `p0085:c01` begins Part 2 and is excluded.
- PASS — all primary sections represented:
  - The Classic Model: PICERL
  - The NIST Model: SP 800-61
  - NIST SP 800-61 Revision 3 and the Cybersecurity Framework
  - Variations on the Classic Model
  - Shortcomings in Existing Models
  - Insufficient Emphasis on Scoping
  - Emphasis on Linear Models
  - Inadequate Resource Prioritization Guidance
  - Lack of Incident Verification Requirements
  - Lack of Root Cause Analysis
  - The Need for a Modern Approach
- PASS — PICERL six-step sequence represented.
- PASS — NIST SP 800-61r2 four-phase lifecycle represented.
- PASS — NIST CSF 2.0 functions GV/ID/PR/DE/RS/RC represented.
- PASS — Figures 16–21 represented as captions/references.
- PASS — footnotes [1] and [2] represented.
- PASS — no listing/table occurs in the canonical boundary.

## Semantic fidelity

- PASS — source treatment of PICERL as a useful but largely linear model preserved.
- PASS — source distinction between NIST SP 800-61 Revision 2 and Revision 3 preserved.
- PASS — Revision 3 shift from tactical incident handling to organizational integration preserved.
- PASS — five shortcomings are preserved:
  - insufficient scoping emphasis;
  - linear-model emphasis;
  - inadequate resource prioritization;
  - no explicit incident-verification requirement;
  - no explicit root cause analysis.
- PASS — source position that these are limitations arising from evolution of incident response, not failures of the models themselves, preserved.
- PASS — transition to the modern model in Chapter 6 preserved.

## Technical integrity

- PASS — identifiers preserved: PICERL, NIST, NIST SP 800-61, NIST SP 800-61r2, NIST SP 800-61r3, CSF 2.0.
- PASS — CSF function identifiers preserved: GV, ID, PR, DE, RS, RC.
- PASS — historical dates and revision numbers preserved.
- PASS — citation identifier `UCRL-MA-106650` preserved.
- PASS — no commands/code are present in this chapter boundary.

## Licensing

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 16–21 remain `THIRD_PARTY_REVIEW_REQUIRED`.
- PASS — Applied Risk direct quotation is not translated or reproduced.
- PASS — NIST SP 800-61r2 direct quotation is not translated or reproduced.
- PASS — bibliographic/source references are preserved without reproducing third-party passages.

## Recorded corrections

1. Removed an over-detailed restatement of the Applied Risk quotation from the fail-closed marker.
2. Corrected Russian grammar: `root cause incident` → `root cause инцидента`.

Correction commit:
`a89c17539f3836fcbf6579f2b4f5c01fcdf0ee11`

## Result

`ACCEPTED`
