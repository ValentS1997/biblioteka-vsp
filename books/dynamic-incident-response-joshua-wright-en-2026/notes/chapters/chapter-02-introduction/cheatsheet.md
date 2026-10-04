# Шпаргалка: Chapter 2 — что делает incident response эффективным

## Symptom / problem framing

Глава рассматривает проблему не как отдельный malware case, а как systemic question:

**почему формально правильные response actions иногда всё равно приводят к плохому outcome?**

Ответ: потому что качество response зависит от decisions, scope и adaptation, а не только от tools или выполнения заранее заданных steps.

## Baseline / context

IR происходит в условиях:

- incomplete information;
- pressure;
- limited time;
- evolving attacker behavior;
- competing technical/business priorities.

Поэтому linear process без verification и re-scoping может дать ложную уверенность.

## Read-only checks

Для этой концептуальной главы shell-команды отсутствуют.

Поддержанные source questions для mental check:

- Понимаем ли мы реальный scope?
- Проверены ли assumptions?
- Может ли containment предупредить attacker?
- Удалена ли persistence?
- Согласован ли recovery plan?
- Понимают ли decision makers impact и uncertainty?

Это не source checklist в формальном виде, а прямой synthesis из аргументации главы.

## Interpretation

### Что не определяет качество response

Само по себе наличие:

- forensic platform;
- endpoint protection;
- threat-intelligence feed;
- managed service provider

не гарантирует effective response.

### Что определяет качество response

- judgment;
- verification;
- scope awareness;
- clear communication;
- cross-team collaboration;
- strategic thinking;
- ability to iterate.

## Next action

Организация должна строить response capability так, чтобы она поддерживала:

1. identification;
2. verification;
3. triage;
4. scoping;
5. containment;
6. eradication;
7. recovery;
8. continuous improvement через metrics и lessons learned.

## Modifying action

[Not applicable]

Глава не приводит конкретных modifying commands или procedures.

## Verification / acceptance checks

Conceptual acceptance для IR program по смыслу главы:

- response decisions учитывают scope, а не только initial indicator;
- technical actions согласованы с stakeholders/decision makers;
- response может изменяться при новой информации;
- lessons learned реально меняют future process;
- metrics используются для оценки effectiveness.

Это conceptual criteria; формальный audit contract Chapter 2 не задаёт.

## Rollback

[Not applicable]

Конкретных state-changing actions в главе нет.

## Changing demands checklist

Современная IR function должна учитывать:

| Driver | Что меняется для response |
|---|---|
| Digital dependence | Incident impact выше |
| Threat complexity/volume | Нужны более mature capabilities |
| Regulation | Нужна reporting/notification readiness |
| Threat-intel sharing | Response становится collaborative |
| Ransomware/extortion | Нужна готовность к high-impact incidents |
| Cloud/third-party | Scope выходит за local infrastructure |
| Remote work | Environment и team distributed |
| Stakeholder expectations | Communication становится частью response |
| Proactive defense | SIEM/XDR/SOAR усиливают detection/response |
| AI-driven attacks | Conventional methods испытывают pressure |

## Main takeaway

```text
tools help
process guides
judgment decides
iteration corrects
```
