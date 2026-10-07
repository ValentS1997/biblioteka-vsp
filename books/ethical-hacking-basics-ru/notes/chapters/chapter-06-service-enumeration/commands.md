# Commands and tools — глава 6 (RAG-only, safe classification)

Source: PDF pp. 140–168, `p0140:c01` … `p0168:c02`. No commands were executed. Historical targets/credentials are not reproduced as runnable examples.

## Read-only / local

- `nbtstat -r` — source example for local NetBIOS name-resolution statistics, p. 149.
- Reviewing saved OpenVAS/Nessus/Metasploit/WPScan output is read-only after collection.
- Tool help and script source review are local operations when they do not contact a target.

## Workload-generating enumeration

The source explicitly uses these tool families against lab targets:

| Tool / function | What it queries | RAG |
| --- | --- | --- |
| nmap service/version and protocol-specific NSE | service/version, cipher, SMB metadata | p. 141–143, 151 |
| rpcinfo / SunRPC scanner | rpcbind/portmapper registered programs | p. 143–145 |
| RMI registry tooling | Java RMI registry/object metadata | p. 146–147 |
| NetBIOS/SMB tools | names, versions, shares and users where permitted | p. 149–156 |
| snmpwalk | MIB/OID system and interface data | p. 158–159 |
| SMTP interactive/scanner tooling | banner/capability/address behavior | p. 160–162 |
| dirb / web directory scanners | directory/path enumeration | p. 162–164 |
| WPScan | WordPress version/theme/plugin/user metadata | p. 165–167 |

These operations are active network/application queries. Exact target syntax is intentionally not reproduced here; use only an explicitly authorized lab scope.

## High-risk source material — not operationalized

The source also shows:
- SMB username/password combination testing;
- SMTP user/address enumeration;
- WordPress login/user enumeration modules;
- SNMP community-string access.

These can trigger lockout, authentication events, privacy exposure or unauthorized credential testing. The chapter artifacts preserve their existence and provenance but do **not** provide a runnable credential-attack sequence.

## Effects, risks, verification, rollback

**Effect:** network/application requests and possible identity/share/system-metadata disclosure.  
**Risks:** lockout, alerts, rate limiting, sensitive-data exposure, request load.  
**Verification:** approved scope + raw evidence + timestamp; actual environment is **[Needs confirmation]**.  
**Rollback:** **[Needs confirmation]**; requests cannot be undone and account/service recovery is environment-specific.
