# Source findings — глава 3

Policy: **rag_only**. No silent correction.

## SF-01 — falling-edge transition contradicts itself

**Classification:** [Source wording mismatch]

**Provenance:** `p0198:c01`, PDF page 198.

RAG says the trigger on figure 3.25г changes state on a **falling edge**, then gives the transition as `0 → 1`.

The same page describes a rising edge as `0 → 1`. Therefore the falling-edge phrase and transition notation are internally inconsistent.

**Handling:** artifacts retain only the distinction “latch = level-sensitive; flip-flop = edge-sensitive” and flag the exact transition wording.

## SF-02 — clock period range unit inconsistency

**Classification:** [Source numeric/unit mismatch]

**Provenance:** `p0192:c01`, PDF page 192.

RAG states clock frequency from `100 MHz` to `4 GHz` and says this corresponds to period from `10 to 250 ps`.

The frequency values and stated period/unit range are internally inconsistent.

**Handling:** no corrected numeric range is substituted into chapter artifacts.

## SF-03 — exercise 42 PCIe bandwidth conflicts with chapter body

**Classification:** [Source numeric mismatch]

**Provenance:** `p0268:c01` versus `p0252:c01`–`p0254:c01`.

Exercise 42 states total PCI Express channel bandwidth as `10 Mbit/s`. Earlier chapter text describes per-direction PCIe rates in gigabit/gigabyte-scale terms and later PCIe versions at hundreds of MB/s per lane / many GB/s aggregate.

**Impact:** a unique numeric answer to exercise 42 cannot be asserted from RAG without adjudicating which source number is erroneous.

**Handling:** review answer 42 is marked `[Needs confirmation]` and only source-supported structural facts are retained.

## Adjudication status

Direct source-page visual inspection and external documentation are outside the current chapter contract. Findings remain unresolved.
