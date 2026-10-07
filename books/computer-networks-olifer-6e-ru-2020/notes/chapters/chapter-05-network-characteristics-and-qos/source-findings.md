# Source findings — chapter 5

Scope: PDF pages 134-180.

## 1. No blank source units inside the chapter

The book RAG manifest lists no blank source units between PDF 134 and PDF 180.

Handling:
- chapter boundary is fully addressable at page level;
- no missing-page reconstruction is required.

## 2. [Source extraction issue] mathematical notation

Several equations and symbols in the statistical and queueing sections lose subscripts, superscripts or Greek-variable formatting in extracted text. Examples include:
- mean / standard-deviation expressions;
- utilization notation in queueing models;
- some rate and burst formulas.

The surrounding prose usually preserves the qualitative meaning.

Handling:
- exact typography is not reconstructed from model knowledge;
- artifacts retain only relationships explicitly supported by prose and unambiguous extracted values;
- exact source equation formatting is [Needs confirmation].

## 3. [Source extraction limitation] figures are text-only in current RAG

The chapter relies on figures 5.1-5.23 for distributions, active/passive measurement, queue behavior, conditioning, feedback, reservation and traffic-engineering examples.

The RAG does not encode these as independent multimodal objects.

Handling:
- Mermaid and SVG artifacts are newly composed from extracted text;
- original visual geometry is not reconstructed.

## 4. [Source scope] Questions to Part I are outside the chapter boundary

PDF 181 starts a separate section titled `Вопросы к части I` that covers multiple chapters.

Handling:
- these questions are not treated as chapter-end review questions for chapter 5;
- `review-questions.md` and `review-answers.md` are therefore not created.

## 5. [Source timeframe] protocol and operational examples are historical source content

RSVP, named QoS mechanisms and example utilization thresholds are preserved in the book's framing.

Handling:
- no web-based freshness correction is applied in `rag_only` mode;
- thresholds/examples are treated as source examples, not universal current prescriptions.
