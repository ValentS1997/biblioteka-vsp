# Шпаргалка: Chapter 17 — Ransomware Response

## Attack types

| Type | Core characteristic |
|---|---|
| HumOR | hands-on-keyboard, lateral movement, staged attack |
| Mass-distributed | automated, volume-focused |
| Encryptionless extortion | data theft without encryption |
| Pseudo-ransomware / wiper | no reliable recovery path |

## Ransomware-specific DAIR

### Prepare
- crisis comms;
- holding statement;
- CTI;
- Tier-0 identity;
- help desk/user training;
- resilient backups;
- recovery priorities.

### Verify/Triage
- confirm attack type;
- assess impact;
- protect victim identifiers;
- engage decision makers;
- assign incident commander;
- plan for extended duration.

### Scope
- affected systems;
- identities;
- backup systems;
- lateral movement;
- exfiltration;
- timeline;
- persistence.

### Eradicate
- remove access/persistence;
- investigate exfiltration;
- close initial vector;
- validate identity;
- evaluate decryptor options.

### Recover
- restore by dependency;
- use clean restore point;
- validate backup integrity;
- monitor for return;
- communicate continuously.

### Debrief
- backup survival;
- dwell time;
- exfiltration confidence;
- ransom decision;
- recovery method;
- identity exposure.

## Backup rule

```text
3 copies
2 media
1 off-site
1 immutable/air-gapped
0 recovery-test errors
```

## Decryptor rule

```text
identify exact variant
→ find candidate tool
→ test sample
→ backup encrypted data
→ decrypt copy
→ validate
```

## Critical warnings

```text
encrypted files restored
≠
incident eradicated
```

```text
ransom paid
≠
stolen data deleted
```

```text
encryption timestamp
≠
initial compromise time
```

## Ransomware metrics

- dwell time;
- backup survival rate;
- exfiltration confidence;
- recovery method distribution;
- encryption spread rate.

## Main takeaway

```text
identity
+ backups
+ scope
+ communications
+ recovery sequencing
+ sustained staffing
= ransomware resilience
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

