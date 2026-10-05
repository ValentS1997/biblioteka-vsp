# Команды и recovery artifacts Chapter 14

Только source-supported examples.

## Windows enhanced auditing

Source Listing 115 uses `auditpol` to enable post-recovery auditing.

Example pattern:

```cmd
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable
auditpol /get /category:*
```

Purpose:
- increase observability after restoration.

Risk:
- increased event volume.

Verification:
- review applied audit policy;
- confirm events reach central collection.

Rollback:
- restore previous audit policy baseline [Needs confirmation].

## Linux auditd monitoring

Source Listing 116 defines audit rules for:
- identity files;
- SSH config/keys;
- process execution;
- network configuration.

Operational note:
- tailor rules to role/platform;
- ARM64 requires architecture adjustment;
- validate logging volume.

State change:
- loading rules and restarting audit service modifies monitoring configuration.

Verification:
- confirm audit service healthy;
- confirm expected events arrive.

Rollback:
- restore prior ruleset [Needs confirmation].

## AWS snapshot listing

```bash
aws ec2 describe-snapshots   --owner-ids self   --query 'Snapshots[*].[SnapshotId,StartTime,Description]'   --output table
```

Purpose:
- select snapshot that predates compromise.

Read-only.

## Cloud snapshot restoration

Source Table 34 shows provider-specific commands for restoring volumes/disks from snapshots.

These are state-changing infrastructure operations.

Before execution:
- verify snapshot timestamp against attack timeline;
- verify region/zone/resource target;
- define rollback.

## Domain Controller backup review

Source Listing 118 uses Windows backup cmdlets to enumerate available DC backups and compare them with incident timeline.

Purpose:
- identify known-good backup.

Read-only.

## Post-restoration AD checks

Source Listing 119 verifies core DC services.

Checks include:
- NTDS;
- DNS;
- Netlogon;
- DFSR.

Source later validates:
- AD replication health;
- enhanced audit state.

These are acceptance checks before moving to the next recovery phase.

## Command discipline

Recovery commands can be highly state-changing.

Before:
1. verify restore source;
2. verify dependency order;
3. document rollback;
4. coordinate with owner;
5. enable monitoring.

After:
1. validate functionality;
2. validate security controls;
3. validate dependencies;
4. obtain owner acceptance;
5. monitor before scaling out.
