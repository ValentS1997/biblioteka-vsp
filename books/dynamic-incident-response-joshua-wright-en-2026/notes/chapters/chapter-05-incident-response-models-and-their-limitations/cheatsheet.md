# Шпаргалка: Chapter 5 — классические IR-модели и их ограничения

## PICERL

```text
Preparation
   ↓
Identification
   ↓
Containment
   ↓
Eradication
   ↓
Recovery
   ↓
Lessons Learned
```

Strengths:
- clear structure;
- containment explicit;
- lessons learned explicit.

Weaknesses:
- commonly represented as linear;
- scoping not explicit;
- verification not explicit;
- prioritization not explicit;
- root cause not explicit.

## NIST SP 800-61 Rev.2

```text
Preparation
   ↓
Detection & Analysis
   ↓
Containment / Eradication / Recovery
   ↓
Post-Incident Activity
   ↺
Preparation
```

Strengths:
- stronger detection/analysis guidance;
- more cyclical than typical PICERL representation;
- metrics and information sharing included.

Weaknesses:
- recovery guidance reduced;
- iteration not elevated into a core loop.

## NIST SP 800-61 Rev.3

```text
Govern
Identify
Protect
Detect
Respond
Recover
```

Shift:

```text
tactical lifecycle
      ↓
enterprise risk-management integration
```

Tradeoff:

- broader organizational integration;
- less detailed operational play-by-play.

## Five gaps

| Gap | Why it matters |
|---|---|
| Scoping | prevents underestimating breadth |
| Iteration | real incidents change as evidence appears |
| Resource prioritization | capacity is limited |
| Verification | not every abnormal event is an incident |
| Root cause analysis | symptom remediation may not prevent recurrence |

## Decision rule

If a framework cannot answer:

- Is this really an incident?
- How broad is it?
- What should we work on first?
- What if new evidence changes scope?
- Why did this happen structurally?

then responders must add that logic themselves.

## Modern model requirements

A modern response model should support:

1. verify;
2. scope;
3. prioritize;
4. iterate;
5. analyze root cause;
6. align response with business objectives.

## Main takeaway

```text
classic models = strong foundation
modern incidents = more dynamic
DAIR motivation = make missing logic explicit
```
