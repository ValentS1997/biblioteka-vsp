# Source findings — глава 4

Policy: **rag_only**. Findings preserve source/extraction inconsistencies without silent correction.

## SF-01 — IFU figure caption names Mic-1 while text uses it to build Mic-2

**Classification:** [Source wording mismatch]

**Provenance:** `p0319:c01` and `p0323:c01`.

Page 319 introduces the independent instruction-fetch unit as an enhancement to relieve Mic-1's ALU/fetch overhead, but the figure caption reads approximately «Instruction Fetch Unit in microarchitecture Mic-1».

Page 323 then explicitly states that **Mic-2** is Mic-1 enhanced with the IFU shown in figure 4.18.

**Handling:** artifacts describe the IFU as the defining enhancement used to form Mic-2 and retain the caption mismatch as a source finding.

## SF-02 — ISHL exercise loses the count of ignored bits

**Classification:** [Source extraction/wording issue]

**Provenance:** `p0374:c01`, exercise 15.

The ISHL exercise says the shift count is taken from the five low bits of the top 32-bit stack word, but then says «the remaining 2 bits» are ignored.

The immediately preceding ISHR exercise correctly describes five low bits and the **remaining 27 bits**.

**Handling:** artifacts do not silently rewrite the exercise statement. The review answer treats the intended 5-bit shift count as source-supported but flags the missing digit.

## Adjudication status

Direct page-image inspection and external documentation are outside the current chapter contract. Findings remain unresolved.
