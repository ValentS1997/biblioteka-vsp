# Commands and tools — глава 17 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0514:c01` … `p0545:c01`, PDF pp. 514–545.

## Executable commands

**Исполняемые shell/router/vendor commands в границе главы не обнаружены.**

Do not inject from model memory:

- `ip -6 addr`, `ip -6 route`, `ip -6 neigh`;
- `ping -6`, `traceroute6`;
- router-advertisement daemon syntax;
- DHCPv6 server/client syntax;
- GRE/6to4 tunnel commands;
- NAT64/DNS64 configuration commands.

## Source-confirmed IPv6 objects and mechanisms

| Object | Role | RAG |
| --- | --- | --- |
| IPv6 128-bit addressing | Expanded network-layer address space | `p0515:c01`–`p0523:c01` |
| Unicast / anycast / multicast | IPv6 address classes in source | `p0516:c01`–`p0523:c01` |
| Link-local / ULA / global addresses | Different address scopes | `p0518:c01`–`p0520:c01` |
| Solicited-node multicast | Targeted multicast for local discovery | `p0521:c01`–`p0522:c01` |
| Base header / extension headers | Fixed base + optional chained functions | `p0523:c01`–`p0527:c01` |
| Hop Limit | IPv6 lifetime/hop bound | `p0525:c01` |
| Path-MTU / endpoint fragmentation | Avoid transit-router fragmentation | `p0527:c01` |
| ICMPv6 | Errors/diagnostics and ND carrier | `p0528:c01`–`p0529:c01` |
| Router Solicitation / Advertisement | Discover routers/prefix/config data | `p0529:c01`–`p0530:c01` |
| Neighbor Solicitation / Advertisement | DAD and link-layer resolution | `p0529:c01`–`p0534:c01` |
| Redirect | Local routing hint in ND family | `p0530:c01` |
| Duplicate Address Detection | Verify tentative address uniqueness | `p0531:c01`–`p0532:c01` |
| Dual stack | Parallel IPv4/IPv6 stacks | `p0537:c01`, `p0541:c01`–`p0542:c01` |
| Translation | Convert between incompatible protocol stacks | `p0538:c01`, `p0543:c01`–`p0545:c01` |
| Tunneling | Encapsulate passenger protocol across transit protocol | `p0539:c01`–`p0543:c01` |
| GRE / 6to4 | Transition/tunnel examples named by source | `p0543:c01` |
| NAT64 / DNS64 | IPv6-only↔IPv4-only translation example | `p0543:c01`–`p0545:c01` |

## Source-described message flow — not executable CLI

### Neighbor Discovery

```text
host → Router Solicitation
router → Router Advertisement

host → Neighbor Solicitation
neighbor → Neighbor Advertisement
```

The same NS/NA family is used in the source both for Duplicate Address Detection and for IPv6→link-layer address resolution.

### NAT64/DNS64

```text
IPv6-only client
  → DNS64 synthesizes IPv6 destination representing IPv4 server
  → route sends packet to NAT64
  → NAT64 translates IPv6 header/address+port state to IPv4
  → IPv4 server
  → reverse translation on reply
```

## Operational boundary

For a real system these remain **[Needs confirmation]**:

- interface addresses and source-address policy;
- RA flags/prefix lifetimes/default-router preference;
- DHCPv6 use and lease/options;
- ND cache/DAD state;
- MTU and ICMPv6 filtering;
- DNS A/AAAA answers;
- native/dual-stack/tunnel topology;
- NAT64 prefix, mapping state and DNS64 behavior.

No platform syntax is invented.
