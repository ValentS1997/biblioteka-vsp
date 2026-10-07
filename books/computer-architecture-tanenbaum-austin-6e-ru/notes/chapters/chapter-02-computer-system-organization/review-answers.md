# RAG-grounded ответы — глава 2

**Provenance:** questions `p0168:c01`–`p0171:c01`; answers use only chapter RAG `p0076:c01`–`p0171:c01`. Not an official publisher key.

## 1
Datapath cycle = 5 + 10 + 5 = **20 ns**. Maximum throughput without pipeline = 1/20 ns = **50 million instructions/s = 50 MIPS**.

## 2
PC must advance so the next fetch selects the next instruction. Without the step, the same instruction is fetched again and execution can repeat indefinitely unless some other mechanism changes PC.

## 3
No. Per-instruction latency alone is insufficient because the two machines may execute different numbers/types of instructions for the same program. Total program time depends on instruction count and per-instruction behavior, not only one nominal latency.

## 4
If memory is on-chip and as fast as CPU, the specific RISC motivations for restricting memory access to LOAD/STORE and keeping many registers become less critical because the memory-latency penalty is reduced. Easy decode, high issue rate, direct hardware execution and parallelism still matter for high performance.

## 5
Closest match: **SIMD / array processor**. One instruction/word is broadcast while many workers/processors apply it simultaneously to different data/books.

## 6
The source gives registers as a few nanoseconds and optical media as vastly slower; with media already inserted, exact optical seek latency is not numerically fixed in retrieved text. Ratio is therefore **order-of-magnitude only: many millions to hundreds of millions times slower**. Exact value: **[Needs confirmation]**.

## 7
Need smallest t such that `3^t ≥ 2^6`. `3^3=27<64`, `3^4=81≥64`; therefore **4 trits**.

General:
`t = ceil(log_3(2^n)) = ceil(n log_3 2)`.

## 8
Each pixel: 3 channels × log2(64)=6 bits = 18 bits/pixel.
10 frames/s from 100 ms resolution.
Rate = 10^6 × 18 × 10 = **180 Mbit/s**.

## 9
44,000 samples/s × 16 bits = **704,000 bit/s = 704 kbit/s**.

## 10
Four nucleotides require 2 bits.
Total = 3×10^9 ×2 = **6×10^9 bits**.
Average/gene = 6×10^9 / 30,000 = **200,000 bits/gene**.

## 11
1,073,741,824 = `2^30`. Binary-addressed memory naturally comes in powers of two; this is 1 GiB under the chapter convention.

## 12
Using even-parity Hamming(7,4), parity positions 1,2,4 and data positions 3,5,6,7:

| Digit | Code |
|---:|---|
| 0 | 0000000 |
| 1 | 1101001 |
| 2 | 0101010 |
| 3 | 1000011 |
| 4 | 1001100 |
| 5 | 0100101 |
| 6 | 1100110 |
| 7 | 0001111 |
| 8 | 1110000 |
| 9 | 0011001 |

## 13
One valid construction: 4-bit digit plus one parity bit chosen for even parity. Any single-bit difference in the 4-bit payload becomes distance at least 2.

| Digit | Code |
|---:|---|
|0|00000|
|1|00011|
|2|00101|
|3|00110|
|4|01001|
|5|01010|
|6|01100|
|7|01111|
|8|10001|
|9|10010|

## 14
For total length `2^n−1`, there are `n` parity positions.
Percentage = `100n/(2^n−1)`.

| n | % parity |
|---:|---:|
|3|42.86%|
|4|26.67%|
|5|16.13%|
|6|9.52%|
|7|5.51%|
|8|3.14%|
|9|1.76%|
|10|0.98%|

## 15
Using source convention: positions numbered from left, parity at 1,2,4,8, even parity; 8 data bits occupy 3,5,6,7,9,10,11,12.

“Earth” → **`C85 DD1 DF2 5F4 4D8`**.

## 16
Checking/correcting one-bit Hamming syndromes yields **“babies”**.

## 17
1024 sectors × 512 bytes × (7200/60) revolutions/s =
**62,914,560 B/s = 60 MiB/s** (≈62.9 MB/s decimal).

## 18
Bus capacity = 4 bytes / 5 ns = 800 MB/s.
Disk at 160 MB/s consumes one 5-ns bus cycle every 25 ns, i.e. **20% of bus time**.

Under the simple cycle-stealing model where that 5 ns delays each 25-ns CPU instruction window, instruction time becomes 30 ns: **20% more time per instruction**, throughput from 40 MIPS to ≈33.3 MIPS (**16.7% throughput reduction**). Exact scheduling can alter instantaneous stalls.

## 19
Yes. Source explains zone recording: outer tracks can contain more sectors than inner tracks at the same angular speed. Therefore allocation location can affect sequential capacity/throughput. Choosing outer-first favors early files; inner-first preserves faster outer zones for later allocations. Policy choice depends on intended workload.

