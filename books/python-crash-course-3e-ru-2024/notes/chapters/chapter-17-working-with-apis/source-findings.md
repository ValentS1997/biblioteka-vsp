# Source findings — глава 17

## Finding 1 — pprint() without import or definition

Classification: **[Source code mismatch]**

Provenance:
- chunk: `e0027:c03`
- EPUB spine item: `27`
- locator: `OEBPS/Text/978544614112-24.xhtml`

Shown code contains:

~~~python
pprint(f"\nKeys: {len(repo_dict)}")
~~~

В показанном `python_repos.py` импорт `pprint` или определение функции `pprint` отсутствует.

Surrounding output operations use built-in `print()`.

Adjudication: intended call `[Needs confirmation]`.

Policy action: canonical RAG не исправлять; artifact сохраняет mismatch отдельно.

## Finding 2 — visiblity key spelling

Classification: **[Source output typo]**

Provenance:
- chunk: `e0027:c03`

Sample list repository keys includes:

~~~text
visiblity
~~~

Spelling differs from normal English word “visibility”.

Whether this is a transcription/source-output typo or historical response artifact: `[Needs confirmation]`.

No external GitHub schema verification was used.

## Finding 3 — API version/header is a temporal claim

Classification: **[Source temporal claim boundary]**

Provenance:
- chunk: `e0027:c02`

Source states that GitHub “currently” uses API version 3 and shows:

~~~python
headers = {
    "Accept": "application/vnd.github.v3+json"
}
~~~

“Currently” refers to the source publication context.

Current GitHub API version/media-type requirements: `[Needs confirmation]`.

Policy action: preserve source example; do not present it as current verified guidance.

## Finding 4 — rate-limit values are historical examples

Classification: **[Source temporal claim boundary]**

Provenance:
- chunk: `e0027:c05`

Source example reports:
- search limit: 10 requests/minute;
- remaining: 9;
- specific epoch reset value.

These values describe a sample response at source time.

Current rate limits/authentication requirements: `[Needs confirmation]`.

## Finding 5 — live repository/Hacker News results are non-reproducible constants

Classification: **[Source live-data reproducibility boundary]**

Provenance:
- chunks: `e0027:c01–c10`

Examples include:
- repository totals;
- stars;
- ordering;
- fixed Hacker News story IDs;
- comments counts;
- claim about the “current” top story.

These are snapshots of live systems, not stable chapter invariants.

Policy action: treat them as historical sample output only.

## Finding 6 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0027:c02`–`e0027:c10`
- EPUB spine item: `27`
- locator: `OEBPS/Text/978544614112-24.xhtml`

Observed starts include continuation fragments such as:
- `ние language:python...`;
- `я response_dict...`;
- `po_dict['stargazers_count']...`;
- `ений частоты обращений API...`;
- `раммы...`;
- `каждого столбца...`;
- `ощью Plotly Express...`;
- `. Это позволит нам...`;
- clipped `--` at start of `e0027:c10`.

Cross-check:
- adjacent chunks preserve transition context;
- exercises 17.1–17.4 recoverable;
- chapter-end summary intact;
- `e0028:c01` confirms chapter 18;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## External-documentation boundary

The chapter explicitly points to Plotly, GitHub API and Hacker News API documentation.

These external sources were not used under `rag_only`.
