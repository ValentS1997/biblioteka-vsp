# Шпаргалка главы 14 — Игровой счет

## Start / restart gate

~~~python
button_clicked = self.play_button.rect.collidepoint(mouse_pos)

if button_clicked and not self.game_active:
    self.settings.initialize_dynamic_settings()
    self.stats.reset_stats()
    self.game_active = True
    self.bullets.empty()
    self.aliens.empty()
    self._create_fleet()
    self.ship.center_ship()
~~~

После model reset требуется обновить scoreboard images.

## Cursor state

On start:

~~~python
pygame.mouse.set_visible(False)
~~~

On game over:

~~~python
pygame.mouse.set_visible(True)
~~~

## Dynamic settings

~~~python
self.speedup_scale = 1.1
self.score_scale = 1.5
~~~

Initial dynamic state:

~~~python
self.ship_speed = 1.5
self.bullet_speed = 2.5
self.alien_speed = 1.0
self.fleet_direction = 1
self.alien_points = 50
~~~

Level-up:

~~~python
self.ship_speed *= self.speedup_scale
self.bullet_speed *= self.speedup_scale
self.alien_speed *= self.speedup_scale
self.alien_points = int(self.alien_points * self.score_scale)
~~~

## Score lifecycle

State:

~~~python
self.score = 0
self.high_score = 0
self.level = 1
~~~

Display:
- `prep_score()`;
- `prep_high_score()`;
- `prep_level()`;
- `prep_ships()`;
- `show_score()`.

Rule: state changed → prepare new image.

## Count every hit

~~~python
for aliens in collisions.values():
    self.stats.score += (
        self.settings.alien_points * len(aliens)
    )
~~~

Then refresh score and high score.

## Formatting

~~~python
rounded_score = round(self.stats.score, -1)
score_str = f"{rounded_score:,}"
~~~

Source uses rounding to tens and comma group separators.

## Remaining lives

`Ship` inherits `Sprite`; `Scoreboard.prep_ships()` creates one ship sprite per `ships_left`.

## Temporary verification changes

Source uses:
- wide bullets to verify multi-hit scoring;
- `print(self.alien_points)` to verify scaling.

Rollback:
- restore normal bullet width;
- remove debug `print()` after validation.

## Acceptance checks

- Play appears only when inactive;
- click outside button does nothing;
- click button during active game does not restart;
- cursor hidden only during active game;
- restart resets transient score/level/speeds/lives;
- high score survives restarts within same process;
- multi-kill awards all points;
- new level increments level and speeds;
- remaining ship icons track `ships_left`.
