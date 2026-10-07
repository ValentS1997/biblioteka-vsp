# RAG-grounded review answers — Appendix A

## 1

```text
1984₁₀ = 11111000000₂
4000₁₀ = 111110100000₂
8192₁₀ = 10000000000000₂
```

## 2

```text
1001101001₂ = 617₁₀ = 1151₈ = 269₁₆
```

## 3

Valid hexadecimal strings contain only `0–9,A–F`.

Valid: **BED, CAB, DEAD, DECADE, ACCEDED, DAD**.

Invalid: **BAG** because `G` is not a hexadecimal digit.

## 4

```text
base 2: 1100100
base 3: 10201
base 4: 1210
base 5: 400
base 6: 244
base 7: 202
base 8: 144
base 9: 121
```

## 5

With leading zeroes allowed, `k` radix-`r` digits encode `r^k` patterns representing `0 ... r^k-1`.

Positive nonzero integers:

```text
r^k - 1
```

## 6

10 binary fingers:

```text
0 ... 2^10-1 = 1023
```

20 binary fingers/toes:

```text
0 ... 2^20-1 = 1,048,575
```

A 20-bit two's-complement number has `2^20 = 1,048,576` distinct values:

```text
-524,288 ... 524,287
```

## 7

8-bit two's complement:

1. `00101101 + 01101111` → raw `10011100`; positive + positive produced a negative sign, so **overflow**.
2. `11111111 + 11111111` → `11111110` = -2; no overflow.
3. `00000000 - 11111111` → `00000001` = +1.
4. `11110111 - 11110111` → `00000000`.

## 8

Ones' complement uses end-around carry.

1. `00101101 + 01101111 = 10011100` → overflow.
2. `11111111 + 11111111` → raw carry + `11111110` → end-around carry gives `11111111` (-0).
3. `00000000 - 11111111` → `00000000` (+0).
4. `11110111 - 11110111` → `11111111` (-0).

## 9

Interpretation: fixed-width 3-bit two's-complement arithmetic.

| Sum | result | sign=1? | zero? | overflow? |
|---|---|---:|---:|---:|
| `000+001` | `001` | no | no | no |
| `000+111` | `111` | yes | no | no |
| `111+110` | `101` | yes | no | no |
| `100+111` | `011` | no | no | **yes** |
| `100+100` | `000` | no | **yes** | **yes** |

The wording ambiguity is recorded in `source-findings.md`.

## 10

For three decimal digits, nine's complement of `x` is `999-x`.

```text
  6 → 006
 -2 → 997
100 → 100
-14 → 985
 -1 → 998
  0 → 000
```

Nine's complement also has a negative-zero encoding `999`; this answer uses +0.

## 11

Rule: add fixed-width values normally. If a carry leaves the most-significant digit, add it back to the least-significant digit.

```text
0001 + 9999 → 0001
0001 + 9998 → 9999   (-0)
9997 + 9996 → 9994   (-5)
9241 + 0802 → 0044   (+44)
```

## 12

Ten's complement is analogous to two's complement:

1. add fixed-width operands normally;
2. discard carry beyond the most-significant digit;
3. do not perform end-around carry.

## 13

| × | 0 | 1 | 2 |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 2 |
| 2 | 0 | 2 | 11 |

`2×2=4₁₀=11₃`.

## 14

```text
0111₂ × 0011₂
= 7 × 3
= 21
= 10101₂
```

As an 8-bit product: `00010101`.

## 15

The source does not specify the output width for two's complement, so use width `W`.

```text
parse optional sign
N = 0
for every decimal digit d:
    N = 10*N + d
apply sign

octal:
    repeatedly divide |N| by 8, collect remainders

hex:
    repeatedly divide |N| by 16, collect remainders

two's complement, width W:
    if N >= 0:
        encode N in W bits
    else:
        encode (2^W + N) in W bits
```

Acceptance condition:

```text
-2^(W-1) <= N <= 2^(W-1)-1
```

Without `W`, the final bit string is not unique.

## 16

Two's-complement addition is ordinary modulo-`2^32` binary addition.

```text
carry = 0
for i = 31 down to 0:
    a = input1[i] - '0'
    b = input2[i] - '0'
    s = a + b + carry
    output[i] = '0' + (s & 1)
    carry = (s >> 1) & 1

discard final carry
```

Optional signed-overflow check:

```text
same input sign && output sign differs
```
