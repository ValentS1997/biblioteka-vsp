# Commands and tools — глава 11 (safe classification)

Source: PDF pp. 298–323. No deauthentication, evil-twin, credential capture or Bluetooth exploitation was executed.

## Safe / lower-risk observation

- Wireshark monitor-mode capture on an **authorized** wireless interface: local interface state changes, then passive observation.
- OS wireless-network list: local discovery view.
- Kismet / WiFi Explorer / NetSpot: wireless survey tools named by source; passive/active behavior depends on tool/mode and must be verified before use.
- Wireshark/tcpdump on an existing monitor interface: capture-only use can expose third-party metadata/content and requires scope/privacy controls.
- Bluetooth device list via normal OS pairing/discovery UI: local discovery; actual radio probing depends on mode.

## State-changing local operation

Source uses Aircrack-ng tooling to put an adapter into monitor mode. This can disable or interfere with normal managed-mode connectivity and network-manager processes. Exact source command is not promoted as a production command; adapter/driver/OS-specific rollback must be known first.

## High-risk source material — intentionally not operationalized

The source includes executable examples for:
- Wi‑Fi deauthentication;
- evil-twin / rogue AP behavior;
- hidden-SSID/brute probe behavior;
- WEP/key-related capture/cracking;
- disruptive wireless testing;
- active Bluetooth enumeration and attack classes.

These can disconnect clients, impersonate networks, collect credentials/data or cause denial of service. Artifact policy: preserve tool names, effects and defensive implications without a runnable attack sequence.

## Effects / risks / verification

**Risks:** wireless outage, client reconnect loops, privacy exposure, third-party radio interaction, credential interception, battery/device impact.  
**Verification:** exact owned AP/client/Bluetooth device, channel, test window and recovery path — **[Needs confirmation]**.  
**Rollback:** return adapter/AP/client to normal state and verify association/connectivity; exact environment commands **[Needs confirmation]**.
