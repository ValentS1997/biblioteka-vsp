# Chapter-end summary

Provenance: PDF pages 652–653; chunks `p0652:c01` and `p0653:c01`.

The chapter's explicit conclusions are:

- Multiple processors can increase both performance and reliability.
- The chapter distinguishes multiprocessors, multicomputers, virtual machines and distributed systems as major organizational forms.
- A multiprocessor has two or more CPUs sharing common memory; CPUs may themselves contain multiple cores.
- Multiprocessor hardware may use buses, crossbars or multistage switching, while OS organizations include per-CPU OS instances, master–slave and SMP.
- SMP requires synchronization; lock wait can use spinning or context switching.
- Multiprocessor scheduling includes time sharing, space sharing and gang scheduling.
- Multicomputers have private memory per processor/node and therefore communicate by messages rather than shared RAM.
- Network-interface CPUs and host CPUs must be synchronized carefully to avoid races.
- User-level communication on multicomputers commonly uses RPC; DSM can emulate shared memory.
- Process placement and load balancing are important, with sender-initiated, receiver-initiated and mixed strategies.
- Distributed systems are loosely coupled complete computers, often geographically separated and running their own operating systems.
- Middleware provides a common model over this heterogeneous base.
- The chapter surveys document-, file-system-, object- and interaction-based middleware, with the Web, CORBA and Linda as examples.
