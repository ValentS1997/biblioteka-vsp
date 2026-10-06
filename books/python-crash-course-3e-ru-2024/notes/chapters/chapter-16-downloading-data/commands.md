# Операции главы 16

## Read local dataset

~~~python
contents = path.read_text()
lines = path.read_text().splitlines()
~~~

Classification: read-only file I/O.

Input file presence: `[Needs confirmation]`.

## CSV reader

~~~python
reader = csv.reader(lines)
header_row = next(reader)
~~~

Classification: in-memory parsing.

## Inspect schema

~~~python
for index, column_header in enumerate(header_row):
    print(index, column_header)
~~~

Classification: read-only inspection.

## Parse date

~~~python
datetime.strptime(row[2], '%Y-%m-%d')
~~~

Classification: in-memory conversion.

## Handle missing numeric data

~~~python
try:
    high = int(row[3])
    low = int(row[4])
except ValueError:
    print(f"Missing data for {current_date}")
else:
    ...
~~~

## Matplotlib display

~~~python
plt.show()
~~~

Classification: UI/workload action.

## Parse GeoJSON

~~~python
all_eq_data = json.loads(contents)
~~~

Classification: in-memory parsing.

## Write readable GeoJSON

~~~python
readable_contents = json.dumps(all_eq_data, indent=4)
path.write_text(readable_contents)
~~~

Classification: persistent file write.

Target path and rollback/backup requirement: `[Needs confirmation]`.

## Plotly world map

~~~python
fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=mags,
    title=title,
)
fig.show()
~~~

Classification: browser/UI workload.

## Inspect Plotly color scales

~~~python
import plotly.express as px
px.colors.named_colorscales()
~~~

Classification: read-only runtime inspection.

## External-data operations

Source describes manual downloads/orders from:
- supplemental book site;
- NOAA;
- USGS earthquake feeds;
- NASA fire-data site.

These external/network operations were not executed in `rag_only`.

Current URLs/data availability/schema: `[Needs confirmation]`.
