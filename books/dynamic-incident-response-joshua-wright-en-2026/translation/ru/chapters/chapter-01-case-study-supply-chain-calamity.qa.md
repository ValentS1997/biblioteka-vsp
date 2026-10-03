---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 1
translated_chapter: "chapter-01-case-study-supply-chain-calamity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0027:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0043:c01"
source_pdf_page_range: "27-43"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 1

## Completeness

- PASS — source heading hierarchy represented:
  - JORDAN
  - PYRIX
  - Lateral Movement
  - Cloud Pivot
  - Exfiltration
  - SAM
  - Identification
  - Containment
  - Eradication
  - Recovery
  - Lessons Learned
  - What Remained
- PASS — source prose blocks represented after recorded correction.
- PASS — Listings 2–23 represented.
- PASS — Figure references 3–6 represented as captions/references.
- PASS — no source footnote/reference block within the chapter boundary was silently omitted.

## Semantic fidelity

- PASS — PICERL framing and the chapter's central failure mode are preserved: the response remained workstation-scoped and did not establish the full compromise scope.
- PASS — causal sequence is preserved: compromised SDK → workstation access → SOCKS/Tor pivot → credential harvesting → internal/cloud access → exfiltration → incomplete response.
- PASS — modal/uncertainty language was not intentionally strengthened.
- PASS — numeric values and identifiers are preserved.

## Technical integrity

- PASS — commands and code/listing bodies are retained verbatim from canonical RAG, except Markdown fencing/line presentation.
- PASS — paths, URLs, AWS identifiers, port numbers, process names, bucket names and CVE/standard-like identifiers present in the source boundary are preserved.
- PASS — product/framework names such as Docker, Tor, MiniServe, AWS, EC2, S3, CloudTrail and PICERL are preserved.

## Provenance

- PASS — Chapter 1 begins at PDF page 27 / chunk `p0027:c01`.
- PASS — Chapter 1 ends at PDF page 43 / chunk `p0043:c01`.
- PASS — PDF page 44 / chunk `p0044:c01` begins Chapter 2 ("Introduction") and is excluded.

## Licensing

- PASS — translation/adaptation is explicitly marked unofficial.
- PASS — CC BY 4.0 attribution path is referenced via `../ATTRIBUTION.md`.
- PASS — figure visual assets 3–6 remain `THIRD_PARTY_REVIEW_REQUIRED` because the RAG does not independently establish their visual provenance/rights.

## Recorded mismatch and correction

Initial QA found one completeness mismatch in the lateral-movement prose: two sentences explaining the proxy-hop perspective and the apparent source of internal connections were omitted between the SOCKS-tunneling paragraph and Listing 15.

Correction commit:
`e89212781113d9810f1c535152f9bd77e97e4d4a`

The missing sentences were restored before acceptance.

## Result

`ACCEPTED`
