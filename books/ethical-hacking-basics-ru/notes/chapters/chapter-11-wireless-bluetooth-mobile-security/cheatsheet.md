# Cheatsheet — глава 11: wireless / Bluetooth / mobile

## Symptom / problem framing

Нужно определить, **какие wireless identities, authentication/encryption states and radio behaviors подтверждены**, и где testing переходит от observation к disruptive interaction. Radio range does not imply authorization.

## Baseline / context

| Область | Source framing |
| --- | --- |
| Wi‑Fi identity | SSID / BSSID / probe / auth / association |
| Wi‑Fi security | WEP, WPA, WPA2, WPA3, Personal/Enterprise |
| Enterprise auth | 802.1X / EAP concepts |
| Wireless evidence | monitor mode, channel, radiotap/802.11 headers, beacons/auth frames |
| BYOD | device trust, isolation, guest networks, NAC/VPN concepts |
| Bluetooth | discovery/pairing and historic attack classes |
| Mobile | app stores, app data leakage, public Wi‑Fi, phishing/smishing |

## Read-only checks

1. Какие AP/BSSID/channels принадлежат разрешённой lab/network scope? [Needs confirmation].
2. Какой adapter/driver supports monitor mode and what local connectivity will be lost?
3. Есть ли baseline SSID/security/channel map?
4. Разрешён ли capture of nearby third-party frames/metadata? [Needs confirmation].
5. Для BYOD/mobile: кто владеет device and what policy applies? [Needs confirmation].
6. Для Bluetooth: какие devices принадлежат lab and are discoverable/pairable intentionally? [Needs confirmation].
7. Для disruptive wireless tests: outage window and recovery owner? [Needs confirmation].

## Interpretation

- SSID is a network name; BSSID identifies an AP/radio endpoint in the source model.
- Seeing a WLAN or Bluetooth device does not authorize probing.
- Monitor mode can capture management/radio frames but is channel-limited; channel hopping misses traffic on other channels.
- WEP/WPA/WPA2/WPA3 descriptions are source-era teaching material, not a current standards compliance matrix.
- Evil-twin/deauth observations are threat patterns, not proof a particular AP is malicious.
- Historic Bluetooth attack names may be obsolete against modern devices; source itself notes this.
- BYOD does not automatically mean “no device restrictions”; actual policy/NAC state must be verified.

## Next action

For defense/troubleshooting: **inventory authorized radios → capture passive evidence → validate auth/encryption configuration → correlate AP/controller/client logs → test disruptive controls only in isolated lab → document recovery and findings**.

## Modifying action

Enabling monitor mode changes the local wireless interface state and may interrupt normal connectivity. Deauth/evil-twin/active Bluetooth attack testing is disruptive/high-risk and not operationalized here.

## Verification / acceptance checks

- Authorized AP/device identifiers documented.
- Capture channel/interface/time window documented.
- Monitor-mode change is reversible and normal connectivity restored.
- Security mode/auth method observed without overclaiming patch/compliance state.
- No neighbor/third-party AP/device actively tested.
- Deauth exercise, if authorized, confined to owned lab AP/client with outage accepted.
- Actual recovery/test output: **[Needs confirmation]**.

## Rollback

For monitor mode: restore managed/normal interface operation and network-management processes; exact commands depend on OS/driver and are **[Needs confirmation]**. For AP/client disruptive tests, reconnect/restart/revert lab equipment as defined in test plan.
