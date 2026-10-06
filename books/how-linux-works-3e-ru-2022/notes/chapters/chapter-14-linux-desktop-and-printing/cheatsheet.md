# Шпаргалка: рабочий стол Linux и печать по главе 14

## Symptom / problem framing

Типовые задачи:

- определить Wayland или X;
- найти compositor/X server;
- увидеть input devices/events;
- понять, почему X application работает через compatibility layer;
- получить window ID / X events;
- понять X input mapping;
- различить system/session D-Bus activity;
- локализовать printing issue по этапам pipeline.

## Baseline / context

Desktop:

~~~text
application
   ↓
toolkit / desktop environment
   ↓
Wayland compositor OR X server + window manager
   ↓
input/display devices
   ↓
kernel / framebuffer
~~~

Printing:

~~~text
application
   ↓
CUPS / queue
   ↓
filter / RIP / Ghostscript
   ↓
printer driver / PPD
   ↓
backend
   ↓
printer
~~~

## Read-only checks

### Wayland/X context

Check source variable:

~~~text
$WAYLAND_DISPLAY
~~~

If it resembles `wayland-0`, source treats the session as Wayland.

Wayland compositor socket owner:

~~~bash
ss -xlp | grep wayland-
~~~

### Input devices/events

~~~bash
libinput list-devices
libinput debug-events --show-keycodes
~~~

These inspect kernel-backed input devices/events.

### X clients/events

~~~bash
xwininfo
xlsclients -l
xev
xinput --list
xinput --list-props <id>
~~~

Useful mapping:
- `xwininfo` → window geometry + ID;
- `xlsclients -l` → client/window list;
- `xev` → X event stream;
- `xinput --list` → device topology;
- `xinput --list-props` → device properties.

### D-Bus

~~~bash
dbus-monitor --system
dbus-monitor --session
~~~

Use system vs session mode depending on event class.

### CUPS

Source gives browser endpoint:

~~~text
http://localhost:631/
~~~

Use for current configuration/jobs visibility. Source does not endorse default web administration as a secure change path.

## Interpretation

### Wayland

Client renders into its own buffer. Compositor combines buffers and routes input.

`WAYLAND_DISPLAY` usually points to compositor socket name.

### X

X server centrally manages display/input. Window manager is an X client assisting with placement/decorations.

`DISPLAY` identifies X display such as `:0`.

### Xwayland

Xwayland lets X applications run under Wayland by operating an X server as a Wayland client.

### Input path

Kernel input events → libinput → compositor/X → application.

If `libinput debug-events` sees input but application does not, failure is above kernel event collection.

### D-Bus

System bus:
- system-wide services/events;
- source config: `/etc/dbus-1/system.conf`;
- Unix socket: `/var/run/dbus/system_bus_socket`.

Session bus:
- per-desktop-session application traffic;
- usually noisier.

### Printing

If job is accepted but printer output is wrong, distinguish:
1. queue/server;
2. filter/RIP;
3. printer-specific conversion;
4. backend/device path.

## Next action

1. Identify Wayland/X.
2. Confirm compositor/X server/session layer.
3. Confirm raw input path if input issue.
4. Move to X/window/client tooling only when relevant.
5. Use D-Bus monitor for cross-process desktop events.
6. For printing, identify the last successful pipeline stage.
7. Do not edit low-level configs when supported desktop/printer tools provide the intended control surface.

## Modifying action

Source-confirmed modifying/session actions:

~~~bash
xinput --set-button-map dev 3 2 1
startx
xinit
~~~

Source also names `xmodmap`, `xkbcomp`, `setxkbmap` and `xset` for X configuration, but does not provide a complete safe write workflow for these in the verified chapter.

Printer modifications are intentionally delegated to graphical distribution tools: exact commands `[Needs confirmation]`.

## Verification / acceptance checks

| Change | Verification |
|---|---|
| input button map | re-check device behavior / properties in active X session |
| manual X session | expected X clients/session start on intended display/VT |
| keyboard/input preference | confirm intended event/key behavior |
| D-Bus diagnosis | expected event appears on correct bus |
| printer setup | CUPS shows intended printer/job and actual output succeeds |

## Rollback

- `xinput --set-button-map` → restore prior mapping only if captured: `[Needs confirmation]`.
- `startx/xinit` → terminate manual graphical session; persistent rollback depends on accompanying config.
- XKB/xmodmap/xset changes → exact inverse depends on previous state: `[Needs confirmation]`.
- D-Bus monitoring → terminate monitor process; no persistent bus change in shown commands.
- Printer config → restore known-good distro/CUPS configuration; exact source rollback `[Needs confirmation]`.
