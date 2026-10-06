# Упражнения главы 20

Source provenance:

- exercises 20.1–20.2: e0030:c08
- exercises 20.3–20.4: e0030:c18
- EPUB spine item: 30
- locator: OEBPS/Text/978544614112-27.xhtml

## 20.1. Другие формы

Применить Bootstrap styling, аналогичный login page, к остальным form-based pages:

- new_topic;
- new_entry;
- edit_entry;
- register.

## 20.2. Форматирование проекта Blog

Использовать Bootstrap для оформления проекта Blog из главы 19.

## 20.3. Блог в Интернете

Развернуть проект Blog на Platform.sh.

Обязательное source condition: DEBUG должен иметь значение False, чтобы пользователи не видели полную Django debug error page.

## 20.4. Расширенное приложение «Журнал обучения»

Сначала добавить простую функцию в Learning Log и отправить изменение в deployed copy.

Затем выполнить более сложное изменение: дать пользователю возможность сделать Topic общедоступной.

Source-defined changes:

- добавить к Topic attribute public;
- default public = False;
- добавить на new_topic form element для выбора public/private;
- выполнить migration;
- изменить views.py так, чтобы public Topic была видима и пользователям без authentication.
