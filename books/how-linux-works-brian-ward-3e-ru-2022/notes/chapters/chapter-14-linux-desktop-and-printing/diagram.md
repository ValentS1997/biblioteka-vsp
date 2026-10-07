# Mermaid — глава 14 «Краткий обзор рабочего стола Linux. Вывод на печать»

Источник: **RAG `p0402:c01`–`p0418:c01`**, PDF/печатные страницы 402–418. Диаграммы синтезированы из текстово подтверждённых связей главы.

## 1. Desktop components

```mermaid
flowchart TD
  FB["Framebuffer"] --> DISP["Display/window system"]
  DISP --> WM["Window manager / compositor"]
  WM --> TK["Toolkit: GTK+ / Qt"]
  TK --> DE["Desktop environment: GNOME / KDE / Xfce"]
  DE --> APP["Applications"]
  APP --> IPC["D-Bus / other IPC"]
```

The chapter treats the Linux desktop as cooperating components rather than a strict deep hierarchy (§14.1).

## 2. X rendering model

```mermaid
flowchart TD
  APP["X client"] --> XS["X server"]
  INPUT["Keyboard / mouse"] --> XS
  XS --> APP
  WM["X window manager = X client/helper"] --> XS
  XS --> FB["Framebuffer / display"]
```

The X server centrally mediates rendering and input; the window manager is itself a client that assists with placement/decorations (§14.1.2, §14.1.4).

## 3. Wayland rendering model

```mermaid
flowchart TD
  C1["Wayland client A"] --> B1["Own window buffer"]
  C2["Wayland client B"] --> B2["Own window buffer"]
  B1 --> COMP["Wayland compositor"]
  B2 --> COMP
  KIN["Kernel input devices"] --> LIB["libinput"]
  LIB --> COMP
  COMP --> C1
  COMP --> C2
  COMP --> FB["Framebuffer / display"]
```

Wayland clients render their own buffers; the compositor combines them and routes input (§14.1.3–14.3.2).

## 4. Xwayland compatibility

```mermaid
flowchart TD
  XAPP["X-only application"] --> XW["Xwayland server"]
  XW --> WL["Wayland compositor"]
  WAPP["Native Wayland application"] --> WL
  WL --> DISP["Display"]
```

Xwayland is an X server running as a Wayland client; the source says the reverse model is not equivalent (§14.3.3).

## 5. Wayland compositor discovery

```mermaid
flowchart TD
  ENV["WAYLAND_DISPLAY"] --> SOCK["Socket under /run/user/<uid> or XDG_RUNTIME_DIR"]
  SOCK --> SS["ss -xlp"]
  SS --> PROC["Owning/listening process"]
  PROC --> IMPL["Compositor implementation, e.g. Mutter via gnome-shell"]
```

The source uses socket ownership as a practical way to infer the compositor process (§14.3.1).

## 6. X diagnostic ladder

```mermaid
flowchart TD
  WIN["Window symptom"] --> INFO["xwininfo / xlsclients"]
  INFO --> EVT["xev"]
  EVT --> INPUT["xinput"]
  INPUT --> OWNER{"Desktop environment owns preference?"}
  OWNER -->|Yes| DE["Change desktop-level setting"]
  OWNER -->|No| LOW["Low-level X input change"]
```

The chapter warns that multiple X configuration paths can overlap and be overridden (§14.4.3–14.4.5).

## 7. Input path

```mermaid
flowchart LR
  DEV["/dev/input event device"] --> LIB["libinput"]
  LIB --> WL["Wayland compositor"]
  LIB --> XS["X server"]
  WL --> APP1["Wayland client"]
  XS --> APP2["X client"]
```

libinput is described as a kernel-event collection/normalization layer used by Wayland and many X systems (§14.3.2).

## 8. D-Bus event relay

```mermaid
flowchart TD
  SRC["System daemon / desktop app"] --> BUS["dbus-daemon"]
  BUS --> SYS["System bus subscribers"]
  BUS --> SES["Session bus subscribers"]
  UDEV["udev event"] --> UDISKS["udisks-daemon"]
  UDISKS --> BUS
```

The source example shows udisks-daemon relaying device events through D-Bus to interested applications (§14.5).

## 9. D-Bus instance split

```mermaid
flowchart LR
  INIT["init/system startup"] --> SYSBUS["System dbus-daemon --system"]
  SYSBUS --> SYSSOCK["/var/run/dbus/system_bus_socket"]
  LOGIN["Desktop session"] --> SESBUS["Session dbus-daemon"]
  SESBUS --> APPS["Desktop applications"]
```

The chapter separates the system bus from the optional per-session desktop bus (§14.5.1).

## 10. Printing pipeline

```mermaid
flowchart TD
  APP["Application document"] --> PS{"Already PostScript/PDF-like?"}
  PS --> SERVER["CUPS print server"]
  SERVER --> QUEUE["Print queue"]
  QUEUE --> FILTER["Print filter / RIP"]
  FILTER --> GS["Ghostscript / raster conversion"]
  GS --> DRIVER["Printer driver / PPD settings"]
  DRIVER --> BACK["Backend"]
  BACK --> PRN["Printer"]
```

The chapter describes printing as a staged conversion/queue/backend pipeline (§14.6).

## 11. Desktop troubleshooting workflow

```mermaid
flowchart TD
  S["Symptom"] --> STACK{"Wayland / X / Xwayland?"}
  STACK --> OWNER["Identify compositor/server/DE"]
  OWNER --> OBS["Use narrow diagnostic tool"]
  OBS --> CHANGE{"Change needed?"}
  CHANGE -->|No| KEEP["Keep state"]
  CHANGE -->|Yes| SNAP["Capture current live setting"]
  SNAP --> APPLY["Apply one owner-layer change"]
  APPLY --> VERIFY["Fresh-session / device verification"]
  VERIFY --> OK{"Acceptance?"}
  OK -->|Yes| DONE["Keep"]
  OK -->|No| RB["Restore baseline / restart clean session"]
```

This is an operational synthesis of the chapter rather than a desktop-specific deployment procedure.
