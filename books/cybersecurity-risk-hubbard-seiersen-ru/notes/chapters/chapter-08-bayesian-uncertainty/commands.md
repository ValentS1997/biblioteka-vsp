# Глава 8 — вероятностные формулы и operational boundary

**Provenance:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 34–35; RAG `e0034:c01–c03`, `e0035:c01–c05`.

## CLI / production commands

**[Not applicable].** Глава не содержит команд запуска penetration testing, shell/API, эксплуатационных действий или конфигураций инфраструктуры.

## Source-confirmed probability formulas

### Complement

```text
P(A) + P(~A) = 1
```

### Joint probability for independent events

```text
P(A,B) = P(A)P(B)
```

Только при независимости.

### Conditional probability

```text
P(A | B) = P(A,B) / P(B)
```

### Chain rule

```text
P(A,B) = P(A | B)P(B)

P(A,B,C) = P(A | B,C)P(B | C)P(C)
```

### Law of total probability

```text
P(A) = P(A | B)P(B) + P(A | ~B)P(~B)
```

### Bayes

```text
P(A | B) = P(A)P(B | A) / P(B)
```

Expanded binary form from source:

```text
P(A | B) =
P(A)P(B | A) /
[P(B | A)P(A) + P(B | ~A)P(~A)]
```

Источник: `e0035:c01–c02`.

## Числовой пример главы

### 1. Probability of remote exploitability

```text
P(УЭУ) =
P(ПТП)P(УЭУ | ПТП) + P(~ПТП)P(УЭУ | ~ПТП)
= (0,01)(0,95) + (1–0,01)(0,0005)
≈ 1,0 %
```

### 2. Prior probability of major breach

```text
P(КУД) =
P(УЭУ)P(КУД | УЭУ) + P(~УЭУ)P(КУД | ~УЭУ)
= (0,01)(0,25) + (1–0,01)(0,01)
= 1,24 %
```

### 3. P(УЭУ | КУД)

Источник печатает/извлекает:

```text
P(УЭУ | КУД) = P(КУД | УЭУ)P(УЭУ)/P(КУД)
= (0,25 (0,01)/(0,0124) = 20,16 %.
```

В числовой строке нарушена скобочная запись. **Не исправлять молча**; см. `source-findings.md`.

### 4. P(УЭУ | ~КУД)

```text
P(УЭУ | ~КУД) =
P(~КУД | УЭУ)P(УЭУ)/P(~КУД)

= (1–0,25)(0,01) / (1–0,0124)
= 0,76 %
```

### 5. Positive penetration test

```text
P(КУД | ПТП) =
P(УЭУ | ПТП)P(КУД | УЭУ)
+ (1 – P(УЭУ | ПТП))P(КУД | ~УЭУ)

= (0,95)(0,25) + (0,05)(0,01)
= 23,8 %
```

### 6. Negative penetration test

```text
P(КУД | ~ПТП) =
P(УЭУ | ~ПТП)P(КУД | УЭУ)
+ (1 – P(УЭУ | ~ПТП))P(КУД | ~УЭУ)

= (0,0005)(0,25) + (1–0,0005)(0,01)
= 1,01 %
```

Источник: `e0035:c04`.

## Safety

В книге penetration test выступает как **evidence variable**, а не как команда к немедленному тестированию production. Scope, authorization, rate limits, target systems, credentials, logging and rollback: **[Needs confirmation]**.

External spreadsheet, упомянутая авторами, не загружалась в режиме `rag_only`.
