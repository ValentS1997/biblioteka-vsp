# Chapter 3 — Circuit and Packet Switching

Book ID: `computer-networks-olifer-6e-ru-2020`.

Status: `RAG_GROUNDED`. Artifact contract: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Scope and provenance

- Source mode: `rag_only`
- PDF pages: **75-102**
- Printed pages: **74-101**
- Next chapter begins at PDF page **103**
- Addressable RAG: `p0075:c01` through `p0102:c01`
- Blank source units inside chapter: none
- Source SHA-256: `e35305daf978f3d14239683d657caa18c92ab6e979626fda22d2f1fa9cc2a5d9`

## Main principle

The chapter compares two fundamental ways of solving the switching problem.

**Circuit switching** reserves a fixed end-to-end composite channel before data transfer. Once established, the flow receives fixed bandwidth and predictable delivery characteristics, but reserved capacity can remain idle when traffic is bursty.

**Packet switching** divides data into packets and statistically shares network resources among many flows. It uses capacity more efficiently for bursty computer traffic, but introduces buffering, queues, variable delay and possible loss.

## Chapter map

1. Circuit switching and elementary channels
2. Composite channels and connection setup
3. Inefficiency for bursty traffic
4. Packet switching and packet structure
5. Buffering and store-and-forward
6. Datagram forwarding
7. Logical connections
8. Virtual circuits
9. Circuit-vs-packet comparison
10. Delay structure and numerical example
11. Ethernet as a packet-switched technology

## Three packet-forwarding modes

| Mode | State/path behavior |
|---|---|
| Datagram | Packets are processed independently; no history of earlier packets is required |
| Logical connection | End systems maintain connection state and may add reliability/security behavior; route is not fixed |
| Virtual circuit | A logical connection includes a fixed route; packets carry a compact virtual-circuit label |

## Key distinctions

- **Circuit vs packet:** reserved capacity and determinism vs statistical sharing and variable delay.
- **Connection setup:** mandatory before transfer in circuit switching; absent in pure datagram transfer.
- **Addressing:** circuit data uses the established local channel mapping; packet switching carries forwarding information in packets or labels.
- **Buffers:** central to packet switching because packets may arrive faster than an outgoing path can serve them.
- **Virtual circuit is not circuit switching:** it still transfers discrete packets rather than a continuous fixed-rate information stream.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

## Limitations

1. Equations on PDF pages 95-100 contain extraction damage: some indices, superscripts and variable symbols are lost.
2. Numerical results are used only where the extracted text is unambiguous.
3. Original figures are not separate multimodal RAG objects.
4. No executable CLI commands or configuration procedures are present.
5. No explicit chapter-end summary or chapter-specific review-question section is present.
