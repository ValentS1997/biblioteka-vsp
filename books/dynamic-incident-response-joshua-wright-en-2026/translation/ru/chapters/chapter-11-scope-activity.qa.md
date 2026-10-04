---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 11
translated_chapter: "chapter-11-scope-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0224:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0243:c01"
source_pdf_page_range: "224-243"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 11

## Boundary and completeness

- PASS — Chapter 11 begins at PDF page 224 / chunk `p0224:c01`.
- PASS — Chapter 11 ends at PDF page 243 / chunk `p0243:c01`.
- PASS — PDF page 244 / chunk `p0244:c01` begins Chapter 12 (`Contain Activity`) and is excluded.
- PASS — Figures 69–73 represented as captions/references.
- PASS — Listings 41–47 represented.
- PASS — Tables 14–15 represented.
- PASS — Scope: Step-by-Step represented with all seven steps.
- PASS — reference [1] represented.

## Semantic fidelity

- PASS — scope preserved as the DAIR activity bridging verification and containment by determining compromise extent.
- PASS — scoping purpose preserved: move from "we have an incident" to understanding breadth/depth.
- PASS — technical IOC categories preserved:
  - file;
  - network;
  - process/service;
  - registry/configuration;
  - account.
- PASS — behavioral IOC categories preserved:
  - temporal;
  - data movement;
  - lateral movement.
- PASS — enterprise-wide hunting and progressive scoping preserved as distinct complementary methodologies.
- PASS — progressive scoping phases preserved: critical asset prioritization, lateral expansion, environmental sweep.
- PASS — scope ownership of the canonical attack-progression timeline preserved.
- PASS — patient-zero, lateral-movement, persistence and exfiltration timeline analysis preserved.
- PASS — visibility-gap treatment preserved for BYOD, shadow IT, legacy, IoT, ICS and cloud-native resources.
- PASS — Siemens S7-1200 example preserved, including limitations of centralized logging and importance of network flow.
- PASS — flow-sampling limitation (1:1000 or higher) preserved.
- PASS — anti-forensic techniques preserved:
  - log deletion/modification;
  - replay/flooding;
  - timestomping;
  - encryption/obfuscation;
  - living off the land.
- PASS — cloud/hybrid scale and ephemeral-resource constraints preserved.
- PASS — integration of scoping with containment, eradication and recovery preserved.
- PASS — LinkedIn attachment case preserved with file/hash/type, PDF structural analysis and URI extraction.
- PASS — Azure cloud-exfiltration case preserved, including 47 blobs, ~8.2 GiB, compromised service principal, external IP, attacker-created VM, five-day activity window and expanded resource-group scope.
- PASS — all seven Scope Step-by-Step actions preserved.

## Technical integrity

- PASS — Listing 41 CSV timeline data preserved.
- PASS — Listings 42–44 command output for file/hash/PDF/URI analysis preserved.
- PASS — Listings 45–47 Azure CLI queries/output preserved.
- PASS — Table 14 AWS/Azure/GCP audit-log quick-reference commands preserved.
- PASS — Table 15 Azure scoping commands preserved.
- PASS — technical identifiers preserved: IOC, NDR, C2, EDR, SIEM, BYOD, ICS, IoT, OT, PLC, Modbus, DNP3, S7comm, WMI, $MFT, AWS, Azure, GCP, Entra ID.
- PASS — source hashes, object IDs, IP addresses, resource-group names, timestamps and file names retained where relevant.

## Glossary consistency

- PASS — `progressive scoping` locked as `поэтапное определение масштаба`.
- PASS — `enterprise-wide hunting` locked as `поиск IOC по всей организации`.
- PASS — `timeline reconstruction` locked as `реконструкция временной шкалы атаки`.
- PASS — `patient zero` locked as `нулевая система`.
- PASS — `anti-forensic techniques` locked as `антифорензик-техники`.

Glossary commit:
`9c4bbe4126bdfaed016870bede8414e524f7b798`

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 69–73 are not reproduced.
- PASS — Figure 71 remains explicitly identified as Siemens third-party material.
- PASS — technical commands and source-authored case-study listings are preserved under the book translation workflow.
- PASS — no external third-party prose passage is silently expanded beyond canonical author framing.

## Result

`ACCEPTED`
