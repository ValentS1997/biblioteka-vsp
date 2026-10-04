# Команды и technical artifacts Chapter 3

## Command coverage

Chapter 3 не содержит defender-side shell/CLI workflow.

Единственный code-like artifact — **Listing 24**, pseudocode Sendmail DEBUG exploit, приведённый для объяснения Morris Worm.

Он не является практическим recommendation и не используется в наших notes как executable procedure.

## Listing 24 — что он показывает

Source pseudocode концептуально иллюстрирует:

1. TCP connection к Sendmail на port 25;
2. использование DEBUG behavior;
3. передачу recipient field как shell pipeline;
4. создание bootstrap C source;
5. compilation;
6. execution bootstrap;
7. cleanup временных files.

Это исторический artifact, объясняющий mechanism of propagation.

## Defensive interpretation

Из Listing 24 можно извлечь только source-supported lessons:

- incident exploited network service behavior;
- remote command execution позволял bootstrap worm code;
- automated propagation масштабировала impact.

Конкретных defensive commands для detection, patching или containment Chapter 3 не даёт.

## Named systems / standards

| Item | Role |
|---|---|
| Sendmail | exploited service in Morris Worm |
| Finger | buffer-overflow target |
| RSH | weak-password access path |
| CERT | coordinated response organization |
| CIAC | DOE incident advisory/response capability |
| SANS | practical incident handling guidance |
| NIST SP 800-61 | formal incident handling framework |
| NIST CSF | broader risk-management framework alignment in Rev.3 |

## State-changing actions

[Not applicable]

## Verification

[Not applicable]

## Rollback

[Not applicable]
