# Source findings — Chapter 6

## [Source code mismatch] Listing 6.3 defines both symmetric functions as `process A`

- PDF page 517 / chunk `p0517:c01`.
- The listing describes two opposite resource-acquisition orders:
  - first function acquires resource 1 then tries resource 2;
  - second function acquires resource 2 then tries resource 1.
- Both function headers are extracted as `void process A(void)`.

Handling: preserve the source label in provenance notes; conceptual artifacts refer to “two symmetric processes” and do not silently rename the second function.

## [Source wording/code mismatch] Detection algorithm is once called an algorithm for “взаимного исключения”

- PDF page 501 / chunk `p0501:c01`.
- The surrounding section, inputs and output are explicitly about detecting **взаимоблокировку**, not testing mutual exclusion.

Handling: do not propagate the isolated wording as a separate algorithm; record it as a source wording defect.

## [Source extraction issue] Review question 26 loses exponent formatting

- PDF page 523 / chunk `p0523:c01`.
- The extracted expression appears as `manb` in the phrase “пропорционально manb”.
- The question then asks for values `a` and `b`, strongly indicating lost superscript/power formatting.

Handling: `review-questions.md` preserves the extracted form and labels the defect. `review-answers.md` derives the algorithmic operation count from the chapter algorithm rather than silently claiming a recovered typeset expression.

## [Source extraction issue] Review question 14 matrix layout is flattened

- PDF pages 521–522, primarily chunk `p0522:c01`.
- The text layer interleaves `C`, `R`, `E`, and `A` into one flattened line.
- The four rows can be reconstructed without external knowledge because the parsed `C` column totals plus `A` equal `E=(2,4,1,4,4)`.

Handling: the normalized matrix layout is shown in `review-questions.md`; the invariant used to normalize it is stated explicitly.

## [Source contradiction or extraction defect] Review question 27 has no finite safe `x` as extracted

PDF page 523 / chunk `p0523:c01` gives:

- process A allocation: `1 0 2 1 1`;
- process A maximum: `1 1 2 1 3`;
- available vector: `0 0 x 1 1`.

For resource 5, the extracted state contains only two existing instances: one allocated to A plus one available. Yet A's declared maximum for that resource is three. Changing `x` changes only resource 3, so no value of `x` can make A's maximum fifth-resource demand satisfiable.

Handling: do not invent a corrected table cell. The answer reports the consequence of the extracted table and marks the intended textbook value/result `[Needs confirmation]`.
