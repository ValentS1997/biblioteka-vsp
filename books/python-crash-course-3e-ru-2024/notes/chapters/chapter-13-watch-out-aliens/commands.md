# Операции главы 13

## Draw alien group

~~~python
self.aliens.draw(self.screen)
~~~

Тип: runtime render.

## Update every alien

~~~python
self.aliens.update()
~~~

Тип: runtime state-changing; вызывает `Alien.update()` для каждого sprite.

## Edge detection

~~~python
alien.check_edges()
~~~

Тип: read-only state check.

## Change fleet direction

Source intended operation:

~~~python
for alien in self.aliens.sprites():
    alien.rect.y += self.settings.fleet_drop_speed

self.settings.fleet_direction *= -1
~~~

Тип: runtime state-changing.

Finding: один listing вызывает имя метода без leading underscore.

## Bullet/alien collision

~~~python
pygame.sprite.groupcollide(
    self.bullets,
    self.aliens,
    True,
    True,
)
~~~

Тип: state-changing collision operation.

Effect: shown arguments remove both collided bullets and aliens.

Alternative shown by source:

~~~python
pygame.sprite.groupcollide(
    self.bullets,
    self.aliens,
    False,
    True,
)
~~~

Effect: bullet survives collision, alien removed.

## Empty group

~~~python
if not self.aliens:
    self.bullets.empty()
    self._create_fleet()
~~~

`empty()` removes all sprites from group.

## Ship collision

~~~python
pygame.sprite.spritecollideany(self.ship, self.aliens)
~~~

Тип: collision check.

## Pause after hit

~~~python
from time import sleep
sleep(0.5)
~~~

Тип: workload-pausing runtime action.

## Clear groups

~~~python
self.aliens.empty()
self.bullets.empty()
~~~

Тип: state-changing.

## Center ship

~~~python
self.rect.midbottom = self.screen_rect.midbottom
self.x = float(self.rect.x)
~~~

## Game state flag

~~~python
self.game_active = False
~~~

Main loop source pattern:

~~~python
self._check_events()

if self.game_active:
    self.ship.update()
    self._update_bullets()
    self._update_aliens()

self._update_screen()
~~~

## Temporary test settings

Changing `bullet_width`, `fleet_drop_speed`, speed, or screen size is state/config-changing.

Acceptance:
- test condition reached faster;
- expected branch observed;
- original gameplay settings restored afterward.
