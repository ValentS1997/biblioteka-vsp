# Разбор упражнений главы 20

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Runtime, Platform.sh и external documentation здесь не использовались.

## 20.1. Другие формы

Source уже показывает pattern для login.html:

~~~django
{% load django_bootstrap5 %}

{% bootstrap_form form %}
{% bootstrap_button button_type="submit" content="Log in" %}
~~~

Для new_topic, new_entry, edit_entry и register следует перенести тот же styling pattern:

1. сохранить существующее наследование base.html;
2. загрузить django_bootstrap5 template tags;
3. сохранить существующий page_header/action/CSRF behavior;
4. заменить прежний form rendering на bootstrap_form;
5. оформить submit button через bootstrap_button.

Exact button labels и существующие action URLs должны сохраняться из соответствующих templates; source exercise не задает новые значения.

Acceptance:

- form functionality не изменена;
- validation errors отображаются в Bootstrap style;
- страницы визуально согласованы с login page.

## 20.2. Форматирование проекта Blog

Source требует применить Bootstrap к Blog из главы 19, но в текущей главе не задает exact Blog template filenames или content.

Source-grounded transfer sequence:

~~~text
existing functional Blog
    ↓
install/use django-bootstrap5
    ↓
shared base template
    ↓
responsive navbar + page_header/content blocks
    ↓
style forms with bootstrap_form/bootstrap_button
    ↓
style list/detail content with suitable Bootstrap components
    ↓
verify existing Blog behavior
~~~

Exact Blog routes/templates/components: [Needs confirmation].

## 20.3. Блог в Интернете

Использовать deployment process главы 20 для Blog:

1. зафиксировать Python dependencies;
2. добавить remote requirements;
3. добавить Platform.sh YAML configuration;
4. добавить Platform-specific settings;
5. подготовить Git repository/.gitignore;
6. убедиться, что git status clean;
7. создать Platform.sh project;
8. выполнить platform push;
9. открыть deployed URL;
10. убедиться, что DEBUG = False в deployed environment.

Source security acceptance: пользователи не должны видеть полную Django debug error page.

Blog-specific configuration names, services и migration state: [Needs confirmation].

## 20.4. Расширенное приложение «Журнал обучения»

### Часть 1 — простой change/deploy cycle

Source-defined workflow:

~~~text
local change
    ↓
git add .        # если появились новые files
    ↓
git commit -am "message"
    ↓
platform push
    ↓
visit deployed project
    ↓
verify intended change
~~~

### Часть 2 — public Topics

Exercise задает следующие requirements:

- Topic получает attribute public;
- default value — False;
- new_topic page получает form control для выбора public/private;
- выполняется migration;
- views.py меняется так, чтобы public Topics были видимы unauthenticated users.

Exact Django field declaration: [Needs confirmation].

Exact ModelForm field declaration/control rendering: [Needs confirmation].

Exact query/view implementation: [Needs confirmation].

Security boundary, который следует сохранить из главы 19:

- private Topic остается доступной только owner;
- новая public visibility не должна случайно сделать все Topics публичными;
- default False сохраняет private behavior для новых объектов, если public не выбран.

Последние два пункта прямо следуют из условия упражнения о public=False и разделении public/private visibility; конкретный код source не предоставляет.
