# Source findings — глава 15

## Finding 1 — xlabel()/ylabel() vs set_xlabel()/set_ylabel()

Classification: **[Source terminology/code mismatch]**

Provenance:
- chunk: `e0025:c02`
- EPUB spine item: `25`
- locator: `OEBPS/Text/978544614112-22.xhtml`

Shown code uses:

~~~python
ax.set_xlabel("Value", fontsize=14)
ax.set_ylabel("Square of Value", fontsize=14)
~~~

But prose says methods `xlabel()` and `ylabel()`.

Adjudication: exact intended naming `[Needs confirmation]`.

Policy action: code-oriented artifacts preserve shown calls and record prose mismatch separately.

## Finding 2 — point_numbers range description

Classification: **[Source prose/code mismatch]**

Provenance:
- chunk: `e0025:c07`

Shown code:

~~~python
point_numbers = range(rw.num_points)
~~~

With default `rw.num_points == 5000`, this expression corresponds to values 0 through 4999.

Prose says the list “contains numbers from 1 to 4999”.

The prose and expression do not describe the same sequence.

Adjudication: `[Needs confirmation]`.

## Finding 3 — figure() vs subplots() sizing explanation

Classification: **[Source prose/code mismatch]**

Provenance:
- chunks: `e0025:c08–c09`

Shown sizing examples:

~~~python
fig, ax = plt.subplots(figsize=(15, 9))
fig, ax = plt.subplots(figsize=(10, 6), dpi=128)
~~~

But prose then says “Функция figure() управляет шириной, высотой, разрешением и цветом фона диаграммы.”

No `figure()` call is shown in this sizing example.

Adjudication: intended API reference `[Needs confirmation]`.

## Finding 4 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0025:c02`–`e0025:c13`
- EPUB spine item: `25`
- locator: `OEBPS/Text/978544614112-22.xhtml`

Observed starts include continuation fragments such as `ares = ...`, `= [1, 2, 3...`, `этих списков...`, `ия по оси Y...`, `модуля random...`, `уем метод set_aspect...`, `основной серии...`, `не дает точного размера...`, `рамм: зайдите...`, `се шесть частот...`, and partial continuation into later dice text.

Cross-check:
- adjacent chunks preserve transition context;
- exercises 15.1–15.10 recoverable;
- chapter-end summary intact;
- `e0026:c01` confirms chapter 16;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## Additional compatibility boundary

Source uses:

~~~python
plt.style.use('seaborn')
~~~

This is a source example, not verified current environment state.

Current availability/behavior of this style: `[Needs confirmation]`.

This is not classified as a source defect without external/current verification.
