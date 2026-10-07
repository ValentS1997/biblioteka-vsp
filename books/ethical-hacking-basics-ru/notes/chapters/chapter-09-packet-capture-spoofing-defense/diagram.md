# Диаграммы — глава 9

## 1. Capture → preserve → analyze

```mermaid
flowchart TD
  S["Authorized interface / SPAN"] --> C["Capture"]
  C --> F{"Capture filter?"}
  F -->|Yes| P["PCAP contains only matching traffic"]
  F -->|No| A["Full permitted capture"]
  P --> R["Preserve raw PCAP"]
  A --> R
  R --> D["Display filters / streams / statistics"]
  D --> E["Evidence + interpretation"]
```

## 2. Capture filter vs display filter

```mermaid
flowchart LR
  NET["Network frames"] --> BPF["BPF capture filter"]
  BPF --> PCAP["Saved PCAP"]
  PCAP --> DF["Wireshark display filter"]
  DF --> VIEW["Visible subset"]
  BPF -. "non-matching frames lost" .-> DROP["Not stored"]
```

## 3. Defensive spoofing signals

```mermaid
flowchart TD
  ARP["Many unsolicited ARP replies"] --> COR["Correlate with switch MAC/port"]
  DHCP["Unexpected DHCP offers or discovery flood"] --> COR
  IP["Unexpected source/interface path"] --> RPF["Reverse-path / routing check"]
  DNS["Suspicious DNS behavior"] --> DSEC["Resolver policy / DNSSEC / logs"]
  COR --> INV["Investigate"]
  RPF --> INV
  DSEC --> INV
```

## 4. Sniffer detection uncertainty

```mermaid
flowchart TD
  P["PROMISC flag visible?"] --> Q{"OS exposes it?"}
  Q -- "Yes" --> I["Possible local capture indicator"]
  Q -- "No/unknown" --> U["Cannot conclude"]
  DNS["Extra reverse DNS lookups"] --> H["Heuristic only"]
  ARP["ARP spoofing indicators"] --> H
  H --> V["Require independent validation"]
```

Source basis: `p0246:c01`–`p0273:c01`.
