---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 14
translated_chapter: "chapter-14-recover-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0405:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0433:c01"
source_pdf_page_range: "405-433"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 14

## Boundary and completeness

- PASS — Chapter 14 begins at PDF page 405 / chunk `p0405:c01`.
- PASS — Chapter 14 ends at PDF page 433 / chunk `p0433:c01`.
- PASS — PDF page 434 / chunk `p0434:c01` begins Chapter 15 (`Debrief Activity`) and is excluded.
- PASS — Figures 122–130 represented as captions/references.
- PASS — Listings 115–121 represented.
- PASS — Tables 32–34 represented.
- PASS — Recover: Step-by-Step represented with all seven steps.
- PASS — references [1]–[2] represented.

## Semantic fidelity

- PASS — recovery preserved as controlled transition from eradication to normal operations, not merely containment removal.
- PASS — competing pressures preserved: restoration urgency versus validation/recompromise risk.
- PASS — pre-restoration verification preserved, including root-cause remediation, patching, persistence removal, backup/rebuild integrity, security-control status, and final IOC scan.
- PASS — system validation preserved across functional, security-control, and interconnectivity testing.
- PASS — system-owner acceptance and formal sign-off preserved.
- PASS — enhanced monitoring preserved, including Windows audit policy, Linux auditd, platform log sources, custom detections, monitoring duration, and log-volume/capacity concerns.
- PASS — recovery RACI preserved: IT/system owners/infrastructure execute restoration while IR provides incident-specific validation and consultation.
- PASS — dependency-aware restoration preserved, including AD/DNS/network infrastructure priority.
- PASS — AWS DNS outage case preserved as dependency/recovery-order example.
- PASS — containment-action removal preserved as incremental and selective, with possibility of retaining controls permanently.
- PASS — recovery metrics and handoff to Debrief preserved.
- PASS — phased versus coordinated recovery trade-offs preserved.
- PASS — Maersk/NotPetya coordinated-recovery case preserved, including surviving Ghana DC backup and large-scale parallel restoration.
- PASS — cloud recovery preserved, including snapshot-date validation, IAM review, enhanced logging, and IaC integrity.
- PASS — recovery challenges preserved: clean-backup data loss, business pressure, eradication uncertainty, coordination complexity, user communication, and post-recovery problem attribution.
- PASS — Lakewood Health Systems phased AD recovery case preserved, including backup selection, DC verification, enhanced auditing, replication validation, gold-image workstation rebuilds, service-account dependency issue, and lessons learned.
- PASS — all seven Recover Step-by-Step actions preserved.

## Technical integrity

- PASS — Windows auditpol commands preserved.
- PASS — Linux auditd rules preserved.
- PASS — event IDs in Table 33 preserved.
- PASS — AWS/Azure/GCP snapshot commands preserved.
- PASS — AWS snapshot-listing command preserved.
- PASS — Windows Backup, Get-Service, dcdiag, auditpol, and repadmin commands preserved in Lakewood example.
- PASS — identifiers preserved where relevant: UAT, EDR, SIEM, WEF, AMSI, Sysmon, IAM, MFA, IaC, AD, DNS, PDC, NTDS, DFSR, RADIUS, MTTR.
- PASS — source timestamps, backup dates, and recovery metrics retained where represented.

## Glossary consistency

- PASS — `pre-restoration verification` locked as `предварительная проверка перед восстановлением`.
- PASS — `system owner acceptance` locked as `приёмка владельцем системы`.
- PASS — `enhanced monitoring` locked as `усиленный мониторинг`.
- PASS — `phased recovery` locked as `поэтапное восстановление`.
- PASS — `coordinated recovery` locked as `координированное восстановление`.
- PASS — `containment action removal` locked as `снятие мер сдерживания`.

Glossary commit:
`fde5a5cc8128029d86ea6ea921ebb9a5db13e394`

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 122–130 are not reproduced; captions/cross-references retained.
- PASS — external case-study sources remain cited without reproducing protected third-party prose.

## Result

`ACCEPTED`
