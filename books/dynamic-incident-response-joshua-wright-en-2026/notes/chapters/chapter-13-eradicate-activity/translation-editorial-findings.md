# Translation / editorial findings — Chapter 13

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0300:c01`–`p0404:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-13-eradicate-activity.md`.

## Итог проверки

- Semantic coverage: extensive.
- Listings 62–114 preserved.
- Tables 26–31 preserved.
- Figures 91–121 represented.
- Main debt: extremely high English-heading density, inconsistent hierarchy, hybrid terminology and very dense technical layout.

## High-priority heading cleanup

Representative examples:

- `ERADICATE OBJECTIVES`
- `Preventing Incident Recurrence Through Investigation`
- `Investigation During Eradication`
- `Short-Form Investigation`
- `Long-Form Investigation for Comprehensive Understanding`
- `Pursuing Root Cause Analysis`
- `Four P's Framework`
- `Fishbone Diagram Mapping`
- `INVESTIGATION TECHNIQUES FOR ERADICATION`
- `Log Investigation`
- `SIEM for Log Investigation`
- `Live Investigation`
- `Endpoint Telemetry Investigation Tools`
- `Memory Investigation`
- `Network Investigation`
- `Malware Investigation`
- `Business Email Compromise Investigation`
- `Identity and Access Investigation`
- `Insider Threat Investigation`
- `Supplier and Supply Chain Investigation`
- `Cloud Investigation`
- `ERADICATE ATTACKER ACCESS`
- `Removing Persistence Mechanisms`
- `Account and Identity Remediation`
- `Krbtgt Account Reset`
- `Hybrid and Entra ID Remediation`
- `Targeted Removal vs. System Rebuild`
- `Vulnerability Remediation`
- `ERADICATION CHALLENGES`
- `Living Off the Land`
- `Fileless Malware`
- `ERADICATE ACTIVITY EXAMPLES`
- `ERADICATE: STEP-BY-STEP`

## Canonical terminology proposal

- Eradicate / Eradication → Искоренение / устранение присутствия атакующего
- Short-Form Investigation → краткое оперативное расследование
- Long-Form Investigation → углублённое расследование
- Root Cause Analysis → анализ корневой причины (RCA)
- Persistence → закрепление / механизмы закрепления
- Live Investigation → анализ работающей системы
- Endpoint Telemetry → телеметрия конечных устройств
- Memory Investigation → анализ памяти
- Network Investigation → сетевое расследование
- Malware Investigation → анализ вредоносного ПО
- Identity Remediation → восстановление/очистка идентификационной инфраструктуры
- Targeted Removal → точечное удаление
- System Rebuild → пересборка системы
- Vulnerability Remediation → устранение уязвимости
- Compensating Controls → компенсирующие меры
- Living off the Land → использование штатных средств системы
- Fileless Malware → бесфайловое вредоносное ПО

Acronyms/tool names (SIEM, Sigma, EDR, VPC, OAuth, PAT, IAM, AD, Entra ID, KRBTGT, Nuclei, Volatility, MemProcFS) should remain.

## Structural findings

1. Heading hierarchy is inconsistent: many sections are rendered as H1 even though semantically they are subsections.
2. Chapter 13 is very long and needs stronger navigation/visual sectioning in v2.
3. Listings 62–114 require extensive A4 monospace/wrapping QA.
4. State-changing identity commands must be visually separated from investigative/read-only commands.
5. High-risk actions such as KRBTGT/DC/trust resets need explicit warning + verification + sequencing callouts.
6. Root Cause Analysis deserves a dedicated visual spread.
7. Investigation techniques should be grouped by evidence domain rather than presented as visually similar long sections.
8. The Step-by-Step section should become a concise operational appendix/summary rather than another dense prose block.

## Visual debt

Figures 91–121.

Highest priority:
- Figure 91 — Eradicate waypoint: CRITICAL
- Figure 92 — Short-form vs Long-form: CRITICAL
- Figures 94–96 — RCA/Fishbone: HIGH
- Figure 98 — Velociraptor hunt: HIGH
- Figure 108 — Eradicate attacker access process: CRITICAL
- Figure 110 — Account recreation approach: HIGH
- Figures 120–121 — coordinated credential reset: HIGH

## Priority

`CRITICAL`

Reason: Chapter 13 is one of the largest and most operationally consequential chapters. It combines investigation, identity remediation, persistence removal, vulnerability remediation and high-risk directory operations. RU v2 must make action risk and sequencing unmistakable.
