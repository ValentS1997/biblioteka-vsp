# Шпаргалка: сетевые аппаратные средства

Цель: проектировать и диагностировать Ethernet/Wi-Fi infrastructure от physical medium до logical segmentation, не выдавая logical configuration за proof of physical health.

## 1. Chapter model

~~~text
requirements
  ↓
medium
  ↓
physical topology
  ↓
switching / wireless access
  ↓
logical segmentation
  ↓
routing boundary
  ↓
testing
  ↓
documentation
  ↓
operations / management
~~~

## 2. Ethernet

Chapter presents Ethernet as the dominant LAN family.

Historical access model:

~~~text
CSMA/CD
Carrier Sense
Multiple Access
Collision Detection
~~~

Modern switched Ethernet reduces collision domains, but broadcast domains remain operationally important.

## 3. Broadcast domain

A broadcast domain is the set of hosts receiving link-layer broadcast traffic.

Modern switch:

~~~text
many physical point-to-point segments
        ↓
one logical Ethernet segment
        ↓
one broadcast domain
~~~

Large logical segments increase broadcast load.

## 4. UTP

Chapter uses UTP as the common Ethernet copper medium.

Relevant concerns:

- cable category;
- bandwidth;
- attenuation;
- crosstalk;
- propagation delay;
- maximum supported link rate;
- installation/termination quality;
- building/fire constraints.

For the chapter's examples, copper Ethernet links are normally limited to 100 m.

## 5. RJ-45 termination

For four-pair UTP chapter points to TIA/EIA-568A termination.

Operational principle:

~~~text
same wiring standard
at both documented endpoints
~~~

Improvised pair assignment creates hard-to-debug faults.

## 6. Fiber

Use when copper is unsuitable because of:

- distance;
- bandwidth;
- electrical interference constraints.

Chapter distinguishes:

~~~text
multimode
  → building/campus use cases
  → larger core
  → cheaper endpoint optics

single-mode
  → long-distance/backbone use cases
  → smaller core
  → precision optics
~~~

Fiber, patching and endpoint optics must match.

## 7. Hubs vs switches

Hub:

~~~text
physical-layer repeater
no frame interpretation
~~~

Switch:

~~~text
link-layer device
learns source MAC → port
forwards only where needed
~~~

Chapter treats switches as the standard Ethernet interconnect.

## 8. Switch loops

Multiple active paths can confuse plain Ethernet forwarding.

Symptom/risk:

~~~text
duplicate paths
→ frames appear on multiple ports
→ unstable forwarding / broadcast amplification
~~~

Do not build redundant physical topology without the control mechanism intended by the switch design.

## 9. Switch capacity

Vendor headline throughput is not enough.

Chapter emphasizes:

- packet forwarding rate;
- tested packet size;
- backplane capacity;
- reliability under load.

Backplane should support aggregate port capacity in a well-designed switch.

## 10. VLAN

VLAN:

~~~text
switch ports
  ↓ software grouping
logical Ethernet segment
~~~

Benefits:

- traffic isolation;
- smaller broadcast domains;
- logical topology independent of physical port placement.

Important:

~~~text
VLAN ≠ complete security boundary
~~~

Inter-VLAN traffic must be controlled by routing/filtering policy.

## 11. 802.1Q trunk

Chapter uses 802.1Q as an example of VLAN trunking.

Purpose:

~~~text
one physical inter-switch link
carries multiple logical VLANs
~~~

## 12. Routers

Router operates at network layer.

Chapter associates router with:

- forwarding based on network-layer header;
- packet filtering;
- traffic priority/QoS;
- topology functions;
- separation of logical Ethernet segments.

## 13. Autonegotiation

Two source rules:

~~~text
1 Gbit/s and faster
→ autonegotiation required

100 Mbit/s and slower
→ both ends must use consistent mode
   automatic/automatic
   or manual/manual
~~~

Bad pattern:

~~~text
one side manual
other side auto
→ speed/duplex mismatch
→ poor performance
~~~

## 14. PoE

PoE sends power and Ethernet over the same UTP infrastructure.

Plan:

- PoE-capable switch ports;
- number of powered endpoints;
- switch power budget;
- cabinet electrical load.

## 15. Jumbo frames

Standard Ethernet payload MTU in chapter:

~~~text
1500 bytes
~~~

Jumbo frames raise MTU, commonly around 9000 bytes in chapter examples.

Precondition:

~~~text
every device on the relevant subnet/path
must support the chosen size
~~~

Safe rollout:

~~~text
standard MTU
  ↓
prove reliability
  ↓
enable larger MTU consistently
  ↓
verify end-to-end
~~~

Do not mix MTU policy casually.

## 16. Wireless architecture

~~~text
wired network
   ↓
WAP
   ))) radio
clients
~~~

WAP can connect to wired infrastructure or participate in wireless mesh-like arrangements.

## 17. SSID and VLAN mapping

SSID is the wireless LAN identifier.

Multiple SSIDs can represent separate user/function groups.

Common chapter model:

