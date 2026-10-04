---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 19
translated_chapter: "chapter-19-incident-response-for-operational-technology.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0613:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0636:c01"
source_pdf_page_range: "613-636"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 19

## Boundary and completeness

- PASS — Chapter 19 begins at PDF page 613 / chunk `p0613:c01`.
- PASS — Chapter 19 ends at PDF page 636 / chunk `p0636:c01`.
- PASS — PDF page 637 / chunk `p0637:c01` begins Chapter 20 (`Integrating DAIR with NIST CSF 2.0`) and is excluded.
- PASS — Figures 191–199 represented.
- PASS — Tables 57–59 represented.
- PASS — references [1]–[9] preserved.
- PASS — source sections preserved: IT/OT differences, OT asset types, benefits of DAIR, common OT incidents, Verify/Triage, Scope, Containment, Eradicate, Recover, Debrief, Five ICS Cybersecurity Critical Controls.

## Semantic fidelity

- PASS — OT safety and physical-process impact preserved as primary constraints on response actions.
- PASS — engineering context preserved as mandatory input for verification, triage, containment, eradication, and recovery.
- PASS — distinction between OT and enterprise incident impact preserved.
- PASS — long asset lifecycles, vendor dependencies, maintenance windows, and operational constraints preserved.
- PASS — Purdue model and Levels 0–5 / 3.5 IDMZ framing preserved.
- PASS — industrial protocols preserved: Modbus, DNP3, EtherNet/IP, PROFINET, ICCP.
- PASS — common OT assets preserved: HMI, engineering workstation, historian, PLC, RTU, protection relay, VFD, SIS.
- PASS — embedded-device limitations and reduced suitability of endpoint-centric investigation preserved.
- PASS — refinery containment case preserved as evidence that aggressive IT containment can cause greater operational disruption than malware.
- PASS — "fighting through the attack" concept and hydroelectric-facility containment case preserved.
- PASS — HILF framing preserved.
- PASS — Oldsmar operator-visibility case preserved, including valid-credential/TeamViewer access and process-aware detection.
- PASS — living-off-the-land OT activity and legitimate-tool abuse preserved.
- PASS — Locard’s Exchange Principle preserved as the forensic framing for OT evidence.
- PASS — controller logic, project files, relay configurations, historian data, HMI actions, remote-access systems, and packet captures preserved as OT evidence sources.
- PASS — controller integrity validation preserved as a core Verify/Triage activity.
- PASS — OT scoping preserved around control zones, engineering systems, trust boundaries, protocol-level activity, and known-good logic validation.
- PASS — containment preserves operator visibility, process stability, and safety-critical functions.
- PASS — island mode preserved as a pre-planned cyber-safe operating state, not an ad-hoc isolation shortcut.
- PASS — OT-specific persistence and eradication preserved across credentials, engineering access, modified controller logic, remote access, and IT/OT trust relationships.
- PASS — recovery preserved across trusted system images, vendor software, project files, controller logic reload, firmware/checksum validation, I/O mapping, physical walkthrough, and controlled startup sequence.
- PASS — OT-specific debrief questions preserved across island mode, engineering exposure, controller integrity, protocol visibility, operational impact, backups, architecture, and containment risk.
- PASS — Five ICS Cybersecurity Critical Controls preserved in source order and meaning.

## Technical integrity

- PASS — identifiers preserved: OT, ICS, SCADA, DCS, PLC, RTU, HMI, VFD, SIS, EDR, PERA, IDMZ.
- PASS — standards/framework identifiers preserved: ISA-95, ISA/IEC 62443, IEC 61511.
- PASS — industrial protocol names preserved without normalization or substitution.
- PASS — source numbers and Oldsmar setpoint values preserved: 100 ppm → 11,100 ppm; 111×; 15,000 residents.
- PASS — Level 3.5 IDMZ containment example preserved.
- PASS — no unsupported commands or remediation procedures invented.
- PASS — references [1]–[9] retained without adding unsupported source metadata.

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — third-party figures and externally sourced visuals are represented with fail-closed handling.
- PASS — canonical English RAG remains source of truth.

## Glossary consistency

- PASS — `Operational Technology` → `операционные технологии (OT)`.
- PASS — `Industrial Control Systems` → `промышленные системы управления (ICS)`.
- PASS — `Purdue model` → `модель Purdue`.
- PASS — `island mode` → `островной режим (island mode)`.
- PASS — `fighting through the attack` → `поддержание управляемой работы во время атаки`.
- PASS — `operator visibility` → `видимость процесса для оператора`.
- PASS — `controller integrity` → `целостность контроллера`.
- PASS — `protocol-aware monitoring` → `мониторинг с учетом промышленных протоколов`.
- PASS — `Safety Instrumented System` → `система противоаварийной защиты (SIS)`.
- PASS — `defensible control system network architecture` → `защищаемая архитектура сети системы управления`.

Glossary commit:
`a681a9b5f2245854d4765817f4d067891e17f186`

## Result

`ACCEPTED`
