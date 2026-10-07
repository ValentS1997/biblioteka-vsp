# Commands and tools — глава 13 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0365:c01` … `p0398:c01`, PDF pp. 365–398.

## Executable commands

The chapter does **not** provide concrete shell/network command syntax.

### Source-named utility: `arp`

`p0384:c01` states that static ARP-table entries may be created manually using an `arp` utility.

- Exact command syntax: **[Needs confirmation]**.
- Platform: **[Needs confirmation]**.
- This is a state-changing operation because it alters local IP→MAC resolution state.

### Source-named file-copy tools: `ftp` / `scp`

`p0391:c01` says a DNS secondary can receive a zone copy through DNS zone transfer or an administrator may use a file-copy protocol/tool such as FTP or SCP.

- Exact invocation: not supplied.
- Authentication/security details: not supplied.
- Do not infer a modern recommended operational procedure from this statement.

## Source-confirmed protocols and mechanisms

| Object | Role | RAG |
| --- | --- | --- |
| TCP | Reliable connection-oriented transport | `p0366:c01` |
| UDP | Datagram transport | `p0366:c01` |
| IP | Connectionless best-effort internetwork delivery | `p0366:c01`–`p0370:c01` |
| IPv4 mask/prefix | Network/host boundary | `p0373:c01`–`p0380:c01` |
| CIDR | Prefix-based address-pool allocation | `p0379:c01`–`p0380:c01` |
| ARP | IPv4→local/MAC resolution | `p0381:c01`–`p0384:c01` |
| RARP | Reverse local-address→IP resolution in source scenario | `p0385:c01` |
| Proxy-ARP | Router answers ARP on behalf of remote node | `p0385:c01`–`p0386:c01` |
| DNS resolver/server | Symbolic-name resolution | `p0389:c01`–`p0392:c01` |
| UDP/TCP port 53 | DNS transport in source description | `p0389:c01`–`p0391:c01` |
| `in-addr.arpa` | IPv4 reverse-DNS hierarchy | `p0393:c01`–`p0394:c01` |
| DHCP | Automated IPv4 host configuration | `p0394:c01`–`p0398:c01` |
| DHCP relay | Forward client requests to remote server | `p0396:c01`–`p0397:c01` |

## Source-described state changes without executable syntax

The source describes configuration of:

- interface IPv4 address and mask;
- default router/gateway;
- DNS server address and host/domain parameters;
- static ARP mappings;
- DNS primary zone data and secondary replication;
- DHCP address pool and lease duration;
- DHCP relay location/target.

For real systems, all commands, before-state capture, verification and rollback remain **[Needs confirmation]**.

No syntax is invented.
