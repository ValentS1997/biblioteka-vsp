# Разбор упражнений главы 14

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Pygame здесь не запускался.

## 14.1. Запуск игры клавишей P

Source прямо предлагает общий helper `start_game()`.

Один source-consistent shape:

~~~python
def start_game(self):
    self.settings.initialize_dynamic_settings()
    self.stats.reset_stats()
    self.sb.prep_score()
    self.sb.prep_level()
    self.sb.prep_ships()

    self.bullets.empty()
    self.aliens.empty()
    self._create_fleet()
    self.ship.center_ship()

    self.game_active = True
    pygame.mouse.set_visible(False)
~~~

Mouse path:

~~~python
if button_clicked and not self.game_active:
    self.start_game()
~~~

Keyboard path:

~~~python
elif event.key == pygame.K_p and not self.game_active:
    self.start_game()
~~~

Название `start_game()` предложено самим exercise.

## 14.2. Стрельба по мишени

Source определяет behavior, но не задаёт готовый class layout.

Минимальная state decomposition:

- `Ship`: vertical movement + fire;
- `Target`: rectangle, vertical speed/direction;
- bullets group;
- misses counter;
- `game_active`;
- Play button.

Core conditions:

~~~text
bullet intersects target → hit handling
bullet exits right edge without hit → miss += 1
misses >= 3 → game_active = False
~~~

Конкретная collision API/Target class implementation в exercise не задаётся: `[Needs confirmation]`.

## 14.3. Учебная стрельба с нарастающей сложностью

Source pattern from current chapter:

~~~python
def initialize_dynamic_settings(self):
    self.target_speed = self.target_initial_speed

def increase_speed(self):
    self.target_speed *= self.speedup_scale
~~~

Конкретные `target_initial_speed` и `speedup_scale`: `[Needs confirmation]`.

Acceptance:
- speed grows during one game;
- Play/reset restores initial speed.

## 14.4. Уровни сложности

Source requires buttons that assign Settings values.

Conceptual mapping:

~~~text
Easy button   → Settings preset A
Medium button → Settings preset B
Hard button   → Settings preset C
~~~

Exact names/count/values of presets: `[Needs confirmation]`.

Verification:
- selected button changes intended settings;
- new game begins with selected initial difficulty;
- dynamic progression continues from that baseline.

## 14.5. Исторический рекорд

Source supports the required lifecycle, but not the exact file implementation:

~~~text
GameStats initialization
    ↓
load persisted high score
    ↓
gameplay may update high_score
    ↓
before sys.exit()
    ↓
write high_score to file
~~~

Exact path, serialization format, missing/corrupt-file behavior and rollback: `[Needs confirmation]`.

Operational classification: persistent state-changing write.

## 14.6. Рефакторинг

Source-suggested extraction:

~~~python
def start_new_level(self):
    self.bullets.empty()
    self._create_fleet()
    self.settings.increase_speed()
    self.stats.level += 1
    self.sb.prep_level()
~~~

Scoreboard aggregation:

~~~python
def prep_images(self):
    self.prep_score()
    self.prep_high_score()
    self.prep_level()
    self.prep_ships()
~~~

These names and goals come directly from exercise 14.6.

Recovery instructions from Appendix Г: `[Needs confirmation]` within chapter-only scope.

## 14.7. Расширение игры

Source-supported options:
- alien fire;
- shelters destructible by both sides;
- sound via `pygame.mixer`.

Implementation details are intentionally open-ended: `[Needs confirmation]`.

## 14.8. Боковая стрельба, финальная версия

Source expects transfer of project concepts rather than a fixed implementation.

Acceptance checklist:
- Play/restart lifecycle;
- dynamic speed scaling;
- score updates;
- reset transient state on new game;
- game-over path;
- refactoring keeps coordinator readable.

Additional custom settings/design choices: `[Needs confirmation]`.
