# Chapter 4 cheatsheet

Source mode: `rag_only`. Scope: PDF 103-133 / printed 102-132.

## Symptom / problem framing

The chapter addresses a scaling problem of network design: how to make complex interaction understandable, interoperable and classifiable.

Its answer is:
1. decompose the task;
2. organize functions into layers;
3. define interfaces and peer protocols;
4. standardize open specifications;
5. use reference models and protocol stacks;
6. classify networks by several independent dimensions.

## Baseline / context

### Layering

A higher layer requests services from the adjacent lower layer. The lower layer hides internal implementation details and exposes a service interface.

### Protocol vs interface

- **Protocol:** rules for interaction between peer entities at the same layer on different nodes.
- **Interface:** rules for interaction between adjacent layers in the same node.
- **Protocol stack:** hierarchical set of protocols sufficient to organize network interaction.

### Encapsulation

A higher-layer PDU becomes data for the lower layer, which adds its own service information. At the destination, corresponding layers interpret and remove their own headers while data moves upward.

## Read-only checks

| Check | Expected interpretation |
|---|---|
| Protocol or interface? | Peer-to-peer across nodes vs adjacent layers within one node |
| Model or implementation? | OSI is a reference model; a concrete protocol stack is an implementation/specification set |
| Layer 2 or layer 3 addressing? | Link delivery inside one network vs global delivery across an internetwork |
| Routed or routing protocol? | Moves packets vs distributes topology/routing information |
| Transport or information service? | Moves information unchanged vs processes/stores/searches information |
| Vertical layer or horizontal plane? | Functional abstraction level vs user/control/management purpose |
| End host or intermediate node? | Full stack vs only the layers needed to perform forwarding plus auxiliary functions |
| Open specification? | Published, accessible specification accepted through an open standardization process |

## Interpretation

### Why layering matters

Layering reduces complexity by separating responsibilities and allowing modules to be developed, tested and changed independently as long as interfaces remain stable.

### OSI is a vocabulary, not a mandatory implementation

The seven-layer OSI model defines names and responsibilities. Real stacks often combine functions differently and may have only three or four visible layers.

### Lower four vs upper three

The chapter groups physical, data link, network and transport layers as the transport subsystem responsible for data delivery. Session, presentation and application layers are more closely connected to user-facing services.

### Network layer as internetworking coordinator

The network layer connects heterogeneous networks through routers, global addresses and routing. Packets are repeatedly encapsulated into link-layer frames appropriate to each traversed network.

### Standardization enables interoperability

Open standards make it possible to mix products from different vendors, replace components and connect networks with less redesign.

### Vertical layering is not enough

Routing, naming and management protocols can be awkward to classify purely by OSI layer. The chapter therefore introduces:
- user plane;
- control plane;
- management plane.

## Next action

When studying a concrete technology or protocol, classify it in two ways:
1. What OSI/TCP-IP responsibility does it implement?
2. Is it carrying user data, controlling the network, or managing the network?

This prevents category errors such as treating every application-layer protocol as a user application protocol.

## Modifying action

[Not applicable] — the chapter does not prescribe configuration changes.

## Verification / acceptance checks

You should be able to explain:

1. decomposition and service interfaces;
2. protocol vs interface;
3. protocol stack and encapsulation;
4. the seven OSI layers and their broad responsibilities;
5. data-link vs network-layer scope;
6. network vs transport responsibilities;
7. open systems and open specifications;
8. why real stacks only approximately match OSI;
9. user/control/management planes;
10. transport vs information services;
11. why hosts, switches and routers implement different portions of the stack;
12. several independent dimensions used to classify networks.

## Rollback

[Not applicable] — no state-changing operation is performed.

## Source caveat

The source presents historical standards/protocol examples in its own timeframe. No external freshness correction is applied in this RAG-only artifact.
