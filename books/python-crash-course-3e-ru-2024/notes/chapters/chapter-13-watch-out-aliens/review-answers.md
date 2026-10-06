# Разбор упражнений главы 13

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Pygame здесь не запускался.

## 13.1. Звезды

Asset: `[Needs confirmation]`.

Source-supported grid pattern повторяет fleet creation:

~~~python
star = Star(self)
star_width, star_height = star.rect.size
current_x, current_y = star_width, star_height

while current_y < self.settings.screen_height - 2 * star_height:
    while current_x < self.settings.screen_width - 2 * star_width:
        self._create_star(current_x, current_y)
        current_x += 2 * star_width

    current_x = star_width
    current_y += 2 * star_height
~~~

Конкретный class/file/asset layout: `[Needs confirmation]`.

## 13.2. Улучшенные звезды

Source даёт только механизм random offset:

~~~python
from random import randint

x_offset = randint(-10, 10)
y_offset = randint(-10, 10)
~~~

Source-grounded application:

~~~python
new_star.rect.x = x_position + x_offset
new_star.rect.y = y_position + y_offset
~~~

Точный диапазон/частота отклонения, кроме указанного `-10..10`, не расширяются.

## 13.3. Капли

Asset: `[Needs confirmation]`.

Source-supported lifecycle по аналогии с aliens/bullets:

~~~python
def update(self):
    self.y += self.settings.drop_speed
    self.rect.y = self.y
~~~

Cleanup:

~~~python
for drop in self.drops.copy():
    if drop.rect.top >= self.settings.screen_height:
        self.drops.remove(drop)
~~~

`drop_speed` и точный class layout: `[Needs confirmation]`.

## 13.4. Дождь

После cleanup source requirement — создать новый ряд сверху.

Один source-consistent control flow:

~~~python
if not self.drops:
    self._create_rain()
~~~

Если реализация хранит несколько рядов одновременно, точная логика определения исчезнувшего ряда: `[Needs confirmation]`.

## 13.5. Боковая стрельба-2

Можно перенести текущие chapter patterns:
- aliens в `pygame.sprite.Group()`;
- `Alien.update()` для движения;
- `pygame.sprite.groupcollide()` для попаданий;
- cleanup/respawn по правилам выбранной игры.

Source предлагает два варианта размещения/movement aliens. Конкретный выбранный вариант: `[Needs confirmation]`.

Collision primitive:

~~~python
pygame.sprite.groupcollide(
    self.bullets,
    self.aliens,
    True,
    True,
)
~~~

## 13.6. Конец игры

Source требует два counters и выбранное пользователем game-over condition.

Минимальная state model:

~~~python
self.aliens_hit = 0
self.ship_hits = 0
self.game_active = True
~~~

При событиях:

~~~python
self.aliens_hit += 1
self.ship_hits += 1
~~~

После каждого relevant event:

~~~python
if [условие завершения]:
    self.game_active = False
~~~

Точный threshold/condition: `[Needs confirmation]`.

Acceptance:
- оба counters меняются только при соответствующих событиях;
- выбранное условие действительно переводит игру в inactive state;
- event handling и render остаются доступны после остановки gameplay, по pattern главы.
