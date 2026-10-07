# Source findings — глава 14 «Краткий обзор рабочего стола Linux. Вывод на печать»

**Scope:** `p0402:c01`–`p0418:c01`, PDF/печатные страницы 402–418. Политика **rag_only**: source wording and recommendations are preserved; no external/model correction is silently substituted.

## F-01 — [Source heuristic boundary]: `WAYLAND_DISPLAY` as X/Wayland detector

- **Locator:** `p0406:c01`, §14.2.
- Source says `WAYLAND_DISPLAY=wayland-0` indicates Wayland, while an empty value means X, then immediately notes exceptions.
- **Decision:** artifacts present this only as the chapter's heuristic, not as a universal detector. Exact session stack remains **[Needs confirmation]** if operationally important.

## F-02 — [Source wording/extraction issue]: “компиляторы” in multi-compositor paragraph

- **Locator:** `p0407:c01`, §14.3.1.
- Source says that to run more than one compositor simultaneously, it is necessary to start “компиляторы” on separate virtual terminals.
- Surrounding context is entirely about Wayland compositors, `wayland-0`, `wayland-1`, and compositor processes.
- **Decision:** preserve the anomalous token here; operational artifacts discuss the surrounding confirmed concept of multiple compositors without silently rewriting the literal source sentence.

## F-03 — [Source terminology issue]: “X Input Extention”

- **Locator:** `p0413:c01`, §14.4.5.
- Extracted text repeatedly names the X input extension as **X Input Extention**.
- **Decision:** preserve source terminology in findings but use neutral phrasing such as “X input extension” in analytical artifacts rather than asserting the exact English spelling as canonical.

## F-04 — [Source applicability boundary]: old X configuration tools

- **Locators:** `p0413:c01`–`p0415:c01`.
- The chapter names `xmodmap`, `xsetroot`, `xset`, `xkbcomp`, `setxkbmap`, while also saying some old tools are no longer normally used or may be overridden by desktop environments.
- **Decision:** tools are catalogued as source-described mechanisms, not current universal recommendations. Effective owner on a real desktop remains **[Needs confirmation]**.

## F-05 — [Security boundary]: input-event/keycode capture

- **Locator:** `p0408:c01`, §14.3.2.
- Source demonstrates `libinput debug-events --show-keycodes` and shows keyboard key press/release events.
- **Decision:** operational artifacts explicitly classify this as sensitive observation because it can reveal user input. This is a safety interpretation directly supported by the displayed event content.

## F-06 — [Security/applicability boundary]: X network transparency

- **Locator:** `p0411:c01`, §14.4.2.
- Source says direct X network listening on TCP port 6000 is usually unencrypted/insecure and that distributions commonly disable it via `-nolisten tcp`.
- **Decision:** preserve the source's architectural explanation, but do not turn direct X TCP listening into an operational recommendation.

## F-07 — [Source instruction boundary]: D-Bus system config

- **Locator:** `p0416:c01`, §14.5.1.
- Source identifies `/etc/dbus-1/system.conf` and explicitly says this configuration should not be changed.
- **Decision:** commands/artifacts allow observation of the system bus but treat this file as a no-edit boundary.

## F-08 — [Security/applicability boundary]: CUPS web administration

- **Locator:** `p0418:c01`, §14.6.1.
- Source says `http://localhost:631/` can show current CUPS configuration/jobs but also says managing the system through the web interface is not very secure under default settings; graphical distribution tools are preferred.
- **Decision:** artifacts distinguish inspection from administration and avoid promoting web-based changes as the preferred path.

## F-09 — [Source scope boundary]: no explicit summary/review section

- **Locator:** `p0418:c01`, §14.7 «Дополнительно об окружениях рабочего стола».
- §14.7 is a concluding scope/transition discussion leading to developer tools, not a labeled `Выводы`, `Резюме` or `Что дальше?`.
- `p0419:c01` begins chapter 15.
- **Decision:** no `summary.md`; no review-question artifacts.

## Current-system applicability

Display stack, compositor process, Wayland socket name, X display number, virtual terminal, input-device IDs/properties, desktop environment ownership, D-Bus implementation details, CUPS configuration and printer driver/backend are environment-specific. Any live-system value remains **[Needs confirmation]** unless supplied by higher-priority evidence.
