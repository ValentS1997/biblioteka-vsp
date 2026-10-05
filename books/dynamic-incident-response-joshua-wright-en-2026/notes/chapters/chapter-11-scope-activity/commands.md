# Команды и scoping artifacts Chapter 11

Только source-supported examples.

## Listing 41 — Network activity timeline CSV

Source uses a simple CSV of timestamps, source systems and C2 labels to visualize attack progression over time.

Purpose:
- reconstruct first-seen activity;
- compare hosts;
- identify attack progression.

## Listing 42 — Basic file triage

```bash
ls -l malware
sha256sum malware
file malware
```

Purpose:
- establish size;
- hash;
- file type before opening the document.

## Listing 43 — PDF structure review

```bash
pdfid.py malware
```

Purpose:
- inspect PDF structural indicators before opening it.

## Listing 44 — Extract embedded URLs

```bash
pdf-parser.py -s /URI malware
```

Purpose:
- identify embedded links/payload references;
- derive network/file indicators for scoping.

## Cloud Audit Log Quick Reference — Table 14

### AWS

```bash
aws cloudtrail lookup-events
aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=<name>
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=<user>
aws cloudtrail lookup-events --start-time <time> --end-time <time>
```

### Azure

```bash
az monitor activity-log list
az monitor activity-log list --resource-id <resource-id>
az monitor activity-log list --caller <object-id>
az monitor activity-log list --start-time <time> --end-time <time>
```

### GCP

```bash
gcloud logging read
gcloud logging read 'resource.type="<type>"'
gcloud logging read 'protoPayload.authenticationInfo.principalEmail="<email>"'
gcloud logging read 'timestamp>="<time>"'
```

## Listing 45 — Azure blob contents

```bash
az storage blob list   --container-name backup-data-archive-2025   --account-name stcorpdata01   --query "[].{Name:name, Size:properties.contentLength, Modified:properties.lastModified}"   --output table
```

Purpose:
- inspect suspicious container contents;
- identify data categories and upload pattern.

## Listing 46 — Azure container creation event

Source queries Activity Log for the suspicious container and extracts:
- caller object ID;
- source IP;
- timestamp;
- operation;
- resource group.

## Listing 47 — Compromised service principal activity

```bash
az monitor activity-log list   --caller c7e2a091-4b38-4d65-9f12-b8a3e6d50c71   --offset 7d   --query "[].{Time:eventTimestamp, Operation:operationName.localizedValue, Provider:resourceProviderName.localizedValue}"   --output table
```

Purpose:
- pivot from one suspicious object to all actions by compromised identity.

## Table 15 — Cloud exfiltration scoping examples

Source includes commands such as:

```bash
az monitor activity-log list --caller <object-id> --offset 90d
az role assignment list --assignee <object-id> --all
az storage container list --account-name stcorpdata01   --query "[?properties.lastModified >= '2025-10-15']" --output table
```

Purpose:
- extend timeline;
- enumerate privilege expansion;
- identify related cloud resources.

## Risk notes

All examples above are read-only investigation/scoping operations as presented.

Platform-specific active scanning may change system/network state indirectly; Chapter 11 mentions it conceptually but does not provide a universal command sequence.

## Verification

A scoping query is only useful if coverage is known.

Check:
- log retention;
- sampled vs unsampled flow;
- managed vs unmanaged endpoints;
- cloud region/account coverage;
- identity scope;
- missing data sources.
