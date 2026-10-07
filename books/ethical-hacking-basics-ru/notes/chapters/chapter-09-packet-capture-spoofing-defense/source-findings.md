# Source findings — глава 9

Canonical source: PDF pp. 246–273, SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`. Policy: `rag_only`.

## F-01 — [Observation side effect] Capture tooling generates DNS traffic

- `p0248:c01`, `p0255:c01`: source shows tcpdump resolving addresses to hostnames, producing additional DNS lookups.
- Impact: analyst tooling can change the traffic being observed and contaminate a capture.
- Source mitigation: `tcpdump -n` suppresses name resolution in the example.

## F-02 — [Evidence loss risk] Capture filter vs display filter

- `p0256:c01`: source explicitly notes that frames not matching BPF capture filter are not saved.
- Impact: overly narrow capture filters can permanently remove evidence.
- Disposition: preserve raw/broad capture where policy and storage permit; use display filtering for later views when appropriate.

## F-03 — [Detection uncertainty] PROMISC visibility is OS-dependent

- `p0257:c01`: macOS example exposes `PROMISC`; Kali examples with `ifconfig`, `ip a`, `ip link` do not.
- Impact: absence of a visible promiscuous-mode flag is not proof that sniffing is absent.
- Source itself frames indirect DNS indicators as non-guaranteed.

## F-04 — [Source caveat] Crafted-packet sniffer detection is unreliable in switched networks

- `p0258:c01`: source discusses using a frame with correct IP but wrong MAC as a sniffer heuristic.
- It immediately notes that switched delivery can prevent the test frame from reaching the device, making the method unreliable.
- Disposition: retain only as a heuristic, not a deterministic test.

## F-05 — [Source wording contradiction] DNS spoofing address comparison

- `p0271:c01`: text says that matching source/destination response addresses may indicate safety and then also says non-matching addresses may indicate safety, followed by “Да, это не имеет особого смысла.”
- Disposition: do not convert this paragraph into a deterministic DNS-spoofing detection rule.

## F-06 — [Needs confirmation] TCP as DNS anti-spoofing guarantee

- `p0271:c01`: source says DNS over TCP / three-way handshake protects or substantially improves protection from spoofing.
- The chapter does not prove a universal guarantee or define threat model/resolver behavior.
- Disposition: preserve source wording as a defensive suggestion, but not as a universal security property. DNSSEC is separately discussed.

## F-07 — [Historical source material] sslstrip / tooling behavior

- `p0270:c01`: source itself says vulnerabilities enabling sslstrip have been fixed in many cases and shows historical experimental-plugin output.
- Tool/version/configuration behavior is not verified as current-2026 state.
- Disposition: keep as historical attack concept; do not reuse source configuration as current guidance.

## F-08 — [High-risk operational boundary] Spoofing / MITM / DHCP exhaustion

- `p0263:c01`–`p0270:c01` contain concrete offensive examples for ARP poisoning, DNS redirection, DHCP exhaustion/rogue DHCP and HTTPS stripping.
- These can intercept traffic, disrupt address allocation or redirect users.
- Artifacts preserve concepts, detection indicators and countermeasures but do not reproduce executable attack sequences.

## Privacy note

PCAP can contain credentials, session identifiers, internal addresses, DNS names and application content. Retention/access policy is not specified by source and remains **[Needs confirmation]**.
