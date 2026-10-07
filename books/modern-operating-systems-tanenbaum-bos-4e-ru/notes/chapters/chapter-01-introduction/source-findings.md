# Source findings — Chapter 1

## [Source extraction issue] Superscript exponents in section 1.11

Affected provenance:

- PDF page 105 / chunk `p0105:c01`
- PDF page 106 / chunk `p0106:c01`
- review question 33 on PDF page 110 / chunk `p0110:c01`

Observed RAG text collapses typographic superscripts into inline digits in several places, for example forms resembling `1012`, `210`, `220`, `230` and `10–10`.

Impact:

- The visual typography of powers of ten/two cannot be reconstructed reliably from the extracted string alone.
- Chapter artifacts must not silently “correct” the authoritative RAG text from model memory.
- Where the prose explicitly states the numeric value (for example, 1 Kbyte = 1024 bytes; 1 Mbyte = 1,048,576 bytes; 1 Gbyte = 1,073,741,824 bytes), calculations may use those source-stated values.
- Any unsupported typography remains `[Needs confirmation]`.

## [Source contradiction] Review question 11 sector size vs requested transfer

Provenance: PDF page 108 / chunk `p0108:c01`.

The question defines a disk sector as 512 bytes and later asks for the time to read 400 Kbytes “from one sector”. Those two statements cannot both be literal.

Handling:

- preserve the question wording;
- do not silently change “one sector” to another storage unit;
- the review answer labels the contradiction and, separately, computes the timing for a 400 KiB transfer after positioning as a clearly stated conditional interpretation.

## [Source wording/code mismatch] Review question 23 `lseek` offset

Provenance: PDF page 109 / chunk `p0109:c01`.

The source shows:

`lseek(fd, 3, SEEK_SET)`

and then states in prose that the call moves the pointer to the “third byte” of the file.

The retrieved chapter does not explicitly reconcile the numeric offset with that wording. The review answer therefore preserves the source-stated third-byte result and flags the mismatch rather than silently applying an external API convention.

No other material contradiction was identified in the chunks used for this chapter analysis.
