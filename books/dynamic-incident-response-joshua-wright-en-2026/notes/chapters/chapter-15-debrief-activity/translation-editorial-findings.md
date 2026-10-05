# Translation / editorial findings — Chapter 15

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0434:c01`–`p0470:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-15-debrief-activity.md`.

## Итог проверки

- Semantic coverage: extensive and strong.
- Tables 35–42 preserved.
- Figures 131–141 represented.
- Main debt: large number of English headings and hybrid reporting/governance terminology.

## High-priority heading cleanup

Representative examples:

- `DEBRIEF OBJECTIVES`
- `Incident Closure`
- `Organizational Learning`
- `DEBRIEF STRATEGIES`
- `Transitioning to Debrief`
- `Managing Temporary Assets`
- `Forensic Evidence Retention`
- `Consolidating Incident Documentation`
- `DOCUMENTATION AND VALUE PROPOSITION`
- `Lightweight Documentation`
- `Formal Documentation`
- `Capturing Incident Metrics`
- `Conducting the After-Action Review`
- `Driving Organizational Improvement`
- `Developing the Incident Report`
- `Two-Report Approach`
- `Incident Summary Report`
- `EXECUTIVE REPORTING LEVERS`
- `Technical Incident Response Report`
- `Presenting Findings and Recommendations`
- `Follow-Up and Accountability`
- `DEBRIEF CHALLENGES`
- `DEBRIEF ACTIVITY EXAMPLES`
- `Sustaining Momentum`
- `DEBRIEF: STEP-BY-STEP`

## Canonical terminology proposal

- Debrief → Разбор инцидента
- Incident Closure → Формальное закрытие инцидента
- Organizational Learning → Организационное обучение
- After-Action Review (AAR) → Разбор после инцидента (AAR)
- Incident Report → Отчёт об инциденте
- Incident Summary Report → Краткий отчёт для руководства
- Technical Incident Response Report → Технический отчёт по реагированию
- Temporary Assets → Временные активы/ресурсы
- Evidence Retention → Хранение доказательств
- Documentation Consolidation → Консолидация документации
- Recommendation Roadmap → План реализации рекомендаций
- Follow-Up → Последующий контроль
- Accountability → Ответственность за выполнение

Acronyms and proper names (AAR, MTTD, MTTR, EDR, MFA, CIO, CISO, ISAC, Okta) should remain.

## Structural findings

1. Heading hierarchy is mostly coherent, but visual density is high.
2. Closure, AAR, Reporting and Improvement should be four visually distinct blocks.
3. Tables 35–42 require A4 QA.
4. Figures 136/138/139 are central to report-format understanding and should be restored where rights permit.
5. Recommendation tracking should be visually emphasized as the real completion criterion.
6. The two-report approach deserves a comparison table in v2.
7. Management-facing "lever" framework deserves a sidebar/callout.
8. Legal/regulatory sections must preserve source framing and not be silently updated.

## Visual debt

Figures 131–141.

Highest priority:
- Figure 131 — Debrief waypoint: CRITICAL
- Figure 132 — transition considerations: HIGH
- Figure 134 — documentation detail flowchart: HIGH
- Figure 135 — visual incident timeline: HIGH
- Figures 136/138/139 — report structure: HIGH
- Figure 140 — incident presentation: HIGH
- Figure 141 — ransomware timeline: HIGH

## Priority

`HIGH`

Reason: Chapter 15 is less technically risky than Chapters 12–14, but it controls whether incident response produces durable organizational improvement.
