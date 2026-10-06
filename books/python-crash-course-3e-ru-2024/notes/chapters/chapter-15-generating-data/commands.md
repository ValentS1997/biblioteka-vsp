# Команды и операции главы 15

## Install Matplotlib

~~~bash
python -m pip install --user matplotlib
~~~

Source alternative: use `python3` if that is the interpreter command.

Classification: **state-changing package-management action**.

Current interpreter/environment/version/rollback: `[Needs confirmation]`.

## Install Plotly + pandas

~~~bash
python -m pip install --user plotly
python -m pip install --user pandas
~~~

Classification: **state-changing package-management actions**.

Source says pandas is required for effective work with Plotly Express.

## Inspect Matplotlib styles

Source interactive session:

~~~python
import matplotlib.pyplot as plt
plt.style.available
~~~

Classification: read-only runtime inspection.

Current available styles: `[Needs confirmation]`.

## Show Matplotlib visualization

~~~python
plt.show()
~~~

Classification: UI/workload action.

## Save Matplotlib visualization

~~~python
plt.savefig('squares_plot.png', bbox_inches='tight')
~~~

Classification: persistent file write.

Source says filename-only target is stored alongside the script; `Path` can target another directory.

Overwrite behavior: `[Needs confirmation]`.

## Random source

~~~python
from random import choice
from random import randint
~~~

Used for random walks and dice.

## Plotly render

~~~python
fig = px.bar(x=poss_results, y=frequencies)
fig.show()
~~~

Classification: browser/UI workload.

Source describes interactive HTML/browser visualization.

## Plotly layout

~~~python
fig.update_layout(xaxis_dtick=1)
~~~

Purpose: show label at every integer result.

## Save Plotly HTML

~~~python
fig.write_html('dice_visual_d6d10.html')
~~~

Classification: persistent file write.

Exact target policy/overwrite behavior: `[Needs confirmation]`.

## Performance boundary

Source explicitly scales:
- random walk: 5000 → 50 000 points;
- dice: 1000 → 50 000 rolls;
- exercise 15.6 asks to increase rolls until system-resource limitations appear.

Therefore large runs are workload-generating; safe maximum on current system: `[Needs confirmation]`.
