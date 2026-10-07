# Source findings — глава 7

**Scope:** `p0208:c01`–`p0243:c01`, PDF/печатные страницы 208–243. Политика **rag_only**: исходные варианты сохраняются; внешняя документация/model memory не используются для исправления.

## F-01 — [Source extraction issue]: malformed dash in `hwclock` example

- **Locator:** `p0226:c01`, §7.5.2.
- Extracted command: `hwclock --systohc –-utc`.
- Перед `utc` присутствует длинный dash/Unicode-like символ плюс hyphen, а не однозначно два ASCII hyphen.
- Ранее на `p0224:c01` приведена форма `hwclock --systohc --utc`.
- **Decision:** canonical command inventory uses the unambiguous p0224 form and records p0226 as an extraction/source-form anomaly rather than silently treating both strings as identical.

## F-02 — [Source wording/code mismatch]: `/etc/login.defs.e` vs `/etc/login.defs`

- **Locator A:** `p0221:c01`, §7.3.3: extracted text names `/etc/login.defs.e`.
- **Locator B:** `p0242:c01`, §7.10.3: the chapter discusses `/etc/login.defs`.
- **Issue:** both forms occur in the same chapter; no evidence says they are distinct configuration files.
- **Decision:** preserve the p0221 variant in this finding; normal chapter discussion references the repeatedly described `/etc/login.defs` on p0242. Exact nature of the extra `.e`: **[Needs confirmation]**.

## F-03 — [Source extraction issue]: footnote marker embedded in cron line

- **Locator:** `p0228:c01`, §7.6.2.
- Extracted source line contains `root❶` before `/usr/local/bin/cleansystem`.
- Surrounding prose explicitly identifies ❶ as an annotation pointing to the user field `root`.
- **Decision:** `commands.md` structurally removes the annotation marker when displaying the cron syntax, while this finding preserves the source form.

## F-04 — [Source wording/code mismatch]: general PAM config guidance vs generated files

- **Locators:** `p0237:c01`–`p0242:c01`.
- §7.10.1 presents application PAM files under `/etc/pam.d` as configuration.
- §7.10.2 warns that distributions may **automatically generate some PAM files** and explicitly says not to edit such files directly; comments should identify their origin.
- **Decision:** no contradiction is inferred about PAM itself, but a generic instruction to “edit /etc/pam.d” would be unsafe. Artifacts require checking file provenance/comments before modification. Exact distro-specific generator: **[Needs confirmation]**.

## F-05 — [Source extraction issue]: original figures unavailable

The chapter references:
- fig. 7.1 — fields of a passwd entry (`p0220:c01`);
- fig. 7.2 — fields of a group entry (`p0223:c01`);
- fig. 7.3 — crontab entry structure (`p0226:c01`);
- fig. 7.4 — PAM rule execution diagram (`p0240:c01`).

`rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal objects.

**Decision:** Mermaid/SVG artifacts reconstruct only text-confirmed relationships and field semantics. Exact original layout/labels/arrows remain **[Needs confirmation]**.

## Current-system applicability

Usernames, UIDs/GIDs, journal retention policy, syslog coexistence, timezone, NTP daemon, cron paths, timer names, PAM stack and password algorithm in the examples are edition/source context. Values for a real host remain **[Needs confirmation]**.
