# Diagram — глава 15: TCP/UDP transport model

```mermaid
flowchart TD
    APP[Application data] --> PORT[Port / socket demultiplexing]
    PORT --> CHOICE{UDP or TCP?}

    CHOICE --> UDP[UDP]
    UDP --> DGRAM[One message → one datagram]
    DGRAM --> UHDR[8-byte header + checksum]
    UHDR --> IP1[IP]
    UDP --> UFAIL[No delivery/reorder recovery]

    CHOICE --> TCP[TCP]
    TCP --> CONN[SYN → SYN+ACK → ACK]
    CONN --> STREAM[Duplex byte stream]
    STREAM --> SEQ[Sequence numbers + cumulative ACK]
    SEQ --> RWND[Receiver window / flow control]
    SEQ --> RTO[RTT estimate + retransmission timer]
    SEQ --> SACK[SACK / selective recovery]
    RWND --> LIMIT[Send limit]
    RTO --> LIMIT
    SACK --> LIMIT
    TCP --> CWND[Congestion window]
    CWND --> LIMIT
    LIMIT --> SEND[min(rwnd, cwnd) concept]
    SEND --> IP2[IP]

    CWND --> SS[Slow Start / duplicate ACK / loss response]
    CWND --> ECN[ECN explicit congestion signal]
```

## Reliability progression

```text
Stop-and-Wait
  → simple, one outstanding unit

Go-Back-N
  → multiple outstanding
  → cumulative ACK
  → timeout can retransmit the missing unit + later unacknowledged units

Selective Repeat
  → receiver buffers out-of-order valid data
  → individual/selective ACK
  → retransmit only missing/expired units

TCP
  → byte-oriented window
  → cumulative ACK + optional SACK
  → adaptive retransmission timing
```

## Two independent limits

```text
rwnd = receiver capacity / flow control
cwnd = sender estimate of safe network load / congestion control

effective send allowance is constrained by both
```

Provenance: `p0442:c01`–`p0471:c01`.
