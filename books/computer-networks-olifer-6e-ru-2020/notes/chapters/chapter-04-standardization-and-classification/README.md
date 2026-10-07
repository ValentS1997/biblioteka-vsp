# Глава 4. Стандартизация и классификация сетей

**Book ID:** `computer-networks-olifer-6e-ru-2020`  
**Artifact contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Status:** `RAG_GROUNDED`

## Scope and provenance

| Property | Verified value |
|---|---|
| Source mode | `rag_only` |
| PDF pages | **103-133** |
| Printed pages | **102-132** |
| Next chapter | PDF **134** |
| Addressable RAG | `p0103:c01` through `p0133:c01` |
| Blank source units in chapter | **none** |
| Source SHA-256 | `e35305daf978f3d14239683d657caa18c92ab6e979626fda22d2f1fa9cc2a5d9` |

## Main principle

The chapter explains how complex network interaction is made manageable through **decomposition, layering, protocols, interfaces and standards**.

The central distinction is:

- an **interface** describes interaction between neighboring layers inside one node;
- a **protocol** describes peer interaction between entities of the same layer on different nodes;
- a **protocol stack** is a hierarchical set of protocols sufficient for network interaction.

The OSI model then provides a standard vocabulary for this decomposition. The chapter also shows that real protocol stacks do not always map cleanly to seven OSI layers, so a second, horizontal classification is useful: **user plane, control plane and management plane**.

## Chapter map

| Block | Main idea | RAG |
|---|---|---|
| Decomposition and layering | Complex interaction is split into modules and ordered layers with service interfaces | `p0103:c01`-`p0106:c01` |
| Protocol and protocol stack | Peer-layer rules are protocols; a hierarchy of them forms a stack | `p0106:c01`-`p0108:c01` |
| OSI model | Seven layers provide a reference decomposition and common terminology | `p0108:c01`-`p0118:c01` |
| Packet/circuit relationship | Circuit-switched networks may provide a physical-layer service to packet networks | `p0118:c01`-`p0119:c01` |
| Open systems and standards | Open specifications enable interoperability, replacement and integration | `p0119:c01`-`p0122:c01` |
| Internet standardization | RFC process; ISOC/IAB/IRTF/IETF roles | `p0122:c01` |
| Standard protocol stacks | OSI stack, NetBIOS/SMB, TCP/IP and imperfect OSI mappings | `p0122:c01`-`p0126:c01` |
| Network services | Transport services move information unchanged; information services process/store/search it | `p0126:c01`-`p0127:c01` |
| Protocol distribution | End hosts implement full stacks; intermediate devices implement only required lower layers plus auxiliary protocols | `p0127:c01`-`p0129:c01` |
| Horizontal planes | User, control and management planes complement vertical OSI layering | `p0129:c01` |
| Network classification | Area, medium, switching, topology, user type, functional role and overlay/primary distinctions | `p0130:c01`-`p0133:c01` |

## OSI layer map

| Layer | Chapter-grounded role |
|---|---|
| 7 Application | Network services exposed to user applications |
| 6 Presentation | Representation, conversion, encryption/decryption, compression |
| 5 Session | Session coordination and synchronization/checkpoints |
| 4 Transport | End-to-end service with required reliability/quality |
| 3 Network | Internetworking, global addressing and route selection across heterogeneous networks |
| 2 Data link | Frame delivery within one network; link addressing, error handling, MAC where applicable |
| 1 Physical | Bit transmission over a physical medium |

The lower four layers are described as the network transport subsystem; the upper three are closely tied to user-facing network services.

## Two orthogonal classifications

### Vertical: OSI layers

This answers: **which level of abstraction and responsibility is involved?**

### Horizontal: planes

This answers: **what kind of traffic/function is being served?**

- **User plane** — protocols carrying user traffic.
- **Control plane** — auxiliary protocols needed for normal network operation, such as routing/name-resolution functions.
- **Management plane** — protocols supporting administrative monitoring and configuration.

This is important because some auxiliary protocols do not fit neatly into a single OSI layer when classified only vertically.

## Network classification dimensions

The chapter explicitly warns that network classification is not unique. It then classifies networks by:

- content/service family;
- geographical scope: LAN / MAN / WAN;
- transmission medium: wired / wireless;
- switching method: packet / circuit;
- packet-forwarding method;
- topology;
- intended users: carrier / corporate / personal;
- functional role: access / aggregation / backbone;
- primary vs overlay network.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

## Limitations

1. Original figures and diagrams are not separate multimodal RAG objects.
2. The chapter contains historical examples of standards, protocol stacks and organizations; artifacts preserve the source framing rather than updating it from the web.
3. Network classifications are presented by the source as non-unique; artifacts do not convert them into an exclusive taxonomy.
4. No executable CLI/configuration procedure is present.
5. No explicit chapter-end summary or chapter-specific review-question section is present.
