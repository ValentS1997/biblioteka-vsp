# Упражнения главы 18

Source provenance:

- EPUB spine item: `28`
- locator: `OEBPS/Text/978544614112-25.xhtml`
- exercise chunks: `e0028:c04`, `c10`, `c13`, `c18`

## 18.1. Новые проекты

Создайте несколько пустых Django projects вне `learning_log`, например:
- `tik_gram`;
- `insta_tok`.

Для каждого:
- создайте virtual environment;
- установите Django;
- создайте project;
- исследуйте generated files/directories;
- сравните их с Learning Log;
- при желании удалите test projects после исследования.

Source exercise показывает `django-admin.py startproject tg_project .`, что расходится с основным setup главы; см. `source-findings.md`.

## 18.2. Короткие записи

Измените `Entry.__str__()`:
- ellipsis добавляется только если text длиннее 50 characters;
- для short Entry ellipsis отсутствует.

Добавьте short Entry через admin и проверьте отображение.

## 18.3. Django API

Изучите documentation по Django queries, указанную source.

В `rag_only` external documentation не открывалась.

## 18.4. Пиццерия

Создайте:
- project `pizzeria_project`;
- app `pizzas`;
- model `Pizza(name)`;
- model `Topping(pizza, name)`, где `pizza` — ForeignKey to Pizza.

Зарегистрируйте models в admin, добавьте pizzas/toppings и исследуйте data через Django shell.

## 18.5. План питания

Создайте:
- folder `meal_planner`;
- Django project;
- app `meal_plans`;
- простую home page.

## 18.6. Главная страница пиццерии

Добавьте home page в project Pizzeria из 18.4.

## 18.7. Документация шаблонов

Изучите Django template documentation, указанную source, и применяйте её в собственных проектах.

Source URL содержит version `2.2`, тогда как основной chapter ориентирован на Django 4.1; mismatch зарегистрирован отдельно.

## 18.8. Страницы проекта «Пиццерия»

Добавьте:
- page со списком pizzas;
- link от каждой pizza к detail page;
- detail page со списком toppings;
- template inheritance.

Нумерация и требования сохранены по RAG.
