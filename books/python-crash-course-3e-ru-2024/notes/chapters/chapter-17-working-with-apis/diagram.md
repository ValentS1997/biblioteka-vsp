# Диаграмма — глава 17

## GitHub API pipeline

~~~mermaid
flowchart LR
    A["Build URL/query"] --> B["requests.get()"]
    B --> C["status_code"]
    C --> D["r.json()"]
    D --> E["inspect total/incomplete/items"]
    E --> F["extract repo fields"]
    F --> G["Plotly bar chart"]
    G --> H["hover + links + styling"]
~~~

## Rate-limit checkpoint

~~~mermaid
flowchart TD
    A["Need repeated API calls"] --> B["inspect rate limit"]
    B --> C{"remaining > 0?"}
    C -- "yes" --> D["continue requests"]
    C -- "no" --> E["wait until reset per source"]
~~~

## Hacker News aggregation

~~~mermaid
flowchart TD
    A["topstories.json"] --> B["story IDs"]
    B --> C["first 30 IDs"]
    C --> D["item/{id}.json per ID"]
    D --> E{"comments field exists?"}
    E -- "yes" --> F["build submission dict"]
    E -- "no" --> G["skip via try/except"]
    F --> H["sort by comments desc"]
    G --> H
~~~
