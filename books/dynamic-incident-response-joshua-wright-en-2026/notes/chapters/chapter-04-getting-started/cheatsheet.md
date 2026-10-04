# Шпаргалка: Chapter 4 — базовый словарь Incident Response

## Core terminology

| Термин | Meaning |
|---|---|
| Incident | adverse event / threat of harm |
| Event | любое observable occurrence |
| EOI | event, требующий дальнейшего investigation |
| IOC | evidence успешной compromise |
| IOA | behavior/intent-oriented indicator |
| MTTD | average time to detect |
| MTTR | average time to respond/resolve |

## Event → Incident pipeline

```text
raw events
   ↓
filter / context
   ↓
EOI
   ↓
correlation + intelligence
   ↓
IOC / behavioral pattern
   ↓
verify against policy / risk
   ↓
incident
```

## Important distinction

```text
Event ≠ Incident
EOI ≠ Incident
IOC strongly supports compromise
Incident declaration is an organizational decision
```

## EOI decision model

Source example: WordPress failed logins.

- 40,592 failures from one IP;
- no successful login from same IP.

Possible interpretations:

- organization A: attack → investigation;
- organization B: attack, but not EOI because unsuccessful.

Conclusion:

**events are objective; interpretation is contextual.**

## IOC types

### Atomic
Examples:
- filename;
- registry key;
- URL;
- IP.

Use:
- fast matching;
- automation.

### Computed
Examples:
- hash;
- regex/pattern.

Use:
- identify artifact despite variable names/content presentation.

### Behavioral
Inputs:
- event sequence;
- attacker behavior;
- TTP;
- baseline.

Use:
- known + unknown technique detection.

## IOC vs IOA

Practical distinction is subtle.

```text
IOC → evidence of compromise
IOA → attacker intent / behavior
behavioral IOC ≈ conceptually close to IOA
```

## MTTD

Good metric only if:

- incident occurrence time is defined;
- detection time is recorded consistently;
- categories are comparable;
- trend is tracked over time.

Risk:
- occurrence time often changes retrospectively.

## MTTR

Useful dimensions:

- incident type;
- severity;
- median/P50;
- P90;
- time to containment;
- time to full resolution.

External dependencies matter:

- IT;
- legal;
- HR;
- vendors;
- law enforcement;
- SLA delays.

## Critical warning

```text
low MTTR + weak investigation = bad response with a good-looking number
```

Pair MTTR with quality score.

## Quality questions

- initial analysis thorough?
- ticket idle?
- related systems checked?
- root cause documented?
- premature closure / reopen?

## Incident Response vs Management

| Incident Response | Incident Management |
|---|---|
| technical | organizational |
| detect/analyze | coordinate |
| contain/eradicate | communicate |
| recover | allocate/escalate |
| collect evidence | legal/compliance/stakeholders |
| validate known-good state | track decisions/remediation |

## Practical acceptance

A mature program should have:

- shared definitions;
- clear incident declaration criteria;
- EOI criteria;
- IOC handling process;
- MTTD/MTTR definitions;
- quality-oriented measures;
- separation of technical response and organizational management responsibilities.
