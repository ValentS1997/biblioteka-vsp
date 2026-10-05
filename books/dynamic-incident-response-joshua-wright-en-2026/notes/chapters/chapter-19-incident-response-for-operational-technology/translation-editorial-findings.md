# Translation / editorial findings — Chapter 19

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0613:c01`–`p0636:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-19-incident-response-for-operational-technology.md`.

## Итог проверки

- Semantic coverage: strong.
- Tables 57–59 preserved.
- Figures 191–199 represented.
- No command listings.
- Main debt: extremely high mixed-language density in headings and OT terminology.

## High-priority heading cleanup

Representative examples:

- `Incident Response в OT Environments`
- `Safety как основная миссия OT Security`
- `Skill Sets для OT Defenders и Responders`
- `Vendor Support и Industrial System Lifecycle Constraints`
- `Industrial System Design и Network Architecture`
- `Security Control Design и Operational Risk Tolerance`
- `WHY STANDARD IT CONTAINMENT CAN BE DANGEROUS IN OT`
- `КОГДА IT CONTAINMENT САМ СОЗДАЕТ OT INCIDENT`
- `Common OT Assets`
- `Non-Traditional Operating System OT Assets`
- `Traditional Operating System-Based OT Assets`
- `Преимущества DAIR для OT Incident Response`
- `FIGHTING THROUGH THE ATTACK`
- `VERIFY AND TRIAGE ДЛЯ OT`
- `Living-off-the-Land в Modern OT Attacks`
- `Traditional vs New Forensic Areas`
- `Common OT Incident Data Sources`
- `SCOPE`
- `Engineering Validation`
- `CONTAINMENT`
- `Island Mode`
- `ERADICATE`
- `RECOVER`
- `DEBRIEF`
- `OT-Specific Debrief Questions`
- `THE FIVE ICS CYBERSECURITY CRITICAL CONTROLS`

## Canonical terminology proposal

- Operational Technology (OT) → операционные технологии (OT)
- Industrial Control Systems (ICS) → промышленные системы управления (ICS)
- Incident Response → реагирование на инциденты
- Safety → безопасность физического процесса / безопасность персонала, context-dependent
- Operator Visibility → операторская наблюдаемость / видимость процесса
- Engineering Workstation → инженерная рабочая станция
- Historian → historian / архив технологических данных
- Control Layer → уровень управления
- Industrial Protocol → промышленный протокол
- Island Mode → автономный режим (island mode)
- Manual Operations → ручное управление
- Controller Logic → логика контроллера
- Known-Good Logic Baseline → эталонная логика контроллера
- Protocol-Level Visibility → видимость на уровне промышленных протоколов
- Defensible Control System Network Architecture → защищаемая архитектура сети управления
- Secure Remote Access → защищённый удалённый доступ
- Risk-Based Vulnerability Management → управление уязвимостями на основе риска
- Fighting Through the Attack → продолжение безопасной работы во время атаки

Acronyms/proper terms (PLC, RTU, DCS, HMI, SCADA, SIS, VFD, PPE, Purdue, Modbus, DNP3, EtherNet/IP, PROFINET, ICCP) should remain.

## Structural findings

1. Safety and engineering authority should be front-of-chapter callouts.
2. The HMI containment case deserves a full-width warning/example block.
3. IT vs OT response differences should become a comparison table.
4. Asset taxonomy should be grouped by embedded vs traditional OS.
5. Purdue model needs restored visual context because architecture is central to scoping.
6. Verify/Triage → Scope → Contain → Eradicate → Recover → Debrief mapping should be visually explicit.
7. Island mode should have a dedicated procedure/decision sidebar.
8. OT evidence sources deserve a dedicated matrix.
9. Recovery acceptance must emphasize process integrity, not only system functionality.
10. Five ICS Critical Controls should be a closing visual summary.
11. Tables 57–59 require A4 QA.
12. Safety-critical recommendations must remain source-level; v2 must not invent site/vendor procedures.

## Visual debt

Figures 191–199.

Priority:
- Figure 191 — Purdue Model: CRITICAL
- Figure 192 — interlocking OT constraints: HIGH
- Figures 193–196 — asset examples: MEDIUM
- Figure 197 — water treatment context: HIGH
- Figure 198 — controller logic recovery: CRITICAL
- Figure 199 — Five ICS Critical Controls: CRITICAL

## Priority

`CRITICAL`

Reason: Chapter 19 is safety-sensitive and depends on precise distinctions between cyber response, engineering authority and physical-process consequences.
