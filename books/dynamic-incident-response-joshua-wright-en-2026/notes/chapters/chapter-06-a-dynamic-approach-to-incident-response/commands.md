# Команды и operational artifacts Chapter 6

Chapter 6 не содержит shell/CLI-команд.

Это framework chapter.

## Operational concepts explicitly defined by source

| Concept | Purpose |
|---|---|
| Prepare | readiness |
| Detect | discovery / threat hunting / EOI detection |
| Verify | confirm event is incident |
| Triage | prioritize by organizational goals |
| Scope | determine breadth and affected systems |
| Contain | limit threat impact |
| Eradicate | remove known threat |
| Recover | restore systems |
| Debrief | assess strengths/weaknesses and improve |
| Response Actions Loop | repeat scope/contain/eradicate/recover as needed |
| Decision Makers | provide organizational context and priorities |

## Example response decisions from source

Production DB servers:
- use live response techniques;
- minimize disruption;
- coordinate maintenance window.

Finance workstations:
- use network segmentation;
- preserve critical access;
- delay more disruptive analysis.

These are conceptual examples, not command recipes.

## State-changing actions

No concrete command-level state changes are provided.

## Verification

Conceptual verification:

- event confirmed as incident;
- priority agreed;
- scope sufficiently understood;
- response actions repeated until no new evidence appears.

## Rollback

[Not applicable]

No command-level rollback is described.
