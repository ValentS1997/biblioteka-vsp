# Разбор упражнений главы 12

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Pygame здесь не запускался.

## 12.1. Синее небо

~~~python
import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 800))
bg_color = (0, 0, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill(bg_color)
    pygame.display.flip()
~~~

Source support: window, event loop, RGB background, flip.

## 12.2. Игровой персонаж

Asset: `[Needs confirmation]`.

Source-supported structure:

~~~python
class Character:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/character.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)
~~~

Path/image are placeholders until actual asset is chosen.

## 12.3. Документация Pygame

External verification intentionally not performed in `rag_only`.

Canonical result: `[Needs confirmation]`.

## 12.4. Ракета

Source patterns extend directly from Ship movement.

~~~python
class Rocket:
    def __init__(self, game):
        self.screen_rect = game.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += 1
        if self.moving_left and self.rect.left > 0:
            self.x -= 1
        if self.moving_up and self.rect.top > 0:
            self.y -= 1
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += 1

        self.rect.x = self.x
        self.rect.y = self.y
~~~

Asset loading/constructor details: `[Needs confirmation]`.

Acceptance: все четыре направления работают, rect не пересекает screen bounds.

## 12.5. Клавиши

~~~python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            print(event.key)

    pygame.display.flip()
~~~

Source objective — наблюдать numeric/key values, а не заранее перечислять их.

## 12.6. Боковая стрельба

Source-grounded adaptation:
- vertical ship flags;
- ship constrained top/bottom;
- bullet starts at ship right side;
- bullet x increases;
- cleanup when `rect.left >= screen_rect.right`.

Bullet update concept:

~~~python
def update(self):
    self.x += self.settings.bullet_speed
    self.rect.x = self.x
~~~

Spawn alignment:

~~~python
self.rect.midleft = ai_game.ship.rect.midright
~~~

Cleanup:

~~~python
for bullet in self.bullets.copy():
    if bullet.rect.left >= self.screen.get_rect().right:
        self.bullets.remove(bullet)
~~~

Полный конкретный file layout может повторять architecture главы; filenames/assets пользователя: `[Needs confirmation]`.
