# Диаграмма — глава 15

## Synthetic visualization pipeline

~~~mermaid
flowchart LR
    A["Generate data"] --> B["Validate domain/shape"]
    B --> C["Transform / aggregate"]
    C --> D["Visualize"]
    D --> E["Inspect pattern"]
    E --> F["Tune style/layout"]
    F --> G["show() or save"]
~~~

## Random walk

~~~mermaid
flowchart TD
    A["(0,0)"] --> B["choose x direction/distance"]
    B --> C["choose y direction/distance"]
    C --> D{"x_step=0 and y_step=0?"}
    D -- "yes" --> B
    D -- "no" --> E["previous + step"]
    E --> F["append x/y"]
    F --> G{"num_points reached?"}
    G -- "no" --> B
    G -- "yes" --> H["visualize"]
~~~

## Dice simulation

~~~mermaid
flowchart TD
    A["Die.roll() repeated"] --> B["results list"]
    B --> C["enumerate possible results"]
    C --> D["count frequency"]
    D --> E["frequencies"]
    E --> F["px.bar()"]
    F --> G["show() / write_html()"]
~~~