~~~text
SSID A → VLAN A
SSID B → VLAN B
SSID C → VLAN C
~~~

Routing/filtering happens beyond the wireless access layer.

## 18. Channel planning

Adjacent WAPs should avoid harmful radio overlap.

Chapter recommends automatic channel selection in most situations.

For manually managed 802.11b/g/n environments, chapter points to non-overlapping channels 1, 6 and 11.

## 19. Coverage and roaming

Large area:

~~~text
multiple WAPs
+ placement study
+ channel/power coordination
~~~

Clients may remain attached to a weak AP instead of moving immediately to a stronger one.

High-density environments therefore need deliberate radio design and coordinated management.

## 20. Wireless client tools

Chapter names:

~~~text
ifconfig
iwlist
iwconfig
wpa_supplicant
~~~

Exact syntax is not supplied by chapter RAG.

## 21. Wireless security

Source framing:

~~~text
WEP
→ chapter considers it unusable/insecure

WPA/WPA2
→ chapter's required baseline for new installations
~~~

Do not generalize beyond the publication context without external verification.

## 22. SDN

Core split:

~~~text
control plane
  ↓ programs
data plane
  ↓ forwards packets
~~~

Benefits described:

- dynamic topology changes;
- performance/security/availability policy;
- API integration;
- cloud/DevOps automation.

Risk:

- vendor-specific SDN can undermine interoperability goals.

## 23. Troubleshooting principle

Chapter's key diagnostic rule:

~~~text
divide network into segments
test each segment
until fault domain is isolated
~~~

Do not diagnose the entire path as one opaque object.

## 24. Cable tester vs packet analyzer

Cable tester:

~~~text
physical/electrical layer
→ length
→ opens
→ wrong termination
→ wiring faults
~~~

Packet analyzer:

~~~text
link/protocol layer
→ packet errors
→ protocol behavior
→ configuration evidence
~~~

Packet analyzer cannot prove cable/power health.

## 25. Wireshark

Chapter explicitly identifies Wireshark as a packet analyzer.

Use conceptually for:

- frame/protocol inspection;
- configuration evidence;
- traffic behavior.

Chapter warns to keep it updated in its publication context.

## 26. Cabling

Core principle:

~~~text
do it correctly the first time
~~~

Invest in:

- good materials;
- competent installation;
- correct termination;
- enough drops;
- labeling;
- documentation.

## 27. Office drops

Chapter recommends multiple connection points rather than a single drop per office.

Reasoning:

- phones/special devices;
- wired fallback;
- future use;
- installation labor dominates retrofitting cost.

## 28. Public/guest ports

Openly accessible ports should not directly expose internal resources.

Chapter suggests guest VLAN placement and 802.1X for protected public ports.

## 29. Cabling administration

TIA/EIA-606 section covers:

- termination hardware;
- cable identity;
- routes/pathways;
- distances;
- color marking;
- component notation.

Operational takeaway: physical infrastructure must be traceable.

## 30. Building constraints

Network design must coexist with:

- architecture;
- cable pathways;
- ceilings/tunnels;
- ventilation spaces;
- fire barriers.

Physical safety/building requirements can invalidate a logically elegant design.

## 31. Expansion

Design for growth where future recabling is expensive.

Chapter recommendation:

~~~text
hard-to-reach path
→ install significantly more cable capacity than current minimum
~~~

It also suggests pre-installing both multimode and single-mode fiber where future access would be difficult.

## 32. Congestion

Potential causes:

- heavily used switches;
- mismatched interfaces;
- slow links;
- high-load protocols.

Mitigation pattern:

~~~text
localize traffic
→ subnets
→ routers
→ smaller fault/load domains
~~~

## 33. Documentation

Maintain:

- cable labels at connection points;
- local wiring diagrams in closets;
- updated electronic records;
- clear switch/router boundaries;
- administrative ownership.

Documentation quality directly affects maintainability.

## 34. Network management

Centralize chapter-wide shared concerns such as:

- topology;
- backbone;
- IP/name coordination;
- supported protocols;
- Internet access policy.

Distribute local operation where it does not endanger shared infrastructure.

## 35. Read-only first

Before changing wireless/logical settings:

~~~text
observe topology
↓
identify exact segment
↓
identify current AP/switch/router boundary
↓
capture current state
↓
change one variable
↓
test same segment
↓
test end-to-end
↓
update documentation
~~~

## 36. Acceptance criteria

For a physical/logical network change:

- medium and endpoint types are compatible;
- cabling/termination is documented;
- switch topology has no uncontrolled loop;
- VLAN membership and routing boundary are intentional;
- VLAN is not assumed to provide security by itself;
- speed/duplex negotiation is consistent at both ends;
- MTU policy is consistent through the path;
- PoE budget is sufficient where used;
- wireless coverage/channel/security design is intentional;
- physical layer is tested separately from packet behavior;
- packet path is verified end-to-end;
- documentation is updated.

Rollback for vendor-specific switch/router/WAP/MTU/SDN changes is not supplied by this chapter: `[Needs confirmation]`.
