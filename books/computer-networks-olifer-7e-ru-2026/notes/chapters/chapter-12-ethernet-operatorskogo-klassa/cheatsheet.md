# Cheatsheet — глава 12: Ethernet операторского класса

## Symptom / problem framing

**Проблема:** provider Ethernet service может быть down/degraded even when local access link is physically up. Fault domain may be service classification, maintenance-domain continuity, provider VLAN encapsulation, path protection or physical section quality. `p0351:c01`–`p0360:c01`.

## Baseline / context

| Layer / mechanism | Source role | RAG |
| --- | --- | --- |
| CE / UNI | Customer edge and provider-facing Ethernet service boundary | `p0351:c01` |
| CFM | Connectivity/fault monitoring for Ethernet service | `p0354:c01`–`p0357:c01` |
| MEP | Maintenance endpoint; generates/receives CCM | `p0354:c01`–`p0357:c01` |
| MIP | Intermediate observation/localization point | `p0354:c01`–`p0356:c01` |
| Y.1731 | Delay/variation/loss measurement | `p0357:c01` |
| Physical remote loopback | Direct-link quality test | `p0357:c01` |
| E-LMI | CE query of service status/parameters | `p0358:c01` |
| C-VID / S-VID | Customer/provider VLAN identifiers | `p0358:c01`–`p0360:c01` |
| Q-in-Q | Stack provider VLAN outside customer VLAN | `p0358:c01`–`p0359:c01` |
| PBB | Stronger provider/customer address separation in source | `p0360:c01` |

## Read-only checks

1. Which service is affected: one customer VLAN/service or all services on the UNI?
2. CE and UNI link operational state: **[Needs confirmation]**.
3. Which maintenance domain and level is expected for customer/provider/operator?
4. Which MEP pair defines the monitored service?
5. Are CCMs received in both directions? Exact CCM interval/alarm state: **[Needs confirmation]**.
6. At which MIP does CCM visibility disappear?
7. If performance degradation: one-way delay, delay variation and frame-loss measurements available?
8. What is C-VID → S-VID mapping on ingress PE?
9. Is the expected S-VID preserved through provider core and removed on egress?
10. Does provider core still need to learn customer MACs for this service model?
11. E-LMI service state/bandwidth/VLAN mapping: **[Needs confirmation]** on actual platform.
12. Underlying path protection/traffic-engineering state: **[Needs confirmation]**.

## Interpretation

- **Link up does not prove service continuity.** CFM exists to test the logical Ethernet service between maintenance endpoints.
- **MEP and MIP are different roles.** MEP terminates/generates maintenance traffic; MIP helps localize by observing transit maintenance traffic. `p0354:c01`–`p0356:c01`.
- **CFM is active monitoring.** Missing CCM indicates a maintenance-session problem/path failure, not absence of user payload alone. `p0354:c01`.
- **Maintenance levels are administrative boundaries.** Higher-level domains pass through lower-level domains according to the source hierarchy model. `p0356:c01`–`p0357:c01`.
- **Y.1731 moves from “is it reachable?” toward “how well is it performing?”.** `p0357:c01`.
- **Remote loopback is not read-only in operational impact.** It disrupts normal traffic and must be treated as a maintenance action. `p0357:c01`.
- **Q-in-Q separates VLAN ID spaces, not necessarily MAC address spaces.** Provider Bridge still learns customer MACs in the source-described limitation. `p0358:c01`–`p0360:c01`.
- **Provider tag is service context.** The core primarily uses S-VID while preserving inner C-VID for the customer. `p0358:c01`–`p0359:c01`.

## Next action

For Carrier Ethernet troubleshooting:

**identify CE/UNI service → verify CFM maintenance domain/MEPs → locate failure via MIP visibility → check Y.1731 performance if service is degraded → verify C-VID/S-VID mapping → trace provider forwarding/protection → only then perform disruptive physical loopback if justified and scheduled**.

## Modifying action

The chapter describes no executable vendor CLI. The following actions are state-changing or service-affecting:

- configure MEP/MIP/domain levels;
- alter C-VID/S-VID mapping;
- change provider bridge service classification;
- trigger remote physical loopback;
- change path/protection configuration.

Before any production change: capture before-state, define expected impact and rollback. Exact procedure: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- explain why classic LAN Ethernet lacks carrier-grade functions;
- distinguish service Ethernet from provider internal transport;
- explain CE/UNI boundary;
- explain MEP vs MIP and CCM behavior;
- describe multidomain maintenance-level hierarchy;
- distinguish CFM continuity from Y.1731 performance monitoring;
- explain why remote loopback is disruptive;
- explain E-LMI purpose;
- trace Q-in-Q insertion/removal and C-VID/S-VID roles;
- explain Provider Bridge scaling limits and why stronger encapsulation/routing mechanisms are needed.

## Rollback

For chapter artifacts — **[Not applicable]**. For production service changes rollback must restore previous maintenance-domain settings, service/VLAN mapping, bridge/path state and disable any loopback test; exact platform procedure: **[Needs confirmation]**.
