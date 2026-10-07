# Commands / procedures — Appendix A

No host-system commands are present in the source.

## Source-supported numeric procedures

### Decimal integer → binary

Method 1:
1. Find largest power of 2 not exceeding the value.
2. Subtract it.
3. Repeat for the remainder.
4. Set corresponding bits.

Method 2:
1. Repeatedly divide by 2.
2. Record remainder 0/1.
3. Read remainders bottom-to-top.

### Binary → decimal

Sum powers of two for every set bit, or scan left-to-right:

```text
acc = 2*acc + next_bit
```

### Negate n-bit two's-complement integer

```text
invert all n bits
add 1
discard carry beyond n bits
```

### Add ones'-complement integers

```text
sum = ordinary fixed-width binary sum
if carry_out:
    sum = sum + 1
```

## State-changing action

[Not applicable]

These are arithmetic algorithms, not commands that modify a live system.
