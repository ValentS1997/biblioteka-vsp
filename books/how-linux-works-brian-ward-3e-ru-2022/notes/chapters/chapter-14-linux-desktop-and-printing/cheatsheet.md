# Cheatsheet — глава 14 «Краткий обзор рабочего стола Linux. Вывод на печать»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0402:c01`–`p0418:c01`, PDF/печатные страницы 402–418. Только `rag_only`.

## Symptom / problem framing

Глава помогает локализовать desktop/printing проблемы по владельцу механизма:

1. display stack: Wayland, X или Xwayland;
2. compositor/window manager;
3. input stack: kernel event device → libinput → compositor/X;
4. X client/window/event layer;
5. D-Bus system/session IPC;
6. CUPS printing pipeline.

Главный operational вопрос: **какой компонент реально владеет состоянием**, прежде чем менять low-level settings.

## Baseline / context

| Область | Модель главы | PDF |
|---|---|---:|
| Framebuffer | Memory image ultimately presented by graphics hardware | 403 |
| X | Central X server mediates clients, input and display | 403–404 |
| Wayland | Clients render buffers; compositor combines them | 404–409 |
| Window manager | X: client/helper; Wayland: compositor role | 404–405 |
| Toolkits | GTK+/Qt provide common widgets/libraries | 405 |
| Desktop environment | GNOME/KDE/Xfce combine toolkit, themes and integration | 405–406 |
| Input | libinput normalizes kernel input events | 407–408 |
| X compatibility | Xwayland runs X clients under Wayland | 408–409 |
| X inspection | xwininfo/xev/xinput expose windows/events/devices | 411–415 |
| D-Bus | system/session message buses connect processes | 415–417 |
| Printing | app → CUPS queue → filters/RIP/driver → backend → printer | 417–418 |

## Read-only checks

```sh
echo "$WAYLAND_DISPLAY"
echo "$XDG_RUNTIME_DIR"
echo "$DISPLAY"

ss -xlp | grep wayland-
weston-info

libinput list-devices
libinput debug-events --show-keycodes

xwininfo
xlsclients -l
xev
xev -id window_id
xinput --list
xinput --list-props device_id
xset q

dbus-monitor --system
dbus-monitor --session
```

Additional inspection points:

- X server process is named `X` or `Xorg` in the source.
- Wayland socket is typically named by `$WAYLAND_DISPLAY` and placed under `/run/user/<uid>` or `$XDG_RUNTIME_DIR`.
- CUPS web interface is shown at `http://localhost:631/` for inspecting configuration/jobs.
- CUPS config is described as commonly under `/etc/cups`.

## Interpretation

| Observation | Interpretation from source | Still unchecked |
|---|---|---|
| `WAYLAND_DISPLAY=wayland-0` | Source heuristic: current session uses Wayland | Exceptions exist; Xwayland may also be present |
| `WAYLAND_DISPLAY` empty | Source heuristic: likely X | Exact session stack [Needs confirmation] |
| `ss -xlp` maps wayland socket to `gnome-shell` | That process owns/listens on Wayland socket | Internal compositor implementation details |
| libinput lists event device | Kernel input device is visible to libinput | Whether desktop/compositor uses same device/config |
| xwininfo returns window ID | X server knows selected client window | Desktop-level ownership/policy |
| xev shows key/mouse events | X client receives server events | Higher-level desktop binding still separate |
| xinput property exists | X input layer exposes configurable property | Desktop may override it |
| dbus-monitor system quiet | System bus currently has little observable activity | Not proof that D-Bus is unused |
| dbus-monitor session busy | Desktop applications exchange many session messages | Which app owns each behavior requires more mapping |
| CUPS queue contains job | Print server accepted job | Filter/backend/printer success still separate |

## Next action

1. Identify display stack first: Wayland, X, or Xwayland compatibility.
2. Identify the owning compositor/window manager or X server.
3. For input issues, inspect kernel/libinput view before changing X/desktop properties.
4. For X behavior, inspect window/event/device state before applying `xinput`/layout changes.
5. For desktop IPC, determine whether the event lives on system or session D-Bus.
6. For printing, follow the queue/filter/backend pipeline rather than jumping directly to the printer.
7. If desktop environment re-applies settings, change the owner layer instead of fighting it with lower-level commands.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| Start `weston` inside X | Runs nested Wayland compositor | Can cause dual-backend apps to choose unexpected Wayland session |
| `chvt` | Switch active virtual terminal | Changes active console/session |
| `startx` / `xinit` | Starts X session manually | Different startup path from display manager |
| `xinput --set-prop` | Changes X input property | May break pointer/input behavior; DE can override |
| `xinput --set-button-map dev 3 2 1` | Reorders mouse buttons | Live user-input change |
| `xmodmap` / `setxkbmap` | Changes keyboard mapping | Can make keyboard layout unusable/confusing |
| `xsetroot` / desktop settings | Changes X/root or desktop background | May be invisible/overridden by DE |
| CUPS printer/config changes | Alters print queues/devices | Can disrupt shared printing |
| `lpr` | Submits print job | Consumes queue/printer resources |

## Verification / acceptance checks

| Change | Verification | Acceptance |
|---|---|---|
| Nested compositor | inspect `WAYLAND_DISPLAY`, socket owner, launched apps | Only intended apps/session use nested compositor |
| X input property | `xinput --list-props` + functional pointer test | Intended property persists long enough and input remains usable |
| Button map | controlled click test | Expected left/right mapping only |
| Keyboard map | `xev` keycodes/keysyms + actual typing test | Intended mapping without lost critical keys |
| D-Bus diagnosis | monitor correct bus while reproducing event | Expected signal/method activity appears |
| Print job | CUPS queue + physical printer result | Job leaves queue successfully and output is correct |
| Printer config | GUI/CUPS readback + test page/job | Intended device/driver/backend selected |

## Rollback

- `xinput`, `xmodmap`, `setxkbmap`: capture prior properties/layout before change. Generic rollback syntax is not fully specified in chapter → **[Needs confirmation]** if baseline was not recorded.
- Nested `weston`: stop the nested compositor and return to the original X session; apps started inside it may need restart.
- `startx`/`xinit`: end the manually started X session to return to previous VT/session.
- Printer configuration: preserve prior CUPS/GUI configuration before changing; exact restore workflow is environment-specific.
- Submitted print jobs are not transactionally reversible once printed; cancellation mechanics are not provided in this chapter.

## Guardrails

- `libinput debug-events --show-keycodes` can reveal key activity: do not capture sensitive typing.
- X network TCP listening is described as insecure without encryption; source says it is commonly disabled.
- Do not use low-level X input settings if the desktop environment owns and continuously reapplies those preferences.
- Do not edit `/etc/dbus-1/system.conf`; the source explicitly says not to.
- Do not treat CUPS web administration as a safe default management path; the source prefers distro graphical tools.
- D-Bus monitoring and input-event monitoring may expose user/system activity; use only on authorized systems.
