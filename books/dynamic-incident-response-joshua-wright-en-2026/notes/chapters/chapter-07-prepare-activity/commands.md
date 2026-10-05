# Команды и technical artifacts Chapter 7

Chapter 7 contains few command-line procedures. Its technical artifacts are primarily configuration/documentation examples and machine-readable intelligence.

## Listing 27 — security.txt

The source includes a Microsoft `security.txt` example as a model for an external security-reporting channel.

Purpose:

- publish security contact information;
- provide encryption/disclosure-policy details;
- route external vulnerability reports to the security team.

Operational point:
- external reporting channel must be documented and internally routed before an incident/disclosure arrives.

## Listing 28 — STIX indicator

Source includes an ISAC STIX indicator for Velvet Tempest C2 infrastructure.

STIX object concepts shown by Chapter 7:

- indicator metadata;
- indicator type;
- STIX pattern;
- valid-from time;
- machine-readable relationship/context.

Example pattern concept in the source:

```text
[url:value = 'https://login-secure-verify.com/auth']
```

The value of STIX is operational automation:
- parse indicator;
- create detection;
- create blocklist entry;
- enrich investigation.

## Named tooling / technologies

### Collaboration / communications
- Slack
- Microsoft Teams
- Signal
- Element

### Identity
- Active Directory
- Entra ID

### Forensics
- Autopsy
- Volatility
- Plaso

### Threat intelligence
- STIX 2.1
- OpenCTI
- ISAC feeds

### Security baselines
- CIS Benchmarks
- DISA STIGs

### Endpoint/network
- EDR
- Sysmon
- Full Packet Capture
- NetFlow
- IPFIX
- sFlow
- eBPF
- NDR

### Framework / prioritization
- MITRE ATT&CK
- CVSS
- EPSS
- BAS

## State-changing guidance

Source describes many preparation changes, but does not give a single universal shell command sequence.

Examples of changes:
- create break-glass accounts;
- deploy logging;
- harden systems;
- deploy EDR/Sysmon;
- configure network monitoring;
- establish retention;
- maintain inventories.

Exact implementation depends on platform and is intentionally not invented here.

## Verification expectations

Preparation controls should be tested:

- break-glass account works;
- backup communication works;
- escalation contact works;
- detection rule fires during simulation;
- telemetry reaches central collection;
- restore process works;
- tabletop exposes and resolves gaps.

## Rollback

Platform-specific rollback is not defined at this chapter level: `[Needs confirmation]`.
