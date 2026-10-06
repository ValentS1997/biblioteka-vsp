# Упражнения главы 19

Source provenance:

- EPUB spine item: `29`
- locator: `OEBPS/Text/978544614112-26.xhtml`
- exercise chunks: `e0029:c07`, `e0029:c11`, `e0029:c16`

## 19.1. Блог

Создайте Django project Blog и app `blogs`.

Требования source:
- две models: одна представляет блог, другая — отдельную публикацию;
- определить подходящие fields;
- создать superuser;
- добавить несколько коротких сообщений через admin;
- home page выводит сообщения в chronological order;
- forms для создания блога, новых сообщений и редактирования existing messages;
- проверить работу forms.

Точные names/fields models source не задаёт: `[Needs confirmation]`.

## 19.2. Учетные записи в блоге

Добавьте authentication/registration к Blog:
- logged-in user видит своё имя;
- anonymous user видит registration link.

## 19.3. Рефакторинг

Вынесите повторяющуюся проверку ownership Topic в функцию `check_topic_owner()` и вызывайте её там, где это необходимо.

## 19.4. Защита страницы new_entry

Перед сохранением новой Entry убедитесь, что текущий user является owner Topic, указанной в URL.

## 19.5. Защищенный блог

Свяжите каждое blog message с конкретным user.

Требования:
- чтение всех сообщений доступно всем;
- только authenticated users могут создавать posts;
- редактировать post может только его owner;
- ownership проверяется до обработки edit form.

Нумерация и требования сохранены по RAG.
