# Шпаргалка главы 15 — Генерирование данных

## Matplotlib baseline

~~~python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(input_values, squares, linewidth=3)
plt.show()
~~~

Data correctness:
- если X-values meaningful — передавать их явно;
- иначе source показывает default indexing from 0.

## Scatter pipeline

~~~python
x_values = range(1, 1001)
y_values = [x**2 for x in x_values]

fig, ax = plt.subplots()
ax.scatter(x_values, y_values, s=10)
ax.axis([0, 1100, 0, 1_100_000])
~~~

Customization:
- `c='red'`;
- `c=(0, 0.8, 0)`;
- `c=y_values, cmap=plt.cm.Blues`;
- `ticklabel_format(style='plain')`.

## Save visualization

~~~python
plt.savefig('squares_plot.png', bbox_inches='tight')
~~~

Classification: persistent file write.

Target/overwrite policy: `[Needs confirmation]`.

## RandomWalk model

State:

~~~python
self.num_points = 5000
self.x_values = [0]
self.y_values = [0]
~~~

Step:

~~~python
direction = choice([1, -1])
distance = choice([0, 1, 2, 3, 4])
step = direction * distance
~~~

Reject:

~~~python
if x_step == 0 and y_step == 0:
    continue
~~~

Next point = previous point + step.

## Random walk visualization

~~~python
point_numbers = range(rw.num_points)

ax.scatter(
    rw.x_values,
    rw.y_values,
    c=point_numbers,
    cmap=plt.cm.Blues,
    edgecolors='none',
    s=15,
)
ax.set_aspect('equal')
~~~

Highlight:
- start: green;
- end: red;
- hide axes for visual focus.

## Plotly dice pipeline

~~~text
Die.roll()
  ↓
results
  ↓
possible results
  ↓
results.count(value)
  ↓
frequencies
  ↓
px.bar(...)
  ↓
fig.show()
~~~

Two dice:
- min result = 2;
- max result = sum of sides;
- distributions reflect number of combinations.

## Persistent Plotly output

~~~python
fig.write_html('dice_visual_d6d10.html')
~~~

Classification: persistent file write.

## Verification checklist

- generated values remain in expected domain;
- number of X/Y points matches;
- plot/scatter maps correct coordinates;
- random walk starts at `(0, 0)`;
- no zero-zero steps are appended;
- dice results stay between valid extrema;
- frequency list covers intended result domain;
- multi-dice chart labels every intended result;
- saved artifact path is confirmed before write.
