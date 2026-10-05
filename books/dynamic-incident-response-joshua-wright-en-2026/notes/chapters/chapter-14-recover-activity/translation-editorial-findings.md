# Translation / editorial findings — Chapter 14

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0405:c01`–`p0433:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-14-recover-activity.md`.

## Итог проверки

- Semantic coverage: strong.
- Listings 115–121 preserved.
- Tables 32–34 preserved.
- Figures 122–130 represented.
- Main debt: English headings and hybrid terminology.

## High-priority heading cleanup

Representative examples:

- `RECOVERY OBJECTIVES`
- `Pre-Restoration Verification`
- `System Validation Testing`
- `System Owner Acceptance`
- `Enhanced Monitoring Configuration`
- `Configuring Platform-Specific Logging and Auditing`
- `Custom Detection and Monitoring Duration`
- `Coordinated Production Restoration`
- `RECOVERY RACI: WHO ACTUALLY DOES THIS WORK?`
- `Restoration Timing`
- `Phased Restoration`
- `Containment Action Removal`
- `Metrics Capture`
- `RECOVERY STRATEGIES`
- `Phased Recovery`
- `Coordinated Recovery`
- `Scheduling Considerations`
- `Cloud Recovery Considerations`
- `Snapshot Restoration`
- `IAM Recovery Validation`
- `Infrastructure as Code`
- `RECOVERY CHALLENGES`
- `Data Loss from Clean-Backup Recovery`
- `Business Pressure for Rapid Restoration`
- `Eradication Verification Uncertainty`
- `Coordination Complexity`
- `User Communication and Expectations`
- `Post-Recovery Problem Attribution`
- `RECOVER: STEP-BY-STEP`

## Canonical terminology proposal

- Recover / Recovery → Восстановление
- Pre-Restoration Verification → Проверка перед восстановлением
- System Validation Testing → Проверка системы
- System Owner Acceptance → Приёмка владельцем системы
- Enhanced Monitoring → Усиленный мониторинг
- Production Restoration → Возврат в production / промышленную эксплуатацию
- Phased Recovery → Поэтапное восстановление
- Coordinated Recovery → Координированное восстановление
- Containment Action Removal → Снятие мер сдерживания
- Metrics Capture → Сбор метрик восстановления
- Snapshot Restoration → Восстановление из snapshot/снимка
- Clean Backup → Заведомо чистая резервная копия
- Rollback → Откат
- System Owner → Владелец системы

Tool/platform names (AWS, Azure, GCP, AD, DNS, Intune, auditpol, auditd) should remain.

## Structural findings

1. Translation hierarchy is much cleaner than Chapter 13 but still uses many English headings.
2. Validation and restoration should be visually separated: first prove readiness, then restore.
3. Phased vs coordinated recovery deserves a comparison table/callout.
4. Listings 115–121 require monospace/A4 QA.
5. Tables 32–34 require A4 QA.
6. State-changing restore commands should be visually distinguished from verification commands.
7. Monitoring-duration wording must preserve source nuance: thirty days is a common practice, not a universal mandate.
8. System-owner acceptance deserves a distinct visual checkpoint.

## Visual debt

Figures 122–130.

Priority:
- Figure 122 — Recover waypoint: CRITICAL
- Figure 123 — Pre-Restoration Verification: HIGH
- Figure 124 — Validation Testing: HIGH
- Figure 125 — Owner Acceptance: HIGH
- Figure 126 — Enhanced Monitoring: HIGH
- Figure 127 — Coordinated Restoration: CRITICAL
- Figure 128 — Containment Removal: HIGH
- Figure 130 — Recovery Timeline: HIGH

## Priority

`CRITICAL`

Reason: Chapter 14 controls the risky transition from remediation back to production. RU v2 must make readiness gates, ownership, rollback and monitoring explicit.
