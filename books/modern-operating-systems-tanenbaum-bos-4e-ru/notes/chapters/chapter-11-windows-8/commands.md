# Source-confirmed Windows APIs and operations

Scope: chapter 11 RAG only, PDF pages 931–1057.

| API / operation | Class | Source-grounded role | Verification / risk |
|---|---|---|---|
| `CreateProcess` | state-changing | Create process and initial thread | Returns process/thread handles and IDs; inheritance/security options matter. |
| `SetPriorityClass` | state-changing | Set process priority class | Changes baseline scheduling class for its threads. |
| `SetThreadPriority` | state-changing | Set thread-relative priority | Combines with process class; does not guarantee CPU time. |
| `SwitchToFiber` | state-changing | Switch execution between fibers | Programmer must avoid switching to an already-running fiber. |
| `WaitForMultipleObjects` | synchronizing | Wait on multiple dispatcher objects | Requires handle-based waitable objects. |
| `InitOnceExecuteOnce` | synchronizing | Ensure one-time initialization | Prevents concurrent duplicate initialization. |
| `VirtualAlloc` | state-changing | Reserve/commit virtual memory | Distinguish reservation from commitment. |
| `VirtualFree` | state-changing | Release/decommit virtual memory | Can invalidate existing references. |
| `VirtualProtect` | state-changing | Change page protection | Verify resulting access mode. |
| `VirtualQuery` | read-only | Query virtual-memory region state | Useful before modifying mappings. |
| `VirtualLock` / `VirtualUnlock` | state-changing | Lock/unlock pages in memory | Subject to system limits. |
| `CreateFileMapping` | state-changing | Create section/file-mapping object | Produces a shareable/named mapping object. |
| `MapViewOfFile` | state-changing | Map section into an address space | Verify offset, size and access. |
| `UnmapViewOfFile` | state-changing | Remove a mapped view | References into the view become invalid. |
| `OpenFileMapping` | state-changing | Open an existing mapping object | Object security still applies. |
| `NtCreateFile` | state-changing | Open/create file or device | Request may traverse filters, device stack and filesystem. |
| `NtReadFile` | read-only / workload-generating | Read file/device data | I/O may complete asynchronously. |
| `NtWriteFile` | state-changing | Write file/device data | I/O may be queued. |
| `NtQueryDirectoryFile` | read-only | Query directory content | Operates through an open object. |
| `NtQueryVolumeInformationFile` | read-only | Query volume information | Handle-scoped operation. |
| `NtSetVolumeInformationFile` | state-changing | Modify volume information | Persistent impact depends on filesystem. |
| `NtQueryInformationFile` | read-only | Query file metadata | Includes names/features/identifiers. |
| `NtSetInformationFile` | state-changing | Modify file information | Requires an open file object. |
| `NtLockFile` / `NtUnlockFile` | state-changing | Byte-range locking | Overlapping access can block. |
| `NtFlushBuffersFile` | state-changing | Force filesystem data toward storage | Used for explicit flush behavior. |
| `NtCancelIoFile` | state-changing | Cancel outstanding I/O | Verify which requests are pending. |
| `NtDeviceIoControlFile` | state-changing | Device-specific control operation | Semantics depend on the driver. |
| `GetTokenInformation` | read-only | Inspect token properties | Check identity/groups/privileges/restrictions. |
| `InitializeSecurityDescriptor` | state-changing | Initialize a security descriptor | Build the intended descriptor before attaching it. |
| `LookupAccountSid` | read-only | Resolve account/SID information | Depends on identity database state. |
| `SetSecurityDescriptorOwner/Group` | state-changing | Set owner/group fields | Alters security metadata being built. |
| `InitializeAcl` | state-changing | Initialize DACL/SACL | ACE order matters. |
| `AddAccessAllowedAce` | state-changing | Add an allow ACE | Earlier deny entries can still control outcome. |
| `AddAccessDeniedAce` | state-changing | Add a deny ACE | Source recommends deny entries before allows. |
| `DeleteAce` | state-changing | Remove an ACE | Can widen or narrow access. |
| `SetSecurityDescriptorDacl` | state-changing | Attach a DACL | Verify resulting open/access behavior. |
| `regedit` export | observational | Chapter exercise exports registry snapshots | Actual diffs require a live Windows system. |

## Read-only-first discipline

Before a real change, determine:

1. object name and handle ownership;
2. requested/granted access;
3. process/thread identity and token;
4. virtual-region state and protection;
5. driver/device/filesystem stack;
6. persistent NTFS/registry location;
7. expected rollback point.

The chapter does not provide current PowerShell/CMD administration recipes; those remain outside `rag_only`.
