# Резюме главы 5

Source section: explicit «Резюме» in `p0306:c01`.

Этот файл сохраняет смысл source summary с минимальной структурной очисткой.

В главе рассмотрена работа с файлами и директориями:
- создание;
- удаление;
- перемещение/переименование;
- чтение/запись;
- дополнительные операции через `os`, `io`, `bufio`, `fmt`.

Отдельный крупный блок посвящён JSON — формату представления и обмена данными, с которым source рекомендует освоиться как можно раньше.

Также рассмотрены:
- сериализация и десериализация;
- struct tags;
- JSON `null`;
- typed structs и `map[string]any`;
- вложенные JSON-объекты;
- file-backed persistence examples.

Глава вводит сборку и конфигурацию приложения:
- `go build`;
- build flags;
- runtime configuration через package `flag`;
- compile-time configuration через `-ldflags`;
- embedding config через `go:embed`;
- `.env` configuration.

## Tic-tac-toe v.3

Добавлена возможность сохранять и загружать игровую сессию в JSON.

Для этого source создаёт:
- `IGameStorage`;
- `IGameLoader`;
- `IGameSaver`;
- `JsonGameStorage`.

В game loop добавляется команда `save`, а runtime-only поля исключаются из JSON.

## Tic-tac-toe v.4

Выполнен крупный refactoring и добавлена игра с компьютером.

Код разделён на packages:
- `board` — игровое поле;
- `player` — `IPlayer`, `HumanPlayer`, `ComputerPlayer`;
- `game` — game logic;
- `model` — `GameSnapshot` для обмена данными без circular dependencies;
- `storage` — save/load sessions.

Computer player получает три уровня:
- easy — random moves;
- medium — blocking winning combinations;
- hard — minimax.

Теперь пользователь может выбрать PvP или PvC и загрузить ранее сохранённую игру.

## Provenance

- Summary source: `go-basics-chernyshev-ru:p0306:c01`
- Project v.3 cross-check: `p0281:c01–p0286:c01`
- Project v.4 cross-check: `p0287:c01–p0305:c01`
