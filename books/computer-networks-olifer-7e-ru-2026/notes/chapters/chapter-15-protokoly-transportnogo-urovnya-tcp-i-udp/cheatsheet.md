# Cheatsheet — глава 15: TCP и UDP

## Symptom / problem framing

**Проблема:** transport failure can be application demultiplexing, UDP loss/corruption, TCP connection-state failure, receive-window pressure, retransmission/RTT behavior or network congestion. “IP is reachable” does not prove that a transport endpoint is usable. `p0442:c01`–`p0471:c01`.

## Baseline / context

| Mechanism | Source role |
| --- | --- |
| Port | Application-facing transport identifier |
| Socket | `IP address + transport port` endpoint abstraction |
| UDP | Message-oriented best-effort transport |
| TCP | Reliable duplex byte stream |
| Sequence number | First data-byte number in a TCP segment |
| ACK number | Next expected byte for cumulative stream acknowledgement |
| Receiver window | Endpoint flow-control limit |
| Retransmission timer | Loss/recovery timing |
| Congestion window | Sender-side network-load limit |
| SACK | Selective acknowledgement extension |
| ECN | Explicit congestion signalling |

## Read-only checks

1. Which protocol is actually used: TCP or UDP?
2. What local/remote IPs and ports identify the communication?
3. For TCP: is the expected connection established, opening, closing or reset?
4. Are SYN/SYN-ACK/ACK exchanges completing?
5. Are sequence/ACK numbers advancing?
6. Are duplicate ACKs or retransmissions visible?
7. What receiver window is being advertised? Is it zero or shrinking?
8. What RTT/retransmission behavior is observed?
9. Is loss correlated with timeout, duplicate ACKs or explicit congestion signalling?
10. For UDP: are application messages leaving and arriving as independent datagrams?
11. Is UDP checksum failure/drop suspected?
12. Actual socket table, packet capture, OS TCP state, cwnd/rwnd and algorithm: **[Needs confirmation]**.

## Interpretation

- **Port reachability is transport/application-specific.** IP reachability alone does not identify a listening/usable transport endpoint.
- **UDP preserves messages but does not supply retransmission/reordering guarantees.** Application requirements above UDP remain outside this chapter's UDP service.
- **TCP does not preserve application message boundaries.** It carries a byte stream segmented for transport purposes.
- **A TCP connection is not identified by server port alone.** Source model identifies it by the two endpoint sockets.
- **ACK number advances only across contiguous received bytes in the basic cumulative model.** Out-of-order data beyond a gap does not move the cumulative boundary.
- **Receiver-window pressure is not the same as network congestion.** `rwnd` is receiver/flow control; `cwnd` is sender/network congestion control.
- **The active send limit is constrained by both.** Source expresses this as `min(rwnd, cwnd)`.
- **A retransmission does not by itself tell you why a packet was lost.** The source discusses endpoint pressure, network congestion and other loss/delay causes.
- **Duplicate ACKs can allow recovery before timeout.** The source uses the three-duplicate-ACK case.
- **ECN is a congestion signal, not a delivery acknowledgement.**

## Next action

For a TCP incident:

**identify 4-tuple/socket pair → verify handshake → inspect sequence/ACK continuity → inspect rwnd → correlate retransmissions with RTT/duplicate ACK/timeout → inspect congestion signals/cwnd context → only then change transport/network tuning**.

For UDP:

**identify socket → verify datagram emission/arrival → check checksum/drop evidence → move to application-level retry/semantics only if the application actually implements them**.

## Modifying action

The chapter describes no executable tuning/configuration syntax.

Potential state-changing areas include:

- application binding/listening port;
- socket/connection parameters;
- receive-buffer/window sizing;
- retransmission/congestion-control algorithm;
- ECN enablement/behavior.

Exact OS commands, sysctls, defaults and rollback are **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- distinguish port, socket and TCP connection;
- compare UDP datagram service with TCP byte-stream service;
- name major TCP header flags and their purposes;
- explain SYN/SYN-ACK/ACK setup and FIN-based close at source level;
- explain Stop-and-Wait, Go-Back-N and Selective Repeat;
- explain cumulative ACK and SACK;
- explain TCP byte-based sliding window;
- distinguish `rwnd` from `cwnd`;
- explain retransmission timeout vs RTT;
- explain Slow Start and duplicate-ACK recovery conceptually;
- explain ECN as explicit congestion signalling.

## Rollback

For chapter artifacts — **[Not applicable]**. For production transport tuning rollback must restore previous socket/buffer/congestion-control/ECN settings. Exact procedure: **[Needs confirmation]**.
