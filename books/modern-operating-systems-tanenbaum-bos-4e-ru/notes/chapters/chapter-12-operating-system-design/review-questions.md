# Review questions — Chapter 12

Provenance: PDF pages 1106–1109; source questions are explicitly numbered 1–28. The wording below is condensed while preserving each exercise's task.

1. What factors could eventually limit continued exponential growth in computer-hardware performance?
2. For a compiler, photo editor and payroll program, which is easier to model with an algorithmic paradigm and which with an event-driven paradigm?
3. Is there a fundamental reason filesystem hierarchical names are written from root downward while DNS names are written in the opposite direction?
4. From the listed UNIX Version 7 / POSIX calls, which are redundant because equivalent behavior can be composed from the others with roughly similar performance?
5. What happens to the layered design in Fig. 12.1 if layers 3 and 4 are exchanged?
6. In a microkernel that only passes messages, can user processes still create and use semaphores? How?
7. If a process makes one 2 ms system call every 10 ms and originally takes 10 s, how much faster is it if system-call execution becomes twice as fast?
8. Compare external and internal names in terms of length, uniqueness and hierarchy.
9. Compare doubling a full table with increasing its size by only 1.5×.
10. In Listing 12.2, can the `found` flag be eliminated by examining `p` after the loop?
11. Can conditional compilation hide the difference between IDE and SCSI disks on otherwise similar x86 systems? Is that a good design?
12. What disadvantages accompany the flexibility gained through indirection?
13. Can reentrant procedures have static global variables?
14. Besides readability, what disadvantages does the macro in Listing 12.4b have compared with the procedure?
15. Design a fast parity test for a 32-bit word using at most 256 KiB of lookup tables; then benchmark it against a loop over all 32 bits.
16. When, if ever, would a 24-bit color palette be a good idea?
17. At what minimum image size does an 8-bit or 16-bit palette stop increasing the file size relative to direct 24-bit pixels?
18. Does keeping every root-directory file permanently open, so its inode stays resident, significantly speed pathname lookup?
19. What extra metadata should accompany a hint to a remote file so that later modification can be detected?
20. How can a hint such as `(name, remote host, remote name)` avoid accidentally referring to a different file after delete-and-recreate?
21. Can filesystem locality optimization hurt a program that continuously reads from one source and writes one or more output files? How can this be mitigated?
22. How can Brooks' estimate of about 1000 debugged lines per programmer-year coexist with the first 13,000-line MINIX version being created by one person in under three years?
23. Using Brooks' 1000 lines/year and a cost of $100,000 per programmer-year, estimate the development cost of Windows 8 and assess the assumptions.
24. At current prices, estimate the cost of a PC using a 100 GiB battery-backed RAM disk instead of a hard disk; would it be competitive?
25. What ordinary general-purpose OS features are unnecessary in an embedded appliance?
26. Write a C routine adding two double-precision arguments, using conditional compilation so it works on 16- and 32-bit machines.
27. Implement linear and more sophisticated lookup for random short strings; benchmark them across array sizes and find the crossover.
28. Write a program that simulates an in-memory filesystem.
