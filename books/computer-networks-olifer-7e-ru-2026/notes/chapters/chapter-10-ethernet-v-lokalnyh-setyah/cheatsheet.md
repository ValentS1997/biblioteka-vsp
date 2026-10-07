# Cheatsheet — глава 10: Ethernet в локальных сетях

## Symptom / problem framing

**Проблема:** Ethernet incident может лежать в разных исторически/функционально разных механизмах: shared-medium collision domain, MAC learning/forwarding, output queue contention или PHY/lane/FEC. Диагностика должна сначала определить, какой именно Ethernet model используется. `p0287:c01`–`p0325:c01`.

## Baseline / context

| Область | Source model | RAG |
| --- | --- | --- |
| Shared medium | One collision domain, CSMA/CD, half duplex | `p0287:c01`–`p0298:c01` |
| MAC addressing | Individual/group/broadcast, OUI/local assignment | `p0291:c01`–`p0292:c01` |
| Ethernet II frame | DA/SA/EtherType/payload/FCS | `p0292:c01`–`p0293:c01` |
| Learning switch | Learn source, forward/filter/flood by destination | `p0299:c01`–`p0304:c01` |
| Layer-2 loop | Frame duplication/circulation + MAC flapping | `p0305:c01`–`p0306:c01` |
| Full duplex | Point-to-point simultaneous TX/RX, no collisions | `p0308:c01`–`p0309:c01` |
| Switch capacity | Port rates + fabric/memory/processing | `p0309:c01`–`p0311:c01` |
| Modular PHY | RS / PCS / PMA / PMD / MDI | `p0313:c01`–`p0314:c01` |
| High-speed scaling | Better coding + parallel lanes + PAM4/FEC | `p0312:c01`–`p0325:c01` |

## Read-only checks

1. Link is **shared/half-duplex** or **point-to-point/full-duplex**?
2. Is there a hub/repeater in path, or only switches?
3. Destination MAC known in forwarding table? If unknown, flooding is expected.
4. Is MAC address moving between ports unexpectedly? That can indicate topology/loop instability.
5. Are broadcast/group/unknown frames dominating? The transparent bridge floods them.
6. Is output-port demand greater than that port's rate, causing queue buildup?
7. Port/link speeds and duplex state agree at both ends? Exact real state: **[Needs confirmation]**.
8. Autonegotiation succeeded on a mutually supported mode?
9. What PHY family is active: copper/fiber, Fast/Gigabit/10G/100G/400G/etc.?
10. For high-speed PHY: number of lanes, line coding, PAM4/NRZ, FEC state and optical module type: **[Needs confirmation]**.

## Interpretation

- **Hub ≠ switch.** A hub preserves one collision domain; a switch buffers frames and creates logical segments. `p0298:c01`–`p0300:c01`.
- **Unknown unicast flooding is normal learning behavior.** It becomes suspicious only if persistent/excessive relative to expected table learning. `p0302:c01`–`p0303:c01`.
- **Broadcast storm is not automatically stopped by a transparent bridge.** Default bridge behavior propagates broadcast/group traffic. `p0303:c01`.
- **A switching loop is worse than a duplicate path.** It can multiply frames and continuously rewrite MAC-table location state. `p0305:c01`–`p0306:c01`.
- **Full duplex removes CSMA/CD, not Ethernet framing.** Modern Ethernet preserves frame/MAC semantics while changing medium access assumptions. `p0308:c01`–`p0313:c01`.
- **Nonblocking does not mean infinite output capacity.** Multiple inputs targeting one slower output still queue/contend. `p0307:c01`–`p0310:c01`.
- **Fast/Gigabit/10G+ evolution is primarily PHY evolution.** Frame/MAC continuity is a major source theme. `p0312:c01`–`p0325:c01`.
- **PAM4 increases bits per symbol but reduces margin.** FEC is paired with it to restore practical reliability at high rate. `p0321:c01`–`p0323:c01`.
- **Parallel lanes are an engineering scaling tool.** Later generations raise lane rate to reduce lane/wavelength count. `p0320:c01`–`p0324:c01`.

## Next action

Для Ethernet troubleshooting использовать порядок:

**identify L1 medium/PHY → verify speed/duplex/autoneg → inspect MAC learning/movement → classify forward/filter/flood behavior → exclude L2 loop/broadcast storm → inspect output contention/queues → inspect PHY lanes/FEC/optics → re-test end-to-end**.

Это source-grounded sequence; concrete vendor commands and thresholds require device evidence.

## Modifying action

**[Not applicable].** Глава описывает manual/static forwarding entries, filters, speed/duplex negotiation and physical choices, но executable configuration syntax отсутствует.

Любое изменение port mode, static MAC/filter, transceiver or topology требует before-state and rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- explain CSMA/CD and why minimum frame size relates to collision detection;
- distinguish physical star via hub from switched star;
- explain Ethernet II fields and EtherType/FCS roles;
- describe source-MAC learning and destination forwarding/filter/flood;
- explain why L2 loops break transparent bridging;
- explain full duplex and disappearance of collisions;
- define nonblocking switch at a high level;
- identify RS/PCS/PMA/PMD roles;
- explain autonegotiation;
- compare the PHY evolution from 10M through PAM4/FEC high-speed Ethernet.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для production Ethernet changes rollback is platform-specific and must restore previous port/topology/forwarding state.
