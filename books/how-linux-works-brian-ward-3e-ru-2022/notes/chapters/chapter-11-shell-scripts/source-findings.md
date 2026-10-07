# Source findings — глава 11 «Сценарии оболочки»

**Scope:** `p0344:c01`–`p0367:c01`, PDF/печатные страницы 344–367. Политика **rag_only**: source examples are preserved; inconsistencies and pedagogical limitations are recorded rather than silently rewritten.

## F-01 — [Source example limitation]: unquoted `$@` in argument-forwarding example

- **Locator:** `p0350:c01`, §11.3.3.
- Source example:
  `gs ... $@`
- Earlier/later chapter text establishes that quoting determines argument boundaries and that shell expansion occurs before the command receives arguments (§11.2).
- **Issue:** the example demonstrates “forward all arguments” but does not discuss preservation of arguments containing spaces/special characters.
- **Decision:** keep the source example unchanged in provenance, but do not present it as a universally robust forwarding template. Exact production-safe forwarding policy: **[Needs confirmation]** from project shell standards.

## F-02 — [Source example limitation]: unquoted filename variable in file loop

- **Locator:** `p0355:c01`, §11.5.5.
- Source loop contains:
  - `[ -f $filename ]`
  - `ls -l $filename`
  - `file $filename`
- **Locator B:** `p0365:c01`, §11.10.4 explicitly warns that filenames may contain spaces/newlines and recommends NUL-delimited handling for `find | xargs`.
- **Issue:** the pedagogical loop is not framed as safe for arbitrary filenames.
- **Decision:** preserve the example as teaching syntax for `for`/`test`; operational artifacts warn that arbitrary filename handling needs stronger boundaries.

## F-03 — [Source example limitation]: PID-named temp file precedes explicit `mktemp` recommendation

- **Locator A:** `p0359:c01`, §11.6.2 uses `FILE=/tmp/whiletest.$$`.
- **Locator B:** `p0360:c01`–`p0361:c01`, §11.8 says a PID-based name can be used, but recommends `mktemp` “чтобы убедиться, что конфликтов не возникнет”.
- **Decision:** the while-loop example is treated as control-flow pedagogy, not the chapter's preferred temporary-file pattern. Operational artifacts use `mktemp` + cleanup as the stronger source-backed pattern.

## F-04 — [Source extraction issue]: malformed dash in tar/subshell pipeline

- **Locator:** `p0366:c01`, §11.11.
- Extracted source:
  `tar cf – orig | (cd target; tar xvf -)`
- The character after `cf` is rendered as a long dash rather than an unambiguous ASCII hyphen.
- **Impact:** the line is not safe to publish as copy-paste executable syntax.
- **Decision:** `commands.md` records the pipeline/subshell concept but does not normalize the ambiguous archive token silently.

## F-05 — [Source example limitation]: direct source/sourcing trust boundary is implicit

- **Locator:** `p0366:c01`–`p0367:c01`, §11.12.
- Source example: `. config.sh`.
- Source correctly distinguishes sourcing from executing a separate script: sourced commands affect the current shell.
- **Operational implication:** any commands in the sourced file execute with the current shell's privileges/environment.
- **Decision:** artifacts surface this as an explicit trust boundary; the chapter does not provide ownership/signature validation commands, so those remain **[Needs confirmation]**.

## F-06 — [Source scope boundary]: no explicit chapter summary/review section

- **Locator:** `p0367:c01`, §11.14 «Когда не стоит использовать сценарии оболочки».
- This is concluding design guidance, but it is not labeled «Выводы», «Резюме», «Что дальше?» or an equivalent chapter summary.
- `p0368:c01` starts chapter 12.
- **Decision:** no `summary.md`; no review-question artifacts.

## Current-system applicability

Interpreter path, shell implementation, command availability, file names, permission policy, temporary directory policy and project linting/quoting conventions are environment-specific. Values and standards for a real system/project remain **[Needs confirmation]** unless supplied by higher-priority evidence.
