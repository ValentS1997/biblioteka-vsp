# Разбор упражнений главы 15

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Библиотеки здесь не устанавливались и visualizations не запускались.

## 15.1. Кубы

Первые пять:

~~~python
import matplotlib.pyplot as plt

x_values = range(1, 6)
y_values = [x**3 for x in x_values]

fig, ax = plt.subplots()
ax.scatter(x_values, y_values, s=100)
plt.show()
~~~

Первые 5000:

~~~python
x_values = range(1, 5001)
y_values = [x**3 for x in x_values]

fig, ax = plt.subplots()
ax.scatter(x_values, y_values, s=10)
plt.show()
~~~

Оформление title/axes можно повторить по chapter pattern.

## 15.2. Цветные кубы

~~~python
ax.scatter(
    x_values,
    y_values,
    c=y_values,
    cmap=plt.cm.Blues,
    s=10,
)
~~~

Точная colormap может быть изменена пользователем; source example использует `Blues`.

## 15.3. Движение молекул

Source-required shape:

~~~python
rw = RandomWalk(5000)
rw.fill_walk()

fig, ax = plt.subplots()
ax.plot(rw.x_values, rw.y_values, linewidth=1)
ax.set_aspect('equal')
plt.show()
~~~

Exact `linewidth` value source exercise не задаёт: значение выше — минимальный placeholder для выполнения требования и может быть изменено.

## 15.4. Измененные случайные блуждания

Variant A — больше distance choices:

~~~python
distance = choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
~~~

Variant B — запрет движения в отрицательную сторону по одной axis:

~~~python
x_direction = choice([1])
~~~

Source требует эксперимент и наблюдение формы; expected final shape заранее не фиксируется.

## 15.5. Рефакторинг

Source directly specifies target:

~~~python
def get_step(self):
    direction = choice([1, -1])
    distance = choice([0, 1, 2, 3, 4])
    return direction * distance
~~~

Then:

~~~python
x_step = self.get_step()
y_step = self.get_step()
~~~

Zero-zero rejection остаётся в `fill_walk()`.

## 15.6. Два кубика D8

~~~python
die_1 = Die(8)
die_2 = Die(8)

results = [
    die_1.roll() + die_2.roll()
    for _ in range(1000)
]

max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result + 1)
frequencies = [
    results.count(value)
    for value in poss_results
]
~~~

Visualization повторяет chapter `px.bar()` pattern.

Safe maximum number of rolls on current system: `[Needs confirmation]`.

## 15.7. Три кубика

~~~python
die_1 = Die()
die_2 = Die()
die_3 = Die()

results = [
    die_1.roll() + die_2.roll() + die_3.roll()
    for _ in range(1000)
]

poss_results = range(3, 19)
frequencies = [
    results.count(value)
    for value in poss_results
]
~~~

Количество rolls exercise не задаёт; 1000 здесь следует текущему chapter baseline, но exact chosen workload: `[Needs confirmation]`.

## 15.8. Умножение

Core change supported by exercise:

~~~python
result = die_1.roll() * die_2.roll()
~~~

Остальная simulation/frequency pipeline повторяет chapter pattern.

Точный набор `poss_results` для произведений source не задаёт: `[Needs confirmation]`. Не следует молча предполагать, что все integers между min/max являются достижимыми произведениями.

## 15.9. Генераторы кубиков

Results loop:

~~~python
results = [
    die_1.roll() + die_2.roll()
    for _ in range(1000)
]
~~~

Frequencies loop:

~~~python
frequencies = [
    results.count(value)
    for value in poss_results
]
~~~

## 15.10. Эксперименты с библиотеками

Требует API knowledge из внешней Matplotlib/Plotly documentation.

В `rag_only`:
- Matplotlib dice implementation: `[Needs confirmation]`;
- Plotly random-walk implementation: `[Needs confirmation]`.

Source purpose — самостоятельно исследовать перенос одного dataset между двумя visualization libraries.
