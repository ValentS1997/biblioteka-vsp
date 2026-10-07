# Source findings — глава 12

## Finding 1 — histogram percentages sum to 105%

Classification: `[Source arithmetic mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0212:c01`

Source histogram:

~~~text
0: 15%
1: 25%
2: 50%
3: 10%
4: 5%
~~~

The values sum to 105%.

Action:
- preserve source values;
- do not silently normalize percentages;
- treat the example as illustration of weighted histogram reduction, not validated statistical data.

## Finding 2 — Join described as from previous chapter

Classification: `[Source wording mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0213:c01`

Source says the Join pattern was considered in the previous chapter, while Join is introduced in chapter 12 itself at `p0206:c01–p0207:c01`.

Action:
- preserve wording discrepancy;
- chapter artifacts identify Join from its actual chapter-local introduction.

## Finding 3 — Merger is not a completeness barrier

Classification: `[Source semantic boundary]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0206:c01–p0207:c01`

Source explicitly contrasts:
- Merger: combines streams;
- Join: waits until the complete parallel data set is ready.

Action:
- do not treat Merger as coordinated completion;
- destructive downstream steps in the image example are placed behind Join semantics.

## Finding 4 — no executable implementation supplied

Classification: `[Needs confirmation]`

The chapter provides conceptual algorithms and pipeline composition only.

Action:
- no runtime/deployment commands are inferred;
- distributed barrier/reducer implementation remains outside RAG evidence.
