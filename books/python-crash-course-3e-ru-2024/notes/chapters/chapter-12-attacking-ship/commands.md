# Команды и операции главы 12

## Установка Pygame

~~~bash
python -m pip install --user pygame
~~~

Классификация: **state-changing package-management action**.

Перед запуском в реальном окружении:
- Python interpreter: `[Needs confirmation]`;
- active environment: `[Needs confirmation]`;
- installed/current pygame: `[Needs confirmation]`;
- rollback/version pin: `[Needs confirmation]`.

Source допускает заменить `python` на `python3`, если именно так запускается interpreter.

## Pygame init / window

~~~python
pygame.init()
self.screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Alien Invasion")
~~~

Тип: runtime/UI state-changing.

## Main event source

~~~python
pygame.event.get()
~~~

Тип: runtime event polling.

## Exit

~~~python
sys.exit()
~~~

Тип: process termination.

## Render

~~~python
self.screen.fill(self.settings.bg_color)
self.ship.blitme()
pygame.display.flip()
~~~

## Frame pacing

~~~python
self.clock = pygame.time.Clock()
self.clock.tick(60)
~~~

Source target: 60 loop iterations/second where system allows.

## Image load

~~~python
pygame.image.load('images/ship.bmp')
~~~

Requires external/local asset. File presence: `[Needs confirmation]`.

## Rect operations

~~~python
surface.get_rect()
self.rect.midbottom = self.screen_rect.midbottom
~~~

## Fullscreen

~~~python
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
~~~

Risk: UI capture/fullscreen. Source prerequisite: verify `Q` exit first.

## Sprite group

~~~python
self.bullets = pygame.sprite.Group()
self.bullets.add(new_bullet)
self.bullets.update()
self.bullets.copy()
self.bullets.remove(bullet)
~~~

## Draw bullet

~~~python
pygame.draw.rect(self.screen, self.color, self.rect)
~~~

Source prose elsewhere says `draw_rect()`; see findings.

## Debug print

~~~python
print(len(self.bullets))
~~~

Source says удалить после verification, потому что terminal output noticeably slows the game.
