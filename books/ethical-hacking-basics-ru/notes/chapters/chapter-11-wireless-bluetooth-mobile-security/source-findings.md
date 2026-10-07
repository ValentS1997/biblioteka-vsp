# Source findings — глава 11

Canonical source: PDF pp. 298–323, SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`. Policy: `rag_only`.

## F-01 — [Operational side effect] Monitor mode changes local interface state

- `p0308:c01` source notes that monitor-mode tooling can conflict with NetworkManager, wpa_supplicant and DHCP/client processes.
- Impact: normal Wi‑Fi connectivity can be lost during capture.
- Rollback commands are environment-specific and not provided as universal source guidance.

## F-02 — [Safety boundary] Deauthentication is explicitly disruptive

- `p0307:c01` warns that such wireless testing can disrupt network traffic and should not be performed against neighbors’ APs.
- `p0311:c01` and `p0315:c01`–`p0316:c01` contain executable deauth examples/exercise.
- Artifact policy: preserve learning objective and evidence criteria, not the runnable attack command.

## F-03 — [Historical/current-state caveat] KRACK wording

- `p0315:c01` says that at the time of writing few automation tools existed and patches were available, so it might no longer be a problem.
- Current device/firmware susceptibility in 2026 is not verified by the chapter RAG.
- Treat as historical source context, not current vulnerability status.

## F-04 — [Needs confirmation] BYOD does not prove absence of device controls

- `p0306:c01` suggests BYOD may mean fewer restrictions on devices.
- The same page also discusses NAC, allow-lists, guest isolation and enterprise authentication.
- Actual BYOD control model must be verified per environment.

## F-05 — [Source extraction issue] Bluetooth attack names

- `p0319:c01`/summary text visually extracts `Bluesnar ng` where the intended source term is rendered with a spacing/ligature break.
- Artifacts normalize only the category label `bluesnarfing`; exact typography is a source-extraction defect.

## F-06 — [Historical applicability caveat] Bluetooth attacks

- `p0319:c01`–`p0323:c01` explicitly says some Bluetooth attacks are old and less likely to succeed on modern devices, while legacy implementations may remain affected.
- Therefore discovering Bluetooth does not imply vulnerability.

## F-07 — [Source-era standards caveat] Wi‑Fi security descriptions

- pp. 302–306 explain WEP/WPA/WPA2/WPA3 and cryptographic details as teaching material.
- This artifact does not silently turn those descriptions into a current certification/compliance matrix.
- Current protocol requirements, approved cipher suites and deployment guidance: **[Needs confirmation]**.

## F-08 — [High-risk boundary] Evil twin / key capture / Bluetooth exploitation

- Source includes evil-twin, wireless key/capture and Bluetooth attack narratives capable of credential/data interception or denial of service.
- These remain threat-model concepts only; no operational attack workflow is reproduced.

## Defensive takeaway

Use owned/authorized radio scope, modern authentication/encryption, segmentation, controlled BYOD, passive monitoring where possible, mobile app provenance controls and explicit recovery planning for disruptive wireless tests.
