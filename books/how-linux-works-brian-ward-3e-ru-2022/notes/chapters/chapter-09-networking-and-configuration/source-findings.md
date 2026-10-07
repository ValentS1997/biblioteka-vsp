# Source findings — глава 9 «Сеть и ее конфигурация»

**Scope:** `p0270:c01`–`p0319:c01`, PDF/печатные страницы 270–319. Политика **rag_only**: варианты источника сохраняются; внешняя документация и model memory не используются для тихого исправления.

## F-01 — [Source contradiction]: IPv6 bit/byte count

- **Locator:** `p0279:c01`, §9.7.
- Source phrase: IPv6 address has **128 bits — 32 bytes**.
- **Conflict:** 128 bits and 32 bytes are arithmetically inconsistent descriptions of the same address length.
- **Decision:** artifacts retain the source's 128-bit statement and do not propagate the 32-byte value as a verified technical fact. Exact intended byte count in the edition: **[Needs confirmation]**.

## F-02 — [Source wording/code mismatch]: route destination typo

- **Locator:** `p0286:c01`, §9.11.2.
- The worked example repeatedly discusses destination network **`192.168.45.0/24`** and command:
  `ip route add 192.168.45.0/24 via 10.23.2.44`.
- A following prose sentence refers instead to **`192.163.45.0/24`**.
- **Decision:** do not treat both prefixes as equivalent. Command inventory preserves the explicit command and records the prose variant here. Real target prefix: **[Needs confirmation]**.

## F-03 — [Source wording/code mismatch]: IPv6 neighbor protocol named as UDP

- **Locator:** `p0316:c01`, §9.26, boxed subsection «IPv6: NDP».
- Heading and surrounding text identify **Neighbor Discovery Protocol (NDP)** for IPv6 and describe neighbor solicitation/advertisement.
- One sentence says the `ip` command combines **ARP with IPv4 and UDP with IPv6**.
- **Mismatch:** `UDP` is inconsistent with the NDP terminology in the same boxed section.
- **Decision:** chapter artifacts describe IPv6 neighbor discovery as NDP because that is the explicit section subject; the anomalous `UDP` token is preserved only in this finding. Silent correction of the source line is not performed.

## F-04 — [Source extraction issue]: embedded annotation/line-wrap artifacts

Examples in the retrieved text include:
- `p0280:c01`–`p0281:c01`: numbered markers ❶/❷/❸ embedded in route output;
- `p0284:c01`: markers ❶/❷ embedded in `ip address show` output;
- `p0298:c01`: phrase containing an isolated `r` in the client/server explanation;
- several paths such as `/etc/resolv.conf` are split visually across extraction line boundaries.

**Decision:** structural annotation markers are omitted from normalized command examples when surrounding prose clearly identifies them as editorial callouts. Ambiguous tokens are not reconstructed unless repeated unambiguously elsewhere.

## F-05 — [Source extraction issue]: original network figures are not multimodal RAG objects

The chapter references figures **9.1–9.7**, including:
- LAN/router topology;
- network with IP addresses;
- IPv6 subnet/interface identifier;
- TCP message flow;
- multi-subnet Linux router;
- incoming/local-process firewall flow diagrams.

`rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal RAG objects.

**Decision:** Mermaid/SVG artifacts reconstruct only text-confirmed relationships. Exact original geometry, labels and arrows remain **[Needs confirmation]**.

## Current-system applicability

IP addresses, prefixes, interface names, gateways, DNS servers, MAC addresses, ports, NetworkManager plugin choices, firewall policies and Wi-Fi names in the chapter are examples. Values for a real host remain **[Needs confirmation]**.
