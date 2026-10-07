# Команды и интерфейсы — глава 14 «Краткий обзор рабочего стола Linux. Вывод на печать»

**Provenance:** `p0402:c01`–`p0418:c01`, PDF/печатные страницы 402–418. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only observation; **WG** — workload-generating / monitor; **SC** — state-changing.

## 1. Определение Wayland/X

```sh
echo "$WAYLAND_DISPLAY"
echo "$XDG_RUNTIME_DIR"
echo "$DISPLAY"
```

Source heuristic:
- `WAYLAND_DISPLAY=wayland-0` → Wayland session likely active;
- empty `WAYLAND_DISPLAY` → source says likely X, with exceptions.

## 2. Wayland compositor / socket

```sh
ss -xlp | grep wayland-
weston-info
```

- `ss -xlp` maps a Unix-domain Wayland socket to the owning process.
- `weston-info` displays compositor interfaces/capabilities in the source.

Start reference compositor:

```sh
weston
```

**Class:** SC/WG runtime session state. The source warns that running a compositor inside X can make dual-capable applications select Wayland unexpectedly.

## 3. libinput diagnostics

```sh
libinput list-devices
libinput debug-events --show-keycodes
```

- `list-devices`: RO device inventory.
- `debug-events --show-keycodes`: WG sensitive event capture.

**Boundary:** keycodes and input events can reveal user activity. Do not capture sensitive typing.

## 4. X server / sessions

Source names the X server process as `X` or `Xorg`.

Source example process form:

```text
Xorg -core :0 -seat seat0 -auth ... -nolisten tcp vt7 -novtswitch
```

This is an observed example, **not** promoted as a command to launch manually.

Manual X session commands:

```sh
startx
xinit
```

**Class:** SC/WG runtime session creation.

Virtual-terminal switching:

```sh
chvt
```

**Class:** SC active-console state. Exact VT argument is environment-specific.

## 5. X client/window inspection

```sh
xwininfo
xlsclients -l
xev
xev -id id
```

- `xwininfo`: select/inspect an X window and its ID/geometry.
- `xlsclients -l`: list X client/window identifiers.
- `xev`: observe X events in a test window.
- `xev -id id`: attach event observation to an existing X window ID.

These are RO/WG diagnostics.

## 6. X input

```sh
xinput --list
xinput --list-props 8
xinput --set-button-map dev 3 2 1
```

Source also names:
- `xinput --set-prop`;
- `xinput --set-ptr-feedback`;
- `xmodmap`;
- `xkbcomp`;
- `setxkbmap`.

Classification:
- list/list-props: **RO**;
- set-prop/set-button-map/set-ptr-feedback/xmodmap/setxkbmap: **SC** live X input state;
- `xkbcomp`: source says it compiles keyboard maps; actual invocation not provided.

No executable syntax is invented where chapter only names the tool.

## 7. X background / settings

Source names:
- `xsetroot` — old X root-window background tool;
- `gsettings` — example of desktop-environment configuration path in some GNOME installations;
- `xset q` — inspect X settings, including screensaver/DPMS state.

Only explicit command syntax supplied:

```sh
xset q
```

`xsetroot` and `gsettings` are not given concrete source invocations, so no flags are invented.

## 8. D-Bus

```sh
dbus-monitor --system
dbus-monitor --session
```

**Class:** WG/RO message observation.

Source system bus details:
- daemon started with `--system`;
- config: `/etc/dbus-1/system.conf`;
- Unix socket: `/var/run/dbus/system_bus_socket`.

The source explicitly says **do not modify** `/etc/dbus-1/system.conf`.

## 9. Printing / CUPS

Source command:

```sh
lpr
```

**Class:** SC/WG — submits a document to the CUPS print server/queue. Exact filename/flags are not supplied in the retrieved chapter.

Source CUPS inspection endpoint:

```text
http://localhost:631/
```

Source notes:
- daemon: `cupsd`;
- configuration commonly under `/etc/cups`;
- IPP uses TCP port 631;
- GUI distribution tools are preferred for adding/changing printers;
- web administration is described as not very secure under default configuration.

## 10. Printing pipeline components

Source names:
- PostScript;
- PDF;
- RIP;
- Ghostscript `gs`;
- PPD files;
- printer backend.

No full shell command sequences are given for filter/driver conversion, so none are invented.

## Command discipline

- Display/input/session commands act on live user state even when not persistent.
- Capture the current input layout/properties before modifying them.
- Do not confuse diagnostic ownership with configuration ownership: desktop environment may override low-level X settings.
- Treat event monitors as potentially sensitive.
- Do not edit system D-Bus config just because monitoring reveals the bus.
- Do not submit test print jobs without considering shared printer/queue impact.
