# Команды и detection artifacts Chapter 8

Только artifacts, явно присутствующие в canonical RAG.

## Listing 29 — Zeek + RITA

```bash
zeek -Cr capture.pcap
/opt/rita/rita.sh import -l ~/zeek-logs -d InvestigationDB
/opt/rita/rita.sh view InvestigationDB
```

Purpose:
- convert packet capture into Zeek logs;
- import logs into RITA;
- analyze beaconing/C2-like behavior.

Notes from source:
- `-C` tells Zeek to process packets with invalid checksums;
- RITA scores beacon consistency, duration, subdomain patterns and other indicators.

## Listing 30 — Azure DCR KQL filtering

```kusto
source
| where StatusCode >= 400
    or OperationType in ("DeleteBlob", "PutBlob",
                         "PutBlock", "CopyBlob")
    or (CallerIpAddress !startswith "10."
        and CallerIpAddress !startswith "192.168.")
| project TimeGenerated, OperationType, StatusCode,
    CallerIpAddress, AccountName, ObjectKey, UserAgentHeader
```

Purpose:
- detection-driven collection;
- discard routine storage noise before SIEM/Log Analytics ingestion;
- retain failed, write/delete and external-source events.

## Listing 31 — JA4 TLS fingerprint

```bash
tshark -r netedge-20260105.pcapng   -Y "tls.handshake.type == 1"   -T fields -e tls.handshake.ja4 | sort -u
```

Then query local DB:

```bash
jq '.[] | select(.ja4_fingerprint == "t13i3110as_e8f1e7e78f70_1f22a2ca17c4")'   ~/ja4db.json
```

Source result maps the fingerprint to AnyDesk v9.6.1.

## Listing 32 — external disclosure email

Not a command. It is a detection artifact showing how an external researcher can provide:
- URLs;
- suspicious accounts;
- source IPs;
- timeline;
- supporting logs.

## Listing 33 — Elasticsearch beacon hunt

Source uses an aggregation query over the last seven days:

Key structure:
- `size: 0`;
- range on `@timestamp`;
- group by `url.keyword`;
- `auto_date_histogram`;
- count requests.

Purpose:
- identify periodic access patterns;
- distinguish human browsing from automated beaconing.

## Named tools

- SentinelOne
- Splunk
- Elastic Security / Kibana / Elasticsearch
- Microsoft Sentinel
- SOAR platforms
- OpenObserve
- RITA
- Zeek
- TShark
- jq
- AWS GuardDuty
- Azure Defender
- Google Cloud Security Command Center

## Risk notes

These examples are detection/analysis oriented.

Potentially state-changing SOAR actions are mentioned conceptually:
- quarantine endpoint;
- block IP;
- disable account.

Source does not provide universal commands for them.

Rollback: `[Needs confirmation]` per platform.
## v1.6 command classification

| Artifact | Classification | Effect | Verification | Rollback |
|---|---|---|---|---|
| Zeek processing | workload-generating | parses PCAP and writes Zeek logs | expected Zeek logs are produced | remove generated local analysis output if required |
| RITA import/view | workload-generating | creates/reads local investigation database | database imports and renders expected analysis | remove local investigation DB if required |
| DCR KQL text | [Needs confirmation] | query/filter logic; deployment context determines whether it becomes configuration | validate retained/discarded event classes against source intent | [Needs confirmation] |
| TShark + jq | read-only against source evidence | extracts JA4 values and reads local JSON DB | fingerprint/result matches selected traffic | [Not applicable] |
| Elasticsearch aggregation | read-only | aggregates existing events | validate index/time window and returned buckets | [Not applicable] |

Conceptual SOAR quarantine/block/disable actions are state-changing, but no executable commands are supplied by the chapter; rollback is platform-specific and remains `[Needs confirmation]`.

