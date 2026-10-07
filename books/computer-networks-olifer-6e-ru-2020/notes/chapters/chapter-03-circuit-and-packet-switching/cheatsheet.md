# Chapter 3 cheatsheet

Source mode: `rag_only`. Scope: PDF 75-102 / printed 74-101.

## Symptom / problem framing

The chapter asks how a network should share communication resources between many flows.

Two fundamental answers are compared:
- reserve an end-to-end channel before sending data;
- divide data into packets and share links dynamically.

## Baseline / context

### Circuit switching

A flow first obtains a composite channel built from elementary channels along the route.

Properties confirmed by the chapter:
- fixed bandwidth along the complete path;
- exclusive use of reserved elementary channels during the session;
- data transfer begins only after connection setup;
- once established, transfer is predictable and does not depend on concurrent sessions;
- setup can fail when required elementary channels are unavailable.

### Packet switching

Data is divided into packets with headers. Packets are buffered and processed by intermediate devices.

Consequences:
- links are statistically shared among many flows;
- bursty traffic is aggregated more efficiently;
- queues may form;
- delay becomes variable;
- buffers may overflow and packets may be lost.

## Read-only checks

| Question | Expected interpretation |
|---|---|
| Is capacity reserved before data transfer? | Yes for circuit switching; no for ordinary datagram packet transfer |
| Can setup be rejected? | Circuit switching can reject a new connection if resources are unavailable |
| Is bandwidth guaranteed to one session? | Circuit switching reserves it; packet switching normally shares it dynamically |
| Why are buffers required? | Store-and-forward, speed mismatch, processing mismatch and temporary overload |
| Can packets of one flow take different paths? | Yes in datagram mode and possibly with a logical connection |
| What does a virtual circuit add? | A fixed route identified by a label |
| Is a virtual circuit equivalent to circuit switching? | No; discrete packets are still forwarded |
| Why is packet switching good for bursty traffic? | Peaks from independent sources tend not to coincide, improving aggregate link utilization |

## Interpretation

### Circuit switching optimizes predictability

Work is done before data transfer: choose the route, verify free elementary channels, reserve them, and create local switching-table state.

This minimizes runtime uncertainty but can waste reserved bandwidth during idle periods.

### Packet switching optimizes statistical utilization

Packets from many sources are interleaved over shared links. This improves efficiency for uneven computer traffic but shifts uncertainty into queues and delay.

### Three packet forwarding modes

1. **Datagram:** every packet is processed independently; best-effort delivery.
2. **Logical connection:** end nodes keep state and can coordinate reliability/security behavior without fixing the route.
3. **Virtual circuit:** a logical connection also fixes the path; packets carry a compact label rather than a full destination address for forwarding.

### Delay structure

Circuit switching includes connection setup plus propagation and serialization.

Packet switching adds packetization, per-hop buffering/store-and-forward, queue waiting and switching/processing delays. Pipeline behavior means total message time is not simply the sum of independent packet transit times.

## Next action

When reading later chapters, map each concrete technology to the model used here:
- what resources are reserved;
- what state is kept;
- what identifier is forwarded on;
- where queues exist;
- whether delivery is best effort or connection-oriented.

## Modifying action

[Not applicable] — no operational configuration procedure is prescribed by the chapter.

## Verification / acceptance checks

You should be able to explain:

1. elementary vs composite channel;
2. why circuit setup may fail;
3. why bursty traffic wastes reserved capacity;
4. why packet switching uses buffers;
5. store-and-forward;
6. datagram vs logical connection vs virtual circuit;
7. best-effort delivery;
8. why virtual circuit is still packet switching;
9. fixed bandwidth vs statistical multiplexing;
10. the qualitative components of end-to-end delay.

## Rollback

[Not applicable] — no state-changing action is performed.

## Source caveat

Mathematical notation on PDF pages 95-100 is partially damaged in extracted text. Exact formula typography is not reconstructed; see `source-findings.md`.
