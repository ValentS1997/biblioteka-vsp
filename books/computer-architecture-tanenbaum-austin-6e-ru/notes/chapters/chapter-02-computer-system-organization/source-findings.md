# Source findings — глава 2

Policy: **rag_only**. Findings preserve source/extraction defects without silent correction.

## SF-01 — malformed Java interpreter declaration

**Classification:** [Source extraction issue]

**Provenance:** `p0079:c01`, PDF page 79.

Extracted listing contains:

```text
public static void interpret(int memory[], int starting_address{
```

The closing parenthesis is absent in RAG text.

**Impact:** listing is used only as conceptual evidence for fetch/decode/execute, not copied as runnable Java.

## SF-02 — exercise 24 ambiguous 3.5-GB phrase

**Classification:** [Source wording/code mismatch]

**Provenance:** `p0170:c01`, PDF page 170.

The exercise assigns `3.5 Гбайт` to «дорожки изображения» while separately specifying image resolution/color depth/frame rate. The role of the extra 3.5 GB is ambiguous in extracted text.

**Impact:** answer 24 is conditional, not a single asserted result.

## SF-03 — exercise 33 malformed color-storage wording

**Classification:** [Source extraction issue]

**Provenance:** `p0171:c01`, PDF page 171.

Extracted wording states that color uses six bytes «в каждом из битов», while the same sentence describes a 24-million-pixel sensor.

**Impact:** review answer gives a conditional result for `6 bytes/pixel`, explicitly not promoted to source truth.

## Adjudication status

Direct PDF-image inspection and external sources are outside the current chapter contract. Findings remain unresolved.
