# Шпаргалка главы 17 — Работа с API

## Request pipeline

~~~python
import requests

url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

headers = {
    "Accept": "application/vnd.github.v3+json"
}

r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

response_dict = r.json()
~~~

Source success criterion shown: `status_code == 200`.

Current API/header compatibility: `[Needs confirmation]`.

## Response inspection

~~~python
print(response_dict.keys())
print(response_dict['total_count'])
print(not response_dict['incomplete_results'])

repo_dicts = response_dict['items']
print(len(repo_dicts))
~~~

Then inspect one repository before designing visualization.

## Repository fields used

~~~text
name
owner.login
stargazers_count
html_url
created_at
updated_at
description
~~~

Only a subset of the full response is required for the chart.

## Rate-limit model

Source response fields:

~~~text
resources
  └─ search
      ├─ limit
      ├─ remaining
      ├─ reset
      └─ used
~~~

`reset` is described as Unix/epoch time.

Numeric sample values are historical, not current.

## Plotly visualization

~~~python
fig = px.bar(
    x=repo_links,
    y=stars,
    title=title,
    labels=labels,
    hover_name=hover_texts,
)

fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
)

fig.update_traces(
    marker_color='SteelBlue',
    marker_opacity=0.6,
)

fig.show()
~~~

## Clickable repository labels

~~~python
repo_link = (
    f"<a href='{repo_url}'>{repo_name}</a>"
)
~~~

Source uses Plotly text/HTML support to turn X-axis labels into links.

## Hacker News pipeline

~~~text
topstories.json
    ↓
submission_ids
    ↓ first 30
item/{id}.json
    ↓
title / discussion link / comments
    ↓
sorted(..., key=itemgetter('comments'), reverse=True)
~~~

## Missing Hacker News comments

Source warns some hiring posts may omit `descendants` and cause `KeyError`.

Source remedy: wrap creation of `submission_dict` in `try-except` and skip such posts.

## Verification checklist

- response status inspected;
- decoded object has expected top-level keys;
- `incomplete_results` checked before trusting completeness;
- number of returned items inspected;
- required per-item fields exist before visualization;
- live counts/stars not treated as static;
- rate-limit state checked when repeated calls matter;
- HN records missing comments are handled explicitly.
