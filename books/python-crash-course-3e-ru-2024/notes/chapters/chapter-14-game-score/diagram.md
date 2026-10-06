# Диаграмма — глава 14

## Game start / restart

~~~mermaid
flowchart TD
    A["Play click / start input"] --> B{"game inactive?"}
    B -- "no" --> C["ignore restart"]
    B -- "yes" --> D["reset stats/settings"]
    D --> E["clear bullets/aliens"]
    E --> F["create fleet + center ship"]
    F --> G["refresh scoreboard"]
    G --> H["game_active = True"]
    H --> I["hide cursor"]
~~~

## Level-up

~~~mermaid
flowchart TD
    A["fleet destroyed"] --> B["clear bullets"]
    B --> C["new fleet"]
    C --> D["increase_speed()"]
    D --> E["level += 1"]
    E --> F["prep_level()"]
~~~

## Scoring

~~~mermaid
flowchart TD
    A["groupcollide()"] --> B{"collisions?"}
    B -- "yes" --> C["sum aliens per collision values"]
    C --> D["score += points × count"]
    D --> E["prep_score()"]
    E --> F["check high score"]
    F --> G["prep_high_score() if needed"]
~~~
