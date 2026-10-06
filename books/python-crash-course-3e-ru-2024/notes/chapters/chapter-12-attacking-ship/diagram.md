# Диаграмма — глава 12

## Main loop

~~~mermaid
flowchart LR
    A["events"] --> B["_check_events()"]
    B --> C["ship.update()"]
    C --> D["_update_bullets()"]
    D --> E["_update_screen()"]
    E --> F["clock.tick(60)"]
    F --> A
~~~

## Movement

~~~mermaid
flowchart TD
    A["KEYDOWN RIGHT"] --> B["moving_right = True"]
    C["KEYUP RIGHT"] --> D["moving_right = False"]
    B --> E["Ship.update()"]
    D --> E
    E --> F{"right edge free?"}
    F -- "yes" --> G["x += ship_speed"]
    F -- "no" --> H["keep position"]
~~~

## Bullet lifecycle

~~~mermaid
flowchart TD
    A["SPACE"] --> B["_fire_bullet()"]
    B --> C{"len(bullets) < allowed?"}
    C -- "yes" --> D["Bullet(self)"]
    D --> E["bullets.add()"]
    E --> F["bullets.update()"]
    F --> G["draw_bullet()"]
    G --> H{"rect.bottom <= 0?"}
    H -- "yes" --> I["remove from copied group iteration"]
    H -- "no" --> F
~~~
