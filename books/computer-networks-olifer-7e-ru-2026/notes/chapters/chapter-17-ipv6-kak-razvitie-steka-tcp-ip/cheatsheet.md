# Cheatsheet — глава 17: IPv6

## Symptom / problem framing

**Проблема:** IPv6 failure should be decomposed into address/scope selection, local Neighbor Discovery, prefix/router information, path MTU/ICMPv6 and IPv4/IPv6 coexistence. A host may have working IPv4 while one of these IPv6 layers is broken. `p0514:c01`–`p0545:c01`.

## Baseline / context

| Mechanism | Source role |
| --- | --- |
| 128-bit IPv6 address | Network-layer identity |
| Link-local address | Communication limited to one link |
| Global/ULA address | Wider or internal scope respectively |
| Solicited-node multicast | Targeted multicast used by ND |
| ICMPv6 | Errors/diagnostics + foundation for ND |
| ND | Router discovery, DAD, address resolution, redirect/config hints |
| Router Advertisement | Prefix/MTU/default-router/autoconfiguration information |
| Path MTU model | End host adapts size; router does not fragment |
| Dual stack | Independent IPv4 and IPv6 operation on one node |
| Tunnel | Carry one network protocol through another transit network |
| NAT64/DNS64 | IPv6-only ↔ IPv4-only translation model in source |

## Read-only checks

1. Which IPv6 addresses exist on the interface and what is each scope?
2. Is a link-local address present?
3. What prefix(es), default router and MTU were learned/configured?
4. Was the address accepted after Duplicate Address Detection?
5. For an on-link destination, does ND resolve the neighbor's link-layer address?
6. Are Router Solicitation / Advertisement exchanges occurring?
7. Are Neighbor Solicitation / Advertisement exchanges occurring?
8. Are ICMPv6 “packet too big” or other diagnostic messages visible?
9. Does the selected source address have a scope compatible with the destination?
10. Is the path native IPv6, dual stack, tunneled or translated?
11. For dual stack: do DNS answers expose A, AAAA or both?
12. For NAT64/DNS64: is the synthesized IPv6 destination/prefix expected?
13. Actual OS address-selection policy, RA flags, DHCPv6 state, MTU and ND cache: **[Needs confirmation]**.

## Interpretation

- **IPv6 address presence is not enough.** Scope and source-address selection must be valid for the destination.
- **Link-local reachability is a local-link property.** It does not establish global IPv6 routing.
- **ND failure is not a DNS failure.** ND resolves/validates local neighbors and routers after an IPv6 destination/next hop is known.
- **Duplicate Address Detection failure means the tentative address must not be treated as usable.**
- **Router Advertisement is control-plane input, not proof of end-to-end reachability.**
- **Path-MTU failure can look application-specific.** In the chapter model, transit routers do not fragment IPv6; endpoint adaptation depends on ICMPv6 feedback.
- **Dual-stack success on IPv4 can hide an IPv6 fault.** Determine which address family the application actually selected.
- **A tunnel does not make the transit network “IPv6-aware”.** It carries passenger packets across another transport.
- **NAT64/DNS64 introduces translation state.** DNS synthesis, routing to the translator and transport-address mapping all become separate failure points.

## Next action

For an IPv6 incident:

**inventory interface addresses/scopes → verify prefix/default-router/RA → verify DAD and ND → verify next-hop reachability → inspect ICMPv6/MTU → verify global routing → determine native/dual-stack/tunnel/NAT64 path → only then change configuration**.

## Modifying action

The chapter discusses state-changing configuration concepts but gives no executable CLI syntax:

- assigning/removing IPv6 addresses/prefixes;
- changing router-advertisement/autoconfiguration parameters;
- changing MTU;
- configuring dual stack;
- creating tunnels;
- configuring translation/NAT64/DNS64 state.

Exact platform commands, before-state capture and rollback are **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- parse and compress an IPv6 address conceptually;
- distinguish unicast / anycast / multicast and address scope;
- explain link-local, ULA and solicited-node multicast roles;
- name the IPv6 base-header fields and extension-header chain;
- explain why routers do not fragment transit IPv6 packets in the source model;
- explain ICMPv6's role relative to ND;
- trace RS/RA and NS/NA;
- explain Duplicate Address Detection;
- compare ARP-style IPv4 resolution with ND's multicast-based IPv6 resolution;
- compare dual stack, translation and tunneling;
- trace the chapter's DNS64 → NAT64 IPv6-only-to-IPv4-only example.

## Rollback

For chapter artifacts — **[Not applicable]**. For production IPv6 changes rollback must restore prior addresses/prefixes, RA/autoconfiguration policy, MTU, tunnel/translation state and DNS synthesis behavior. Exact procedure: **[Needs confirmation]**.
