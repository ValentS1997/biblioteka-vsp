# Source findings — Chapter 3

## [Source contradiction] Base/limit values around figure 3.3

Relevant provenance:

- PDF page 220 / chunk `p0220:c01` defines the base register as the physical start address and says the limit register contains the program length.
- The same paragraph says that for the second program the values are `16 384` and `32 768`, respectively.
- Review question 2 on PDF page 291 / chunk `p0291:c01` states that the base and limit registers shown in figure 3.3 both have the value `16 384`.

These source variants cannot all describe the limit register as a program length for the same 16-KiB second program.

Handling:

- the contradiction is preserved rather than silently corrected;
- conceptual artifacts state only that base and limit are independent relocation/protection parameters;
- the exact numeric interpretation of figure 3.3 is marked `[Needs confirmation]` in the review answer.

No external source or model-memory adjudication was used.
