# Chapter 11 cheatsheet — Windows 8

## Architecture

- Win32/WinRT: documented application-facing interfaces.
- Native NT services: low-level system-service boundary.
- NTOS executive: object, process/thread, memory, I/O, cache and security managers.
- Kernel: scheduling, synchronization, traps and interrupts.
- HAL: selected hardware-specific details.
- Hyper-V may provide a virtualization layer below the OS.

## Object model

`handle → per-process handle table → kernel object`

Handles are opaque user-mode references. Object Manager supplies naming, lifetime/reference counting, handle translation and common object operations.

## Scheduling

- Windows schedules threads, not processes.
- 32 priority levels are used in the chapter model.
- Process priority class plus thread-relative priority determines base priority.
- Current priority may be temporarily boosted for ordinary threads.
- Autoboost reduces priority inversion by boosting a resource owner needed by a higher-priority waiter.
- Ideal-processor and NUMA placement aim to preserve cache/memory locality.

## Memory

- Reservation and commitment are separate.
- VADs describe virtual-address regions.
- Working set means pages resident for a process.
- Soft fault: resolved without reading storage.
- Hard fault: storage input is required.
- Physical pages move among free, zeroed, standby and modified states.
- Inactive modern-app processes may be written out in larger extents and restored with relatively few I/O operations.

## I/O

`API → Object Manager → I/O Manager → driver/device stack → filesystem/device`

I/O Request Packets travel through device stacks and complete back upward. The model is fundamentally asynchronous.

## NTFS

- MFT stores records for files, directories and filesystem metadata.
- File content and metadata are attributes; data streams may be named or unnamed.
- Nonresident data is represented as logical ranges and physical extents.
- Reparse points support path redirection such as symbolic links and mount points.
- Compression, journaling and encryption are integrated features.

## Security

- SID identifies a user or group.
- Access token carries identity and related security properties.
- Security descriptor carries DACL/SACL information.
- Integrity level adds a mandatory write restriction independent of ordinary DACL authorization.
- Impersonation allows a server thread to act using a client's security context.
- Source-era mitigations include /GS, NX, ASLR, heap hardening, code integrity, PatchGuard, Windows Update and Defender.

## Operational checks

1. Identify the owning subsystem before changing state.
2. Distinguish handle identity from raw pointers.
3. Distinguish thread priority from process priority class.
4. Distinguish reserved address space from committed memory.
5. Distinguish soft faults from storage-backed hard faults.
6. Trace I/O through the full stack.
7. For NTFS, validate MFT attributes/extents rather than assuming one byte stream.
8. For access problems, inspect token, DACL and integrity level together.

## Rollback

The chapter does not define one universal administrative rollback procedure. Record the pre-change state and use platform-specific rollback only after independent verification. Exact modern commands remain `[Needs confirmation]` under `rag_only`.
