# Cheatsheet — глава 9: packet capture and spoofing detection

## Symptom / problem framing

Нужно понять, что реально происходит в сети: какие frames/packets проходят через интерфейс, какие protocol fields и flows подтверждают проблему, и есть ли признаки interception/spoofing. Capture itself can expose sensitive traffic and must stay within approved scope.

## Baseline / context

| Область | Source framing |
| --- | --- |
| tcpdump/tshark | CLI capture/decoding |
| Wireshark | GUI capture, decode, streams, statistics, expert information |
| PCAP | saved capture for later analysis |
| BPF | capture-time filtering |
| Display filter | post-capture view filtering |
| SPAN | switch port mirroring |
| PROMISC | interface may accept frames not addressed to its MAC |
| Spoofing indicators | unsolicited ARP, unexpected DHCP, route/source anomalies |

## Read-only checks

1. Какой interface и VLAN/network разрешены для capture? [Needs confirmation].
2. Нужен ли full-packet payload или достаточно headers/snaplen? [Needs confirmation].
3. Куда сохраняется PCAP и кто имеет к нему доступ? [Needs confirmation].
4. Может ли capture содержать credentials/tokens/PII? [Needs confirmation].
5. Нужен ли capture filter, и не исключит ли он evidence, которое понадобится позже?
6. Есть ли baseline ARP/DHCP/DNS behavior для сравнения? [Needs confirmation].

## Interpretation

- Capture filter ≠ display filter: BPF at capture time can permanently omit data from saved PCAP.
- Name resolution by capture tooling may itself create DNS traffic; this can contaminate interpretation.
- PROMISC flag is not uniformly visible across OSes; absence of the flag is not proof that no capture occurs.
- Unsolicited ARP replies/high ARP volume are indicators, not automatic attribution to a specific host/user.
- Unexpected DHCP offers or many uncompleted DHCPDISCOVER events can indicate abuse but require context.
- Wireshark-calculated fields/expert warnings are analysis aids, not automatic root cause.

## Next action

For troubleshooting/defense: **define scope → capture minimally sufficient evidence → preserve raw PCAP → analyze with display filters/streams/statistics → correlate with switch/DHCP/DNS/log data → report finding with uncertainty**.

## Modifying action

Packet capture normally does not modify target configuration, but it can be privacy-sensitive and resource-consuming. Port mirroring changes switch configuration. Spoofing/MITM/DHCP-exhaustion/traffic-redirection are active disruptive actions and are not operationalized here.

## Verification / acceptance checks

- Capture interface/time window/scope documented.
- Raw PCAP preserved unchanged; analyst copy used for filtering if necessary.
- Capture filter documented so missing traffic is explainable.
- Tool-induced DNS traffic considered.
- Findings correlate with at least one independent source where possible.
- Sensitive captures stored/retained according to policy: [Needs confirmation].

## Rollback

Stopping capture ends new collection; already captured sensitive data still requires secure retention/deletion policy. Port-mirroring rollback is switch-specific and **[Needs confirmation]**. Spoofing-side rollback is not applicable because offensive sequences are not executed here.
