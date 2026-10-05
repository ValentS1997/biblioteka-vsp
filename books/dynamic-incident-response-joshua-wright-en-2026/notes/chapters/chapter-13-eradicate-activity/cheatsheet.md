# Шпаргалка: Chapter 13 — Eradicate Activity

## Core objective

```text
understand attacker
      ↓
remove persistence/access
      ↓
fix exploited weakness
      ↓
validate no recurrence path remains
```

## Investigation tracks

| Track | Purpose |
|---|---|
| Short-form | enough evidence for immediate eradication |
| Long-form | deep forensic understanding |

## RCA

Use:
- Four P's;
- Fishbone;
- Five Whys.

Question:
```text
what enabled compromise?
not only
what artifact was malicious?
```

## Investigation toolbox

- logs / Sigma / SIEM / Hayabusa;
- live differential analysis;
- Velociraptor;
- process memory;
- whole-system memory;
- Volatility / MemProcFS;
- PCAP / flow / DNS / proxy / firewall;
- malware static/dynamic analysis;
- identity/OAuth;
- cloud control-plane and IAM.

## Persistence removal

Windows:
- services;
- tasks;
- registry;
- startup;
- unauthorized accounts.

Linux:
- cron;
- systemd;
- SSH keys;
- local users;
- startup/config hooks.

Cloud:
- malicious serverless functions;
- IAM policy changes;
- app registrations;
- tokens/keys;
- modified images/containers.

## Identity remediation

Priority areas:
- privileged users;
- service accounts;
- KRBTGT;
- DC machine accounts;
- trust passwords;
- unconstrained delegation;
- Entra/SSO;
- OAuth;
- PAT/API keys.

## KRBTGT rule

```text
reset
→ verify replication
→ wait ≥ max ticket lifetime
→ reset again
→ verify replication
```

## Rebuild decision

Do not ask only:
- "can we wipe it?"

Ask:
- do we know root cause?
- are identities clean?
- are images/templates trusted?
- is the vulnerability fixed?
- can persistence survive rebuild?

## Vulnerability remediation

- patch;
- verify;
- track;
- phase;
- compensate if unpatchable;
- assess broader environment;
- harden;
- disable unnecessary services.

## Validation

Confirm:
- no known persistence remains;
- revoked credentials fail;
- blocked IOC triggers detection;
- exploited vulnerability is closed;
- attacker activity does not resume.

## Main takeaway

```text
remove artifact
+ remove persistence
+ remove access
+ fix root cause
+ validate
= eradication
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

