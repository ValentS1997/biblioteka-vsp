# Source findings — глава 15 «Инструменты разработки»

**Scope:** `p0419:c01`–`p0441:c01`, PDF/печатные страницы 419–441. Политика **rag_only**: source wording/examples are preserved; internal mismatches and applicability limits are recorded rather than silently corrected.

## F-01 — [Source wording/applicability boundary]: build-tool installation note

- **Locator:** `p0420:c01`, §15.1.
- Source says to install `build-essential` for Debian/Ubuntu or use `yum groupinstall` for Fedora/CentOS, otherwise search for `gcc` or “C compiler” packages.
- The exact package/group names and package-manager syntax are distribution/version dependent.
- **Decision:** preserve the source note as edition context. Current installation command/package names: **[Needs confirmation]**.

## F-02 — [Source path inconsistency]: dynamic loader path

- **Locator:** `p0425:c01`, §15.1.3.
- Example `ldd /bin/bash` output ends with:
  `/lib64/ld-linux-x86-64.so.2`.
- Immediately afterward the prose says the actual location of `ld.so` is:
  `/lib/ld-linux.so.2`.
- These are different paths/loader names in the same section.
- **Decision:** do not normalize them into one target-system path. Runtime loader path is architecture/system specific and remains **[Needs confirmation]**.

## F-03 — [Source path mismatch]: `libweird.so.1` example

- **Locator:** `p0426:c01`, §15.1.3.
- Prose introduces `libweird.so.1` in:
  `/opt/obscure/lab`.
- The following compiler example uses:
  `-Wl,-rpath=/opt/obscure/lib -L/opt/obscure/lib -lweird`.
- **Decision:** preserve both literal source paths and flag the mismatch. The command is not rewritten to match the prose.

## F-04 — [Source example limitation]: unquoted `$@` in LD_LIBRARY_PATH wrapper

- **Locator:** `p0427:c01`, §15.1.3.
- Source wrapper ends with:
  `exec /opt/crummy/bin/crummy.bin $@`.
- Earlier chapter 11 material establishes that shell quoting affects argument boundaries.
- **Decision:** retain the chapter 15 wrapper literally as source evidence, but do not present it as a universally robust argument-forwarding template. Production wrapper policy: **[Needs confirmation]**.

## F-05 — [Source formatting issue]: `-Wl, -rpath`

- **Locator:** `p0428:c01`, end of §15.1.3.
- Prose refers to using `-Wl, -rpath` with spacing after the comma, while the earlier executable command uses `-Wl,-rpath=...`.
- **Decision:** command inventory uses the exact earlier command form and records the prose variant here instead of silently reconciling it.

## F-06 — [Source/example boundary]: self-reference in Makefile flag example

- **Locator:** `p0436:c01`, §15.2.8.
- Source example contains:
  `CFLAGS=$(CFLAGS) $(MYPACKAGE_INCLUDES) $(PNG_INCLUDES)`
  and similarly for `LDFLAGS`.
- The chapter does not explain evaluation flavor/override behavior for this self-reference.
- **Decision:** preserve the example as source content but do not promote it as a canonical reusable Makefile pattern outside the chapter. Exact GNU make behavior/policy is **[Needs confirmation]** without external documentation.

## F-07 — [Source extraction issue]: `Cc` in make output

- **Locators:** `p0432:c01` and `p0434:c01`.
- Retrieved examples show commands beginning with `Cc` in some make output, while surrounding text and other lines use `cc`.
- **Decision:** treat `Cc` as an extraction/source rendering artifact candidate. Analytical artifacts use neutral “compiler command” wording unless the source unambiguously shows `cc`.

## F-08 — [Source applicability boundary]: Java invocation

- **Locator:** `p0440:c01`, §15.5.
- Source literal command is:
  `java file.class`.
- The chapter does not provide additional qualification about class naming/classpath rules.
- **Decision:** preserve the literal source command in `commands.md` and mark real-target Java runtime behavior as **[Needs confirmation]** rather than correcting it from external knowledge.

## F-09 — [Source scope boundary]: explicit transition section, no review questions

- **Locator:** `p0441:c01`, §15.6 «А что дальше? Компиляция пакетов».
- This is an explicitly labeled transition/final section and is preserved as `summary.md`.
- `p0442:c01` begins chapter 16.
- No control/review questions are present.
- **Decision:** create `summary.md`; omit review-question artifacts.

## F-10 — [Source figure unavailable]: Makefile dependency diagram

- **Locator:** `p0432:c01`, fig. 15.1 «Зависимости Makefile».
- Project RAG does not provide the original diagram as a multimodal object.
- **Decision:** `diagram.md` reconstructs only dependencies explicitly stated in the surrounding text. Exact original visual layout remains **[Needs confirmation]**.

## Current-system applicability

Compiler choice/version, library locations, dynamic-loader path, installed development packages, Make implementation, interpreter paths, Java runtime/JDK layout and package build policy are environment-specific. Any live-system value remains **[Needs confirmation]** unless supplied by higher-priority evidence.
