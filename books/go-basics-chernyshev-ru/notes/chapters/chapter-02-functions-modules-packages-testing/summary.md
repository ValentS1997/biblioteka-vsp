# Резюме главы 2

Source section: explicit «Резюме» in `p0150:c01–p0151:c01`.

Этот файл сохраняет смысл source summary с минимальной структурной очисткой.

Глава рассматривает функции в Go:
- способы объявления;
- передачу аргументов по значению и через pointer;
- возврат нескольких значений;
- variadic functions;
- anonymous functions;
- closures;
- functions as first-class values;
- recursion;
- generator functions на goroutines/channels;
- `defer` для отложенного выполнения и освобождения ресурсов.

Source отдельно подчёркивает отсутствие в Go:
- default argument values;
- function overloading.

Далее глава вводит modules и packages:
- создание пользовательских packages;
- различие package/module;
- external dependencies;
- `go.mod` / `go.sum`;
- semantic versioning;
- `vendor`;
- import aliases;
- local module dependencies.

В summary перечислены команды `go mod`:
- `go mod init`;
- `go mod tidy`;
- `go mod download`;
- `go mod vendor`;
- `go mod graph`;
- `go mod verify`;
- `go mod edit`;
- `go mod why`.

В части testing глава подчёркивает пользу tests для раннего обнаружения ошибок и рассматривает unit/table-driven/subtests, coverage и performance benchmarks.

В проекте «Крестики-нолики» создана версия v.1:
- исходный монолитный код разбит на functions;
- применён procedural approach;
- логика перенесена в package `game`;
- реализованы initialization, alternating moves, occupied-cell validation, win/draw checks, player switching, main game loop and early quit.

## Provenance

- Summary source: `go-basics-chernyshev-ru:p0150:c01–p0151:c01`
- Project context: `p0144:c01–p0149:c01`
