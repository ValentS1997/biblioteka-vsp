# Chapter-end summary

Provenance: PDF pages 519–520; chunks `p0519:c01` and `p0520:c01`.

The chapter's explicit conclusions are:

- Deadlocks are a potential problem in any operating system when each member of a process group waits for an event that only another member can cause.
- Resource release is the common awaited event, but communication processes can also deadlock while waiting for messages.
- Resource deadlocks can be avoided by distinguishing safe and unsafe states.
- A safe state has a sequence that guarantees all processes can finish; an unsafe state lacks that guarantee.
- The banker's algorithm refuses a request when granting it would make the state unsafe.
- Deadlocks can also be prevented structurally by making at least one required condition impossible.
- Examples include limiting simultaneous ownership patterns and imposing a global increasing resource order.
- Communication deadlocks are a separate class and can often be handled with suitable timeouts.
- Livelock can stop useful forward progress even though the involved processes are not actually blocked.
- Starvation is a different failure mode; a FIFO resource-allocation policy can prevent the chapter's starvation example.
