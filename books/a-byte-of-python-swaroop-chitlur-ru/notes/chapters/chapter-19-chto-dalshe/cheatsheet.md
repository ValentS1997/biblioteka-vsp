# Chapter 19 cheatsheet — «Что дальше»

## Symptom / problem framing

Базовые конструкции Python уже пройдены; следующий шаг — самостоятельные проекты,
чтение/разбор существующего кода и выбор специализированных libraries/tools.

## Baseline / context

Source progression:

`learn syntax → build project → practice → read code → use libraries/community → specialize`

## Read-only checks

Перед самостоятельным project проверить:

1. Что именно программа должна делать.
2. Какие данные нужно хранить.
3. Нужна ли persistence.
4. Какие operations являются state-changing.
5. Существуют ли подходящие standard/external libraries.
6. Какие platform/licensing constraints есть у выбранных tools.
7. Являются ли source recommendations всё ещё актуальными — **[Needs confirmation]**
   вне `rag_only` workflow.

## Interpretation

### Address book

Source decomposition:

`Contact class → dict keyed by name → pickle persistence → CRUD/search behavior`.

### replace

Source leaves design open:

`files + search string/pattern + replacement → modified files`.

### Continuing study

Source recommends:

- exercises;
- reading programs;
- Q&A/documentation;
- video/tutorials;
- discussion communities;
- news;
- package catalog + `pip`;
- GUI toolkits;
- alternative Python implementations;
- functional programming.

## Next action

После главы 19 заканчивается основной учебный текст. Далее идут приложения:

- 20 — FLOSS;
- 21 — о книге;
- 22 — история версий;
- 23 — инструкция по переводу.

## Modifying action

### Address-book persistence

Source suggests `pickle`.

Effect: persistent filesystem writes.

Verification: data survives program restart.

Rollback: **[Needs confirmation]** — no source implementation/path/restore process.

### File replacement utility

Conceptual effect: modifies provided files.

No canonical source command or implementation exists.

Verification criteria before any implementation:

- intended files changed;
- unintended files unchanged;
- expected replacements count/content confirmed.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

For an address-book implementation derived later from the task:

- add/search/update/delete all work;
- stored data reloads;
- contact names map to source-model dictionary keys.

For `replace`:

- search semantics defined;
- replacement semantics defined;
- target files explicitly known;
- safe write/rollback model defined before execution.

These are task acceptance criteria derived from source requirements, not source-provided
code.

## Rollback

No executable implementation is supplied by chapter 19.

Any future persistent/file-modifying implementation requires an explicit rollback design.
