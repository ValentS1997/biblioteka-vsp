# Translation / editorial findings — Chapter 12

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0244:c01`–`p0299:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-12-contain-activity.md`.

## Итог проверки

- Semantic coverage: extensive.
- Listings 48–61 preserved.
- Tables 16–25 preserved.
- Figures 74–90 represented.
- Main debt: very high English-heading density, hybrid terminology and some duplicated headings.

## High-priority heading cleanup

Examples:

- `CONTAINMENT OBJECTIVES`
- `Stopping Attacker Activity`
- `Evidence Collection and Preservation`
- `CONTAINMENT STRATEGIES`
- `Passive Containment`
- `Active Containment`
- `Adaptive Containment`
- `TIMING AND COORDINATION`
- duplicate `Immediate Containment Triggers`
- `Coordinated Containment`
- `TECHNICAL IMPLEMENTATION`
- `Network-Level Containment`
- `Host-Level Containment`
- `Application-Level Containment`
- `Identity and Access Management Containment`
- duplicate `Identity and Access Management Containment`
- `Active Session Termination`
- `Residual-Access Window`
- `Refresh Token and Persistent Credential Revocation`
- `EVIDENCE COLLECTION DURING CONTAINMENT`
- `CLOUD CONTAINMENT`
- `CONTAINMENT CHALLENGES`
- `Remote Worker Environments`
- `Beyond Traditional Host Compromise`
- `CONTAINMENT VALIDATION`
- `CONTAIN ACTIVITY EXAMPLES`
- `CONTAIN: STEP-BY-STEP`

## Canonical terminology proposal

- Contain / Containment → Сдерживание
- Passive Containment → Пассивное сдерживание
- Active Containment → Активное сдерживание
- Adaptive Containment → Адаптивное сдерживание
- Evidence Collection → Сбор доказательств / артефактов
- Network Isolation → Сетевая изоляция
- Host Isolation → Изоляция узла
- Credential Revocation → Отзыв учётных данных
- Active Session Termination → Завершение активных сессий
- Refresh Token Revocation → Отзыв refresh-токенов
- Conditional Access → Условный доступ
- Residual-Access Window → Окно остаточного доступа
- Cloud Containment → Сдерживание в облачной среде
- Containment Validation → Проверка эффективности сдерживания

Acronyms/tool names (EDR, IAM, MFA, SSO, OAuth, SAML, JWT, WAF, NSG, RBAC, AWS, Azure, Okta, CrowdStrike) should remain.

## Structural findings

1. Duplicate `Immediate Containment Triggers` heading in current translation.
2. Duplicate `Identity and Access Management Containment` heading.
3. Chapter is extremely long; stronger visual hierarchy required.
4. Tables 16–25 require A4 QA.
5. Listings 48–61 require monospace/wrapping QA.
6. Risky state-changing commands should be visually distinguished from read-only verification.
7. Step-by-Step uses inconsistent heading levels in current translation; normalize hierarchy.
8. Identity containment should receive a dedicated visual sequence because order of operations is critical.

## Visual debt

Figures 74–90.

Highest priority:
- Figure 74 — Contain waypoint: CRITICAL
- Figure 75 — strategy evolution: HIGH
- Figure 77 — implementation layers: CRITICAL
- Figure 80 — IAM containment steps: CRITICAL
- Figure 81 — risk-based conditional access: HIGH
- Figure 82 — cloud responsibility summary: HIGH
- Figures 88–90 — EDR isolation/validation: HIGH

## Priority

`CRITICAL`

Reason: Chapter 12 is one of the most operationally dense chapters in the book and contains many state-changing actions. RU v2 must make terminology, action risk, verification, rollback context and visual hierarchy exceptionally clear.
