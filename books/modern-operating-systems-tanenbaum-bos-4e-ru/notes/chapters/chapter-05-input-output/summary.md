# Chapter-end summary

Provenance: PDF pages 479–480; chunks `p0479:c01` and `p0480:c01`.

The chapter's explicit conclusions are:

- I/O is a major part of an operating system.
- Three fundamental transfer methods are compared:
  1. programmed I/O, where the CPU performs each transfer unit and waits/polls;
  2. interrupt-driven I/O, where the CPU starts work and continues other processing until completion interrupts arrive;
  3. DMA, where a separate controller moves a block and interrupts after the block has been transferred.
- The I/O software stack is layered: interrupt handlers, device drivers, device-independent I/O software, and user-space libraries/spooling.
- Drivers handle device-specific mechanics while presenting standardized interfaces upward; device-independent software provides functions such as buffering and error reporting.
- Disk behavior includes physical geometry, RAID, formatting, request scheduling, media-error handling and stable-storage techniques.
- Disk scheduling can improve performance, but virtual geometry complicates direct optimization.
- Clocks support timekeeping, process-runtime limits, watchdogs and accounting.
- Character terminals require rules for special input characters and terminal escape sequences; canonical and less-processed input modes serve different application needs.
- X Window separates display/input server behavior from applications, while GUI systems use event-driven interaction.
- Thin clients trade local complexity for centralized administration and resource use.
- Power management matters for mobile systems and large installations; both the OS and applications can reduce energy use, including by trading quality/performance for battery life.
