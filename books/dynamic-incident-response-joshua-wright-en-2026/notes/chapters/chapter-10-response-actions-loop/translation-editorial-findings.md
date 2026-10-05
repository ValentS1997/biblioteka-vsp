# Translation / editorial findings — Chapter 10

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0213:c01`–`p0223:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-10-response-actions-loop.md`.

## Итог проверки

- Semantic coverage: strong.
- Figure placeholders 66–68 present.
- References [1]–[2] preserved.
- Main debt: English headings and hybrid process terminology.

## High-priority heading cleanup

Current headings requiring normalization:

- `ON THE ITERATIVE NATURE OF INCIDENT RESPONSE`
- `THE FOUR RESPONSE ACTIONS LOOP ACTIVITIES`
- `Scope: Understanding Breadth`
- `Contain: Stopping the Bleeding`
- `Eradicate: Removing the Threat`
- `Recover: Restoring Operations`
- `ITERATION TRIGGERS`
- `New Indicators of Compromise`
- `Scope Expansion`
- `Incomplete Eradication`
- `Evidence Analysis Revelations`
- `Changing Business Priorities and Obligations`
- `Stakeholder Communication`
- `DOCUMENTATION AND COMMUNICATION`
- `Decision Documentation`
- `Impact Assessment`
- `KNOWING WHEN TO STOP`
- `PRACTICAL CONSIDERATIONS`
- `Resource Management`
- `Documentation Burden`
- `Stakeholder Patience`
- `RESPONSE ACTIONS LOOP: STEP-BY-STEP`

## Terminology normalization

Recommended canonical RU v2 terms:

- Response Actions Loop → Цикл действий реагирования
- Scope → Определение масштаба
- Contain → Сдерживание
- Eradicate → Искоренение
- Recover → Восстановление
- iteration → итерация
- iteration trigger → триггер новой итерации
- stakeholder communication → коммуникация с заинтересованными сторонами
- decision documentation → документирование решений
- impact assessment → оценка воздействия
- residual risk → остаточный риск
- loop exit → завершение цикла / выход из цикла

## Structural findings

1. This chapter is highly process-oriented and should visually emphasize the loop rather than present it as long linear prose.
2. Exit criteria deserve a distinct callout/table in v2.
3. Iteration triggers should be rendered as a separate checklist.
4. Figures 67/68 are pedagogically important because they compare linear vs iterative processing.
5. Step-by-Step should be visually separated from the explanatory body.

## Visual debt

Figures 66–68:

- Figure 66 — Response Actions Loop Activities
- Figure 67 — Linear Response Threat Processing
- Figure 68 — Iterative Response Threat Processing

Priority:
- Figure 66 — CRITICAL
- Figures 67/68 — HIGH

## Priority

`CRITICAL`

Reason: Chapter 10 is the core operational cycle of DAIR. If loop semantics are not visually and terminologically clear, later chapters Scope/Contain/Eradicate/Recover lose context.
