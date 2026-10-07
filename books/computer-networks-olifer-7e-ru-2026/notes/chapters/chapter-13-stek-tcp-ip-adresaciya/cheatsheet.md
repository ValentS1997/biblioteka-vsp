# Cheatsheet — глава 13: TCP/IP и адресация

## Symptom / problem framing

**Проблема:** “сеть не работает” на TCP/IP часто распадается на несколько разных address-resolution failures: wrong IP/prefix, wrong next-hop/local mapping, DNS failure or DHCP configuration failure. Проверять их нужно отдельно. `p0365:c01`–`p0398:c01`.

## Baseline / context

| Layer / service | Source role |
| --- | --- |
| IP | Network-layer identity and inter-network packet delivery |
| Local link address | Delivery within one directly connected technology/domain |
| ARP | IPv4 next-hop → local/MAC mapping |
| DNS | Symbolic name → IP mapping; reverse zone supports IP → name |
| DHCP | Automated host/interface configuration |
| TCP / UDP | Transport above IP |
| Prefix/mask | Defines network vs host portion of IPv4 address |

## Read-only checks

1. What IPv4 address and prefix/mask are expected on the interface?
2. Does the address belong to the intended subnet?
3. What is the expected default router/gateway?
4. Is the destination on-link or reachable through a next hop?
5. Does the ARP cache contain the expected IP→MAC mapping for the next hop?
6. If ARP is missing, is broadcast reachability on the local L2 segment intact?
7. Does DNS resolve the required name? Is the answer authoritative or cached?
8. Is reverse DNS expected, and does an `in-addr.arpa` record exist?
9. Which DNS server is configured on the host?
10. Is addressing static or DHCP-derived?
11. For DHCP: is the client local to the server or dependent on a relay?
12. Lease/pool/default-router/DNS options and actual client state: **[Needs confirmation]** on a real network.

## Interpretation

- **IP address and MAC address are not substitutes.** IP gives network-layer identity across the internetwork; MAC/local address is only meaningful on the current local technology. `p0370:c01`–`p0381:c01`.
- **A correct IP address with a wrong prefix is still wrong configuration.** The prefix determines which destinations are treated as local versus reached through a router.
- **ARP failure is an L2/local-next-hop problem before it is a DNS problem.** ARP resolves the local address needed to build the next frame. `p0381:c01`–`p0384:c01`.
- **ARP cache entries can age.** Stale or absent dynamic mappings must be distinguished from static entries. `p0384:c01`.
- **DNS success does not prove packet reachability.** Name resolution produces addresses; IP routing/local-link delivery must still work.
- **Authoritative and cached DNS answers have different provenance.** Cached data can remain until its configured lifetime expires. `p0390:c01`–`p0392:c01`.
- **DHCP is configuration distribution, not reachability itself.** A client may receive address/mask/gateway/DNS successfully and still have another network-layer fault.
- **DHCP relay changes server location, not the client’s local broadcast behavior.** The relay forwards discovery toward a remote server. `p0396:c01`–`p0397:c01`.
- **Dynamic addresses complicate identity-based operations.** Monitoring/security/DNS workflows may require stable addressing for infrastructure endpoints. `p0398:c01`.

## Next action

For a generic IPv4 addressing incident:

**capture IP/prefix/gateway/DNS → determine on-link vs routed destination → verify ARP next-hop mapping → verify IP reachability → verify DNS mapping/provenance → verify DHCP lease/relay only if configuration is DHCP-derived**.

This is a source-grounded sequence; exact commands depend on OS/device.

## Modifying action

Source-described state-changing operations include:

- manually assigning an IPv4 address/mask/gateway/DNS settings;
- adding a static ARP mapping with the `arp` utility;
- editing DNS zone data on the primary server;
- configuring DHCP pools/leases/relay;
- changing static vs dynamic address assignment.

Executable syntax, current config and rollback are **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- name the four TCP/IP layers and their roles;
- explain packet vs frame and hop-by-hop re-encapsulation;
- distinguish local address, IP address and domain name;
- explain IPv4 mask/prefix semantics;
- explain private/public address scopes and CIDR;
- describe ARP request/reply/cache behavior;
- distinguish ARP / RARP / Proxy-ARP conceptually;
- explain resolver/server/zone/authoritative/cache DNS concepts;
- compare iterative vs recursive DNS resolution;
- explain reverse DNS;
- trace DHCP discovery → offers → request → acknowledgement without assuming vendor-specific behavior.

## Rollback

For chapter artifacts — **[Not applicable]**. For production changes rollback must restore prior IP/prefix/gateway/DNS, ARP static entries, zone data or DHCP pool/relay state. Exact procedure: **[Needs confirmation]**.
