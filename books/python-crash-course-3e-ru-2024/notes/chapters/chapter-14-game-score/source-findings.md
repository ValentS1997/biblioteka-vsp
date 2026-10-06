# Source findings — глава 14

## Finding 1 — prep_msg() vs _prep_msg()

Classification: **[Source method-name mismatch]**

Provenance:
- chunks: `e0024:c01–c02`
- EPUB spine item: `24`
- locator: `OEBPS/Text/978544614112-21.xhtml`

`Button.__init__()` calls:

~~~python
self.prep_msg(msg)
~~~

But the method shown immediately afterward is defined as:

~~~python
def _prep_msg(self, msg):
~~~

Leading underscore differs.

Adjudication: intended name `[Needs confirmation]`.

## Finding 2 — level-up operation order

Classification: **[Source prose/code ordering mismatch]**

Provenance:
- chunk: `e0024:c05`

Prose says `increase_speed()` is called when the last alien is destroyed, **before** creating the new fleet.

Shown listing:

~~~python
self.bullets.empty()
self._create_fleet()
self.settings.increase_speed()
~~~

The stated order and listed order differ.

Adjudication: intended order `[Needs confirmation]`.

## Finding 3 — high-score receiver

Classification: **[Source receiver mismatch]**

Provenance:
- chunks: `e0024:c09–c10`

Method is defined in `Scoreboard`:

~~~python
def check_high_score(self):
~~~

But the `AlienInvasion` collision listing calls:

~~~python
self.check_high_score()
~~~

The surrounding architecture stores the scoreboard as `self.sb`.

Adjudication: intended receiver `[Needs confirmation]`.

Policy action: preserve mismatch; do not silently rewrite canonical RAG.

## Finding 4 — create_fleet() vs _create_fleet()

Classification: **[Source method-name mismatch]**

Provenance:
- chunks: `e0024:c10–c11`

Level-up listing contains:

~~~python
self.create_fleet()
~~~

Project code in chapters 13–14 otherwise uses:

~~~python
self._create_fleet()
~~~

Leading underscore differs.

Adjudication: `[Needs confirmation]`.

## Finding 5 — check_bullet_alien_collisions() naming

Classification: **[Source method-name mismatch]**

Provenance:
- chunk: `e0024:c10`

One listing defines:

~~~python
def check_bullet_alien_collisions(self):
~~~

Elsewhere chapter/project uses:

~~~python
def _check_bullet_alien_collisions(self):
~~~

Adjudication: `[Needs confirmation]`.

## Finding 6 — caption spelling

Classification: **[Source string typo]**

Provenance:
- chunk: `e0024:c07`

Shown code:

~~~python
pygame.display.set_caption("ALien Invasion")
~~~

Earlier project code uses `"Alien Invasion"`.

Policy action: preserve as source typo; no canonical correction.

## Finding 7 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0024:c02`–`e0024:c13`
- EPUB spine item: `24`
- locator: `OEBPS/Text/978544614112-21.xhtml`

Observed starts include partial continuations such as `параметр self...`, `вому методу...`, `n.py...`, `значением...`, `возвращаться...`, `пляра Scoreboard...`, `ся...`, `обавляется новая функция...`, `llisions(self)...`, `x задается...`, `в нужных местах...`.

Cross-check:
- adjacent chunks preserve context;
- exercises 14.1–14.8 recoverable;
- summary intact;
- `e0025:c01` confirms chapter 15;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.
