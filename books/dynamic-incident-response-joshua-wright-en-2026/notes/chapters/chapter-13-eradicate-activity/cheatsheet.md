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
