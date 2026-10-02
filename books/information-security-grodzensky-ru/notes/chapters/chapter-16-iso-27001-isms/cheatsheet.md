# Шпаргалка: ISO 27001 и СУИБ

## PDCA

| Этап | Что происходит по главе |
|---|---|
| Plan | Контекст, scope, leadership, риски, цели, ресурсы |
| Do | Внедрение и эксплуатация процессов/мер |
| Check | Метрики, внутренний аудит, management review |
| Act | Корректирующие действия и улучшение |

## СУИБ

В источнике СУИБ — часть общей системы менеджмента организации, основанная на оценке бизнес-рисков и цикле создания, внедрения, поддержки и улучшения ИБ.

## Scope

Перед внедрением:
1. определить внешние/внутренние факторы;
2. определить заинтересованные стороны;
3. собрать их требования;
4. выбрать критичные бизнес-процессы;
5. зафиксировать границы СУИБ.

## Leadership

Руководство:
- утверждает Политику ИБ;
- выделяет ресурсы;
- назначает роли/полномочия;
- может назначить куратора или создать Комитет по ИБ;
- участвует в review.

## Risk layer

```text
risk assessment
→ treatment plan
→ applicable controls
→ residual risk
→ Statement of Applicability
```

## Документы

Иерархия главы:

```text
Policy
↓
ISMS manual
↓
procedures / regulations / standards
↓
instructions / awareness materials
↓
records / acts / protocols
```

## Check

Три основных процесса:
1. monitoring/measurement;
2. internal audit;
3. management review.

## Метрики

Метрика должна быть:
- измеримой;
- значимой;
- управляемой владельцем процесса;
- иметь target;
- иметь threshold.

## Correction vs corrective action

- correction — устранить единичное проявление;
- corrective action — устранить root cause, чтобы проблема не повторилась.

## GAP-analysis

```text
AS-IS
vs
TO-BE / ISO requirements
→ gaps
→ project plan
```

## 8D

```text
D0 Plan
D1 Team
D2 Describe problem
D3 Interim containment
D4 Root cause
D5 Permanent correction
D6 Corrective action
D7 Prevent recurrence
D8 Recognize team
```

## Ishikawa

Используется для систематизации причин.

Источник предлагает 5M:
- material;
- machine;
- man;
- method;
- measuring.

Дополняется «Пять почему?».

## Read-only checks

1. Scope СУИБ документирован?
2. Stakeholders и требования определены?
3. Есть owner СУИБ?
4. Владельцы процессов назначены?
5. Политика утверждена и распространена?
6. Цели измеримы?
7. Risk process работает?
8. Statement of Applicability создан?
9. Метрики имеют target/threshold?
10. Internal audit независим?
11. Management review проводится?
12. Несоответствия ведут к root-cause actions?
13. GAP-analysis актуален?
14. Documentation/records управляются?

## Next action

```text
context/scope
→ leadership
→ risks/objectives
→ implement
→ measure/audit/review
→ root cause
→ improve
```

## Acceptance

- процессы реально работают, а не существуют только в документах;
- результаты измерений воспроизводимы;
- audit findings документируются;
- corrective actions проверяются на эффективность;
- СУИБ пересматривается при изменениях.

## Rollback

Универсального rollback для management-system changes глава не задаёт.
