# Диаграмма: логика главы 6

```mermaid
flowchart TD
    start["Application needs process-to-process communication"] --> service{"Transport service?"}

    service --> tcp["TCP: connection + reliable ordered byte stream"]
    service --> udp["UDP: connectionless datagrams + ports"]
    service --> newer["QUIC / other transport evolution"]

    tcp --> sockets["Socket lifecycle: SOCKET → BIND/LISTEN/ACCEPT or CONNECT"]
    sockets --> transfer["SEND / RECEIVE → CLOSE"]

    tcp --> reliability["Sequence numbers + ACK + timers + retransmission"]
    reliability --> flow["Flow control: receiver window"]
    flow --> congestion["Congestion control: congestion window / AIMD"]

    udp --> appsem["Application supplies needed reliability/timers if required"]
    udp --> realtime["RTP/RTCP: media timing, jitter buffering, feedback"]

    congestion --> tcpcc["Slow start / duplicate ACK / SACK / ECN / CUBIC"]
    newer --> quic["QUIC over UDP: connection/stream evolution"]
    newer --> bbr["BBR: estimate bottleneck bandwidth + RTT"]

    tcpcc --> performance["Performance analysis"]
    quic --> performance
    bbr --> performance
    realtime --> performance

    performance --> host["Host processing: copies, context switches, fast path, timers"]
    performance --> path["Path: RTT + bandwidth-delay product + segment/window size"]
    performance --> compression["Header compression / protocol efficiency"]
```

Диаграмма отражает переход главы от transport service и connection lifecycle к reliability/flow/congestion control, затем к UDP/TCP/QUIC и итоговому performance analysis.
