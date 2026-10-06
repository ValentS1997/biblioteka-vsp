# Команды и detection artifacts Chapter 4

Только artifacts, явно присутствующие в canonical RAG.

## Listing 25 — MySQL review WordPress login failures

```sql
SELECT event_type,
       DATE_FORMAT(FROM_UNIXTIME(MIN(created_on)), '%Y-%m-%d %H:%i:%s')
       AS first_observed_failure,
       client_ip,
       COUNT() AS failure_count
FROM wp_wsal_occurrences
WHERE alert_id = 1002
  AND FROM_UNIXTIME(created_on) >= NOW() - INTERVAL 1 DAY
GROUP BY event_type, client_ip
ORDER BY first_observed_failure ASC;
```

Purpose:

- aggregate failed-login events;
- group by client IP;
- identify high-volume source;
- support EOI interpretation.

Source also shows a second query:

```sql
select object, event_type, user_agent
from wp_wsal_occurrences
WHERE alert_id = 1000
  AND client_ip = '185.196.220.113';
```

Result:

```text
Empty set
```

Interpretation from source:

- many login failures existed;
- no successful login from that IP was found;
- whether this becomes an EOI depends on organizational policy.

## Listing 26 — Sigma rule concept for FortiOS IOC

Source uses a Sigma rule for detection of CVE-2024-55591-related FortiOS exploitation.

Key matching elements shown in RAG:

```yaml
detection:
  keywords:
    - 'type="event"'
    - 'subtype="system"'
    - 'logdesc="Object attribute configured"'
    - 'action="Add"'
    - 'cfgpath="system.admin"'
    - 'cfgattr="password[*]accprofile[super_admin]vdom[root]"'
  condition: keywords
```

Context:

- product: Fortinet FortiOS;
- category: firewall;
- level: high;
- tags include persistence and CVE identifiers.

## Tooling named by source

- SIEM
- EDR
- NDR
- Sigma
- ServiceNow
- Jira
- ticketing systems
- incident response platforms

## Risk / verification

These examples are analysis/detection artifacts.

No destructive remediation commands are provided in Chapter 4.

Rollback: `[Not applicable]`.

## Source gaps

MTTD and MTTR equations are absent in canonical RAG text layer.

They are intentionally not reconstructed from model memory.
## v1.6 command classification

| Artifact | Classification | Effect | Verification | Rollback |
|---|---|---|---|---|
| Listing 25 SQL queries | read-only | reads/aggregates WordPress audit data | query result matches intended time/IP scope | [Not applicable] |
| Listing 26 Sigma rule | [Not applicable as an executed command] | detection rule artifact | validate rule logic against intended FortiOS events | [Not applicable] |

No state-changing command is supplied by this chapter.

