# Диаграмма — глава 16

## Weather CSV pipeline

~~~mermaid
flowchart LR
    A["CSV file"] --> B["read_text().splitlines()"]
    B --> C["csv.reader()"]
    C --> D["inspect header"]
    D --> E["parse date/temp fields"]
    E --> F{"ValueError?"}
    F -- "yes" --> G["skip incomplete record"]
    F -- "no" --> H["append synchronized lists"]
    H --> I["Matplotlib plot/fill_between"]
~~~

## GeoJSON pipeline

~~~mermaid
flowchart LR
    A["GeoJSON file"] --> B["read_text()"]
    B --> C["json.loads()"]
    C --> D["features"]
    D --> E["mag / lon / lat / title"]
    E --> F["scatter_geo()"]
    F --> G["size/color/projection/hover"]
~~~

## Data-quality gate

~~~mermaid
flowchart TD
    A["Dataset"] --> B["Confirm provenance/date"]
    B --> C["Inspect schema"]
    C --> D["Convert values"]
    D --> E{"Missing/invalid?"}
    E -- "yes" --> F["handle/skip explicitly"]
    E -- "no" --> G["include record"]
    F --> H["validate resulting series"]
    G --> H
    H --> I["visualize"]
~~~
