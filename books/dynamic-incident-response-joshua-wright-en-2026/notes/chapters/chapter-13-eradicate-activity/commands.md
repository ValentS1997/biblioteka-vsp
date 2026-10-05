# Команды и eradication artifacts Chapter 13

Только source-supported примеры. Для state-changing действий параметры нормализованы до placeholders, чтобы материал оставался учебным и не превращался в непрозрачный production runbook.

## Read-only / investigation

### Hayabusa timeline

```bash
hayabusa csv-timeline   -d eventlogs/   -T   -o hayabusa-threathunting.csv   -E   --timeline-start "<start>"   --timeline-end "<end>"   --no-color
```

Purpose:
- анализ EVTX;
- построение threat timeline.

### Memory strings

```powershell
strings.exe <process-memory.dmp> > memory_strings.txt
Select-String -Encoding Unicode -Pattern "powershell\s+-" .\memory_strings.txt
```

Purpose:
- извлечь readable strings;
- найти command execution artifacts.

### Whole-system memory capture

Source uses WinPMEM to acquire a full memory image.

Purpose:
- preserve volatile processes, connections, registry/kernel artifacts.

Verification:
- confirm capture completed and evidence file was produced.

### Volatility

```bash
vol -qf <memory-image> windows.driverscan.DriverScan
```

Purpose:
- enumerate loaded Windows drivers;
- identify suspicious or vulnerable drivers.

### MemProcFS IOC search

```powershell
Get-ChildItem -Path .\forensic\ -Recurse -File |
  Select-String -SimpleMatch '<IOC>'
```

Purpose:
- search memory-derived artifacts for known indicators.

### Nuclei broader vulnerability assessment

```bash
nuclei -t <template.yaml> -list <authorized-target-list>
```

Purpose:
- identify additional systems affected by the same known vulnerability.

Risk:
- active scanning can affect fragile systems.
- target authorization/scope must be verified first.

## State-changing examples

Chapter 13 includes concrete state-changing examples for:
- removing malicious Windows services;
- removing unauthorized Windows/Linux accounts;
- removing unauthorized AD group membership;
- KRBTGT rotation;
- domain-controller machine account resets;
- trust-password remediation;
- disabling unconstrained delegation;
- Entra ID account/session/token revocation;
- AWS IAM access-key revocation;
- Azure service-principal credential rotation;
- patching/hardening;
- disabling unnecessary services.

These are not safe as generic copy-paste actions. Execution requires environment-specific target validation and rollback planning.

## KRBTGT sequencing

Source-supported sequence:

```text
reset #1
→ verify AD replication
→ wait at least maximum Kerberos ticket lifetime
→ reset #2
→ verify replication again
```

Verification command shown by source:

```cmd
repadmin /replsum
```

Risk:
- incorrect sequencing or incomplete replication can cause domain-wide authentication failures.

Rollback:
- no simple rollback is defined by the source.

## Domain-controller machine account reset

Source uses `netdom resetpwd` per domain controller after KRBTGT remediation.

Operational constraints:
- reset controllers individually;
- allow replication to complete;
- avoid exceeding password-history tolerance before replication.

## Account removal

Source pattern:

```text
verify account exists
→ remove only confirmed unauthorized account
→ query again to verify absence
```

Risk:
- deleting a required service/local account can break applications or automation.

## Patch / hardening discipline

Before broad change:
1. test non-production where possible;
2. define expected result;
3. document rollback;
4. use phased rollout for large environments;
5. verify functionality after patching.

For unpatchable systems:
- segmentation;
- application-layer controls;
- enhanced monitoring;
- formal residual-risk tracking;
- replacement/upgrade timeline.

## Verification

Eradication acceptance checks:

- IOC rescan clean;
- persistence entries removed;
- revoked credentials no longer authenticate;
- suspicious sessions/tokens do not reappear;
- exploited vulnerability closed;
- compensating controls tested;
- no renewed attacker activity.

## Rollback

Platform-specific rollback remains `[Needs confirmation]` unless the source explicitly defines it.
