# Главы — Основы администрирования информационных систем

- Book ID: `information-systems-administration-bobyntsev-ru`; inventory: `0024`.
- RAG status: `ACCEPTED`; source SHA-256: `a5d6a2677d4b0e33a34dec3b7aae8b77f711bb748046d25766becb479f66663f`.
- Numbered chapters verified against RAG TOC: **8**.
- Complete chapter directories committed in this branch: **2/8 (25%)** (nine individual chapter files verified; chapter-notes/SVG CI PASS at artifact HEAD 5c8182bf).
- Remaining: **6**; next chapter to analyze: **3 — Доменная модель безопасности в вычислительных сетях**.
- Chapter artifact link: [Глава 1 — Введение в администрирование информационных систем](chapter-01-vvedenie-v-administrirovanie-informatsionnyh-sistem/README.md). All six required files and three conditional files are committed and read back. [Chapter validation PASS](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38865448781) for artifact HEAD 5c8182bf; any subsequent Git commit is rechecked separately.
- Source-verified chapter inventory and PDF locators: [plan.yaml](plan.yaml).

## Canonical publication process

Use `templates/process-compliance-router-v1.2.yaml`, `templates/chapter-publication-v1.0.yaml`, `templates/chapter-analysis-request-v1.4.yaml` and `templates/chapter-artifact-collection-v1.8.yaml` from `main`. The source of chapter facts is canonical addressable RAG only. Files must be written as individual Git paths on the book branch, not as ZIP/archives or chat attachments. Publication must not modify the reading status.

## TOC provenance and source finding

RAG TOC chunks `p0004-c01` and `p0005-c01` (PDF pp. 4–5) enumerate chapters 1–8. The eight openings were independently located at PDF pages 24, 51, 86, 116, 142, 145, 159 and 188.

**[Source contradiction]** The TOC chunk `p0004-c01` lists chapter 1's «Контрольные вопросы» at printed page 78 although chapter 2 begins at printed page 50. This anomalous entry was not used to infer chapter boundaries and requires source-aware review when analyzing chapter 1. The extracted heading of chapter 6 on PDF p. 145 also contains the textual defect «ДАННЬК», while the TOC on p. 5 says «ДАННЫХ»; no independent correction is asserted.

## Published chapters

- [Глава 1 — Введение в администрирование информационных систем](chapter-01-vvedenie-v-administrirovanie-informatsionnyh-sistem/README.md) — RAG PDF p. 24–50, all nine individual Git files verified; [chapter-notes/SVG CI PASS](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38865448781) for artifact commit 5c8182bf; branch-tip CI tracked separately.
- [Глава 2 — Администрирование вычислительных сетей](chapter-02-administrirovanie-vychislitelnyh-setey/README.md) — RAG PDF p. 51–85, six mandatory Git artifacts plus review-questions, review-answers and source-findings; **46** questions/answers; all nine individual files read back. Chapter validation CI on this updated branch is pending.
- Remaining chapters 3–8 have no complete published artifact collection. Next chapter analysis starts only upon explicit user command.
