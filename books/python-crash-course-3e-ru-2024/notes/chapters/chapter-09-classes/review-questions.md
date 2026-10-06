# Упражнения главы 9

Source provenance:

- EPUB spine item: `18`
- locator: `OEBPS/Text/978544614112-15.xhtml`
- exercise chunks: `e0018:c03–c04`, `c06`, `c10`, `c14–c15`

## 9.1. Ресторан

Создайте `Restaurant` с attributes `restaurant_name`, `cuisine_type`; methods `describe_restaurant()`, `open_restaurant()`. Создайте instance, выведите оба attributes и вызовите оба methods.

## 9.2. Три ресторана

На основе 9.1 создайте три разных instances и вызовите `describe_restaurant()` для каждого.

## 9.3. Пользователи

Создайте `User` с `first_name`, `last_name` и дополнительными profile attributes; methods `describe_user()`, `greet_user()`. Создайте несколько users и вызовите оба methods.

## 9.4. Посетители

Добавьте `number_served = 0` в `Restaurant`. Проверьте прямое изменение; затем `set_number_served()`; затем `increment_number_served()`.

## 9.5. Попытки входа

Добавьте `login_attempts` в `User`; methods `increment_login_attempts()` и `reset_login_attempts()`. Несколько раз увеличьте counter, проверьте значение, затем reset до 0.

## 9.6. Киоск с мороженым

Создайте `IceCreamStand(Restaurant)`; attribute `flavors`; method вывода flavours. Создайте instance и вызовите method.

## 9.7. Администратор

Создайте `Admin(User)`; attribute `privileges` со списком строк; method `show_privileges()`. Создайте instance и вызовите method.

## 9.8. Привилегии

Вынесите privileges и `show_privileges()` в отдельный class `Privileges`; instance `Privileges` должен стать attribute `Admin`.

## 9.9. Обновление аккумулятора

Добавьте `Battery.upgrade_battery()`: если battery size не 65 — установить 65. Сравните `get_range()` до и после upgrade.

## 9.10. Импортирование класса Restaurant

Сохраните последнюю версию `Restaurant` в module, импортируйте в отдельный file, создайте instance и вызовите method.

## 9.11. Импортирование класса Admin

Сохраните `User`, `Privileges`, `Admin` в одном module. В отдельном file импортируйте `Admin`, создайте instance и вызовите `show_privileges()`.

## 9.12. Множественные модули

Сохраните `User` в одном module, `Privileges` и `Admin` — в другом. Создайте `Admin` в отдельном file и вызовите `show_privileges()`.

## 9.13. Игра в кости

Создайте `Die(sides=6)` и `roll_die()`, использующий `randint()`. Смоделируйте 10 бросков для 6-, 10- и 20-гранного кубика.

## 9.14. Лотерея

Создайте list/tuple из 10 numbers и 5 letters. Случайно выберите четыре элемента и выведите winning combination.

## 9.15. Анализ лотереи

Создайте `my_ticket` и цикл генерации combinations до выигрыша. Выведите число iterations, потребовавшихся для совпадения.

## 9.16. Модуль недели

Откройте PyMOTW, выберите интересный module и прочитайте его description либо изучите документацию `random`. В режиме `rag_only` внешний сайт не открывался.

Нумерация и требования сохранены по RAG; формулировки структурно уплотнены.
