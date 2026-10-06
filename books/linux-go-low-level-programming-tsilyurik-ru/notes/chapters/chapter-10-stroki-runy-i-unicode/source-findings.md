# Source findings — глава 10 «Строки, руны и UNICODE»

## Finding 1 — UTF-8 width claim is source-scoped

Classification: **[Source technical claim / Needs confirmation]**

Provenance:

- page 223, chunk `p0223:c01`.

Observed:

Источник описывает UTF-8 символы как имеющие длину:

```text
1, 2, 3, 4 … потенциально до 6 байт
```

Impact:

Глава не приводит отдельной спецификации/проверки верхней границы и не связывает её с конкретной версией Unicode/UTF-8.

Action:

- формулировка не используется как canonical technical fact;
- в артефактах сохраняются только наблюдаемые byte/rune результаты examples;
- external adjudication: **[Needs confirmation]**.

## Finding 2 — palindrome regexp can produce a false-positive for unsupported scripts

Classification: **[Source experiment flaw]**

Provenance:

- page 228, chunk `p0228:c01`;
- output continuation on page 229.

Source pattern:

```go
var nonAlphaNum = regexp.MustCompile(`[^a-zа-я0-9 ]+`)
```

Before regexp filtering source also removes spaces and lowercases input.

Observed test output includes Greek phrase:

```text
true : Νίψον ανομήματα μη μόναν όψιν
```

But the shown allow-list pattern contains only Latin `a-z`, Cyrillic `а-я`, digits and space.

Impact:

For input made of a script outside that allow-list, meaningful characters can be removed before palindrome comparison. An empty or reduced rune slice can therefore yield `true` without validating the original phrase.

Action:

- source output is preserved as experiment evidence, not accepted as proof of Unicode-complete palindrome normalization;
- verification must inspect normalized intermediate text;
- no external regex correction injected.

## Finding 3 — mixed-script regexp range looks internally suspicious

Classification: **[Source pattern anomaly]**

Provenance:

- page 231, chunk `p0231:c01`.

Observed source pattern:

```text
([Ё-Яa-ё]|[a-zA-Z])+
```

The first range visibly mixes Cyrillic `Ё-Я`, Latin `a`, and Cyrillic `ё`.

Impact:

The intended Russian alphabet range cannot be established safely from this text alone.

Action:

- pattern retained exactly as source evidence;
- intended character/range: **[Needs confirmation]**.

## Finding 4 — \pL+ description is broader than chapter evidence

Classification: **[Source wording scope]**

Provenance:

- pages 231–232.

Observed:

Источник объясняет `\pL+` как соответствие «любому символу UNICODE».

The shown examples demonstrate matching letters/word-like content in several scripts, but do not test punctuation, symbols, combining marks, numbers or arbitrary Unicode categories.

Impact:

The universal wording is not established by chapter evidence.

Action:

- canonical artifacts describe `\pL+` only as the source's multilingual-letter pattern example;
- exact RE2 category semantics: **[Needs confirmation]**.

## Finding 5 — regexp capability claim is very broad

Classification: **[Source technical claim / Needs confirmation]**

Provenance:

- page 229.

Observed:

Источник states that Go `regexp` covers the capabilities of Perl, egrep and Python regular expressions, then later identifies RE2 syntax and notes differences.

Impact:

The chapter itself signals dialect differences and does not demonstrate feature equivalence across those engines.

Action:

- no claim of full feature parity is promoted to canonical notes;
- source is summarized only as using Go's `regexp`/RE2-oriented syntax.

## Finding 6 — string relocation wording is implementation-level

Classification: **[Source implementation claim / Needs confirmation]**

Provenance:

- page 224.

Observed:

Источник explains string immutability by saying transformation takes a string from one memory location and places a modified copy in a completely different memory location.

Impact:

The examples show non-in-place string transformation at language level, but do not observe or prove exact memory placement/allocation behavior.

Action:

- canonical notes retain the observable rule: individual string elements are not mutated in-place in the shown examples and transformations return strings;
- exact allocation/address behavior: **[Needs confirmation]**.
