# Source findings — глава 13

## Finding 1 — change_fleet_direction() vs _change_fleet_direction()

Classification: **[Source method-name mismatch]**

Provenance:
- chunk: `e0023:c07`
- EPUB spine item: `23`
- locator: `OEBPS/Text/978544614112-20.xhtml`

Method defined as:

~~~python
def _change_fleet_direction(self):
~~~

but edge handler calls:

~~~python
self.change_fleet_direction()
~~~

Leading underscore differs.

Adjudication: intended method name `[Needs confirmation]`.

Policy action: canonical RAG unchanged; architecture artifacts use the internally consistent helper naming and preserve this finding.

## Finding 2 — stats.ships_left missing self

Classification: **[Source code mismatch]**

Provenance:
- chunk: `e0023:c12`

Shown `_ship_hit()` condition:

~~~python
if stats.ships_left > 0:
~~~

Elsewhere stats instance is created as:

~~~python
self.stats = GameStats(self)
~~~

and previous code accesses:

~~~python
self.stats.ships_left -= 1
~~~

Shown condition therefore differs from surrounding object access pattern.

Adjudication: `[Needs confirmation]`.

## Finding 3 — AlienInvasion.__init__(self, ai_game)

Classification: **[Source signature mismatch]**

Provenance:
- chunk: `e0023:c12`

Game-over section shows:

~~~python
def __init__(self, ai_game):
~~~

for `AlienInvasion`.

Earlier and later chapter/project code instantiates `AlienInvasion()` without an argument and defines its constructor as `__init__(self)`.

Adjudication: `[Needs confirmation]`.

## Finding 4 — _create_alien coordinate wording

Classification: **[Source prose/code mismatch]**

Provenance:
- chunk: `e0023:c04`

Shown call:

~~~python
self._create_alien(current_x, current_y)
~~~

and later definition:

~~~python
def _create_alien(self, x_position, y_position):
~~~

But prose says the call passes values on axes “Y and X”.

Code/order and prose wording differ.

Adjudication: `[Needs confirmation]`.

## Finding 5 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0023:c02`–`e0023:c13`
- EPUB spine item: `23`
- locator: `OEBPS/Text/978544614112-20.xhtml`

Observed starts include continuation fragments such as `super().__init__()...`, `льцев в верхней части...`, `ate_fleet()...`, `ления каждого ряда...`, `liens()...`, `авно 1...`, `емента с прямоугольником...`, `❷ self.bullets.empty()...`, `аботать столкновения...`, `mport Ship...`, `от вторжения...`, `self._update_aliens()...`.

Cross-check:
- adjacent chunks preserve context;
- exercises 13.1–13.6 recoverable;
- summary intact;
- `e0024:c01` confirms chapter 14;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## Additional observation — indentation in fleet-edge listing

Classification: **[Source code/extraction ambiguity]**

In `e0023:c07`, indentation around `_check_fleet_edges()` body is visually inconsistent in extracted text. Surrounding prose supplies the intended containment of the loop and condition, but exact source-vs-extraction origin is `[Needs confirmation]`.

Policy action: no RAG modification.
