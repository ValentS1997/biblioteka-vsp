# Translation / editorial findings — Chapter 20

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0637:c01`–`p0648:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-20-integrating-dair-with-nist-csf-2-0.md`.

## Итог проверки

- Semantic coverage: strong.
- Figure 200 represented.
- Tables 60–64 preserved.
- No command listings.
- Main debt: mixed governance/compliance terminology and English-heavy headings.

## High-priority heading cleanup

Representative examples:

- `Что требует Compliance`
- `DAIR как Implementation CSF 2.0`
- `Mapping DAIR Activities to CSF Functions`
- `Value of Iterative Response for Compliance`
- `Decision Maker Integration и Govern Function`
- `Meeting Compliance Through DAIR Activities`
- `Compliance Artifacts from DAIR Activities`
- `Demonstrating Control Effectiveness`
- `Satisfying Audit Requirements`
- `Incident Tracking Platform Configuration`
- `Ticketing and Case Management`
- `Communication Templates`

## Canonical terminology proposal

- Compliance → соответствие требованиям
- Control Effectiveness → эффективность контроля
- Compliance Artifact → свидетельство соответствия / артефакт аудита
- Assessor → оценщик / аудитор, context-dependent
- Decision Maker → лицо, принимающее решения
- Risk Management Strategy → стратегия управления рисками
- Roles, Responsibilities, and Authorities → роли, обязанности и полномочия
- Supply Chain Risk Management → управление рисками цепочки поставок
- Incident Tracking Platform → платформа учёта инцидентов
- Case Management → управление кейсами/инцидентами
- Continuous Improvement → непрерывное улучшение
- Audit Requirement → требование аудита
- Demonstrated Effectiveness → подтверждённая эффективность

NIST, CSF, DAIR, GV/ID/PR/DE/RS/RC should remain.

## Structural findings

1. Figure 200 should be restored because it is the chapter’s core mapping visual.
2. Tables 60–64 deserve careful A4 QA; they are the chapter’s main reference material.
3. DAIR→CSF mapping should appear early as a concise visual.
4. Govern category mapping deserves a separate compact matrix.
5. Iteration-as-evidence is a core idea and should get a dedicated callout.
6. Distinguish policy/procedure/playbook terminology consistently.
7. Ticketing-platform recommendations should be rendered as a configuration checklist.
8. Executive vs technical communication templates should be visually separated.
9. Preserve source wording around compliance; do not silently elevate guidance into mandatory legal requirements.

## Visual debt

- Figure 200 — DAIR Model Mapped to NIST CSF 2.0 Functions: CRITICAL

Tables:
- Table 60 — HIGH
- Table 61 — CRITICAL
- Table 62 — HIGH
- Table 63 — HIGH
- Table 64 — HIGH

## Priority

`HIGH`

Reason: Chapter 20 is primarily a governance/mapping chapter rather than a high-risk operational chapter, but terminology and table clarity are essential for audit use.
