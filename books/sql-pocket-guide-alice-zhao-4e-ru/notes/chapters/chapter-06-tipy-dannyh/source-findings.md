# Source findings — глава 6. Типы данных

**Scope:** PDF 155–189, RAG `p0155:c01`–`p0189:c01`.  
**Policy:** source/text-layer defects are recorded, never silently corrected in `rag_only`.

## F-01 · [Source extraction issue] · ASCII/Unicode powers lost

On `p0171:c01`, extracted text contains:
- `ASCII 28 = 128`
- `В Unicode 221 символ`
- `первые 28 символов`

These strings are not unambiguous mathematical notation and likely lost superscript/formatting information in extraction. The same passage also renders a bit-pattern for `!`.

**Policy:** do not infer missing exponent formatting from model knowledge. Numeric capacity claims from this subsection are **[Needs confirmation]**.

## F-02 · [Source code mismatch] · MySQL datetime INSERT value order

On `p0177:c01` table definition is:
```sql
(dt, tm, dttm, ts, yr)
```
but INSERT explicitly targets:
```sql
INSERT INTO my_table (dt, tm, dttm, yr)
VALUES ('21-7-4', '6:30',
        2021, '2021-12-25 7:00:01');
```

The displayed result then shows:
- `dttm = 2021-12-25 07:00:01`
- `yr = 2021`

That output corresponds to the opposite order of the last two INSERT values.

**Finding:** code and displayed result are internally inconsistent. Do not reorder values silently. Runnable MySQL demo is **[Needs confirmation]**.

## F-03 · [Source wording/code mismatch] · date format text

On `p0173:c01` prose says the date format is `YYYYMM-DD`, while immediately below the sample date is:
`'2022-10-15'`
and table 6.11 uses `'2021-02-25'`.

**Finding:** prose format string and examples differ. Exact intended prose token is [Needs confirmation]; artifacts use source examples but preserve this mismatch here.

## F-04 · [Source code mismatch] · SQLite TEXT/REAL/INTEGER datetime demo

On `p0182:c01`–`p0183:c01`, source defines:
```sql
dt_text TEXT,
dt_real REAL,
dt_integer INTEGER
```
then inserts the **same quoted datetime string** into all three columns and displays textual datetime values.

Immediately afterward table 6.18 says:
- TEXT stores a formatted string;
- REAL stores Julian-day count;
- INTEGER stores Unix seconds.

**Finding:** the preceding INSERT/output does not demonstrate the numeric representations described by the table. Whether SQLite coercion or the example is intended differently is **[Needs confirmation]**. No correction is made.

## F-05 · [Source extraction issue] · split type-name tokens

The extracted tables contain forms:
- `TINY TEXT`, `MEDIUM TEXT`, `LARGE TEXT` on `p0169:c01`–`p0170:c01`;
- `TINY BLOB`, `MEDIUM BLOB`, `LARGE BLOB` on `p0188:c01`.

These may be layout/tokenization artifacts or literal typography of the edition. The current RAG does not establish whether whitespace belongs to the executable type name.

**Policy:** do not normalize to a different token in a runnable command without external/source visual verification.

## F-06 · [Needs confirmation] · BOOLEAN output scope

On `p0184:c01`, prose first says MySQL, PostgreSQL and SQLite support Boolean types, then a single demonstration shows values `TRUE/FALSE/1` rendering as `1/0/1`.

The text does not identify which RDBMS produced that specific output.

**Finding:** do not generalize the displayed representation to all three systems. Target output/type behavior [Needs confirmation].

## F-07 · [Needs confirmation] · “ASCII character = byte” wording

On `p0165:c01`, source says “Каждый символ представлен байтом” and gives `7 = 00000111` as a byte-form example. Later `p0171:c01` separately discusses ASCII/Unicode encoding.

**Finding:** exact intended distinction between numeric value, encoded character and byte representation is not sufficiently precise in the chapter text-layer. Do not use this sentence as a general encoding rule.

## F-08 · [Needs confirmation] · version-sensitive type ranges and product behavior

Tables 6.4–6.19 contain many product-specific limits/ranges/defaults. Chapter also states behavior such as:
- Oracle `FLOAT` being equivalent to NUMERIC in this discussion (`p0165:c01`);
- Unicode support mappings (`p0172:c01`);
- timezone/date ranges (`p0177:c01`–`p0183:c01`);
- boolean/binary type support (`p0184:c01`–`p0189:c01`).

These are **source assertions**, not current-version verification. Any production schema design must verify exact RDBMS/version separately.

## F-09 · [Needs confirmation] · external-file size heuristic

On `p0185:c01`, source recommends file-path storage when files exceed 1 MB and binary-in-DB for small files, linking this to load/performance and backup convenience.

This is a source heuristic, not a benchmark or universal threshold. Storage architecture depends on environment and remains [Needs confirmation].

## Control

- Canonical source/RAG unchanged.
- No external correction was imported.
- `commands.md` avoids treating ambiguous fragments as verified runnable syntax.
