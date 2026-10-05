# Команды и ransomware artifacts Chapter 17

Chapter 17 содержит немного command-level material. Основной контент — process, checklists, tables and case studies.

## Listing 140 — LockBit RaaS database query

Source shows a MySQL query against leaked LockBit affiliate-panel data to illustrate victim-build statistics and the uniqueness of generated ransomware payloads.

Purpose:
- support the argument that victim-specific payload hashes have limited proactive detection value;
- reinforce preference for TTP-focused detection.

This is analytical/source material, not an operational defender action.

## Read-only investigation themes

Source recommends collecting/reviewing:

- authentication logs;
- EDR telemetry;
- firewall/VPN logs;
- NetFlow/NDR;
- SIEM;
- cloud audit logs;
- SaaS audit logs;
- file-access telemetry;
- database activity;
- backup infrastructure status.

Exact commands vary by platform and are not universally prescribed in this chapter.

## Decryption workflow

No universal decrypt command is provided.

Source-supported process:

1. identify ransomware family and variant;
2. check trusted decryption resources;
3. verify tool matches exact version;
4. test on sample files;
5. backup encrypted data;
6. run decryption on copies/dedicated systems where possible;
7. validate restored data;
8. monitor.

## State-changing actions

Potentially state-changing response actions are described conceptually:
- isolate hosts;
- revoke credentials;
- disable attacker access;
- restore/rebuild systems;
- apply decryptor;
- restore from backup.

Exact commands are not provided here because the chapter does not provide a universal safe sequence.

## Verification

Acceptance checks:

- attack type correctly identified;
- scope includes pre-encryption activity;
- backup integrity tested;
- restore point predates compromise;
- decryptor tested before broad use;
- recovered systems validated;
- attacker access absent;
- exfiltration assessment documented;
- communication/notification obligations tracked.

## Rollback

Environment-specific: `[Needs confirmation]`.
