# Source findings — глава 13 «Пользовательское окружение»

**Scope:** `p0390:c01`–`p0401:c01`, PDF/печатные страницы 390–401. Политика **rag_only**: source wording and recommendations are preserved; no external/model correction is silently substituted.

## F-01 — [Source recommendation boundary]: `$HOME/bin` vs `$HOME/.local/bin`

- **Locator:** `p0393:c01`, §13.3.1.
- Main recommendation says users often create `$HOME/bin` and may put it at the start of PATH.
- Immediate note says that “в настоящее время” binaries are placed in `$HOME/.local/bin`.
- **Decision:** both source statements are preserved. Which user-local binary directory is actually used on the target system is **[Needs confirmation]**.

## F-02 — [Source model boundary]: Bash startup ordering is edition-specific guidance

- **Locators:** `p0395:c01`–`p0398:c01`, §13.4.1.
- Source model:
  - login bash reads `/etc/profile`, then the first of `.bash_profile`, `.bash_login`, `.profile`;
  - interactive non-login bash reads `/etc/bash.bashrc`, then `~/.bashrc`;
  - noninteractive shells are described as not reading startup files in the chapter's simplified model;
  - login behavior can also be forced with `-l`/`--login`.
- **Decision:** artifacts preserve this model and do not reconcile distro/shell-version differences from external documentation. Actual target behavior is **[Needs confirmation]** if operationally important.

## F-03 — [Source alternative designs]: symlink vs sourcing `.bashrc`

- **Locator A:** `p0395:c01`, §13.4.1 recommends `.bashrc` plus a symbolic link `.bash_profile` pointing to it.
- **Locator B:** `p0397:c01` says an even clearer approach is to create `.bash_profile` containing `. $HOME/.bashrc`.
- These are two alternative source designs for sharing configuration.
- **Decision:** do not collapse them into one canonical mechanism. Operational artifacts require identifying which mechanism exists before editing.

## F-04 — [Source wording boundary]: `which` described as a shell builtin

- **Locator:** `p0394:c01`, §13.3.4.
- Source says the shell built-in command `which` can identify an alias but not where it was created.
- **Decision:** preserve the wording as edition content. Whether `which` is builtin/external and how it handles aliases on a specific shell is **[Needs confirmation]**.

## F-05 — [Source recommendation boundary]: tcsh/csh startup behavior

- **Locators:** `p0398:c01`–`p0399:c01`, §13.4.2.
- Source says tcsh does not distinguish login/non-login startup behavior for the described startup-file search and recommends `.cshrc` over `.tcshrc`.
- **Decision:** preserve this chapter model without external correction. Target-shell semantics remain **[Needs confirmation]**.

## F-06 — [Source scope boundary]: no explicit summary/review section

- **Locator:** `p0401:c01`, §13.7 «Далее о файлах запуска».
- This is a forward-looking scope note about graphical startup files and the next chapter, not a labeled `Выводы`, `Резюме` or `Что дальше?` summary.
- `p0402:c01` begins chapter 14.
- **Decision:** no `summary.md`; no review-question artifacts.

## Current-system applicability

Shell executable, distro startup-file paths, login manager behavior, PATH order, user-local binary directory, prompt conventions, `umask` policy, editor/pager defaults and graphical-session startup chain are environment-specific. Any live-system value remains **[Needs confirmation]** unless supplied by higher-priority evidence.
