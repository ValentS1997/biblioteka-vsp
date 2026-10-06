# Source findings — глава 12 «Скоростные и другие сравнения языков»

## Finding 1 — invalid-looking Go type declaration in bubble-sort listing

Classification: **[Source code/build mismatch]**

Provenance:

- page 250, chunk `p0250:c01`.

Observed source line:

```go
type data_t int 64
```

The same subsection then shows successful execution of binaries built from the Go implementation.

Impact:

The printed listing and the demonstrated successful build/run cannot both be taken as a literal single source state without clarification.

Action:

- listing is preserved as source evidence;
- canonical intended declaration: **[Needs confirmation]**;
- no silent correction injected.

## Finding 2 — missing semicolon in C sieve listing

Classification: **[Source code/build mismatch]**

Provenance:

- page 255, chunk `p0255:c01`.

Observed:

```c
printf("простых чисел %lu\n", j)
if(debug) {
```

The terminating semicolon after `printf(...)` is absent in the printed listing.

Later source shows successful compilation and execution of `erastof_c`.

Impact:

The printed listing does not exactly match the successfully built source used for the timing run.

Action:

- no code correction in chapter artifacts;
- intended source state: **[Needs confirmation]**.

## Finding 3 — complexity notation is internally unclear

Classification: **[Source terminology anomaly]**

Provenance:

- page 244, chunk `p0244:c01`.

Observed:

The source asks for tasks with very high growth, giving an example described as “экспоненциальную” followed by notation `O(n)`.

Later it explicitly labels bubble sort as `O(n^2)`.

Impact:

The intended complexity notation for the “exponential” example is unclear from the chapter text alone.

Action:

- artifact does not normalize the notation externally;
- benchmark rationale is preserved qualitatively: choose a workload whose cost grows enough to produce measurable runtimes.

## Finding 4 — bubble-sort comparison is explicitly non-equivalent

Classification: **[Source experiment limitation]**

Provenance:

- pages 248–251.

Observed:

The source itself states that the C++ result is not a fair direct comparison because the C++ version uses STL `vector<long long>` and iterators, while other variants use direct array/slice-style indexing.

Impact:

The timing difference cannot be attributed purely to language/compiler.

Action:

- keep the result as an example of implementation-structure cost;
- do not use it as a clean C++ vs Go ranking.

## Finding 5 — optimization policy changes across subsections

Classification: **[Source experiment limitation]**

Provenance:

- Fibonacci and bubble-sort sections use `-O0`;
- Hanoi and sieve sections show `-O3`.

Impact:

Timings from different algorithms cannot be combined into a single cross-language leaderboard without carrying the optimization context.

Action:

- compare only within one subsection/configuration;
- record compiler flags with every interpretation.

## Finding 6 — timing conclusions are environment-specific

Classification: **[Source experiment limitation]**

Provenance:

- pages 245–257.

Observed:

The source reports single representative timings after saying that several runs were actually performed, first run was excluded, and a stable/average-looking value was selected.

Impact:

Absolute values depend on hardware, OS load, cache state, compiler/runtime versions and build flags.

Action:

- preserve timings as source observations only;
- chapter artifacts retain the methodological rule: repeat, verify result, record environment, interpret broad differences.

## Finding 7 — priority-adjusted benchmark changes scheduler state for the process

Classification: **[Operational risk note]**

Provenance:

- page 245.

Observed template:

```bash
time nice -9 <command> <size>
```

Source says negative nice is used under root to raise the task priority and reduce dispersion.

Impact:

This is not a neutral read-only measurement; it changes scheduling priority for the launched process and may affect other workloads on the host.

Action:

- classify as priority-affecting;
- avoid on production/shared systems without an explicit reason and impact check.
