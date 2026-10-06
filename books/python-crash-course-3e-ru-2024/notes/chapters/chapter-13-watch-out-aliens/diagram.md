# Диаграмма — глава 13

## Fleet lifecycle

~~~mermaid
flowchart TD
    A["_create_fleet()"] --> B["nested while grid"]
    B --> C["aliens Group"]
    C --> D["_update_aliens()"]
    D --> E{"edge reached?"}
    E -- "yes" --> F["drop fleet"]
    F --> G["direction *= -1"]
    G --> H["aliens.update()"]
    E -- "no" --> H
~~~

## Bullet collision

~~~mermaid
flowchart TD
    A["bullets.update()"] --> B["groupcollide()"]
    B --> C["remove collided bullet/alien"]
    C --> D{"aliens empty?"}
    D -- "yes" --> E["bullets.empty()"]
    E --> F["_create_fleet()"]
    D -- "no" --> G["continue"]
~~~

## Player loss

~~~mermaid
flowchart TD
    A["alien hits ship"] --> C["_ship_hit()"]
    B["alien reaches bottom"] --> C
    C --> D{"ships remain?"}
    D -- "yes" --> E["ships_left -= 1"]
    E --> F["clear groups"]
    F --> G["new fleet + center ship"]
    G --> H["sleep(0.5)"]
    D -- "no" --> I["game_active = False"]
~~~
