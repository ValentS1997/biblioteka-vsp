# Диаграмма: рабочий стол Linux и печать по главе 14

## Wayland model

~~~mermaid
flowchart TD
    APP["Wayland client"] --> BUF["Client-owned buffer"]
    BUF --> COMP["Compositor / window manager"]
    INPUT["Kernel input → libinput"] --> COMP
    COMP --> FB["Display framebuffer"]
    COMP --> APP
~~~

## X model

~~~mermaid
flowchart TD
    CLIENT["X client"] --> SERVER["X server"]
    WM["Window manager (X client)"] --> SERVER
    INPUT["Input devices"] --> SERVER
    SERVER --> CLIENT
    SERVER --> FB["Framebuffer / display"]
~~~

## X on Wayland

~~~mermaid
flowchart LR
    XAPP["X application"] --> XW["Xwayland"]
    XW --> WL["Wayland compositor"]
    WL --> DISPLAY["Display"]
~~~

## Desktop diagnosis

~~~mermaid
flowchart TD
    S["Desktop symptom"] --> P{"Wayland or X?"}
    P -->|Wayland| WS["WAYLAND_DISPLAY / ss socket owner"]
    WS --> LI["libinput devices/events"]
    P -->|X| XS["DISPLAY / X server / clients"]
    XS --> XWIN["xwininfo / xev / xinput"]
    LI --> APP["Application/toolkit layer"]
    XWIN --> APP
    APP --> DBUS["D-Bus if cross-process event/state"]
~~~

## D-Bus

~~~mermaid
flowchart LR
    SYS["System services"] --> SB["System dbus-daemon"]
    UDEV["udev/udisks events"] --> SB
    SB --> APPS["Interested processes"]
    DESK["Desktop applications"] --> SES["Session dbus-daemon"]
    SES --> DESK2["Other desktop applications"]
~~~

## Print pipeline

~~~mermaid
flowchart LR
    APP["Application"] --> CUPS["CUPS / queue"]
    CUPS --> FILTER["Filter"]
    FILTER --> RIP["RIP / Ghostscript"]
    RIP --> PPD["Driver + PPD settings"]
    PPD --> BACKEND["Backend"]
    BACKEND --> PRN["Printer"]
~~~
