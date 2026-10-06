# Audit — официальный answer key vs chapter-derived answers

Source of truth for official answers:
- Appendix RAG: `p0307:c01–p0318:c01`
- PDF: `307–318`

Compared against:
- `notes/chapters/chapter-*/review-answers.md`

## Result before corrections

| Status | Count |
|---|---:|
| Semantic/polarity match | 96 |
| Mismatch | 2 |
| Total | 98 |

## Mismatch 1 — Chapter 8 / Question 8

Question:
> Включает ли этот скрипт возможность корректировки параметров БД Chroma на основе показателей эффективности выполнения сеанса?

Chapter-derived answer:
- `Нет`.

Official appendix answer:
- `Да`.

Why the derived answer differed:
- chapter code measures session time and exposes tunable behavior;
- it does not show automatic Chroma-parameter adjustment driven by those metrics.

Appendix framing:
- performance measurements can be used to make project-dependent adjustments.

Resolution:
- `review-answers.md` follows official `Да`;
- rationale preserves the implementation limitation.

Status: `[Appendix/chapter interpretation tension]`.

## Mismatch 2 — Chapter 9 / Question 5

Question:
> Является ли скачивание данных с Hugging Face единственным ресурсом для подготовки датасетов?

Chapter-derived answer:
- `Нет`.

Official appendix answer:
- `Да`.

Why the derived answer differed:
- chapter uses Hugging Face/SciQ as the worked source;
- chapter evidence does not establish that Hugging Face is the only possible dataset source.

Appendix framing:
- Hugging Face is specifically designated as the source used in the chapter.

Resolution:
- `review-answers.md` follows official `Да`;
- rationale records that exclusivity is not established by chapter implementation.

Status: `[Appendix/question wording tension]`.

## Additional appendix/chapter tension — Chapter 8 / Question 3

Official polarity matches our answer: `Нет`.

However, the appendix explanation refers to a token/API access to Chroma. The chapter implementation uses a local temporary `chromadb.Client()` and does not show separate Chroma authentication.

Status: `[Appendix/chapter wording tension]`.

## Non-binary source wording

Two appendix answers do not reduce cleanly to a literal leading «да/нет»:

- Chapter 1 / Q6 — answer says retrieval is usually triggered by a query from a user or automated system. Compact semantic normalization: `Да`.
- Chapter 2 / Q8 — answer explains that explicit component separation is beneficial, while simpler RAG can work without it. Compact semantic normalization: `Нет, с оговоркой`.

## Correction policy

For chapter-level `review-answers.md`:

1. Official appendix polarity is authoritative for “what the book answers”.
2. Chapter-derived rationale remains evidence of implementation behavior.
3. When appendix and chapter evidence diverge, both are retained and the tension is explicit.
4. No external knowledge is used to adjudicate the conflict.

## Post-correction acceptance

Verified:
- official polarity aligned: `98/98`;
- all 10 chapter files retain chapter provenance;
- appendix provenance is present in all 10 chapter answer files;
- the two original mismatches are corrected to the official appendix polarity;
- appendix/chapter tensions remain documented rather than silently erased.
