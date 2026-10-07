# Source findings — глава 16 «Компиляция программ из исходного кода на языке C»

**Scope:** `p0442:c01`–`p0457:c01`, PDF/печатные страницы 442–457. Политика **rag_only**: source wording/examples are preserved; inconsistencies and applicability limits are recorded rather than silently corrected.

## F-01 — [Edition/applicability boundary]: development-tool installation guidance

- **Locators:** `p0446:c01`, §16.3.1, and surrounding chapter text.
- Source names `build-essential` for Debian/Ubuntu and a Development Tools/groupinstall workflow for Fedora-like systems.
- Package names/package-manager interfaces are distribution/version dependent.
- **Decision:** preserve as edition context. Current target-system installation commands are **[Needs confirmation]**.

## F-02 — [Security heuristic boundary]: absolute paths inside source archives

- **Locator:** `p0444:c01`, §16.2.
- Source says an archive containing members such as `/etc/passwd` or `/etc/inetd.conf` should simply be discarded because it may contain a Trojan or other malicious code.
- This is presented as a source trust heuristic, not as a detailed archive-extraction security model.
- **Decision:** artifacts preserve the stop/reject guidance without adding external assumptions about specific tar implementations.

## F-03 — [Source/applicability boundary]: Autoconf out-of-tree build description

- **Locator:** `p0448:c01`, boxed subsection on separate build directories.
- Source says running `configure` from a separate build directory creates a “ферму символических ссылок” pointing to the source tree.
- Exact generated-file/link behavior can vary by package/build system.
- **Decision:** artifacts retain the general source-backed idea—separate build tree keeps source tree cleaner—without asserting identical mechanics for every package.

## F-04 — [Source formatting issue]: OpenSSL `.pc` example

- **Locator:** `p0451:c01`, §16.3.7.
- The extracted example contains:
  `Cflags: -I${includedir} exec_prefix=${prefix}`
- The placement of `exec_prefix=${prefix}` on the `Cflags` line is suspicious relative to the preceding metadata layout.
- **Decision:** preserve the literal source example only in provenance; operational artifacts do not reproduce that line as a canonical `.pc` template.

## F-05 — [Source model boundary]: pkg-config default search path

- **Locators:** `p0451:c01`–`p0452:c01`.
- Source states that pkg-config normally looks under `lib/pkgconfig` of its installation prefix and describes nonstandard `.pc` directories via links/copies or `PKG_CONFIG_PATH`.
- **Decision:** treat this as the chapter's source model. Exact search behavior on a real pkg-config implementation/environment is **[Needs confirmation]**.

## F-06 — [Source wording mismatch]: `-L` described for include files

- **Locator:** `p0456:c01`, §16.6.1.
- In the missing-header discussion, source correctly says to add an include path with `-I` through `CPPFLAGS`.
- The following parenthetical then says a linker flag `-L` may also be needed “для include-файлов”.
- Earlier chapter text (`p0448:c01`–`p0449:c01`) distinguishes `-I`/CPPFLAGS for headers from `-L`/LDFLAGS for libraries.
- **Decision:** do not propagate the phrase “`-L` for include files” as a verified technical rule. Preserve it here as an internal source mismatch.

## F-07 — [Security/applicability boundary]: temporarily adding `.` to PATH

- **Locator:** `p0456:c01`, §16.6.1.
- Source first recommends editing a broken Makefile to invoke a just-built helper as `./prog`.
- It then offers temporarily adding `.` to PATH as an alternative.
- **Decision:** artifacts keep the narrower `./prog` edit as the preferred source-supported action and record the PATH alternative here as a broader command-resolution change with security implications.

## F-08 — [Source applicability boundary]: checkinstall / rpmdev-setuptree / rpmbuild

- **Locator:** `p0447:c01`, §16.3.2.
- Source demonstrates `checkinstall make install` for Debian-like systems and names `rpmdev-setuptree` / `rpmbuild` for RPM package workflows.
- Availability, packaging policy and exact commands vary by distribution/version.
- **Decision:** commands are preserved as source context; live-system package-building workflow is **[Needs confirmation]**.

## F-09 — [Source scope boundary]: explicit final section, no review questions

- **Locator:** `p0457:c01`, §16.7 «Что дальше?».
- This is an explicitly labeled concluding/transition section.
- `p0458:c01` begins chapter 17.
- No review/control questions are present.
- **Decision:** create `summary.md`; omit review-question artifacts.

## Current-system applicability

Compiler/build-system versions, package-manager tooling, install prefixes, dependency paths, pkg-config search rules, patch applicability, package ownership and uninstall/rollback mechanisms are environment-specific. Any live-system value remains **[Needs confirmation]** unless supplied by higher-priority evidence.
