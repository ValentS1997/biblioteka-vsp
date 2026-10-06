# Source findings — глава 11 «Элементы функционального программирования»

## Finding 1 — closure “freezes context at definition” is broader than demonstrated

Classification: **[Source wording scope / Needs confirmation]**

Provenance:

- pages 233–234;
- chunks `p0233:c01`, `p0234:c01`.

Observed:

Источник формулирует closure как функцию, которая «замораживает» окружающий контекст именно на момент определения, а не вызова.

Examples shown:

- Python `multiplier(n)`;
- Go `makeAdder(x)`;
- Python default-argument example.

Impact:

Эти examples не проверяют все варианты изменения captured variables после создания closure и не доказывают универсальную семантику словом «замораживает».

Action:

- canonical artifacts описывают observable behavior examples;
- exact capture semantics не исправляются внешней спецификацией;
- adjudication: **[Needs confirmation]**.

## Finding 2 — “Go functions are always full closures” is over-broad

Classification: **[Source technical claim / Needs confirmation]**

Provenance:

- page 238, chunk `p0238:c01`.

Observed:

Источник утверждает:

```text
В Go функции всегда являются полными замыканиями
```

и проводит аналогию с C++11 capture `[&]`.

Impact:

Глава показывает anonymous functions that reference surrounding state, но не доказывает утверждение обо всех функциях Go или полную эквивалентность C++ capture model.

Action:

- chapter notes retain only demonstrated closure behavior;
- universal equivalence claim not promoted.

## Finding 3 — lifetime explanation via reference counting + GC is implementation-level

Classification: **[Source implementation claim / Needs confirmation]**

Provenance:

- page 238.

Observed:

Источник объясняет возможность использования captured local variables после выхода из defining scope «подсчётом ссылок» и работой garbage collector.

Impact:

Chapter examples demonstrate lifetime behavior, but do not inspect runtime implementation or prove reference-counting as the mechanism.

Action:

- behavior preserved;
- implementation mechanism left **[Needs confirmation]**.

## Finding 4 — Memoize is described as recursive, but recursion path is indirect in shown code

Classification: **[Source wording ambiguity]**

Provenance:

- page 241, chunk `p0241:c01`.

Observed:

После `Memoize()` источник пишет: «Это также рекурсивная функция».

Shown code:

- `Memoize` creates a cache and returns a closure;
- the returned closure invokes `mf(key)`;
- `mf` in the Fibonacci construction refers through `fibMem` to the memoized recursive chain.

Impact:

Неясно, относится ли слово «рекурсивная» непосредственно к `Memoize`, к returned closure или к composed Fibonacci calculation.

Action:

- canonical notes describe the call/data flow instead of assigning ambiguous label.

## Finding 5 — Fibonacci timing values are environment-specific

Classification: **[Source experiment limitation]**

Provenance:

- pages 241–242.

Observed:

Source reports specific microsecond/millisecond/second timings for `fibos` and `fibom`.

Impact:

Absolute timing depends on host, Go/runtime version and load. The valid source-level conclusion is qualitative: caching removes repeated subproblem computation and radically changes growth behavior in this example.

Action:

- preserve result values and qualitative speedup;
- do not treat absolute timings as portable benchmark.

## Finding 6 — “pure function” discussion mixes purity and immutability terminology

Classification: **[Source conceptual wording / Needs confirmation]**

Provenance:

- pages 242–243.

Observed:

Источник moves from pure functions to “немутабельность” and uses a value-returning `Point.Add` method as the concrete example.

Impact:

The chapter demonstrates non-mutating value transformation, but does not formally establish equivalence between purity and immutability as concepts.

Action:

- canonical artifact uses phrase `pure-function style / non-mutating value transformation`;
- formal terminology is not externally normalized.
