# Шпаргалка: IP-маршрутизация

Цель: различать data-plane forwarding и control-plane route calculation, выбирать минимально необходимую routing strategy и проверять изменения до persistence.

## 1. Two different meanings of routing

~~~text
Forwarding
= use existing routing table
  to send one packet to next hop

Route calculation
= build/update routing table
  using config + protocols + daemons
~~~

Do not mix these layers during troubleshooting.

## 2. Next-hop routing

IP routing in chapter:

~~~text
packet destination
   ↓
routing table
   ↓
choose next hop only
~~~

Router does not need the full physical path encoded in packet.

## 3. Route-table lookup

~~~text
destination network directly connected?
  ├─ yes → send directly
  └─ no
      ↓
specific route exists?
  ├─ yes → use its gateway/interface
  └─ no
      ↓
default route exists?
  ├─ yes → send to default gateway
  └─ no  → destination unreachable
~~~

Gateway must be one hop away on a connected network.

## 4. Link header vs IP header

On router forwarding:

~~~text
Ethernet destination
changes hop by hop

IP source/destination
remain end-to-end identities
~~~

This is why a packet can be sent to router MAC while IP destination remains final host.

## 5. Inspect routing state

~~~bash
netstat -rn
ip route
~~~

Chapter notes netstat/net-tools as legacy on Linux and ip route as recommended Linux method in that publication context.

## 6. IPv4 and IPv6

Routing model is the same conceptually.

But:
- address spaces are separate;
- protocol instances/configuration may be separate;
- IPv6 has link-local routes;
- do not treat IPv4 routing config as automatically covering IPv6.

## 7. Static routing

Best fit:
- simple topology;
- one external exit;
- stable paths;
- leaf networks.

Typical client pattern:

~~~text
connected networks
+
one default route
~~~

Avoid dynamic routing when it adds no operational value.

## 8. Why dynamic routing

Needed when:
- topology is complex;
- multiple paths exist;
- links can fail and alternatives should be discovered;
- administrative boundaries require policy;
- manual route maintenance no longer scales.

## 9. Routing daemon data flow

~~~text
configuration files
       +
kernel routing table
       +
peer daemons
       ↓
routing daemon
       ↓
route calculation
       ↓
kernel routing table
       +
protocol advertisements
~~~

Topology changes cause recalculation/convergence.

## 10. Distance-vector

Concept:

~~~text
neighbor says:
network Y is cost N from me

local router derives:
network Y is cost N + local-link-cost
~~~

Advantages:
- simple;
- lightweight.

Risks:
- loops;
- slow convergence;
- frequent update traffic.

## 11. RIP / RIPng

RIP:
- distance-vector;
- hop-count metric;
- practical scale limited by fifteen-hop reachability rule;
- RIPv2 carries mask/CIDR information;
- simple and widely interoperable.

RIPng:
- RIP-family protocol for IPv6;
- runs separately from IPv4 RIPv2.

## 12. Link-state / topology protocol

Concept:

~~~text
routers advertise adjacency/link state
        ↓
each router builds topology map
        ↓
each router computes own routes
~~~

Advantages:
- faster convergence;
- can avoid routing loops;
- supports richer path calculation.

Cost:
- more CPU/memory/complexity.

## 13. OSPF

OSPF is chapter's main link-state protocol.

Features highlighted:
- large/complex networks;
- multiple routes;
- areas;
- hierarchical addressing/topology;
- IPv4 OSPFv2;
- IPv6 OSPFv3.

Use when network scale/complexity justify it.

## 14. Routing metric

~~~text
link cost + link cost + ...
= total path cost
~~~

Possible meanings:
- hop count;
- latency;
- financial/administrative cost;
- other protocol-specific metrics.

Default metrics are sufficient for most systems in chapter.

Artificially raise cost only with a clear administrative reason.

## 15. Autonomous system

~~~text
one administrative/political routing domain
= autonomous system
~~~

Interior routing:
~~~text
inside one AS
~~~

Exterior routing:
~~~text
between autonomous systems
~~~

## 16. EIGRP

Chapter describes EIGRP as:
- Cisco proprietary;
- distance-vector family with mechanisms to avoid classic loop/slow-convergence problems;
- functionally comparable to OSPF for many uses;
- separate IPv4/IPv6 routing domains.

Vendor dependence affects future interoperability.

## 17. BGP

BGP:

~~~text
exterior routing protocol
between autonomous systems
~~~

Chapter associates it with:
- Internet backbone;
- very large route tables;
- multiple upstream providers;
- policy between administrative domains.

Single-uplink routers often need only a static default route.

## 18. Multicast coordination

Routing protocols need a way to find/exchange control information with peers.

Chapter shows protocol-specific multicast addresses for router coordination.

This traffic may appear during packet capture and is not necessarily application traffic.

## 19. Strategy levels

Chapter gives four routing-management levels:

