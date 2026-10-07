# Chapter-end summary

Provenance: PDF pages 1052–1053; chunks `p1052:c01` and `p1053:c01`.

The chapter's explicit conclusions are:

- Windows kernel mode consists of the HAL, the kernel layer, the NTOS executive and many device/filesystem/network/graphics drivers.
- HAL hides selected hardware differences. The kernel manages processor-level mechanisms, scheduling and synchronization; the executive implements most kernel-mode services.
- The executive is built around kernel/executive objects representing processes, threads, memory sections, drivers, devices and synchronization objects.
- User processes receive handles to objects and use those handles in later system-service calls. The Object Manager also maintains an object namespace.
- Processes are resource/address-space containers; threads are scheduled execution units; section objects represent memory objects and mapped files, including EXE/DLL images and shared memory.
- Windows uses demand-paged virtual memory and working sets. Physical pages move through several lists, and working sets are trimmed under memory pressure.
- The Cache Manager maps file regions into kernel virtual address space and cooperates with the Memory Manager to improve file-I/O performance.
- Windows I/O is driver-based and fundamentally asynchronous. Devices form stacks, and I/O Request Packets flow through the corresponding drivers.
- Filesystem volumes are themselves integrated into the I/O device model.
- NTFS is based on the Master File Table. Files and directories have MFT records; filesystem metadata is itself stored in NTFS files.
- NTFS models files as collections of attributes, supports resident/nonresident attributes, Unicode, multiple data streams, compression, journaling and encryption.
- Windows security uses access tokens to identify users/groups/privileges and security descriptors containing ACLs on protected objects.
- Newer Windows versions add integrity levels and exploit mitigations including volume encryption, address-space randomization and non-executable memory.
