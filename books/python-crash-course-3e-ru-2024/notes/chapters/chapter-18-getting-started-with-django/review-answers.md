# Разбор упражнений главы 18

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Django здесь не устанавливался и команды не запускались.

## 18.1. Новые проекты

Source goal — повторить bootstrap несколько раз и исследовать generated structure.

Используя основной chapter flow:

~~~text
create project directory
    ↓
python -m venv <env>
    ↓
activate environment
    ↓
pip install django
    ↓
django-admin startproject <project_name> .
    ↓
inspect files/directories
~~~

Exercise itself показывает вариант `django-admin.py startproject`; exact intended command form: `[Needs confirmation]`.

Удаление test projects — optional destructive cleanup. Exact cleanup command source не задаёт: `[Needs confirmation]`.

## 18.2. Короткие записи

Source-required behavior:

~~~python
def __str__(self):
    if len(self.text) > 50:
        return f"{self.text[:50]}..."

    return self.text
~~~

Acceptance:
- Entry > 50 chars → truncated representation + ellipsis;
- Entry <= 50 chars → full representation without ellipsis.

## 18.3. Django API

External Django query documentation required by exercise.

В `rag_only`:
- additional QuerySet methods: `[Needs confirmation]`;
- current documentation behavior/version: `[Needs confirmation]`.

Chapter-supported query examples remain:
- `Topic.objects.all()`;
- `Topic.objects.get(id=1)`;
- `topic.entry_set.all()`;
- `Topic.objects.order_by('date_added')`.

## 18.4. Пиццерия

Source-supported models:

~~~python
from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Topping(models.Model):
    pizza = models.ForeignKey(
        Pizza,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
~~~

`max_length=200` follows the chapter's short-text model pattern; the exercise itself does not specify an exact length, so this value is an implementation choice, not an exercise fact.

Required process from chapter:
1. add app to `INSTALLED_APPS`;
2. `makemigrations`;
3. `migrate`;
4. register `Pizza` and `Topping` in admin;
5. create sample data;
6. inspect through shell.

## 18.5. План питания

Source requires only a simple project/app/home page.

Architecture can repeat chapter pattern:

~~~text
project urls.py
    ↓ include app urls
app urls.py
    ↓ path('', views.index, name='index')
view
    ↓ render(request, '<app>/index.html')
template
~~~

Exact project package name and page text: `[Needs confirmation]`.

## 18.6. Главная страница пиццерии

Use the same URL → view → template flow.

Source does not prescribe home-page copy: `[Needs confirmation]`.

## 18.7. Документация шаблонов

Requires external documentation.

В `rag_only` no extra template tags/filters are added beyond chapter examples:
- `extends`;
- `block/endblock`;
- `url`;
- `for/endfor`;
- `empty`;
- variable output with `{{ ... }}`;
- `date`;
- `linebreaks`.

## 18.8. Страницы проекта «Пиццерия»

Source-grounded routing pattern:

~~~python
path('pizzas/', views.pizzas, name='pizzas')
path(
    'pizzas/<int:pizza_id>/',
    views.pizza,
    name='pizza',
)
~~~

List view:

~~~python
def pizzas(request):
    pizzas = Pizza.objects.order_by('name')
    context = {'pizzas': pizzas}
    return render(
        request,
        'pizzas/pizzas.html',
        context,
    )
~~~

Detail view:

~~~python
def pizza(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.all()
    context = {
        'pizza': pizza,
        'toppings': toppings,
    }
    return render(
        request,
        'pizzas/pizza.html',
        context,
    )
~~~

Templates should inherit from one base template and use named URL links, matching the Learning Log pattern.

Exact wording/styling/order of toppings: `[Needs confirmation]`.