~~~text
1. no routing
2. static routing only
3. mostly static + clients receive RIP updates
4. dynamic routing
~~~

Choose the lowest complexity that meets topology requirements.

## 20. Strategy decision

~~~text
No external path?
→ no routing required

One exit?
→ static default route

Few stable internal exceptions?
→ static routes + default

Multiple alternative paths / admin boundaries?
→ dynamic routing

Internet multihoming?
→ BGP
~~~

## 21. Avoid ICMP redirects as policy

Chapter explicitly rejects relying on ICMP redirects as the main routing mechanism.

Reason:
- implementations differ;
- learned redirects can expire differently;
- behavior is inconsistent;
- correctly configured network should not depend on them.

## 22. UNIX/Linux as routers

Chapter stance:

~~~text
production infrastructure
→ prefer dedicated routers

test / sparse / auxiliary network
→ UNIX/Linux gateway can be practical
~~~

This is source-specific guidance, not expanded beyond RAG.

## 23. routed

Legacy RIP daemon.

Passive mode:

~~~text
routed -q
~~~

Behavior:
- receives routing updates;
- does not advertise its own;
- installs learned routes into kernel table.

Useful as a simple RIP receiver.

## 24. Quagga

Architecture:

~~~text
zebra
  ↕ kernel table
  ↕ routing protocol daemons
     ripd
     ripngd
     ospfd
     ospf6d
     bgpd
~~~

Each daemon has its own configuration.

## 25. Quagga CLI

Chapter names:

~~~text
Linux: vtysh
Solaris: quaggaadm
~~~

Cisco-like control flow:

~~~text
enable
config term
...
write
~~~

Do not invent protocol-specific config commands not present in RAG.

## 26. XORP

XORP aims beyond routing alone:
- packet filtering;
- traffic management;
- router-like network functions;
- multi-OS support in chapter context.

It represents the software-router idea more broadly than Quagga.

## 27. Cisco IOS access levels

Two primary levels:

~~~text
user mode
router>

privileged mode
router#
~~~

Enter privileged mode:

~~~text
enable
~~~

Privileged mode removes important safety barriers.

## 28. Cisco read-only inspection

~~~text
show interfaces
show ?
show running
show config
~~~

Use before configuration.

Compare running vs stored config before changing state.

## 29. Cisco config flow

~~~text
ssh <router>
  ↓
show current state
  ↓
enable
  ↓
config term
  ↓
select interface/config context
  ↓
make one change
  ↓
verify
  ↓
write mem
~~~

Do not persist first and troubleshoot later.

## 30. Interface address change

Chapter example:

~~~text
interface Ethernet0
ip address 192.225.40.253 255.255.255.0
~~~

High risk over remote access.

Before change:
- verify device hostname;
- verify target interface;
- verify address/mask;
- know management route;
- have physical/console fallback.

## 31. Router naming

Chapter recommends setting meaningful hostname.

Purpose:

~~~text
prompt shows device identity
→ reduces risk of changing wrong router
~~~

## 32. Configuration backup

Chapter recommends:

~~~text
scp / tftp
→ copy router configuration elsewhere
~~~

Also keep copies in NVRAM/removable storage where available.

## 33. Access security

Chapter recommends:
- SSH instead of Telnet;
- restrict CLI access;
- use interface access lists;
- physically secure routers.

Operational security is part of routing reliability.

## 34. RANCID

RANCID workflow described:

~~~text
periodically login to routers
  ↓
retrieve config
  ↓
compare changes
  ↓
store in version control
~~~

This turns interactive router state into auditable configuration history.

## 35. Troubleshooting model

~~~text
1. inspect routing table
2. identify expected specific/default route
3. verify next hop is directly reachable
4. inspect protocol/daemon if route should be dynamic
5. compare running vs persistent config
6. verify path after one change
7. persist only after acceptance
~~~

## 36. Failure interpretation

No route:

~~~text
no matching specific route
and no usable default
~~~

Wrong next hop:

~~~text
route exists
but gateway/interface is incorrect
~~~

Route disappears:

~~~text
dynamic route not refreshed
or daemon/protocol state changed
~~~

Slow recovery after failure:

~~~text
protocol convergence behavior
or unsuitable protocol/topology
~~~

Unexpected path:

~~~text
metric/policy selected different route
~~~

## 37. Acceptance criteria

After routing change:
- routing table contains intended prefix/default;
- next hop is reachable on connected network;
- IPv4/IPv6 domains are checked separately where relevant;
- dynamic route source/protocol is understood;
- no unintended route loop appears;
- end-to-end path is verified;
- management access is preserved;
- running config matches intended state;
- persistent config is written only after success;
- prior router configuration is backed up;
- rollback command is documented or marked `[Needs confirmation]`.

## 38. Source gap

`p0517:c01` is absent from RAG.

Do not infer its contents.

Available evidence already contains sections 15.1–15.7 and the beginning of 15.8 literature/RFC references.
