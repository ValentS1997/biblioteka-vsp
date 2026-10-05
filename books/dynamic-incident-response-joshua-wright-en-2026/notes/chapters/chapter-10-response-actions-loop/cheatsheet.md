# Шпаргалка: Chapter 10 — Response Actions Loop

## Core loop

```text
Scope
  ↕
Contain
  ↕
Eradicate
  ↕
Recover
  ↺
```

Не фиксированная последовательность.

## Why iterate

Single-pass response fails because of:

- incomplete understanding;
- insufficient insight;
- incomplete evidence;
- limited scope.

## Iteration triggers

### 1. New IOC
New artifact → go back to Scope.

### 2. Scope expansion
Known IOC reaches new systems/business units.

### 3. Incomplete eradication
Reinfection / persistence remains.

### 4. Evidence revelation
Memory/log/timeline/malware analysis reveals new facts.

### 5. Business/external change
Legal, regulator, insurance, law enforcement, priorities change.

## Documentation minimum

For every major action:
- what;
- when;
- who;
- why;
- business impact.

Maintain continuity across iterations.

## Exit criteria

### Technical
- no new IOC;
- no signs of attacker;
- eradication verified;
- systems stable after recovery.

### Business
- objectives met;
- acceptable risk achieved;
- cost-benefit supports closure;
- residual uncertainty accepted.

## Exit decision

Must be documented:

```text
decision maker
+ evidence
+ business context
+ accepted residual risk
+ timestamp
```

## Practical risks

- responder fatigue;
- budget pressure;
- slow tools/manual forensics;
- documentation burden;
- poor shift handoff;
- stakeholder impatience.

## Communication

Audience-specific:
- executive summary;
- technical briefing;
- user/service update.

Frequency should follow severity and phase.

## Main takeaway

```text
new evidence
   ↓
new understanding
   ↓
new response cycle
   ↓
better resolution
```
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

