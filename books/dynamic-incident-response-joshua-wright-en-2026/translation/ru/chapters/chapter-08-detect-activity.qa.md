---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 8
translated_chapter: "chapter-08-detect-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0166:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0189:c01"
source_pdf_page_range: "166-189"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 8

## Boundary and completeness

- PASS — Chapter 8 begins at PDF page 166 / chunk `p0166:c01`.
- PASS — Chapter 8 ends at PDF page 189 / chunk `p0189:c01`.
- PASS — PDF page 190 / chunk `p0190:c01` begins Chapter 9 (`Verify and Triage Activities`) and is excluded.
- PASS — Figures 50–56 represented as captions/references.
- PASS — Listings 29–33 represented; Listing 32 remains fail-closed as third-party correspondence.
- PASS — Detect: Step-by-Step represented.
- PASS — references [1]–[6] represented.
- PASS — no source table exists in the canonical boundary.

## Semantic fidelity

- PASS — signature-based, behavioral, ML and hybrid detection methodologies preserved.
- PASS — business-unit-scoped baselines and ML limitations (model drift, training-data quality, evasion, HITL) preserved.
- PASS — active vs passive detection and Pyramid of Pain threat-hunting rationale preserved.
- PASS — EDR, NDR, SIEM, SOAR, OpenObserve and RITA coverage preserved.
- PASS — human detection sources and cloud-native detection for containers/Kubernetes, serverless/microservices and hybrid cloud preserved.
- PASS — data-volume/velocity, detection-driven collection, encrypted traffic/JA4, adversary evasion and skills-gap challenges preserved.
- PASS — external breach hunter and SIEM beaconing examples preserved.
- PASS — all eight Detect Step-by-Step actions preserved.

## Technical integrity

- PASS — Listing 29 Zeek/RITA commands preserved.
- PASS — Listing 30 KQL DCR transformation preserved.
- PASS — Listing 31 TShark/jq JA4 analysis preserved.
- PASS — Listing 33 Elasticsearch aggregation query preserved.
- PASS — identifiers preserved: EOI, IOC, TTP, MTTD, MTTR, EDR, NDR, SIEM, SOAR, CWPP, eBPF, ECH, ESNI, JA4+, MSSP, MITRE ATT&CK.
- PASS — numeric details preserved where relevant, including 24-hour RITA capture guidance, 2,016 requests, five-minute beaconing interval, 45-day external-authentication claim, and $60,000 Cobalt Strike acquisition reference.

## Glossary consistency

- PASS — signature-based detection locked.
- PASS — behavioral detection locked.
- PASS — machine learning detection locked.
- PASS — human-in-the-loop / HITL locked.
- PASS — active detection and passive detection locked.
- PASS — detection-driven collection locked.

Glossary commit:
`b5e07b336db9dc020c6aaa09a27d39de2e5c2eb0`

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 50–56 not reproduced.
- PASS — direct Conti leaked-chat quotation not translated/reproduced.
- PASS — Listing 32 direct third-party correspondence from Tom Liston not translated/reproduced; author-supported factual claims around it are retained.
- PASS — bibliographic references preserved without reproducing third-party protected passages.

## Result

`ACCEPTED`
