# Cheatsheet — Appendix B

## Generic model

```text
N = sign × significand × radix^exponent
```

- exponent bits → range;
- significand bits → precision.

## Normalize

For binary:

```text
1.xxxxx × 2^e
```

For a format whose binary point is left of the explicit mantissa:

```text
0.1xxxx × 2^e
```

Normalization shifts the significand and compensates in the exponent.

## IEEE single precision

```text
31            23            0
+---+-----------+-------------+
| S | exponent  | fraction    |
+---+-----------+-------------+
 1      8            23
bias = 127
```

Normalized value:

```text
(-1)^S × 1.fraction × 2^(E-127)
```

## IEEE double precision

- sign: 1 bit;
- exponent: 11 bits;
- fraction: 52 bits;
- bias: 1023.

## Special classes

- exponent zero + zero fraction → signed zero;
- exponent zero + nonzero fraction → denormal/subnormal;
- exponent all ones + zero fraction → infinity;
- exponent all ones + nonzero fraction → NaN.

## Add two floating-point numbers

```text
unpack
→ compare exponents
→ shift smaller significand
→ add/subtract significands
→ normalize
→ round
→ check overflow/underflow
→ repack
```

## Precision hazard

```text
x ≈ y
x - y
→ leading significant bits cancel
→ large relative precision loss
```
