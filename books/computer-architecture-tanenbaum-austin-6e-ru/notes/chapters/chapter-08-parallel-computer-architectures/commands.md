# Parallel primitives — глава 8

**Provenance:** RAG `p0590:c01`–`p0698:c01`.

This artifact records source-level parallel-computing primitives and concepts, not host shell commands.

## Message passing

Source primitives:

- `send`
- `receive`

Semantics discussed:

- synchronous;
- buffered;
- nonblocking.

## MPI examples

The source explicitly shows forms equivalent to:

```text
MPI_Send(buffer, count, datatype, destination, tag, communicator)
MPI_Recv(&buffer, count, datatype, source, tag, communicator, &status)
```

MPI concepts:

- communicator = process group + context;
- datatype;
- point-to-point communication;
- collective communication;
- virtual topology.

MPI-1 process groups are treated as already created/static in the chapter; MPI-2 adds dynamic processes and additional capabilities.

## Shared-memory synchronization vocabulary

Memory-ordering operations named by the chapter:

- synchronization operation for weak consistency;
- `acquire`;
- `release`.

These are architectural/semantic primitives, not necessarily literal ISA mnemonics.

## Cache-coherence actions

Conceptual actions:

- invalidate remote copies;
- update/write through;
- write back dirty line;
- request exclusive ownership;
- snoop shared bus;
- directory lookup.

## Interconnect operations

- route packet/request;
- arbitrate shared bus;
- switch through crossbar;
- traverse omega/multistage network;
- broadcast;
- send reply packet.

## GPU / VLIW scheduling

TriMedia compiler places operations into compatible instruction slots.

Fermi groups software threads onto streaming multiprocessors; SIMD-style execution benefits when threads follow the same control path.

## State-changing boundary

These are descriptive source primitives. No production MPI/CUDA command line or current library API syntax is added from external knowledge.
