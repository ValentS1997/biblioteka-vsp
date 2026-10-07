# RAG-grounded review answers — Appendix B

## 1

IEEE single precision:

| Value | Hex |
|---|---|
| 9 | `41100000` |
| 5/32 = 0.15625 | `3E200000` |
| -5/32 | `BE200000` |
| 6.125 | `40C40000` |

## 2

| Hex | Decimal |
|---|---:|
| `42E28000` | **113.25** |
| `3F880000` | **1.0625** |
| `00800000` | **2^-126 ≈ 1.17549435×10^-38** |
| `C7F00000` | **-122880** |

## 3

The IBM/370-style format uses:

- sign: 1 bit;
- biased exponent: 7 bits, bias 64;
- base: 16;
- explicit 24-bit fraction with point to its left.

`7/64 = 0.1C₁₆ × 16^0`.

Biased exponent:

```text
0 + 64 = 64 = 1000000₂
```

Result:

```text
0 | 1000000 | 000111000000000000000000
= 401C0000H
```

## 4

Bias = 64, radix = 2.

1. `0 1000000 0001010100000001`

Three leading zeroes must be shifted away:

```text
exponent: 0 → -3
biased exponent: 61 = 0111101
mantissa: 1010100000001000
```

Normalized:

```text
0 0111101 1010100000001000
```

2. `0 0111111 0000001111111111`

Six leading zeroes:

```text
exponent: -1 → -7
biased exponent: 57 = 0111001
mantissa: 1111111111000000
```

Normalized:

```text
0 0111001 1111111111000000
```

3. `0 1000011 1000000000000000` is already normalized.

## 5

```text
3EE00000H = 0.4375
3D800000H = 0.0625
sum        = 0.5
```

Normalized IEEE single result:

```text
3F000000H
```

## 6

### Model 0.001

- exponent bits: 7, bias 64 → exponent range `-64...+63`;
- significand: 8 explicit binary fraction bits, normalized with leading 1.

Smallest positive normalized:

```text
0.10000000₂ × 2^-64 = 2^-65
```

Largest:

```text
0.11111111₂ × 2^63
= (255/256) × 2^63
≈ 9.19×10^18
```

Precision:

```text
8 log10(2) ≈ 2.41 decimal digits
```

### Model 0.002

- exponent bits: 5, bias 16 → `-16...+15`;
- significand: 10 bits.

Smallest:

```text
0.1000000000₂ × 2^-16 = 2^-17 ≈ 7.63×10^-6
```

Largest:

```text
0.1111111111₂ × 2^15
= (1023/1024) × 32768
= 32736
```

Precision:

```text
10 log10(2) ≈ 3.01 decimal digits
```

The purchase question has no unique factual answer: model 0.001 buys much greater range; model 0.002 buys somewhat greater precision.

## 7

**Catastrophic cancellation**: subtracting two nearly equal values of the same sign, or equivalently adding opposite-sign values with nearly equal magnitudes.

Leading significant bits cancel, leaving a result whose remaining bits contain much less relative precision.

## 8

For:

```text
N = m × 2^e
```

make `e` even if necessary, then:

```text
sqrt(N) = sqrt(m) × 2^(e/2)
```

A fast approximation can therefore:

1. adjust an odd exponent by rescaling the significand;
2. halve the exponent;
3. use a coarse approximation/lookup for `sqrt(m)`;
4. optionally refine with Newton-Raphson.

The exercise does not specify an error bound.

## 9

Single-precision addition procedure:

```text
unpack S,E,F
classify zero / denormal / infinity / NaN
restore implicit leading bit for normalized values
compare exponents
shift the smaller significand right by exponent difference
add significands if signs equal
subtract smaller magnitude if signs differ
determine result sign
normalize result
round discarded bits
handle exponent overflow/underflow
repack sign/exponent/fraction
```

Guard/sticky information should be retained during alignment so rounding does not depend only on already-truncated bits.

## 10

For radix-16 exponent and binary explicit significand:

```text
unpack sign, exponent, significand
compare exponents
for every exponent step:
    shift smaller significand right by 4 bits
add/subtract significands
if carry creates an extra hex digit:
    shift right 4
    exponent += 1
while top four significand bits are 0000:
    shift left 4
    exponent -= 1
round
check range
repack
```

Because the exponent radix is 16, normalization changes happen in **4-bit groups**, not one bit at a time.
