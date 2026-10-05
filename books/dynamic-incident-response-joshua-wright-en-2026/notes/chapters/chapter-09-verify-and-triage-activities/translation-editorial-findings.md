# Translation / editorial findings — Chapter 9

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0190:c01`–`p0212:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-09-verify-and-triage-activities.md`.

## Итог проверки

- Semantic coverage: good.
- Listings 34–40 preserved.
- Figures 57–65 represented.
- Main debt: English-heavy headings and hybrid professional terminology.

## High-priority heading cleanup

Current headings requiring normalization:

- `VERIFICATION AS A GATING FUNCTION`
- `VERIFICATION RESPONSE ACTIONS`
- `DOCUMENTATION`
- `THE NEED FOR PRISTINE DOCUMENTATION`
- `INITIAL RISK ASSESSMENT`
- `VERIFICATION AND CYBER THREAT INTELLIGENCE`
- `EOI Validation and Enrichment`
- `Informing Initial Risk Classification`
- `SAME DOMAIN, TWO RISK ASSESSMENTS`
- `Pivoting to Related Indicators`
- `VERIFICATION ACTIVITY EXAMPLES`
- `The Unresponsive WordPress Site`
- `The Unpaid Toll`
- `The Simple, Secure Storage Bucket`
- `A TEMPERAMENTAL SERVER`
- `TRIAGE ACTIVITY`
- `Presenting the Incident`
- `TRIAGE EXAMPLE: THE THIRD-PARTY VENDOR BREACH`
- `VERIFY AND TRIAGE: STEP-BY-STEP`

## Terminology normalization

Recommended v2 policy:

- Verify → Проверка / Подтверждение
- Triage → Триаж / Приоритизация
- gating function → функция допуска / контрольная точка
- Decision Makers → лица, принимающие решения
- Initial Risk Assessment → начальная оценка риска
- CTI → киберразведка об угрозах (CTI), first use
- enrichment → обогащение контекстом
- pivoting → переход к связанным индикаторам
- false positive → ложное срабатывание
- incident tracking platform → платформа учёта инцидентов
- pristine documentation → целостная/незагрязнённая документация
- resource allocation → распределение ресурсов
- third-party vendor breach → инцидент у стороннего поставщика

Tool names/acronyms (AWS, S3, CTI, VERIS, FAIR, NIST, CASB) should remain.

## Structural findings

1. Chapter has a strong logical structure; v2 should emphasize it visually as a gate:
   `Detect → Verify → Continue/Stop/Defer → Triage`.
2. The distinction IOA vs EOI in the "Unpaid Toll" example is pedagogically important and should receive a highlighted callout.
3. The "Temperamental Server" section deserves a sidebar on proving a negative.
4. Listings 35–40 require monospace/A4 QA.
5. Decision-maker responsibility should remain clearly separated from analyst responsibility.

## Visual debt

Figures 57–65.

Highest priority:
- Figure 57 — Verify/Triage waypoint
- Figure 58 — Verification Process
- Figure 63 — CTI related-indicator pivot
- Figure 64/65 — phishing example

## Priority

`HIGH`

Chapter 9 establishes the gate between detection and active response, so terminology and flow must be exceptionally clear in RU v2.
