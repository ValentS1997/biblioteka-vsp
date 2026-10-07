# Chapter 12 cheatsheet — Operating-system design

## Design review sequence

| Question | What to establish |
|---|---|
| What is the system for? | explicit goals, workload, trust and hardware constraints |
| Is the interface understandable? | simplicity, completeness, efficient implementation |
| Is the architecture structured? | layers, client–server boundaries, failure domains |
| What is mechanism vs policy? | stable primitive vs replaceable decision |
| Are concepts orthogonal? | unrelated choices controlled independently |
| When are decisions bound? | compile / boot / load / run time |
| Are structures static or dynamic? | predictability vs flexibility |
| Is communication synchronous or asynchronous? | blocking/thread complexity vs event/state complexity |
| Is the code reentrant? | concurrent and interrupt-safe behavior |
| Are errors checked before resource acquisition? | simpler rollback and fewer leaks |
| Is optimization evidence-based? | measurements identify the actual bottleneck |
| Is the fast path the common path? | optimize frequent cases without corrupting structure |
| Can the project organization scale? | interfaces, ownership, integration and test strategy |

## Architecture choices

### Layered system

`hardware → low-level machine handling → threads/synchronization → drivers → VM/filesystems/syscalls`

Lower layers hide awkward hardware detail so higher layers can use cleaner abstractions.

### Exokernel / end-to-end view

Kernel provides secure resource allocation; higher-level abstractions may live in user libraries when endpoint code must validate correctness anyway.

### Microkernel client–server

Kernel provides a small mechanism such as message passing. Services/drivers can run as isolated processes. Main tradeoff: modularity/fault isolation versus communication/context-switch cost.

## Core design rules

- Prefer fewer mechanisms when they can compose into richer behavior.
- Separate mechanism from policy.
- Preserve orthogonality: CPU type, word length and unrelated properties should not be encoded into one overloaded switch.
- Use symbolic names instead of magic numbers.
- Add indirection when it buys useful flexibility, but account for lookup and state complexity.
- Bind decisions as late as needed, not later by default.
- Choose dynamic structures only when the flexibility justifies allocator/error-path complexity.
- Make reusable routines reentrant when they can execute concurrently or be re-entered from interrupts.
- Validate errors before acquiring resources.
- Use brute-force/simple algorithms for small or rare cases if they reduce code and defect risk.

## Performance rules

1. Make the first working version simple.
2. Measure where time/memory is actually consumed.
3. Optimize only meaningful bottlenecks.
4. Accept a good solution when further improvement disproportionately increases complexity.
5. Exploit caching and locality.
6. Treat cache entries as correct state; treat hints as untrusted accelerators.
7. Optimize the common case; keep rare paths correct.

## Project-management rules

- Large projects spend substantial effort on planning, module/interface definition, integration and test.
- Adding people to a late project can increase communication/training cost rather than reduce schedule.
- Team structure and interface ownership matter as much as coding rate.
- Experience helps because architecture and integration mistakes are costly and difficult to predict from isolated modules.
- There is no single technique that removes the intrinsic complexity of large system software.

## Acceptance checklist

- goals and non-goals are explicit;
- API surface has no obvious redundant mechanisms;
- dependencies form understandable layers/boundaries;
- policy can change without rewriting mechanism;
- failure domains are identified;
- concurrency model is explicit;
- error paths release all resources;
- performance claims have measurements;
- optimization preserves maintainability;
- project ownership and integration points are documented.

## Rollback

For design changes, rollback means restoring the previous interface/architecture decision and its dependent implementation. The chapter does not provide repository or deployment commands; exact operational rollback remains environment-specific.
