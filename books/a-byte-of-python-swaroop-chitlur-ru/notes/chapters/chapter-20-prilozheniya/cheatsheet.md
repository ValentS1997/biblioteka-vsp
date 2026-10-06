# Chapter 20 cheatsheet — «Приложения»

## Symptom / problem framing

Нужно закрыть финальные приложения книги одним каноническим артефактом без потери
исходной структуры 20–23 и без превращения исторических source claims в current facts.

## Baseline / context

Merged source map:

`FLOSS → book-production history → version history → translation workflow → final author bio`

Boundary:

`p0151:c01 → p0160:c01` / PDF 151–160.

## Read-only checks

1. Любой claim о popularity/current status трактовать как source-edition statement.
2. Original appendix number сохранять при ссылке на материал.
3. Не нормализовать повреждённые URLs молча.
4. Не выводить exact Git/build commands, которых нет в source.
5. Version-history dates сохранять как source timeline.
6. PDF 160 не называть частью Appendix 23 — это separate final back matter.

## Interpretation

- FLOSS source framing: use/change/distribute + sharing/community.
- Appendix 21 documents the tools/formats used to produce the book over time.
- Appendix 22 is a changelog/history, not current Python release history.
- Appendix 23 gives a high-level contributor/translation workflow.
- Final PDF page gives a short author biography.
- All four appendices are merged only at artifact-organization level.

## Next action

Book chapter-analysis workflow: **complete after merge and post-merge verification**.

Remaining reading state: unchanged from repository metadata.

## Modifying action

### Translation workflow actions

Source instructs the contributor to:

- create a repository fork;
- download the repository;
- edit `.pd` files;
- read Pandoc README;
- install required conversion/build software.

Effect: would modify local/remote repository state and local files/tooling.

Exact commands: **[Needs confirmation]**.

Verification: **[Needs confirmation]** — source provides no explicit acceptance test.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- Appendix 20 material maps to PDF 151–152.
- Appendix 21 material maps to PDF 153–154.
- Appendix 22 timeline maps to PDF 155–158.
- Appendix 23 instructions map to PDF 159.
- PDF 160 is recorded as final back matter.
- No source pages remain after PDF 160.
- No synthetic operational command is introduced.

## Rollback

Canonical note creation is repository documentation work.

For any future translation/build actions described by the source:
**[Needs confirmation]**.
