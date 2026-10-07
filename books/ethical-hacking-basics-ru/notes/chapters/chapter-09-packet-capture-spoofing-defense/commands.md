# Commands and tools — глава 9 (safe capture subset)

Source: PDF pp. 246–273. Only capture/read/filter operations are reproduced. Spoofing/MITM attack commands from section 9.2 are intentionally not operationalized.

## Source-confirmed capture/read commands

| Source form | Classification | Note |
| --- | --- | --- |
| `tcpdump` | local/network observation | default capture; may perform name resolution |
| `tcpdump -n` | local/network observation | source uses it to suppress address-to-name DNS resolution |
| `tcpdump -vv -s 0` | local/network observation | more verbose, full snap length in source example |
| `tcpdump -i <AUTHORIZED_IFACE> -X` | local/network observation, payload-visible | hex/ASCII output may expose sensitive contents |
| `tcpdump not port 22` | capture filter | source example to exclude SSH noise |
| `tcpdump tcp and \(host <AUTHORIZED_HOST>\)` | capture filter | source BPF example, parameterized target |
| `tshark` | local/network observation | source warns against unnecessary root execution |
| `tshark -Tfields -e frame.number -e ip.src -e ip.dst -e ip.tos -e ip.ttl` | local/network observation | field-selective display |

Source also describes `-w` for writing PCAP and `-r` for reading it back. File path, interface and retention are environment-specific **[Needs confirmation]**.

## GUI / network infrastructure

- Wireshark: capture, display filtering, Follow Stream, protocol hierarchy, endpoints/statistics and expert analysis.
- SPAN/port mirroring: switch configuration used to deliver copied traffic to a monitoring port; this is **state-changing network configuration** and requires a switch-specific rollback plan.
- Windump: source names it as a Windows port of tcpdump.

## High-risk material — not operationalized

Section 9.2 includes tools/steps for ARP poisoning, DNS redirection, DHCP exhaustion/rogue configuration and HTTPS-stripping/MITM. Exact commands/configuration are not reproduced because they can intercept or redirect third-party traffic and disrupt address assignment.

## Risks / verification / rollback

**Risks:** privacy exposure, credential/token capture, disk growth, packet loss, capture-filter evidence loss, switch oversubscription.  
**Verification:** confirm interface, packet counters, timestamps and expected test traffic.  
**Rollback:** stop capture; for SPAN/mirror configuration use approved switch rollback — **[Needs confirmation]**.
