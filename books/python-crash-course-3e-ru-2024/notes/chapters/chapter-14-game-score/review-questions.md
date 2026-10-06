# Упражнения главы 14

Source provenance:

- EPUB spine item: `24`
- locator: `OEBPS/Text/978544614112-21.xhtml`
- exercise chunks: `e0024:c04–c06`, `e0024:c12–c13`

## 14.1. Запуск игры клавишей P

Добавьте запуск игры по клавише P. Source предлагает, при необходимости, вынести общую логику из `_check_play_button()` в `start_game()`, вызываемый и mouse handler, и keyboard handler.

## 14.2. Стрельба по мишени

Создайте отдельную игру:
- target rectangle у правого края;
- target постоянно движется вверх/вниз;
- ship у левого края двигается вверх/вниз;
- ship стреляет по target;
- Play button запускает игру;
- после трёх промахов game over;
- Play снова запускает новую игру.

## 14.3. Учебная стрельба с нарастающей сложностью

Продолжите 14.2:
- target speed увеличивается по ходу игры;
- при новом нажатии Play скорость возвращается к initial value.

## 14.4. Уровни сложности

Добавьте набор buttons для выбора initial difficulty. Каждая button должна присваивать `Settings` значения, соответствующие выбранному уровню.

Конкретные presets source не задаёт: `[Needs confirmation]`.

## 14.5. Исторический рекорд

Сделайте high score persistent между запусками программы:
- перед `sys.exit()` записывайте рекорд в file;
- при инициализации `GameStats.high_score` загружайте его.

File path/format/error handling: `[Needs confirmation]`.

## 14.6. Рефакторинг

Найдите methods/functions с несколькими responsibilities. Source предлагает, в частности:
- часть `_check_bullet_alien_collisions()`, запускающую новый level, вынести в `start_new_level()`;
- четыре `prep_*` calls из `Scoreboard.__init__()` вынести в `prep_images()`;
- использовать `prep_images()` при start/restart.

Перед refactoring source отсылает к Appendix Г для recovery procedure; приложение не входит в chapter scope.

## 14.7. Расширение игры

Source examples:
- aliens стреляют по ship;
- destructible shelters;
- sound effects через `pygame.mixer`.

Выбранное расширение и design: `[Needs confirmation]`.

## 14.8. Боковая стрельба, финальная версия

Продолжите side-shooter:
- Play button;
- acceleration where appropriate;
- scoring system;
- ongoing refactoring;
- дополнительные settings по необходимости.

Нумерация и требования сохранены по RAG.
