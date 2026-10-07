# Source findings — глава 6

Canonical source: `ethical-hacking-basics-ru`, PDF pp. 140–168, SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`. Режим `rag_only`.

## F-01 — [Source extraction issue] BaRMIe output contains embedded markup

- Source: `p0147:c01`, PDF p. 147.
- Extracted terminal text contains XML/line-markup fragments inside the program output.
- Exact console output cannot be treated as clean verbatim evidence.
- Artifact policy: retain only the high-level fact that BaRMIe is shown for RMI enumeration; exact output formatting is **[Needs confirmation]**.

## F-02 — [Source wording ambiguity] SNMPv2 vs SNMPv2c

- `p0158:c01` distinguishes SNMPv2 and SNMPv2c, noting that v2c retains community strings.
- `p0159:c01` later gives defensive advice using a broader phrase about replacing older SNMP versions.
- This can blur the distinction between v2 and v2c.
- Artifacts preserve the source framing without inventing a standards matrix. Current implementation requirements: **[Needs confirmation]**.

## F-03 — [Historical data] tool/version/count examples are dated

- nmap, Metasploit, WordPress/WPScan and OS/version outputs across pp. 141–167 are historical demonstrations.
- p. 150 mentions a count of SMB NSE scripts in the then-current installation.
- These values are not current-2026 inventory facts.

## F-04 — [Source/output anomaly] WPScan release date

- `p0166:c01` output shows WordPress 6.1.1 and a release date rendered as `0001-01-01`.
- That date is unusable as trustworthy historical evidence.
- The version/output remains only a source example; the date is not propagated as fact.

## F-05 — [Needs confirmation] SMB version inference is environment-dependent

- `p0153:c01` maps Windows release families to typical SMB versions.
- Actual protocol enablement can depend on configuration and compatibility settings.
- Do not infer host OS solely from a textbook default mapping.

## F-06 — [Sensitive operation boundary] login/user enumeration

- `p0153:c01`–`p0154:c01`, `p0161:c01`, `p0164:c01` describe protocol/module behaviors that can test identities or credentials.
- Risk: account lockout, alerts, privacy exposure and unauthorized credential testing.
- Artifacts record that the source contains these techniques but do not reproduce an executable credential-attack workflow. Authorization/lockout policy: **[Needs confirmation]**.

## F-07 — [Interpretation caveat] “Passive” detections inside WPScan

- `p0167:c01` labels some individual findings as `Passive Detection`.
- The same source output reports many HTTP requests and also aggressive checks.
- Therefore an internal detection-method label must not be interpreted as an overall passive/no-traffic scan.

## Defensive takeaway

Across SMB, SNMP, SMTP and Web, the source consistently recommends reducing exposed metadata and restricting service reachability. Relevant source pages: `p0157:c01`, `p0159:c01`, `p0162:c01`, `p0167:c01`–`p0168:c02`.
