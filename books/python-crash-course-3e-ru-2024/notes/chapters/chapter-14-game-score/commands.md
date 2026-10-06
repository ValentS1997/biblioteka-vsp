# Операции главы 14

## Button rendering

~~~python
pygame.font.SysFont(None, 48)
font.render(msg, True, text_color, button_color)
screen.fill(button_color, rect)
screen.blit(msg_image, msg_image_rect)
~~~

Тип: runtime UI rendering.

## Mouse click

~~~python
pygame.mouse.get_pos()
self.play_button.rect.collidepoint(mouse_pos)
~~~

Тип: input/read-only geometry check.

## Cursor visibility

~~~python
pygame.mouse.set_visible(False)
pygame.mouse.set_visible(True)
~~~

Тип: runtime UI state-changing.

## Start/reset operations

~~~python
self.stats.reset_stats()
self.settings.initialize_dynamic_settings()
self.bullets.empty()
self.aliens.empty()
self._create_fleet()
self.ship.center_ship()
~~~

Тип: runtime game-state reset.

## Difficulty scaling

~~~python
self.settings.increase_speed()
~~~

Тип: runtime state-changing.

Source dynamic values are multiplied by scale factors.

## Score refresh

~~~python
self.sb.prep_score()
self.sb.prep_high_score()
self.sb.prep_level()
self.sb.prep_ships()
~~~

Тип: rebuild rendered UI state from current model values.

## High score comparison

Defined by source in `Scoreboard`:

~~~python
if self.stats.score > self.stats.high_score:
    self.stats.high_score = self.stats.score
    self.prep_high_score()
~~~

Finding: one listing calls receiver inconsistently; see `source-findings.md`.

## Draw scoreboard

~~~python
self.sb.show_score()
~~~

Includes score/high score/level and ship sprites after final evolution.

## Debug verification

~~~python
print(self.alien_points)
~~~

Temporary only. Source explicitly says remove after verification because terminal output affects performance and distracts player.

## Persistent high score — exercise 14.5

Source requirement:
- write high score to a file before `sys.exit()`;
- load it when initializing `GameStats.high_score`.

Exact file API/path/format/error handling in this chapter: `[Needs confirmation]`.

Classification: persistent state-changing.

Rollback/backup policy: `[Needs confirmation]`.
