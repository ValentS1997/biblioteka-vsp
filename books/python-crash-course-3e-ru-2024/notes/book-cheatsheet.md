# Сводная шпаргалка — «Изучаем Python. 3-е изд.»

Эта шпаргалка агрегирует RAG-grounded chapter/appendix artifacts. Она не заменяет current external documentation для Python, libraries, Django или hosting providers.

## 1. Ментальная модель обучения

```text
minimal working example
  → observe actual result
  → change one concept
  → verify
  → refactor
  → test
  → combine into project
  → deploy
  → troubleshoot from evidence
```

## 2. Core Python

### Variables and simple values

```text
value → meaningful variable → operation → output → check
```

Key themes:
- strings, numbers, f-strings;
- whitespace cleanup;
- numeric operators;
- comments and readability;
- traceback/syntax as diagnostic evidence.

### Collections

Lists:
- ordered mutable sequence;
- index/slice;
- append/insert/remove/pop;
- sort/sorted/reverse;
- copy through slicing when an independent list is required.

Dictionaries:
- key → value mapping;
- `get()` when a missing key is valid state;
- `items()`, `keys()`, `values()`;
- nested structures.

Tuples:
- immutable element sequence in source examples.

## 3. Control flow

Condition choice:

```text
one condition → if
two outcomes → if/else
one of many → if/elif/else
multiple independent truths → separate if
```

While-loop contract:

```text
initial state
→ continue condition
→ guaranteed state change / exit
```

User input:
- `input()` returns text in chapter model;
- convert explicitly when numeric behavior is needed.

## 4. Functions and modules

Good function:

```text
one responsibility
+ clear name
+ explicit inputs
+ predictable output
+ minimal hidden mutation
```

Source covers:
- positional/keyword/default arguments;
- return values;
- optional parameters;
- list mutation vs passing a copy;
- `*args` / `**kwargs`;
- modules/imports/aliases.

## 5. Classes

```text
what object knows → attributes
what object does  → methods
specialization    → inheritance
separate component→ composition
```

Source pattern:
- `__init__()`;
- instance methods;
- defaults and controlled mutation;
- `super()`;
- method override;
- module imports.

## 6. Files, errors, persistence

```text
resource
→ read/write intent
→ expected failure
→ try/except
→ success path
→ verify persistent state
```

Source tools:
- `pathlib.Path`;
- text read/write;
- relative/absolute paths;
- `splitlines()`;
- JSON `dumps()` / `loads()`;
- `Path.exists()`.

Boundary: write operations may overwrite data.

## 7. Testing

pytest flow:

```text
expected behavior
→ test
→ code change
→ rerun
→ regression detected early
```

Source emphasizes:
- `test_*.py`;
- test functions;
- `assert`;
- fixtures;
- fix production code when a correct regression test fails.

## 8. Game project — Pygame

Core loop:

```text
events/input
→ update state
→ collisions/cleanup
→ render
→ frame timing
```

Architecture:
- `Settings` = configuration;
- `Ship`, `Bullet`, `Alien` = object responsibilities;
- Groups = lifecycle of many sprites;
- flags = continuous movement state;
- `GameStats` = score/lives/state;
- `Scoreboard` = state → rendered UI.

Project lesson:

```text
simple implementation → verify → refactor → next feature
```

## 9. Data visualization

Generic pipeline:

```text
generate/load
→ inspect schema
→ parse/convert
→ handle missing data
→ validate
→ aggregate/transform
→ visualize
→ refine
→ optionally persist
```

Source covers:
- Matplotlib line/scatter;
- random walks;
- Plotly bar/scatter_geo;
- CSV;
- GeoJSON;
- dates;
- missing records.

Data correctness comes before cosmetic tuning.

## 10. APIs

```text
request
→ check response
→ decode JSON
→ inspect schema
→ extract required fields
→ aggregate/visualize
```

Dynamic boundaries:
- response content changes;
- rate limits change;
- availability changes.

Treat live API values as runtime evidence, not permanent facts.

## 11. Django model

Initial application lifecycle:

```text
specification
→ venv
→ project/app
→ model
→ makemigrations
→ migrate
→ admin/seed
→ query
→ URL
→ view
→ template
```

Model change invariant:

```text
edit models
→ makemigrations
→ inspect
→ migrate
→ verify
```

Request/presentation split:

```text
URL → view → context → template
```

## 12. Forms, authentication, authorization

Form flow:

```text
GET → empty/prefilled form
POST → bind data
→ validate
→ save/mutate
→ redirect
```

Ownership flow:

```text
authenticate
→ login-required private views
→ filter list by owner
→ verify owner on object access
→ attach owner on create
```

Critical lesson from Chapter 19: authentication alone does not close cross-user object-ID paths.

## 13. Styling and deployment

```text
working Django app
→ consistent Bootstrap UI
→ explicit dependencies
→ hosting configuration
→ clean Git snapshot
→ deploy
→ verify
→ DEBUG=False
→ custom error pages
→ controlled update loop
```

Production boundary:
- secrets/credentials remain out of artifacts;
- debug information must not be exposed.

## 14. Appendices — operational craft

### А — Python installation

```text
command fails
→ identify OS/executable
→ verify version/path
→ repair installation
→ verify interpreter
```

### Б — editor/IDE

Use the simplest editor configuration that lets you focus on code.

High-value areas:
- consistent spaces;
- visible whitespace;
- line ruler;
- useful shortcuts;
- interactive terminal when `input()` is required.

### В — help/support

Before asking:

```text
What am I trying to do?
What have I already tried?
What exactly happened?
```

Then:
- reproduce;
- keep exact error;
- simplify to minimal example;
- search docs/community;
- ask a specific question.

### Г — Git

```text
status
→ stage new files
→ commit known-good snapshot
→ status/log
→ change
→ keep or rollback
```

Risk ladder:
- restore uncommitted edits;
- inspect old commit;
- hard history rollback;
- destroy/recreate repository metadata.

The last two are destructive and not routine recovery.

### Д — deployment troubleshooting

```text
read actual deployment log
→ find failed stage
→ first/last actionable error
→ one targeted fix
→ redeploy
→ verify
```

Do not execute commands from untrusted sources when you do not understand their effect.

## 15. Book-wide verification discipline

Across chapters the recurring working pattern is:

1. establish baseline;
2. make one understandable change;
3. inspect actual output/state;
4. localize failures from evidence;
5. refactor only after behavior works;
6. test critical behavior;
7. persist/deploy only a verified state;
8. keep rollback/recovery scope explicit.

## 16. High-risk / high-value boundaries

| Boundary | Source-grounded lesson |
|---|---|
| List/file mutation | know whether state is modified or copied |
| Exceptions | catch expected failures, not everything blindly |
| Tests | green means only asserted behavior is covered |
| Game objects | cleanup invisible/off-screen objects |
| External data | inspect schema and handle missing values |
| APIs | live data/rate limits are dynamic |
| Django ownership | object authorization must be checked on every relevant path |
| Production Django | disable debug detail |
| Git restore/reset/history deletion | distinguish reversible vs destructive recovery |
| Deployment commands | trust source and understand effect |

## 17. Книга одной строкой

```text
Python syntax
+ data/control abstractions
+ modular design
+ tests
+ three applied projects
+ versioned deployment/troubleshooting
= practical path from first script to maintainable application
```
