---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 13
translated_chapter: "chapter-13-eradicate-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0300:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0404:c01"
source_pdf_page_range: "300-404"
qa_status: "QA_BLOCKED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 13

## Blocking mismatch

- FAIL — canonical RAG bibliography is incomplete.
- `p0403:c01` contains references [1]–[25].
- `p0404:c01` contains references [37]–[38].
- References [26]–[36] are absent from the canonical RAG objects and repository code search.
- Translation preserves each missing entry as `RAG_MISS`; bibliographic metadata was not reconstructed from model memory or external web sources.
- This violates the QA completeness requirement: `footnotes/references preserved`.

## Boundary and structural checks

- PASS — Chapter 13 begins at PDF page 300 / chunk `p0300:c01`.
- PASS — Chapter 13 ends at PDF page 404 / chunk `p0404:c01`.
- PASS — PDF page 405 / chunk `p0405:c01` begins Chapter 14 (`Recover Activity`) and is excluded.
- PASS — Figures 91–121 represented as captions/references.
- PASS — Listings 62–114 represented or explicitly fail-closed where executable malicious payload reproduction is inappropriate.
- PASS — Tables 26–31 represented.
- PASS — Eradicate Step-by-Step represented with all nine steps.
- PASS — Reference numbers [1]–[38] are represented structurally; [26]–[36] are explicit `RAG_MISS` markers.

## Semantic fidelity

- PASS — short-form vs long-form investigation model preserved.
- PASS — root cause analysis, four P's, fishbone, and Five Whys preserved.
- PASS — log/SIEM, live/differential, endpoint telemetry, memory, network, malware, BEC, insider, supply-chain, cloud investigation tracks preserved.
- PASS — persistence removal across Windows, Linux, web applications, cloud, IAM, and container images preserved.
- PASS — local, AD, KRBTGT, DC machine account, trust, delegation, hybrid/Entra, OAuth/PAT/session remediation preserved.
- PASS — targeted removal vs rebuild decision model preserved.
- PASS — exploited-vulnerability remediation, patching, compensating controls, broader vulnerability assessment, and hardening preserved.
- PASS — living-off-the-land, fileless malware, RMM, and cross-trust eradication challenges preserved.
- PASS — memory-forensics and coordinated credential-reset examples preserved.
- PASS — all nine Eradicate Step-by-Step actions preserved.

## Technical integrity

- PASS — commands/configuration/identifiers preserved except explicit fail-closed malicious executable payloads.
- PASS — CVE-2025-64446 and technical product/framework identifiers preserved.
- PASS — Listings 62–114 numbering retained.
- PASS — source example IPs, paths, IDs, account names, timestamps, and cloud identifiers retained where represented in canonical RAG.

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 91–121 not reproduced.
- PASS — third-party quotations/screenshots remain fail-closed.
- PASS — executable web-shell and fileless-malware payload material is not duplicated verbatim in the reader-facing translation; canonical English RAG remains source of truth.

## Required remediation before acceptance

1. Repair canonical English RAG coverage for the missing bibliography entries [26]–[36] from the canonical source.
2. Re-run chapter translation QA against the repaired RAG boundary.
3. Replace the eleven `RAG_MISS` bibliography markers with canonical bibliographic entries.
4. Only then change `translation_status` and `qa_status` to `ACCEPTED`.
5. Do not delete Chapter 13 work segments or merge the translation branch while QA remains blocked.

## Result

`QA_BLOCKED`
