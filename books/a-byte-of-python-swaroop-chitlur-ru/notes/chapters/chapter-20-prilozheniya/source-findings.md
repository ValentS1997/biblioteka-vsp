# Source findings — глава 20 «Приложения»

Mode: `rag_only`

## Finding 1 — version-history statement conflicts with present metaclass section

Classification: **[Source contradiction]**

Provenance:

- `a-byte-of-python-swaroop-chitlur-ru:p0155:c01`, Appendix 22 / version 2.0;
- chapter 14 source boundary includes section 14.7 «Метаклассы» at
  `p0118:c01–p0120:c01`.

Appendix 22 says version 2.0 simplified the text by removing optional sections including
`метаклассы`.

However, this Russian source contains section 14.7 «Метаклассы». Chapter 14 analysis also
records a translator note saying the metaclass material was hidden/commented in the
original version and surfaced in this translation/source.

Action: preserve both source variants. Do not infer which editorial history is
authoritative beyond this source.

## Finding 2 — multiple URL/extraction glyph corruptions

Classification: **[Source extraction issue]**

Provenance:

- `p0151:c01–p0152:c01`: names such as `LibreOﬃce`, `underbird`,
  `Microso`, `Apae`;
- `p0153:c01`: `OpenOﬃce`, `anta+`;
- `p0154:c01`: `hp://www.swaroopch.com/about/`;
- `p0159:c01`: `hps://github.com/swaroopch/byte_of_python`.

Issue: source text layer contains font/ligature substitutions in project names and URL
schemes.

Action: preserve anomalies here. Canonical artifacts may use unambiguous project names
when context makes the intended name clear, but do not silently publish a repaired URL
as source-exact text.

## Finding 3 — FLOSS popularity/market-share claims are historical

Classification: **[Needs confirmation]**

Provenance: `p0151:c01–p0152:c01`, Appendix 20.

The source makes time-sensitive statements including:

- Ubuntu described as perhaps the most popular GNU/Linux distribution;
- Firefox described relative to Internet Explorer;
- Apache described as serving more than half of all websites;
- MySQL/LAMP popularity statements.

Action: treat these as statements from the source edition, not current verified facts.

## Finding 4 — software/platform capability statements are historical

Classification: **[Needs confirmation]**

Provenance: `p0151:c01–p0152:c01`.

The source describes platform support/capabilities for Ubuntu, LibreOffice, Mono,
Apache, MySQL, VLC, GeexBox and other software.

Action: preserve source meaning without promoting platform support or project status to
current facts.

## Finding 5 — “Сейчас” authoring-tool statement is edition-relative

Classification: **[Needs confirmation]**

Provenance: `p0154:c01`, Appendix 21 section 21.1.3 «Сейчас».

Source says:

`Использую Vim, Pandoc, и Mac OS X.`

The word “Сейчас” is relative to the source edition, not to the present analysis date.

Action: interpret as authoring state at the source's editorial time.

## Finding 6 — translation workflow lacks exact operational commands

Classification: **[Needs confirmation]**

Provenance: `p0159:c01`, Appendix 23.

Source instructs the reader to fork/download the repository, edit `.pd` files, read the
Pandoc README and install required software, but gives no exact Git/build/install
commands in the RAG text.

Action: canonical commands artifact contains no synthesized commands.

## Finding 7 — final author-role statement is time-sensitive back matter

Classification: **[Needs confirmation]**

Provenance: `p0160:c01`, final PDF page.

Source says Swaroop C H is currently an engineering manager for a machine-learning team
at Helpshift and gives earlier employment history.

Issue: “В настоящее время” is source-edition-relative and not externally verified.

Action: record it only as final back-matter source content.

## Finding 8 — final page is outside numbered appendices

Classification: **[Source extraction issue]**

Provenance:

- Appendix 23 content is on `p0159:c01`;
- `p0160:c01` contains only author biography text and no Appendix 23 heading/footer.

Action: merged chapter 20 includes PDF 160 solely to close canonical source coverage,
while explicitly labeling it final back matter rather than Appendix 23 content.
