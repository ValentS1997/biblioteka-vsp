# Резюме главы 3

Source section: explicit «Резюме» in `p0197:c01`.

Этот файл сохраняет смысл source summary с минимальной структурной очисткой.

Глава рассматривает написание Go-кода в объектно-ориентированном стиле и механизмы, которыми source реализует знакомые ООП-концепции.

Основные выводы summary:

- при работе с interfaces не следует собирать все methods структуры в один oversized interface;
- доступ к functionality часто нужно разграничивать по потребителю, поэтому небольшие interfaces дают более точную abstraction boundary;
- регистр имени structure, fields и methods определяет export boundary;
- если functionality не требуется из другого package, source рекомендует hiding через lowercase names;
- в Go нет language-level constructors, поэтому source рекомендует constructor functions `New...` для создания structure instances;
- interfaces повышают уровень abstraction, flexibility и readability;
- generics уменьшают code duplication, с которым Go-разработчики сталкивались до version 1.18.

В проекте «Крестики-нолики» выполнен refactoring v.1 → v.2 с переходом от procedural organization к object-oriented organization при сохранении возможностей предыдущей версии.

Код распределён по трём основным structures:

- `Board` — состояние поля, initialization, move validation, win/draw checks;
- `Player` — текущий игрок, X/O и switch turn;
- `Game` — coordination, user input, board/player interaction и game state.

## Provenance

- Summary source: `go-basics-chernyshev-ru:p0197:c01`
- Project cross-check: `p0190:c01–p0196:c01`
