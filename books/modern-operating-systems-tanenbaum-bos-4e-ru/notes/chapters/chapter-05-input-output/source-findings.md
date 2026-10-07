# Source findings — Chapter 5

## [Source contradiction] Duplicate section number 5.8.2

- PDF page 470 / chunk `p0470:c01`: `5.8.2. Роль операционной системы`.
- PDF page 476 / chunk `p0476:c01`: `5.8.2. Роль прикладных программ`.
- The table of contents on PDF page 10 also exposes both entries as `5.8.2`.

Handling: preserve both source labels; do not silently renumber the application subsection.

## [Source wording/code mismatch] ECC value count for a 16-byte field

PDF page 432 states that a 16-byte ECC field has `2^144` possible values in the argument comparing 512-byte data with ECC values. The editor footnote on the same page explicitly states that 16 bytes can store only `2^128` values unless a 9-bit “byte” is being assumed.

Handling: preserve the source statement and editor correction as conflicting variants. No external adjudication is used.

## [Source contradiction] Review question 2 vs Table 5.1 wireless standard

- PDF page 382 / chunk `p0382:c01`: Table 5.1 contains `802.11n` at 37.5 MB/s.
- PDF page 480 / chunk `p0480:c01`: review question 2 asks about `802.11g` while explicitly referring to the speeds in Table 5.1.

Handling: the review answer gives the result using the table entry actually present in RAG and marks the exact 802.11g-specific result `[Needs confirmation]`.

## [Source contradiction] Review question 41 character count

PDF page 485 describes an 80-line × 80-character window but gives the total as `6480` characters. Arithmetic from the stated dimensions gives 6400.

Handling: both values are preserved. The answer shows the calculation using the dimensions and separately reports the source-literal 6480 variant.

## [Source contradiction] Full-HD dimensions in GUI discussion

PDF page 455 first lists the common resolution `1920 × 1080`, then later on the same page refers to `1920 × 1800` as “full HD” while calculating framebuffer requirements.

Handling: no silent correction is made; this inconsistency is not used as a basis for review calculations.

## [Source extraction issue] Unnumbered BitBlt exercise after question 45

PDF page 485 ends with explicit question 45 about 24-bit RGB. PDF page 486 begins with a separate BitBlt/font exercise containing subitems 1 and 2, followed by explicit question 46.

The text layer does not expose a top-level number for that BitBlt block.

Handling: `review-questions.md` and `review-answers.md` preserve it as an “Unnumbered source item after question 45” and do not invent or shift source numbering.
