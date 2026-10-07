# Диаграммы — глава 10

## 1. Social-engineering decision boundary

```mermaid
flowchart TD
  R["Request / message / visitor"] --> C{"High-risk action or sensitive data?"}
  C -- "No" --> N["Normal process"]
  C -- "Yes" --> V["Verify identity through independent channel"]
  V --> A{"Verified and authorized?"}
  A -- "No" --> S["Stop / report / preserve evidence"]
  A -- "Yes" --> P["Proceed under approved process"]
```

## 2. Influence cues are not authentication

```mermaid
flowchart LR
  I["Authority / urgency / scarcity / reciprocity"] --> T["Trust pressure"]
  B["Branding / familiar contact / social proof"] --> T
  T --> Q["Pause and verify"]
  Q --> ID["Independent identity check"]
```

## 3. Phishing artifact review

```mermaid
flowchart TD
  M["Message"] --> S["Sender/address/domain"]
  M --> L["Visible link vs actual destination"]
  M --> A["Attachment type / context"]
  M --> U["Urgency / reward / fear cues"]
  S --> E["Evidence set"]
  L --> E
  A --> E
  U --> E
  E --> R["Report / contain if confirmed"]
```

## 4. Defense-in-depth for social engineering

```mermaid
flowchart TD
  H["Human awareness"] --> D["Reduced success probability"]
  M["MFA / least privilege"] --> D
  E["Email/web filtering"] --> D
  P["Physical access controls"] --> D
  W["Wireless trust baseline"] --> D
  V["Independent verification process"] --> D
```

Source basis: `p0274:c01`–`p0297:c01`.
