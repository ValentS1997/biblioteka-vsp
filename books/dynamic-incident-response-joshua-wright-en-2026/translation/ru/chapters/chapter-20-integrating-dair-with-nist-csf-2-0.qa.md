---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 20
translated_chapter: "chapter-20-integrating-dair-with-nist-csf-2-0.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0637:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0648:c01"
source_pdf_page_range: "637-648"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 20

## Boundary and completeness

- PASS — Chapter 20 begins at PDF page 637 / chunk `p0637:c01`.
- PASS — Chapter 20 ends at PDF page 648 / chunk `p0648:c01`.
- PASS — PDF page 649 / chunk `p0649:c01` begins the Afterword and is excluded.
- PASS — Figure 200 represented.
- PASS — Tables 60–64 represented.
- PASS — reference [1] preserved.
- PASS — source sections preserved: NIST SP 800-61 R3 / CSF 2.0 framing, six CSF functions, compliance requirements, DAIR mapping, iterative-response value, Govern mapping, compliance artifacts, control effectiveness, audit requirements, tracking-platform configuration, communication templates, concluding integration.

## Semantic fidelity

- PASS — Chapter framing preserved: compliance and operational effectiveness are complementary rather than competing goals.
- PASS — NIST SP 800-61 Revision 3 shift from stand-alone incident handling to integrated cyber risk management preserved.
- PASS — all six CSF 2.0 functions preserved: Govern, Identify, Protect, Detect, Respond, Recover.
- PASS — CSF 2.0 compliance obligations preserved across documented capabilities, demonstrated effectiveness, metrics/measurement, and continuous improvement.
- PASS — DAIR-to-CSF mapping preserved in source structure.
- PASS — Prepare → Protect, Detect/Verify/Triage → Detect, Response Actions Loop → Respond, Recover/Debrief → Recover mappings preserved.
- PASS — Decision Maker coordination preserved across Govern/Identify and throughout the response lifecycle.
- PASS — iterative Response Actions Loop preserved as positive evidence of adaptive response rather than process backtracking.
- PASS — requirement to record iteration triggers and resulting remediation preserved.
- PASS — Govern category mapping preserved for GV.OC, GV.RM, GV.RR, GV.PO, and GV.SC.
- PASS — policy/procedure/playbook distinction preserved.
- PASS — supply-chain response obligations and third-party access revocation preserved.
- PASS — DAIR-generated compliance artifacts preserved by phase.
- PASS — control effectiveness evidence preserved for Detect, Respond, and Recover.
- PASS — audit preparation preserved across document organization, personnel interviews, CSF terminology, standardized incident records, timelines, and lessons learned.
- PASS — incident tracking configuration preserved, including iterative workflow support and Decision Maker documentation.
- PASS — communication-template guidance preserved, including CSF function / DAIR activity tagging and audience variants.
- PASS — final integration conclusion preserved: compliance artifacts arise naturally from effective DAIR operations.

## Technical integrity

- PASS — identifiers preserved: NIST SP 800-61 Revision 3, CSF 2.0, DAIR, GV, ID, PR, DE, RS, RC.
- PASS — Govern category identifiers preserved: GV.OC, GV.RM, GV.RR, GV.PO, GV.SC.
- PASS — Response Actions Loop components preserved: Scope, Contain, Eradicate, Recover.
- PASS — Mean Time to Detect (MTTD) preserved.
- PASS — RACI, JIRA, Remedy, Emergency Communication Plan terminology preserved.
- PASS — no unsupported framework mappings or compliance requirements invented.
- PASS — no external-source enrichment added beyond the canonical chapter content.

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figure 200 is represented without reproducing third-party visual material.
- PASS — canonical English RAG remains source of truth.

## Glossary consistency

- PASS — `NIST Cybersecurity Framework 2.0` → `NIST Cybersecurity Framework (CSF) 2.0`.
- PASS — six CSF function identifiers preserved.
- PASS — `compliance artifact` → `артефакт соответствия требованиям`.
- PASS — `control effectiveness` → `эффективность мер контроля`.
- PASS — `risk-aligned decision-making` → `принятие решений с учетом риска`.

Glossary commit:
`96adefb89c709429959f1fa655136b7aed9879f0`

## Result

`ACCEPTED`
