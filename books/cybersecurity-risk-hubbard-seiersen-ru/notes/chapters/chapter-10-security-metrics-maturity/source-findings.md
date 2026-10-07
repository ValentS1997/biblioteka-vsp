# Глава 10 — source findings

**Book:** `cybersecurity-risk-hubbard-seiersen-ru`. **Boundary:** EPUB spine 41–42. **Mode:** `rag_only`.

## F-01 — [Source code mismatch] Posterior sampling line is internally inconsistent

- Locator: spine 42, `OPS/ch1-40.xhtml`, chunk `e0042:c05`.
- Prior/posterior beta parameters are stored as a two-element object `beta.post.par`.
- Immediately before sampling source uses:
  ```text
  qbeta(c(0.05, 0.95), beta.post.par[1], beta. post.par[2])
  ```
- Posterior sample line is:
  ```text
  post.sample <– rbeta(1000, beta.post.par[1], beta.post.par[1], beta.post.par[2])
  ```
- Observation: `beta.post.par[1]` is repeated and `beta.post.par[2]` appears as an additional argument rather than the paired second parameter used in the preceding interval calculation.
- Source prose says this samples from the new posterior beliefs; the line is therefore internally suspicious.
- Adjudication: do **not** silently rewrite it. Correct executable form: **[Needs confirmation]** from original typeset page/code workbook.

## F-02 — [Source extraction issue] Variable name is split inside qbeta call

- Locator: `e0042:c05`.
- Extracted line:
  ```text
  qbeta(c(0.05, 0.95), beta.post.par[1], beta. post.par[2])
  ```
- The embedded space in `beta. post.par` makes the token inconsistent with `beta.post.par` used before/after.
- Likely categories include typesetting/extraction defect, but the chapter artifact does not adjudicate beyond the RAG text.

## F-03 — [Source wording/code mismatch] R operators/quotes are typographic, not safely executable as copied

- Locator: `e0042:c03–c05`.
- Assignment is repeatedly extracted as `<–` rather than a plain ASCII operator.
- Package install instruction is extracted as:
  ```text
  install.packages(«LearnBayes»).
  ```
- These are preserved as source text; `commands.md` separates them from verified executable R.
- Correct normalization: **[Needs confirmation]** if exact copy/paste compatibility is required.

## F-04 — [Source extraction issue] Figures 10.1–10.3 unavailable as standalone RAG images

- Fig. 10.1: security analytics maturity model, `e0041:c01`.
- Fig. 10.2: beta triplot after 3 successes / 7 failures, `e0042:c04`.
- Fig. 10.3: beta triplot after 5 successes / 30 failures, `e0042:c04`.
- Captions and prose are available; original axes/layout/curves are not.
- Chapter SVG/Mermaid artifacts are conceptual reconstructions only, not copies.

## F-05 — [External artifact not retrieved] R package/docs and online tutorials

The chapter names R, RStudio, `LearnBayes`, CRAN and external tutorials. Under `rag_only`, no external package documentation or downloadable code was used to repair source snippets.

## F-06 — [Source-context caution] Operational targets are examples, not local SLA

The functional-metrics section gives concrete mitigation timing examples. Those values belong to source exposition and are not adopted as policy for the user's environment.

**Итог:** canonical EPUB, checksum, RAG and reading state remain unchanged.
