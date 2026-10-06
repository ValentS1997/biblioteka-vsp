# Source findings — глава 16

## Finding 1 — population GeoJSON vs earthquake project

Classification: **[Source scope/prose mismatch]**

Provenance:
- chunk: `e0026:c01`
- EPUB spine item: `26`
- locator: `OEBPS/Text/978544614112-23.xhtml`

Вступление говорит, что модуль `json` будет использоваться для обращения к «данным численности населения, хранимым в формате GeoJSON».

Фактический GeoJSON section главы работает с earthquake datasets, извлекая magnitude, longitude, latitude и title.

Population dataset/process далее в chapter scope не показан.

Adjudication: intended intro wording `[Needs confirmation]`.

## Finding 2 — color='red' vs c='red'

Classification: **[Source prose/code mismatch]**

Provenance:
- chunk: `e0026:c03`

Shown code:

~~~python
ax.plot(highs, color='red')
~~~

Surrounding prose говорит: «аргумент `c='red'`».

Argument names differ.

Adjudication: `[Needs confirmation]`.

## Finding 3 — simple Sitka dataset description vs header

Classification: **[Source dataset-description mismatch]**

Provenance:
- chunks: `e0026:c01–c02`

Shown header:

~~~text
STATION, NAME, DATE, TAVG, TMAX, TMIN
~~~

No `PRCP` column is shown.

Но prose говорит, что simple dataset содержит информацию «только об уровне осадков и температуре».

Within shown header, precipitation field is absent.

Adjudication: exact dataset description `[Needs confirmation]`.

## Finding 4 — earthquake input filename variants

Classification: **[Source filename mismatch]**

Provenance:
- chunks: `e0026:c07–c08`

Source uses several variants for the one-day earthquake file:

~~~text
q_1_day_m1.geojson
eq_1_day_m1.json
eq_data/eq_data_1_day_m1.geojson
~~~

These names/extensions are not mutually identical.

Adjudication: canonical intended filename `[Needs confirmation]`.

Policy action: artifacts describe the data flow without silently choosing one historical filename as authoritative.

## Finding 5 — readable GeoJSON filename mismatch

Classification: **[Source filename mismatch]**

Provenance:
- chunk: `e0026:c08`

Shown code writes:

~~~python
Path('eq_data/readable_eq_data.geojson')
~~~

Prose then instructs the reader to open:

~~~text
readable_eq_data.json
~~~

Extensions differ.

Adjudication: `[Needs confirmation]`.

## Finding 6 — features assignment prose vs code

Classification: **[Source variable-name mismatch]**

Provenance:
- chunk: `e0026:c09`

Shown code:

~~~python
all_eq_dicts = all_eq_data['features']
~~~

Prose says the data associated with `features` are saved «в `all_eq_data`».

The target variable differs from shown code.

Adjudication: `[Needs confirmation]`.

## Finding 7 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0026:c02`–`e0026:c13`
- EPUB spine item: `26`
- locator: `OEBPS/Text/978544614112-23.xhtml`

Observed starts include continuation fragments such as `иная с начала документа...`, `itka_highs.py...`, `dates, highs = ...`, `область между...`, `ние, мы напрямую...`, `е кнопку Station List...`, `дой M1 и выше...`, `етрясению...`, `print(mags[:10])...`, `ате и преобразование...`, `ckbody...`, and a clipped start in `e0026:c13`.

Cross-check:
- adjacent chunks preserve transition context;
- exercises 16.1–16.9 recoverable;
- chapter-end summary intact;
- `e0027:c01` confirms chapter 17;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## External-data boundary

Source examples contain specific historical dates, counts and URLs.

Without external verification these are source examples only, not claims about current NOAA/USGS/NASA state.
