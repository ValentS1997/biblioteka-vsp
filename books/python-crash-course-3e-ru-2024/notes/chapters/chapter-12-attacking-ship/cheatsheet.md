# Шпаргалка главы 12 — Атакующий корабль

## Game loop

~~~python
while True:
    self._check_events()
    self.ship.update()
    self._update_bullets()
    self._update_screen()
    self.clock.tick(60)
~~~

Pipeline:
1. input/events;
2. state update;
3. cleanup;
4. render;
5. frame pacing.

## Event model

~~~python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        ...
    elif event.type == pygame.KEYUP:
        ...
~~~

Continuous movement:
- KEYDOWN → `moving_right/left = True`;
- KEYUP → flag `False`;
- `Ship.update()` читает flags каждый frame.

## Fractional movement

~~~python
self.x = float(self.rect.x)

if self.moving_right:
    self.x += self.settings.ship_speed

self.rect.x = self.x
~~~

Source rationale: Rect position хранит integer display coordinate; отдельный float state сохраняет точность движения.

## Boundary checks

~~~python
if self.moving_right and self.rect.right < self.screen_rect.right:
    ...
if self.moving_left and self.rect.left > 0:
    ...
~~~

Acceptance: ship не выходит за левый/правый край.

## Bullets lifecycle

~~~text
SPACE
  ↓
_fire_bullet()
  ↓
Bullet(self)
  ↓
Group.add()
  ↓
Group.update()
  ↓
draw_bullet()
  ↓
rect.bottom <= 0
  ↓
Group.remove()
~~~

Перебирать copy, если удаляем элементы из Group:

~~~python
for bullet in self.bullets.copy():
    if bullet.rect.bottom <= 0:
        self.bullets.remove(bullet)
~~~

## Resource boundary

Invisible bullet ≠ destroyed bullet.

Source предупреждает: bullets за экраном продолжают существовать, потреблять memory и processing time.

## Refactoring rule

Когда coordinator method разрастается:
- event handling → `_check_events()`;
- key handlers → `_check_keydown_events()`, `_check_keyup_events()`;
- render → `_update_screen()`;
- bullet update/cleanup → `_update_bullets()`.

## Fullscreen safety

До fullscreen source требует убедиться, что работает выход по `Q`.

~~~python
elif event.key == pygame.K_q:
    sys.exit()
~~~

## Verification checklist

- окно создаётся;
- QUIT завершает process;
- frame rate стабилизируется относительно source target;
- ship отображается внизу по центру;
- movement continuous;
- simultaneous left/right не даёт дрейфа;
- edge constraints работают;
- Space создаёт bullets;
- bullets удаляются после ухода за верхний край;
- bullet count ограничен `bullets_allowed`.
