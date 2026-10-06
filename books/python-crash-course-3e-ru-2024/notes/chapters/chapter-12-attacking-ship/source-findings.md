# Source findings — глава 12

## Finding 1 — Ship(screen) vs Ship(ai_game)

Classification: **[Source code/prose mismatch]**

Provenance:
- chunk: `e0022:c06`
- spine: `22`
- locator: `OEBPS/Text/978544614112-19.xhtml`

`Ship.__init__()` определён как:

~~~python
def __init__(self, ai_game):
~~~

и использует `ai_game.screen`.

Но integration listing показывает:

~~~python
self.ship = Ship(screen)
~~~

Surrounding prose говорит, что Ship передаётся текущий instance `AlienInvasion`, то есть объект, дающий доступ к screen/resources.

Adjudication: exact intended token `[Needs confirmation]`.

Policy action: canonical RAG не исправлять. В архитектурных artifacts использовать только согласованную model «Ship получает game instance», явно сохраняя mismatch.

## Finding 2 — check_events vs _check_events

Classification: **[Source method-name mismatch]**

Provenance:
- chunk: `e0022:c08`

Shown listing содержит:

~~~python
def check_events(self):
~~~

Но до и после этого chapter repeatedly defines/calls:

~~~python
self._check_events()
def _check_events(self):
~~~

Adjudication: `[Needs confirmation]`.

## Finding 3 — bullet cleanup indentation

Classification: **[Source code/extraction mismatch]**

Provenance:
- chunk: `e0022:c15`

В RAG listing cleanup loop, `_update_screen()` и `clock.tick(60)` визуально dedented за пределы `while True`.

Surrounding prose утверждает:
- bullet positions update every main-loop iteration;
- off-screen bullets are then removed;
- updated state is rendered each iteration;
- later `_update_bullets()` is said to be cut from `run_game()` and called inside `while`.

Следовательно, extracted indentation расходится с described control flow.

Root cause source-layout vs extraction: `[Needs confirmation]`.

## Finding 4 — draw_rect() terminology

Classification: **[Source terminology/code mismatch]**

Provenance:
- chunk: `e0022:c14`

Code:

~~~python
pygame.draw.rect(self.screen, self.color, self.rect)
~~~

Prose затем называет вызов «функция draw_rect()».

Exact naming mismatch preserved; no silent normalization of source text.

## Finding 5 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0022:c02`–`e0022:c16`
- spine: `22`
- locator: `OEBPS/Text/978544614112-19.xhtml`

Observed starts include continuation fragments such as `соответствующим образом...`, `рамма обнаруживает...`, `ть до 16 миллионов...`, `отек...`, `y прямоугольника...`, `ым методом...`, `ame.QUIT...`, `e() корабля...`, `ние"...`, `ше значения...`, `ight...`, `кле событий...`, `наряд на экран...`, `ullet...`, `арядов...`.

Cross-check:
- neighboring chunks preserve context;
- exercises 12.1–12.6 recoverable;
- summary intact;
- `e0023:c01` confirms chapter 13;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.
