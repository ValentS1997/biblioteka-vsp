# Cheatsheet — Appendix A

## Positional notation

```text
(d_n...d_1d_0)_r = Σ d_i r^i
```

For `k` digits in radix `r`:

- bit patterns / nonnegative values: `r^k`;
- positive nonzero integers: `r^k - 1`.

## Binary ↔ octal / hex

- 1 octal digit = 3 bits.
- 1 hex digit = 4 bits.

Example:

```text
1001101001₂
= 001 001 101 001₂
= 1151₈
= 0010 0110 1001₂
= 269₁₆
```

## Signed representations

### Sign magnitude
MSB is sign; remaining bits are magnitude. Has +0 and -0.

### Ones' complement
Negate by flipping all bits. Has +0 and -0.

Addition: add normally; if a carry leaves the MSB, add it back to the LSB.

### Two's complement
Negate:

```text
~x + 1
```

For `n` bits:

```text
range = -2^(n-1) ... 2^(n-1)-1
```

Carry out of MSB is discarded.

### Biased
Store:

```text
encoded = value + bias
```

## Overflow

For two's complement addition:

```text
same-sign operands + opposite-sign result → overflow
```

Equivalent hardware rule:

```text
carry_into_sign != carry_out_of_sign
```

## Hex mental map

```text
0=0000  4=0100  8=1000  C=1100
1=0001  5=0101  9=1001  D=1101
2=0010  6=0110  A=1010  E=1110
3=0011  7=0111  B=1011  F=1111
```
