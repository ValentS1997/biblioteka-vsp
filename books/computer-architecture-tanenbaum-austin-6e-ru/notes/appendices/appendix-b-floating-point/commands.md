# Procedures — Appendix B

No host-system commands are present.

## Normalize a binary floating value

```text
while leading significand bit is 0:
    significand <<= 1
    exponent -= 1
```

## Floating-point addition

```text
unpack sign/exponent/significand
classify zero/denormal/infinity/NaN
align exponents
add or subtract significands
normalize
round
handle overflow/underflow
pack fields
```

## Approximate square root

For `N = m × 2^e`:

1. if `e` is odd, rescale `m` so exponent becomes even;
2. compute/approximate `sqrt(m)`;
3. halve the exponent.

```text
sqrt(N) = sqrt(m) × 2^(e/2)
```

The exponent operation provides a fast coarse approximation; significand refinement can follow.

## State-changing action

[Not applicable]
