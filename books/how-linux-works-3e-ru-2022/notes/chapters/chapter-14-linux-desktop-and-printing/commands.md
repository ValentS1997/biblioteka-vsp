# Команды и интерфейсы главы 14

Только commands/interfaces, явно подтверждённые RAG главы 14.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `$WAYLAND_DISPLAY` | Identify Wayland display/socket name | read-only environment inspection | No state change | Empty value not an absolute proof in all edge cases | Compare with active session/socket | N/A |
| `ss -xlp | grep wayland-` | Find listening Wayland Unix socket/process | read-only | No state change | Match socket to process/PID | N/A |
| `weston-info` | Inspect compositor interfaces | read-only/workload-generating | Queries compositor | Limited diagnostic scope | Review advertised interfaces | N/A |
| `libinput list-devices` | List input devices/capabilities | read-only | No intended state change | Output can be large | Match kernel event path/device | N/A |
| `libinput debug-events --show-keycodes` | Observe input events/keycodes | workload-generating/read-only | Streams input events | Exposes keystroke metadata while running | Generate controlled input and observe | Stop process |
| `weston` | Run reference Wayland compositor | state-changing/session | Starts compositor/session context | Can change backend selection of dual-capable apps; source warns of confusion inside X | Confirm compositor/window behavior | Terminate compositor |
| `startx` | Start X session manually | state-changing/session | Starts X session | Session mechanics differ from display-manager session | Confirm intended session/display | Terminate session; config rollback `[Needs confirmation]` |
| `xinit` | Start basic X session | state-changing/session | Starts X session | Same startup/config mismatch risk | Confirm intended clients/session | Terminate session; config rollback `[Needs confirmation]` |
| `xwininfo` | Inspect selected X window | read-only | No state change | Requires X window selection | Obtain window ID/geometry | N/A |
| `xlsclients -l` | List X clients/window IDs | read-only | No state change | None | Compare client/window list | N/A |
| `xev` | Observe X events | workload-generating/read-only | Creates/uses event-monitor window | Event stream may be noisy | Generate controlled pointer/key event | Stop process |
| `xev -id <id>` | Attach X event monitor to existing window | workload-generating/read-only | Observes selected window events | Wrong ID monitors wrong window | Confirm target window ID | Stop process |
| `xinput --list` | List X input topology | read-only | No state change | None | Map device IDs | N/A |
| `xinput --list-props <id>` | Show X input device properties | read-only | No state change | Device IDs can change across sessions | Confirm device name + properties | N/A |
| `xinput --set-button-map dev 3 2 1` | Remap 3-button mouse example | state-changing/input | Changes active X button mapping | Can make pointer controls confusing/unusable | Test buttons / inspect state | Restore previous mapping: `[Needs confirmation]` |
| `xmodmap` | Legacy X key mapping mechanism, source mention | state-changing potential | Can modify X keymap depending invocation | Exact workflow not supplied | `[Needs confirmation]` | `[Needs confirmation]` |
| `xkbcomp` | Compile XKB keyboard map, source mention | state-changing potential/tooling | Produces/handles keyboard map | Full workflow not supplied | `[Needs confirmation]` | `[Needs confirmation]` |
| `setxkbmap` | Load/activate XKB map, source mention | state-changing/input | Changes active keyboard mapping | Can disrupt keyboard layout | Verify intended key behavior | Restore prior map: `[Needs confirmation]` |
| `xset q` | Show X settings/status | read-only | No state change | Legacy/limited scope | Review screensaver/DPMS status | N/A |
| `dbus-monitor --system` | Monitor system D-Bus | workload-generating/read-only | Subscribes to bus events | May expose event/message metadata | Trigger controlled system event | Stop process |
| `dbus-monitor --session` | Monitor session D-Bus | workload-generating/read-only | Subscribes to session events | High-volume output / metadata exposure | Trigger controlled desktop event | Stop process |
| `lpr` | Simple CUPS client named by source | state-changing/workload | Submits print data/job | Exact invocation/file target not given | Verify CUPS job/output | Cancellation workflow `[Needs confirmation]` |

## Configuration / endpoints named by source

- Wayland runtime socket usually under `/run/user/<uid>`, or location from `$XDG_RUNTIME_DIR`.
- X display environment: `DISPLAY`.
- D-Bus system config: `/etc/dbus-1/system.conf` — source says do not edit it.
- D-Bus system socket: `/var/run/dbus/system_bus_socket`.
- CUPS configuration usually under `/etc/cups`.
- CUPS/IPP: TCP port `631`.
- CUPS local web view: `http://localhost:631/`.

## Source safety notes

1. Direct X TCP network transparency is normally unencrypted and source considers it unsafe; distributions commonly disable it with `-nolisten tcp`.
2. Do not casually run a second compositor inside X; source warns dual-backend applications may switch unexpectedly.
3. Input remapping is state-changing and previous mapping should be captured before modification.
4. Do not edit `/etc/dbus-1/system.conf`.
5. Source does not recommend default CUPS web administration for changes; prefer distribution graphical printer tools.
