# Шпаргалка главы 13 — Осторожно, пришельцы!

## Fleet creation

Source pattern:

~~~python
alien = Alien(self)
alien_width, alien_height = alien.rect.size
current_x, current_y = alien_width, alien_height

while current_y < (self.settings.screen_height - 3 * alien_height):
    while current_x < (self.settings.screen_width - 2 * alien_width):
        self._create_alien(current_x, current_y)
        current_x += 2 * alien_width

    current_x = alien_width
    current_y += 2 * alien_height
~~~

Acceptance:
- rows aligned;
- spacing maintained;
- room remains for ship/gameplay.

## Fleet movement

~~~python
self.fleet_direction = 1
self.x += self.settings.alien_speed * self.settings.fleet_direction
~~~

Edge check:

~~~python
return (
    self.rect.right >= screen_rect.right
    or self.rect.left <= 0
)
~~~

On edge:
1. drop every alien by `fleet_drop_speed`;
2. multiply `fleet_direction` by `-1`.

## Collision flow

Bullets vs aliens:

~~~python
pygame.sprite.groupcollide(
    self.bullets,
    self.aliens,
    True,
    True,
)
~~~

- first `True`: collided bullets removed;
- second `True`: collided aliens removed.

Ship vs aliens:

~~~python
pygame.sprite.spritecollideany(self.ship, self.aliens)
~~~

Returns collided alien or `None` according to source.

## Empty-fleet reset

~~~python
if not self.aliens:
    self.bullets.empty()
    self._create_fleet()
~~~

## Ship-loss lifecycle

~~~text
alien hits ship OR alien reaches bottom
            ↓
        _ship_hit()
            ↓
 ships_left -= 1
 aliens.empty()
 bullets.empty()
 _create_fleet()
 center_ship()
 sleep(0.5)
~~~

When no ships remain:
- `game_active = False`;
- events/render still run;
- ship/bullets/aliens updates stop.

## Test-only modifications

Source examples:
- `bullet_width = 300` or even 3000;
- larger `fleet_drop_speed`;
- smaller screen;
- faster bullets.

Purpose: accelerate validation.

Rollback: restore normal settings after testing.

## Verification checklist

- first alien displayed;
- complete fleet grid generated;
- fleet reverses at both edges;
- fleet drops once per edge encounter;
- bullets remove aliens;
- destroyed fleet respawns;
- ship collision decrements lives;
- alien reaching bottom uses same loss path;
- final ship loss sets inactive state;
- quit/events still work when game inactive.
