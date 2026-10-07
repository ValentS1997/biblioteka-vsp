# Commands and tools — глава 15 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0442:c01` … `p0471:c01`, PDF pp. 442–471.

## Executable commands

**Исполняемые shell/network/vendor commands в границе главы не обнаружены.**

Do not inject from model memory:

- `ss` / `netstat`;
- `tcpdump` / Wireshark filters;
- `sysctl` TCP tuning;
- socket API code;
- firewall/port commands;
- congestion-control selection commands.

## Source-confirmed transport objects and mechanisms

| Object | Role | RAG |
| --- | --- | --- |
| TCP/UDP port | Transport demultiplexing identifier | `p0442:c01`–`p0444:c01` |
| Socket | `IP + port` endpoint abstraction | `p0444:c01` |
| UDP datagram | Message-oriented transport PDU | `p0445:c01`–`p0446:c01` |
| UDP checksum | Corruption detection; damaged datagram dropped | `p0446:c01` |
| TCP segment | Byte-stream transport PDU | `p0446:c01`–`p0448:c01` |
| SYN / ACK / FIN / RST / PSH / URG | TCP control flags | `p0447:c01`–`p0450:c01` |
| Sequence / ACK numbers | Byte ordering and cumulative acknowledgement | `p0448:c01`, `p0461:c01`–`p0464:c01` |
| ARQ | Ack/timer/retransmission reliability family | `p0452:c01`–`p0460:c01` |
| Stop-and-Wait | One outstanding unit | `p0453:c01`–`p0454:c01` |
| Go-Back-N | Send window + cumulative ACK/retransmit tail | `p0456:c01`–`p0458:c01` |
| Selective Repeat | Send/receive windows + individual recovery | `p0458:c01`–`p0460:c01` |
| Receiver window | TCP flow-control advertisement | `p0462:c01`–`p0465:c01` |
| Retransmission timeout | Recovery timer based on RTT estimate | `p0464:c01`–`p0466:c01` |
| SACK | Selective acknowledgement extension | `p0464:c01` |
| Congestion window | Sender-side network-load control | `p0466:c01`–`p0469:c01` |
| Slow Start | Classical cwnd growth/recovery algorithm | `p0468:c01`–`p0469:c01` |
| ECN | Explicit congestion notification | `p0469:c01`–`p0470:c01` |
| CUBIC / BBR / HyStart++ / Westwood+ / MPTCP | TCP evolution examples in source table | `p0470:c01`–`p0471:c01` |

## Operational boundary

For a real transport incident these remain **[Needs confirmation]**:

- operating system/kernel version;
- actual listening sockets and established connections;
- packet-capture evidence;
- TCP state machine;
- receive/send buffer sizes;
- `rwnd`, `cwnd`, MSS;
- retransmission timer/RTT estimate;
- selected congestion-control algorithm;
- SACK/ECN negotiation;
- application retry semantics for UDP.

No command syntax is invented.
