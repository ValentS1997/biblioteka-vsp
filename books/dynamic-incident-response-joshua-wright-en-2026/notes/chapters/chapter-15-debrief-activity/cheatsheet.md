# Шпаргалка: Chapter 15 — Debrief Activity

## Core flow

```text
Active Response Ends
      ↓
Closure Readiness
      ↓
Temporary Asset Review
      ↓
Documentation Consolidation
      ↓
Metrics
      ↓
After-Action Review
      ↓
Reports / Presentation
      ↓
Recommendations
      ↓
Owners + Deadlines + Follow-up
```

## Two objectives

- Incident Closure
- Organizational Learning

## Closure checklist

- threat handled;
- decision makers agree;
- temporary assets reviewed;
- evidence retention defined;
- access removed where no longer needed;
- monitoring disposition decided;
- records consolidated.

## Documentation depth

### Lightweight
Use for:
- low severity;
- single-system;
- standard playbook;
- no major external obligations.

### Formal
Use for:
- multi-system;
- privileged compromise;
- data exposure;
- executive decisions;
- regulatory notification;
- significant impact.

## Metrics

Track:
- MTTD;
- MTTR;
- scope;
- business impact;
- resource hours;
- cost;
- total lifecycle.

## AAR questions

1. What was supposed to happen?
2. What actually happened?
3. Why did it happen?
4. What should improve?
5. What worked?
6. Why did it work?

## Recommendation horizons

- Immediate
- Short-term
- Long-term

## Executive lever format

```text
Opportunity
Benefit
Cost
Time
Resources
Compliance
Protections
```

## Presentation output

Must produce:
- decisions;
- approvals/deferrals;
- action items;
- owners;
- deadlines;
- follow-up date.

## Anti-pattern

```text
lessons learned
without
owner + deadline + tracking
=
lessons documented, not learned
```

## Main takeaway

Debrief quality is measured by what changes afterward.
## v1.6 compatibility contract

### Symptom / problem framing

See the chapter-specific framing above. If the chapter is conceptual rather than diagnostic, this field is `[Not applicable]` as a troubleshooting symptom.

### Baseline / context

Use only the source-grounded chapter context documented above.

### Read-only checks

See `commands.md` for source-confirmed checks/tools. If the chapter provides no operational checks, this field is `[Not applicable]`.

### Interpretation

Use the source-grounded interpretation and chapter logic documented above.

### Next action

Follow the chapter-specific source-grounded flow above. Unsupported next actions remain `[Needs confirmation]`.

### Modifying action

See `commands.md` for source-confirmed modifying actions. If none are supplied by the chapter, this field is `[Not applicable]`.

### Verification / acceptance checks

Use the source-supported verification/acceptance criteria in this chapter and `commands.md`. If no modifying action exists, this field is `[Not applicable]`.

### Rollback

Use source-supported rollback only. If the source does not provide rollback, mark it `[Needs confirmation]`.

