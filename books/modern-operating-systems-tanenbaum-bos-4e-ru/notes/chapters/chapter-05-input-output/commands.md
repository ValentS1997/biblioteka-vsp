# Source-confirmed commands, APIs and control operations

Scope: chapter 5 RAG only, PDF pages 380–487.

| Item | Class | Source-grounded role | Risk / verification / rollback |
|---|---|---|---|
| `sort <input >output` | workload-generating | Demonstrates device-independent input/output naming and redirection | Reads `input`, writes `output`. Exact overwrite/rollback semantics are `[Needs confirmation]`. |
| `IN REG,PORT` / `IN R0,4` | read-only | Read an I/O-port register into a CPU register | Privileged/architecture-specific. Verify returned status/data. |
| `OUT PORT,REG` | state-changing | Write a CPU register value to an I/O control port | May issue device commands/change device state. Rollback `[Needs confirmation]`. |
| `TEST PORT_4` | read-only | Test a memory-mapped control register while waiting for device readiness | MMIO must not be stale-cached. |
| `open` / `close` | state-changing | Acquire/release an exclusive device represented as a special file | Failed `open` may indicate busy device; ensure ownership is released. |
| `read` | read-only | Blocking user-facing read can hide asynchronous physical I/O | Verify returned byte/block count and error result. |
| `write(fd, buffer, nbytes)` | state-changing | User-space library wrapper around an I/O system call | Writes data to target descriptor; rollback depends on target. |
| `printf` / `scanf` | workload-generating | Format output / parse input before underlying I/O | No device-specific rollback defined. |
| `down`, `wait`, `receive` | state-changing | Examples of driver blocking until I/O completion | Changes thread/process state; semantics depend on OS. |
| `up`, `signal` | state-changing | Examples used by interrupt handlers to wake a blocked driver | Verify intended waiter becomes runnable. |
| `IRET` | state-changing | Example return-from-interrupt instruction | Architecture-specific; exact state requirements `[Needs confirmation]`. |
| `alarm` | state-changing | User process requests a later notification | Verify signal/notification at requested time. |
| ANSI `ESC [ m;n H` | state-changing terminal output | Move cursor to row m, column n | Affects terminal display state only. |
| ANSI `ESC [ n P` | state-changing terminal output | Delete n characters at cursor | Verify only intended characters are removed. |
| ANSI `ESC [ n L` / `ESC [ n M` | state-changing terminal output | Insert/delete lines | Verify surrounding screen contents. |
| `XOpenDisplay`, `XCreateSimpleWindow`, `XSelectInput`, `XNextEvent`, `XMapRaised` | state-changing | Create X connection/window, select events, receive events and map window | Changes X resources; matching cleanup is described below. |
| `XFreeGC`, `XDestroyWindow`, `XCloseDisplay` | state-changing | Release X graphics context/window/connection | Source-supported lifecycle cleanup. |
| `RegisterClass`, `CreateWindow`, `ShowWindow`, `UpdateWindow` | state-changing | Register Windows window class and create/show/update a window | GUI state change; exact rollback is window destruction/exit `[Needs confirmation]`. |
| `GetDC`, `TextOut`, `ReleaseDC` | state-changing | Obtain device context, output text, release context | `hdc` defines target/clipping/properties; release after use. |
| `Rectangle(hdc,...)` | state-changing | Draw a rectangle using attributes from device context | Affects drawable/window contents. |
| `BitBlt(...)` | state-changing | Copy/combine a bitmap region between device contexts | Verify source/destination coordinates and raster operation. |

## Source pseudo-code: programmed I/O

```c
copy_from_user(buffer, p, count);
for (i = 0; i < count; i++) {
    while (*printer_status_reg != READY);
    *printer_data_register = p[i];
}
return_to_user();
```

This is explicitly an example of busy waiting/polling. It is not a production recommendation.

## Source ANSI example

To delete line 3, the chapter gives:

```text
ESC [ 3 ; 1 H ESC [ 0 K ESC [ 1 M
```

Spaces are explanatory separators and are not sent.

## Safety boundary

The chapter does not provide modern Linux/Windows commands for DMA, interrupt routing, disk formatting, RAID administration, ACPI or device power control. Do not invent production commands from model memory. Exact platform procedures remain `[Needs confirmation]`.