## 20
Each cylinder: 4 tracks ×10 ms = 40 ms.
10,000 cylinders = 400,000 ms.
Adjacent-cylinder seeks: 9,999 ×1 ms = 9,999 ms.
Total = **409,999 ms ≈ 410 s ≈ 6.83 min**.

## 21
RAID 3 parity can reconstruct a failed bit when the failed disk position is known. RAID 2 uses a Hamming-style error-correcting layout that can identify/correct errors through redundant check bits rather than relying only on known failed-device location. Thus RAID 2 addresses a stronger error-location problem at the cost of more check disks.

## 22
80 min ×60 ×75 sectors/s = 360,000 sectors.

Type 2: 360,000 ×2336 = **840,960,000 bytes**.
Type 1 user data: 360,000 ×2048 = **737,280,000 bytes**.

## 23
At 1×: 75 sectors/s ×98 frames/sector ×588 channel bits/frame.
At 10×: **43,218,000 channel bits/s**.
Bit/pulse interval ≈ **23.14 ns**.

## 24
**[Needs confirmation]** because source wording for the additional 3.5 GB item is ambiguous; see source-findings.

Conditional calculation if the 3.5 GB is an additional non-video track:
raw video = 720×480×3 bytes×30×(133×60) ≈ 248.21 GB decimal.
Compression into 4.7 GB with +3.5 GB extra requires ≈ **53.6×** using decimal GB, or ≈ **49.9×** using binary-GiB arithmetic.

## 25
Following the chapter convention for storage capacity as powers of two:
25×2^30 bytes ×8 / 4.5×10^6 bit/s ≈ **13.26 h**.
If “25 GB” is interpreted decimal, result ≈ **12.35 h**. Source convention favors the first value.

## 26
Use **indexed color**: the one-byte pixel stores an 8-bit index (0–255) into a hardware palette of 256 entries, while each palette entry is a 24-bit RGB color. The hardware can choose 256 simultaneous colors from a larger 2^24 color space.

## 27
Each pixel: 5 channels × log2(32)=5 bits =25 bits.
10 ms resolution =100 frames/s.
10^8 ×25×100 =2.5×10^11 bit/s = **31.25 GB/s**.

## 28
Pixel periods/s =1920×1080×75 =155,520,000.
Duration = 1/that = **≈6.43 ns/pixel**.

## 29
4000 chars/page.
Each char area =4 mm²; 25% toner →1 mm².
Thickness 25 μm =0.025 mm.
Toner volume/page =4000×1×0.025 =100 mm³.

Cartridge =25×8×2 cm³ =400 cm³ =400,000 mm³.
Pages =400,000/100 = **4000 pages**.

## 30
64 frequencies encode log2(64)=6 bits per slot.
With n slots/s: **6n bit/s**.

## 31
QAM-64 source figure states 6 bit/Hz.
Total cable =12 MHz ×6 =72 Mbit/s.
Active homes = `n(1-f)`.
Per-active-user rate >2 Mbit/s when:

`72 / [n(1-f)] > 2`

so **`n(1-f) < 36`**.

## 32
Raw image =3000×2000×3 =18,000,000 bytes.
After 5× compression =3,600,000 bytes.
In 2 s → **1.8 MB/s**.

## 33
Source wording is malformed; see source-findings.

If intended value is **6 bytes/pixel**:
raw =24,000,000×6 =144,000,000 bytes;
compressed 5× =28,800,000 bytes/image;
8×2^30 /28,800,000 ≈298.26.
Therefore **298 complete images** under that interpretation.

## 34
Chapter p107 gives an explicit rough estimate of **1 MiB text per average book**. Using that as the source-grounded estimate:

- characters ≈1,048,576 if one byte/character;
- ASCII + parity =8 bits/character → **8,388,608 bits/book**;
- 10,000 books ≈10,000 MiB text.

Using chapter media capacities:
- 650-MiB CD: ceil(10,000/650) = **16 CDs**;
- 8.5-GiB single-sided dual-layer DVD: **2 DVDs**.

This ignores illustrations because the exercise asks character text.

## 35
Language-neutral pseudocode, even parity, parity positions 1,2,4,8:

```text
hamming(ascii[7]):
    code[1..11] = 0
    put data bits into 3,5,6,7,9,10,11
    for p in {1,2,4,8}:
        parity = XOR of code[i] for all i where (i AND p) != 0 and i != p
        code[p] = parity
    return code
```

## 36

```text
distance(code[0..n-1], n, k):
    best = k + 1
    for i = 0 .. n-2:
        for j = i+1 .. n-1:
            d = popcount((code[i] XOR code[j]) masked to k bits)
            if d < best:
                best = d
    return best
```

This implements the chapter definition of Hamming distance: number of bit positions in which two codewords differ.
