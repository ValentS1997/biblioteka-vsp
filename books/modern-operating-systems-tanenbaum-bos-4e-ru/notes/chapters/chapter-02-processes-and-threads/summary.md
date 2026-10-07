# Chapter-end summary

Provenance: PDF page 205; chunk `p0205:c01`.

The chapter concludes with these source-grounded points:

- Operating systems present a conceptual model of concurrently running sequential processes to hide the disruptive detail of interrupts and context switching.
- Processes are dynamically created and destroyed and each has its own address space.
- Multiple threads can execute inside one process. Threads are independently schedulable and have their own stacks while sharing the process address space.
- Threads may be implemented in user space or in the kernel.
- Processes/threads coordinate through IPC and synchronization primitives such as semaphores, monitors and messages.
- The same primitives are used to keep multiple execution streams out of conflicting critical sections and to order dependent operations.
- A process may be running, ready or blocked.
- Classical synchronization problems include producer-consumer, dining philosophers and readers-writers; careless synchronization can still produce races and deadlocks.
- Scheduling algorithms differ by workload and goal. The chapter highlights shortest-job-first, round-robin, priority, multilevel queues, guaranteed, lottery and fair-share scheduling.
- Separating scheduling policy from mechanism can let user-space software influence scheduling decisions without implementing the kernel scheduler itself.
