# Диаграммы — глава 11

## 1. Wi‑Fi connection evidence

```mermaid
flowchart LR
  STA["Station"] --> P["Probe / discovery"]
  P --> A["802.11 authentication"]
  A --> S["Association"]
  S --> SEC["Security/authentication context"]
  SEC --> DATA["Protected data traffic"]
```

## 2. Passive observation vs disruptive testing

```mermaid
flowchart TD
  R["Authorized wireless scope"] --> O["Survey / monitor capture"]
  O --> E["Evidence: SSID/BSSID/channel/frames"]
  E --> Q{"Need disruptive validation?"}
  Q -- "No" --> REP["Report / harden"]
  Q -- "Yes" --> L{"Isolated owned lab + outage approval?"}
  L -- "No" --> STOP["Stop"]
  L -- "Yes" --> T["Controlled test"]
  T --> REC["Restore connectivity / verify"]
```

## 3. BYOD / mobile trust boundary

```mermaid
flowchart TD
  DEV["Personal/mobile device"] --> WIFI["Wireless access"]
  WIFI --> ISO["Guest / isolated segment"]
  WIFI --> AUTH["Enterprise auth / policy"]
  ISO --> RES["Restricted resources"]
  AUTH --> VPN["Additional secure access"]
  VPN --> CORP["Business resources"]
```

## 4. Bluetooth threat interpretation

```mermaid
flowchart TD
  D["Nearby Bluetooth device"] --> DISC["Discovery / pairing surface"]
  DISC --> H["Historic attack classes"]
  H --> Q{"Applicable to current device?"}
  Q -- "Unknown" --> U["[Needs confirmation]"]
  Q -- "Verified in owned lab" --> E["Evidence / remediation"]
```

Source basis: `p0298:c01`–`p0323:c01`.
